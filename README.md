# Introduction

This project was developed per a specification for a job interview to demonstrate the provisioning of vritual machine (VM) to display a static web page displaying "Automation for the People".  Using Vagrant and Ansible, it installs ntp and nginx into a CentOS 7 VM, configures ip table rules, and copies the contents of the `src` directory into `/var/lib/www/automation_people` to meet these requirements.

# Prerequistes

In order to ensure reproducibility, this project isolates the tool dependencies required to build the VM.  It was developed and tested on Mac OS X 10.11.6 using the following Vagrant 1.9.1 and VritualBox 5.1.12.  Using this project to build a VM on Linux or Windows and/or other hypervisors has not been tested. 

## pyenv and Ansible

Due to a [bug](https://github.com/ansible/ansible/issues/18965) in Ansible 2.2, `async` option on the `service` task is broken with systemd services.  This option is required to properly configure ip tables rules.  Therefore, Ansible 2.1.x or lower is required for provisioning to function properly.  This project includes a pinned Ansible version in `requirements.txt` that is not affected by this bug.  To simplify installing the correct dependency versions without corrupting other Python environments, please install [pyenv](https://github.com/yyuu/pyenv) and the [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) plugin.  Together, these tools manage Python versions and isolated environments based on the presence of the `.python-version` in the project directory.  Using the [Homebrew](http://brew.sh) package manager, Mac users be install these tools using the following command:

```
# brew install pyenv pyenv-virtualenv
```

Once ``pyenv`` and ``pyenv-virtualenv`` are successfully installed, please execute the following commands in the project root directory to prepare an isolated environment for this project:

```
# pyenv install 2.7.11
# pyenv virtualenv automation-people
# pip install -r requirements.txt
# pyenv rehash
```

Upon completion, Ansible, Python, and the unit testing tools will be installed and ready for use.

## Vagrant

[Vagrant](https://vagrantup.com) is required to build and test the VM.  Install it and [VirtualBox](https://www.virtualbox.org) per the instructions for your environments.  Using the [Homebrew Cask](https://caskroom.github.io/) package manager, Mac users can install these applications with the following command:

```
# brew cask install vagrant virtualbox
```

# Building and Running the VM

From the project root directory, the VM is built by executing the following command:

```
# vagrant up
```

By default, the page will be displayed at the ``http://localhost:28080`` URL.  If port 28080 conflicts with an existing service, the following command will change the port on which traffic from the VM is forwarded:

```
# AUTOMATE_PORT=<desired port> vagrant up
```

# Testing the VM

A full unit test suite is provided to verify the construction of the VM using tox and nosetest.  It performs the following steps:

1. Builds and starts the VM using Vagrant
1. Verifies that GET requests to the following URLs return HTML containing the phrase "Automation for the People":
    * ``http://localhost:28080``
    * ``http://localhost:28080/``
    * ``htto://localhost:28080/index.html``
1. Destroys the VM

In order to avoid destroying existing work, the test suite will fail if Vagrant is already running the VM.  The following command run the test suite:

```
# tox
```

The following is a sample of the test output:

```
```
