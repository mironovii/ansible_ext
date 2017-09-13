#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import Popen, PIPE

DISTRIB = get_distribution()

def get_libre_office_facts():
    if any(list(map(lambda x: x == DISTRIB, ['Ubuntu', 'Debian']))):
        dict={'default': '0'}
        dpkg = Popen(['dpkg', '-s', 'libreoffice-writer'], stdout=PIPE, stderr=PIPE)
        dpkg.wait()
        if dpkg.returncode:
            dict['libre_office_version'] = 'libreoffice-writer not installed'
            return dict
        else:
            grep = Popen(['grep', 'Version'], stdin=dpkg.stdout, stderr=PIPE, stdout=PIPE)
            dpkg.stdout.close()
            grep.wait()
            res = grep.communicate()
            if grep.returncode:
                dict['libre_office_version'] = 'error'
                return dict
            dict['libre_office_version'] = res[0][11:20].decode('utf-8')
            return dict

def main():
    module = AnsibleModule(argument_spec={})
    module.exit_json(**get_libre_office_facts())


if __name__ == '__main__':
    main()
