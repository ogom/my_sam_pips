import sys
import subprocess


def main():
    if len(sys.argv) < 2:
        print("No argument!")
        sys.exit()

    print("Argument:{}".format(sys.argv[1]))
    subprocess.run(['ls'])


if __name__ == '__main__':
    main()
