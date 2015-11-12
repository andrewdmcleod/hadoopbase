import subprocess
from glob import glob


def pre_install():
    """
    Do any setup required before the install hook.
    """
    install_pip()
    install_bundled_resources()


def install_pip():
    subprocess.check_call(['apt-get', 'install', '-yq', 'python-pip', 'bzr'])


def install_bundled_resources():
    """
    Install the bundled resources libraries.
    """
    archives = glob('resources/python/*')
    subprocess.check_call(['pip', 'install'] + archives)

