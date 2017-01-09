# Introduction

This project was developed for a job interview to demonstrate the provisioning of vritual machine (VM) to display a static web page displaying "Automation for the People".  Using Vagrant and Ansible, it installs ntp and nginx into a CentOS 7.2 VM, configures ip table rules, and copies the contents of the `src` directory into `/var/lib/www/automation_people` to meet these requirements.

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
(automation-people) ➜  automation-people git:(master) ✗ tox
py27 create: /Users/jburwell/Documents/projects/automation-people/.tox/py27
py27 installdeps: -rrequirements.txt, nose==1.3.7, nose-parameterized==0.5.0, python-vagrant==0.5.14, rednose==1.2.1, requests==2.12.4
py27 installed: ansible==2.1.3.0,autopep8==1.2.4,cffi==1.9.1,colorama==0.3.7,cryptography==1.7.1,enum34==1.1.6,idna==2.2,ipaddress==1.0.17,Jinja2==2.8.1,MarkupSafe==0.23,nose==1.3.7,nose-parameterized==0.5.0,paramiko==2.1.1,pep8==1.7.0,pluggy==0.4.0,py==1.4.32,pyasn1==0.1.9,pycparser==2.17,pycrypto==2.6.1,python-termstyle==0.1.10,python-vagrant==0.5.14,PyYAML==3.12,rednose==1.2.1,requests==2.12.4,six==1.10.0,tox==2.5.0,virtualenv==15.1.0
py27 runtests: PYTHONHASHSEED='1588031762'
py27 runtests: commands[0] | nosetests --stop -vv --rednose --nocapture
nose.config: INFO: Ignoring files matching ['^\\.', '^_', '^setup\\.py$']
Starting Vagrant VM ...
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'bento/centos-7.2'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'bento/centos-7.2' is up to date...
==> default: Setting the name of the VM: automation-people_default_1483986985202_29101
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 8080 (guest) => 28080 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Remote connection disconnect. Retrying...
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => /Users/jburwell/Documents/projects/automation-people
==> default: Running provisioner: ansible...
    default: Running ansible-galaxy...
- extracting jburwell.nginx to /Users/jburwell/Documents/projects/automation-people/.galaxy/jburwell.nginx
- jburwell.nginx was installed successfully
- downloading role 'iptables', owned by kbrebanov
- downloading role from https://github.com/kbrebanov/ansible-iptables/archive/v3.0.1.tar.gz
- extracting kbrebanov.iptables to /Users/jburwell/Documents/projects/automation-people/.galaxy/kbrebanov.iptables
- kbrebanov.iptables was installed successfully
- downloading role 'ntp', owned by resmo
- downloading role from https://github.com/resmo/ansible-role-ntp/archive/0.4.0.tar.gz
- extracting resmo.ntp to /Users/jburwell/Documents/projects/automation-people/.galaxy/resmo.ntp
- resmo.ntp was installed successfully
    default: Running ansible-playbook...

PLAY [all] *********************************************************************

TASK [setup] *******************************************************************
ok: [default]

TASK [Create the content directory for the site assets] ************************
changed: [default]

TASK [Copy the site assets to the content directory] ***************************
changed: [default]

TASK [resmo.ntp : Add the OS specific variables] *******************************
ok: [default]

TASK [resmo.ntp : Install the required packages in Redhat derivatives] *********
changed: [default]

TASK [resmo.ntp : Install the required packages in Debian derivatives] *********
skipping: [default]

TASK [resmo.ntp : Copy the ntp.conf template file] *****************************
changed: [default]

TASK [resmo.ntp : Start/stop ntp service] **************************************
changed: [default]

TASK [kbrebanov.iptables : Include distribution specific variables] ************
ok: [default]

TASK [kbrebanov.iptables : Include release specific variables] *****************
skipping: [default]

TASK [kbrebanov.iptables : Install iptables packages] **************************
ok: [default] => (item=[u'iptables'])

TASK [kbrebanov.iptables : Install iptables packages] **************************
skipping: [default] => (item=[])

TASK [kbrebanov.iptables : Create iptables configuration] **********************
changed: [default]

TASK [kbrebanov.iptables : Create iptables6 configuration] *********************
changed: [default]

TASK [kbrebanov.iptables : Ensure iptables is started and enabled on boot] *****
ok: [default]

TASK [jburwell.nginx : Install repos and packages] *****************************
included: /Users/jburwell/Documents/projects/automation-people/.galaxy/jburwell.nginx/tasks/redhat.yml for default

TASK [jburwell.nginx : Include CentOS-specific variables] **********************
ok: [default]

TASK [jburwell.nginx : Include RHEL-specific variables] ************************
skipping: [default]

TASK [jburwell.nginx : Add the nginx Yum repository] ***************************
changed: [default]

TASK [jburwell.nginx : Add CentOS/RHEL 6 EPEL Yum repository] ******************
skipping: [default]

TASK [jburwell.nginx : Add CentOS/RHEL 7 EPEL Yum repository] ******************
skipping: [default]

TASK [jburwell.nginx : Install nginx packages and dependencies] ****************
changed: [default] => (item=[u'nginx', u'libselinux-python'])

TASK [jburwell.nginx : Create the directories for site specific configurations]
changed: [default] => (item=sites-available)
changed: [default] => (item=sites-enabled)

TASK [jburwell.nginx : Copy the nginx configuration file] **********************
changed: [default]

TASK [jburwell.nginx : Copy the nginx default configuration file] **************
changed: [default]

TASK [jburwell.nginx : Copy the nginx default site configuration file] *********
changed: [default]

TASK [jburwell.nginx : Create the link for site enabled specific configurations] ***
changed: [default]

TASK [jburwell.nginx : Create the configurations for sites] ********************
changed: [default] => (item={u'server': {u'root': u'/var/lib/www/automation_people', u'location1': {u'index': u'index.html', u'name': u'/'}, u'listen': 8080, u'server_name': u'localhost', u'file_name': u'automation_people'}})

TASK [jburwell.nginx : Create the links to enable site configurations] *********
changed: [default] => (item={u'server': {u'root': u'/var/lib/www/automation_people', u'location1': {u'index': u'index.html', u'name': u'/'}, u'listen': 8080, u'server_name': u'localhost', u'file_name': u'automation_people'}})

TASK [jburwell.nginx : start the nginx service] ********************************
changed: [default]

RUNNING HANDLER [resmo.ntp : restart ntp] **************************************
changed: [default]

RUNNING HANDLER [kbrebanov.iptables : restart iptables] ************************
changed: [default]

RUNNING HANDLER [jburwell.nginx : restart nginx] *******************************
changed: [default]

RUNNING HANDLER [jburwell.nginx : reload nginx] ********************************
changed: [default]

PLAY RECAP *********************************************************************
default                    : ok=28   changed=21   unreachable=0    failed=0

Vagrant VM started
test_get_success_0_http_localhost_28080 (test.tests.TestProvisionVM) ... passed
test_get_success_1_http_localhost_28080_ (test.tests.TestProvisionVM) ... passed
test_get_success_2_http_localhost_28080_index_html (test.tests.TestProvisionVM) ... passed
Destroying Vagrant VM ...
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
Vagrant VM destroyed

-----------------------------------------------------------------------------
3 tests run in 73.956 seconds (3 tests passed)
_________________________________________________________________ summary __________________________________________________________________
  py27: commands succeeded
  congratulations :)
  ```
