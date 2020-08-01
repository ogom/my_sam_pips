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
