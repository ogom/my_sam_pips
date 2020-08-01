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
