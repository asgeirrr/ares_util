# coding=utf-8

from fabric import colors
from fabric.context_managers import settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import local


def print_success(message):
    try:
        from colorama import init, Back

        init()
        print(Back.GREEN + colors.white(u"%s" % message, bold=True))
    except ImportError:
        print(colors.green(u"%s" % message, bold=True))


@task()
def update_package_tools():
    local("easy_install -U pip")
    local("pip install setuptools --upgrade")
    local("pip install wheel --upgrade")

    print_success("Updated.")


@task()
def install_requirements():
    local("pip install -r .\\requirements.txt --upgrade")

    print_success("Installed || Updated.")

@task()
def test_install():
    update_package_tools()
    with settings(warn_only=True):
        local("pip uninstall ares_util --yes")
        print_success("Uninstall OK.")

    local("pip install --use-wheel --no-index --find-links dist ares_util")
    local("pip uninstall ares_util --yes")
    print_success("Install test OK.")


@task()
def test():
    local("nosetests --with-coverage --cover-package=ares_util --cover-tests --cover-erase --with-doctest")
    print_success("Test OK.")


@task()
def build():
    # https://coderwall.com/p/qawuyq
    test()
    local("pandoc --from=markdown --to=rst README.md -o README.rst")
    local("python setup.py sdist")
    local("python setup.py bdist_wheel")

    print_success("Build OK.")


@task()
def publish():
    if confirm(u'Really publish?', default=False):
        local('python setup.py sdist upload -r pypi')
        local('python setup.py bdist_wheel upload -r pypi')

        print_success("Published.")