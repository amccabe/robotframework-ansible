#!/usr/bin/python

import ansible.runner
from robot.api import logger
from robot.utils import asserts

class AnsibleLibrary(object):

    def __init__(self):
        pass

    def get_default_ansible_params(self):
        # See ansible.runner.Runner.__init__
        import ansible.constants as C
        return { 
                "host_list": C.DEFAULT_HOST_LIST,
                "module_path": None,
                "module_name": C.DEFAULT_MODULE_NAME,
                "module_args": C.DEFAULT_MODULE_ARGS,
                "forks": C.DEFAULT_FORKS,
                "timeout": C.DEFAULT_TIMEOUT,
                "pattern": C.DEFAULT_PATTERN,
                "remote_user": C.DEFAULT_REMOTE_USER,
                "remote_pass": C.DEFAULT_REMOTE_PASS,
                "remote_port": None,
                "private_key_file": C.DEFAULT_PRIVATE_KEY_FILE,
                "sudo_pass": C.DEFAULT_SUDO_PASS,
                "background": 0,
                "basedir": None,
                "setup_cache": None,
                "transport": C.DEFAULT_TRANSPORT,
                "conditional": 'True',
                "callbacks": None,
                "sudo": False,
                "sudo_user": C.DEFAULT_SUDO_USER,
                "module_vars": None,
                "is_playbook": False, 
                "inventory": None,
                "subset": None,
                "check": False,
                "diff": False,
                "environment": None,
                "complex_args": None
                }

    def set_ansible_param(self, params, k, v):
        if not params.has_key(k):
            logger.info("Parameters did not contain key %s, adding..." % k)
        params[k] = v
        return params

    def run_ansible_basic(self, pattern, forks, moduleName, moduleArgs):
        result = ansible.runner.Runner(pattern, forks, moduleName, moduleArgs)
        logger.debug(result)
        return result

    def run_ansible_extended_params(self, paramDict):
        result = ansible.runner.Runner(**paramDict)
        logger.debug(result)
        return result

    def ansible_result_host_is_dark(self, result, host):
        asserts.assert_true( 
                result["dark"].has_key(host))

    def ansible_result_host_is_contacted(self, result, host):
        asserts.assert_true(
                result["contacted"].has_key(host))

    def ansible_result_host_is_successful(self, result, host):
        asserts.assert_true(
                ("failed" not in result["contacted"][host]) and
                (result["contacted"][host].get("rc", 0) == 0)
                )

    def get_ansible_result_host_message(self, result, host):
        mergedResults = dict(result["contacted"].items() + result["dark"].items())
        if not mergedResults.has_key(host):
            asserts.fail("No entry in results for host %s" % host)
        return mergedResults[host].get("msg", "") # returns empty string by default
