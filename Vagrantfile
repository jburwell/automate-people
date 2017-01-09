# -*- mode: ruby -*-
# vi: set ft=ruby :
# Copyright 2017 John S. Burwell III
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FORWARD_PORT_ENV_VAR = "AUTOMATE_PORT"
PLAYBOOK_ROOT = "playbooks"

def local_relative_path(elements)
  elements.join File::SEPARATOR
end

FORWARD_PORT = ENV.key?(FORWARD_PORT_ENV_VAR) ? ENV[FORWARD_PORT_ENV_VAR].to_i : 28080
SITE_PORT = 8080

Vagrant.configure("2") do |config|

  config.vm.box = "bento/centos-7.2"
  config.vm.network "forwarded_port", guest: SITE_PORT, host: FORWARD_PORT

  config.vm.provision "ansible" do |ansible|

    ansible.galaxy_role_file = local_relative_path [PLAYBOOK_ROOT, "requirements.yml"]
    ansible.galaxy_roles_path = ".galaxy"

    ansible.extra_vars = {
      site_root: "/var/lib/www/automation_people",
      site_port: SITE_PORT
    }

    ansible.playbook = local_relative_path [PLAYBOOK_ROOT, "site.yml"]
    ansible.sudo = true

  end

end
