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
import mimetypes
import os
import requests

from nose.tools import ok_, eq_
from nose_parameterized import parameterized
from vagrant import Vagrant, stdout_cm, stderr_cm
from unittest import TestCase
from urlparse import urlparse

HOST_NAME_ENV_VAR_NAME = "AUTOMATE_HOST_NAME"
PORT_ENV_VAR_NAME = "AUTOMATE_PORT"
PROVIDER_ENV_VAR_NAME = "AUTOMATE_PROVIDER"

class TestProvisionVM(TestCase):

    @classmethod
    def setup_class(cls):

        cls.vagrant_client = Vagrant(out_cm=stdout_cm,
                                     err_cm=stderr_cm,
                                     quiet_stdout=False,
                                     quiet_stderr=False)

        status = cls.vagrant_client.status()
        eq_(len(status), 1, "Only one Vagrant VM should be defined")

        vm_state = status[0].state
        eq_(vm_state, "not_created", "The Vagrant VM is in '{}' state which prevents the test from proceeding".format(
            vm_state))
        
        provider = os.environ[PROVIDER_ENV_VAR_NAME]
        ok_(provider, "No Vagrant provider in environment variable {}".format(PROVIDER_ENV_VAR_NAME))

        print "Starting Vagrant VM ..."
        cls.vagrant_client.up(provider=provider)
        print "Vagrant VM started"

    @classmethod
    def teardown_class(cls):
        print "Destroying Vagrant VM ..."
        cls.vagrant_client.destroy()
        print "Vagrant VM destroyed"

    def generate_urls():
        host_name = os.environ[HOST_NAME_ENV_VAR_NAME]
        port = os.environ[PORT_ENV_VAR_NAME]

        ok_(host_name, "{} environment variable not defined".format(
            HOST_NAME_ENV_VAR_NAME))
        ok_(port, "{} environment variable not defined".format(PORT_ENV_VAR_NAME))

        yield "http://{}:{}".format(host_name, port)
        yield "http://{}:{}/".format(host_name, port)
        yield "http://{}:{}/index.html".format(host_name, port)

    @parameterized.expand(generate_urls())
    def test_get_success(self, url):
        ok_(url, "test_get_success requires a url parameter")
        ok_(urlparse(url), "{} is an invalid url".format(url))

        response = requests.get(url)

        ok_(response, "No response from {}".format(url))
        eq_(response.headers["content-type"], mimetypes.types_map[".html"])
        eq_(response.status_code, 200, "GET from {} failed with status {}".format(url, response.status_code))
        ok_("Automation for the People" in response.text, "Failed to find expected text in {}".format(response.text))
