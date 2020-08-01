# my_sam_pips

```
$ sam init --name my_sam_pips --runtime python3.8 --dependency-manager pip --app-template hello-world
$ cd my_sam_pips/
$ echo pytest > requirements.txt
$ echo pytest-mock >> requirements.txt
```

```bash
$ mkdir .circleci
$ touch .circleci/config.yml
```

```yaml
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3.8
    working_directory: ~/repo
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-dependencies-{{ checksum "requirements.txt" }}
            - v1-dependencies-
      - run:
          name: install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum "requirements.txt" }}
      - run:
          name: run tests
          command: |
            . venv/bin/activate
            python -m pytest tests/ -v
```

```bash
$ circleci config validate
$ circleci local execute
```

---

```bash
sam build --use-container
sam deploy --guided
Stack Name [sam-app]: my-sam-pips
AWS Region [us-east-1]: ap-northeast-1
#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
Confirm changes before deploy [y/N]: n
#SAM needs permission to be able to create roles to connect to the resources in your template
Allow SAM CLI IAM role creation [Y/n]: y
HelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
Save arguments to samconfig.toml [Y/n]: y
```

```
$ echo aws-sam-cli >> requirements.txt
```

```yaml
version: 2

references:
  default: &default
    docker:
      - image: circleci/python:3.8
    working_directory: ~/repo
  cache_key: &cache_key v1-dependencies-{{ checksum "requirements.txt" }}
  restore_cache_requirements: &restore_cache_requirements
    restore_cache:
      keys:
        - *cache_key
  save_cache_requirements: &save_cache_requirements
    save_cache:
      paths:
        - ./venv
      key: *cache_key

jobs:
  test:
    <<: *default
    steps:
      - checkout
      - *restore_cache_requirements
      - run:
          name: install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
      - *save_cache_requirements
      - run:
          name: run tests
          command: |
            . venv/bin/activate
            python -m pytest tests/ -v
  build:
    <<: *default
    steps:
      - checkout
      - *restore_cache_requirements
      - run:
          name: run sam build
          command: |
            . venv/bin/activate
            sam build
  deploy:
    <<: *default
    steps:
      - checkout
      - *restore_cache_requirements
      - run:
          name: run sam deploy
          command: |
            . venv/bin/activate
            sam build
            python manage.py deploy

workflows:
  version: 2
  test_and_build_and_deploy:
    jobs:
      - test
      - build:
          requires:
            - test
      - deploy:
          requires:
            - build
          filters:
            branches:
              only:
                - master
                - integrate
```

```bash
$ touch manage.py
```

```python
import os
import sys
import subprocess


def main():
    if len(sys.argv) < 2:
        print("No argument!")
        sys.exit()

    execute_command = sys.argv[1]
    git_branch = os.environ.get('CIRCLE_BRANCH')

    print("Execute Command: {}".format(execute_command))
    print("Git Branch: {}".format(git_branch))

    if execute_command == 'deploy':
        if git_branch == 'master':
            subprocess.run([
                'sam', 'deploy',
                '--stack-name', 'master-my-sam-pips',
                '--s3-bucket', 'aws-sam-cli-managed-default-samclisourcebucket-128f92u2xqf55',
                '--s3-prefix', 'my-sam-pips',
                '--region', 'ap-northeast-1',
            ])
        elif git_branch == 'integrate':
            subprocess.run([
                'sam', 'deploy',
                '--stack-name', 'integrate-my-sam-pips',
                '--s3-bucket', 'aws-sam-cli-managed-default-samclisourcebucket-1078k6hr9hsla',
                '--s3-prefix', 'my-sam-pips',
                '--region', 'us-west-2',
            ])


if __name__ == '__main__':
    main()
```
