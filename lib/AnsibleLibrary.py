#!/usr/bin/python

import ansible.runner
from robot.api import logger
from robot.utils import asserts

class AnsibleLibrary(object):

    def __init__(self):
        pass

    def get_default_ansible_params(self):
        """ 
        Return a dictionary of default parameters to the runner, compatible 
        with Ansible 0.7.1
        """
        import ansible.constants as C
        return { 
                "host_list": C.DEFAULT_HOST_LIST,
                "module_path": C.DEFAULT_MODULE_PATH,
                "module_name": C.DEFAULT_MODULE_NAME,
                "module_args": C.DEFAULT_MODULE_ARGS,
                "forks": C.DEFAULT_FORKS,
                "timeout": C.DEFAULT_TIMEOUT,
                "pattern": C.DEFAULT_PATTERN,
                "remote_user": C.DEFAULT_REMOTE_USER,
                "remote_pass": C.DEFAULT_REMOTE_PASS,
                "remote_port": C.DEFAULT_REMOTE_PORT,
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
                }

    def set_ansible_param(self, params, k, v):
        """
        Override or set a key in a dictionary containing ansible parameters
        @param params: the dictionary of Ansible Runner parameters
        @param k: key name
        @param v: destired key value
        """
        if not params.has_key(k):
            logger.info("Parameters did not contain key %s, adding..." % k)
        params[k] = v
        return params

    def run_ansible_basic(self, pattern, forks, moduleName, moduleArgs):
        """
        Run Ansible in a basic mode, which only allows the user to specify
        host pattern, number of forks, and the module name/args.
        @param pattern: host name patter, see Ansible docs for further info
        @param forks: number of concurrent hosts, see Ansible docs...
        @param moduleName: name of the module to run
        @param moduleArgs: arguments to the module
        """
        result = ansible.runner.Runner(pattern, forks, moduleName, moduleArgs)
        logger.debug(result)
        return result

    def run_ansible_extended_params(self, paramDict):
        """
        Run Ansible by passing Runner a dict of parameters
        @param paramDict:
        """
        result = ansible.runner.Runner(**paramDict).run()
        logger.debug(result)
        return result

    def ansible_result_host_is_dark(self, result, host):
        """
        Assert a host did not get a response
        @param result: result returned from Runner.run()
        @param host: host name
        """
        asserts.assert_true( 
                result["dark"].has_key(host))

    def ansible_result_host_is_contacted(self, result, host):
        """
        Assert a host did get a response, but not testing if it succeeded
        @param result: result returned from Runner.run()
        @param host: host name
        """
        asserts.assert_true(
                result["contacted"].has_key(host))

    def ansible_result_host_is_successful(self, result, host):
        """
        Assert a host got a response and the module executed successfully
        @param result: result returned from Runner.run()
        @param host: host name
        """
        asserts.assert_true(
                ("failed" not in result["contacted"][host]) and
                (result["contacted"][host].get("rc", 0) == 0)
                )

    def ansible_result_host_message(self, result, host):
        """
        Get the message (if one exists, otherwise empty string) whether the 
        module executed successfully or not.
        @param result: result returned from Runner.run()
        @param host: host name
        """
        mergedResults = dict(result["contacted"].items() + result["dark"].items())
        if not mergedResults.has_key(host):
            asserts.fail("No entry in results for host %s" % host)
        return mergedResults[host].get("msg", "") # returns empty string by default
