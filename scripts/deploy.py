import os
import shutil
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    commit = os.environ.get("TRAVIS_COMMIT", "manual")
    author_email = os.environ.get("COMMIT_AUTHOR_EMAIL")
    author_name = os.environ.get("COMMIT_AUTHOR_NAME")

    shutil.copytree('../home/.git', '../template/deploy/.git')

    log.info('Git user ...')
    subprocess.check_call(['git', 'config', 'user.email', author_email], cwd='../template/deploy')
    subprocess.check_call(['git', 'config', 'user.name', author_name], cwd='../template/deploy')

    log.info('Commiting ...')
    subprocess.check_call(['git', 'add', '-A'], cwd='../template/deploy')
    subprocess.check_call(['git', 'commit', '-a', '-m', 'Site deploy for %s' % commit], cwd='../template/deploy')

    log.info('Pushing ...')
    subprocess.check_call(['git', 'push', 'origin', 'init'], cwd='../template/deploy')


if __name__ == "__main__":
    main()
