import re
import os
import yaml
import shutil
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)



def validate(fullpath):
    """Validate the formatting of the given jobs file.
    The contents of the file will be validated later; this is just checking
    that the file will parse.
    """
    data = open(fullpath, 'r').read()
    path = os.path.basename(fullpath)

    try:
        data = data.decode('utf8')
    except UnicodeDecodeError:
        raise AssertionError("%s: is not valid UTF-8" % path)
    chunks = re.split(r'^---[ \t]*$', data, flags=re.M)
    assert len(chunks) >= 3, \
        "%s: should be YAML and Markdown, prefixed by --- lines" % path
    assert not chunks[0].strip(), \
        "%s: data before initial ---" % path

    try:
        yaml.safe_load(chunks[1])
    except Exception as e:
        raise AssertionError("%s: malformed YAML: %s" % (path, e))


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        log.info('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            log.info('{}{}'.format(subindent, f))


def main():
    hand_source = './hands'
    hand_dest = '../template/content/hands'

    log.info('Copying hands ...')
    for hand_file in os.listdir(hand_source):
        assert hand_file.endswith('.html'), '%s: hand files must end in .html' % hand_file

        log.info('Copying hand: %s', hand_file)
        src_path = '%s/%s' % (hand_source, hand_file) # This is safer than join()
        dest_path = '%s/%s' % (hand_dest, hand_file)

        validate(src_path)

        shutil.copyfile(src_path, dest_path)

    log.info('Building ...')
    subprocess.check_call(['hyde', '-x', '-s', '../template/', 'gen', '-r'])

    log.info('Displaying Tree ...')
    list_files('../template/deploy')


if __name__ == "__main__":
    main()
