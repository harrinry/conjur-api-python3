import unittest
from unittest.mock import patch

from .util.cli_helpers import cli_arg_test, cli_test

from conjur.version import __version__
from conjur.cli import Cli

RESOURCE_LIST = [
    'some_id1',
    'some_id2',
]
WHOAMI_RESPONSE = {
    "account": "myaccount"
}
VAR_HELP = '''Usage:
     conjur [global options] variable <subcommand> [options] <VARIABLE_ID> <VALUE>

positional arguments:
  {get,set}
    get       Get the value of one or more variables
    set       Set the value of a variable

Options:
  -h, --help  Display help list and exit
'''

VAR_GET_HELP = '''usage:  get [-h] variable_id [variable_id ...]

positional arguments:
  variable_id  ID of a variable

optional arguments:
  -h, --help   show this help message and exit
'''

VAR_SET_HELP = '''usage:  set [-h] variable_id value

positional arguments:
  variable_id  ID of the variable
  value        New value of the variable

optional arguments:
  -h, --help   show this help message and exit
'''
class CliTest(unittest.TestCase):
    @cli_test()
    def test_cli_without_args_shows_help(self, cli_invocation, output, client):
        self.assertIn("Usage:", output)

    @patch('conjur.cli.Cli')
    def test_cli_is_run_when_launch_is_invoked(self, cli_instance):
        Cli.launch()

        cli_instance.return_value.run.assert_called_once_with()

    @cli_test(["-h"])
    def test_cli_shows_help_with_short_help_flag(self, cli_invocation, output, client):
        self.assertIn("Usage:", output)

    @cli_test(["--help"])
    def test_cli_shows_help_with_long_help_flag(self, cli_invocation, output, client):
        self.assertIn("Usage:", output)

    @cli_test(["-v"])
    def test_cli_shows_version_with_short_version_flag(self, cli_invocation, output, client):
        self.assertRegex(str(output), f"Conjur CLI version {(__version__)}")

    @cli_test(["--version"])
    def test_cli_shows_version_with_long_version_flag(self, cli_invocation, output, client):
        self.assertRegex(str(output), f"Conjur CLI version {format(__version__)}")

    @cli_test(["-v"])
    def test_cli_check_copyright_short_version_flag(self, cli_invocation, output, client):
        self.assertRegex(str(output), '''
Copyright 2020 CyberArk Software Ltd. All rights reserved.
<www.cyberark.com>
''')

    @cli_test(["--version"])
    def test_cli_check_copyright_long_version_flag(self, cli_invocation, output, client):
        self.assertRegex(str(output), '''
Copyright 2020 CyberArk Software Ltd. All rights reserved.
<www.cyberark.com>
''')

    # Optional params

    # Account
    @cli_arg_test(["-a", "myaccount"], account='myaccount')
    def test_cli_passes_account_short_flag_to_client(self): pass

    @cli_arg_test(["--account", "myaccount"], account='myaccount')
    def test_cli_passes_account_long_flag_to_client(self): pass

    # API key
    @cli_arg_test(["-k", "myapikey"], api_key='myapikey')
    def test_cli_passes_api_key_short_flag_to_client(self): pass

    @cli_arg_test(["--api-key", "myapikey"], api_key='myapikey')
    def test_cli_passes_api_key_long_flag_to_client(self): pass

    # CA Bundle
    @cli_arg_test(["-c", "mycabundle"], ca_bundle='mycabundle')
    def test_cli_passes_ca_bundle_short_flag_to_client(self): pass

    @cli_arg_test(["--ca-bundle", "mycabundle"], ca_bundle='mycabundle')
    def test_cli_passes_ca_bundle_long_flag_to_client(self): pass

    # Debug
    @cli_arg_test(["-d"], debug=True)
    def test_cli_passes_debug_short_flag_to_client(self): pass

    @cli_arg_test(["--debug"], debug=True)
    def test_cli_passes_debug_long_flag_to_client(self): pass

    @cli_arg_test(["--verbose"], debug=True)
    def test_cli_passes_verbose_as_the_debug_long_flag_to_client(self): pass

    # User
    @cli_arg_test(["-u", "myuser"], login_id='myuser')
    def test_cli_passes_login_id_short_flag_to_client(self): pass

    @cli_arg_test(["--user", "myuser"], login_id='myuser')
    def test_cli_passes_login_id_long_flag_to_client(self): pass

    # Password
    @cli_arg_test(["-p", "mypassword"], password='mypassword')
    def test_cli_passes_password_short_flag_to_client(self): pass

    @cli_arg_test(["--password", "mypassword"], password='mypassword')
    def test_cli_passes_password_long_flag_to_client(self): pass

    # SSL Verify
    @cli_arg_test(["--insecure"], ssl_verify=False)
    def test_cli_passes_insecure_flag_to_client(self): pass

    # URL
    @cli_arg_test(["-l", "myurl"], url='myurl')
    def test_cli_passes_url_short_flag_to_client(self): pass

    @cli_arg_test(["--url", "myurl"], url='myurl')
    def test_cli_passes_url_long_flag_to_client(self): pass

    # Main method invocations

    @cli_test(["variable", "set", "foo", "bar"])
    def test_cli_invokes_variable_set_correctly(self, cli_invocation, output, client):
        client.set.assert_called_once_with('foo', 'bar')

    @cli_test(["variable"])
    def test_cli_variable_parser_doesnt_break_without_action(self, cli_invocation, output, client):
        self.assertIn("Usage", output)

    @cli_test(["variable", "-h"])
    def test_cli_variable_short_help(self, cli_invocation, output, client):
        expected = VAR_HELP
        self.assertEquals(expected, output)

    @cli_test(["variable", "--help"])
    def test_cli_variable_long_help(self, cli_invocation, output, client):
        expected = VAR_HELP

        self.assertEquals(expected, output)

    '''TODO - more code is needed for this test to be enabled @cli_test(["variable", "test_var"]) 
    def test_cli_invokes_variable_without_get_or_set(self, cli_invocation, output, client): expected = "conjur 
    variable: error: argument action: invalid choice: 'test_var' (choose from 'get', 'set') \n"+ VAR_HELP 
    self.assertEquals(expected, output) '''

    @cli_test(["variable", "get", "-h"])
    def test_cli_variable_get_help(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_GET_HELP)

    @cli_test(["variable", "get", "--help"])
    def test_cli_variable_get_help_long(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_GET_HELP)

    '''TODO - more code is needed for this test to be enabled 
    @cli_test(["variable", "get"])
    def test_cli_variable_get_help_no_param(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_GET_HELP)
    '''

    @cli_test(["variable", "set", "-h"])
    def test_cli_variable_set_help(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_SET_HELP)

    @cli_test(["variable", "set", "--help"])
    def test_cli_variable_set_help_long(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_SET_HELP)

    '''TODO - more code is needed for this test to be enabled 
    @cli_test(["variable", "set"])
    def test_cli_variable_set_help_no_param(self, cli_invocation, output, client):
        self.assertEquals(output, VAR_SET_HELP)
    '''

    @cli_test(["variable", "get", "foo"])
    def test_cli_invokes_variable_get_correctly(self, cli_invocation, output, client):
        client.get.assert_called_once_with('foo')

    @cli_test(["variable", "get", "foo", "bar"], get_many_output={"foo": "A", "bar": "B"})
    def test_cli_invokes_variable_get_correctly_with_multiple_vars(self, cli_invocation, output, client):
        client.get_many.assert_called_once_with('foo', 'bar')

    @cli_test(["variable", "get", "foo", "bar"], get_many_output={})
    def test_cli_variable_get_with_multiple_vars_doesnt_break_on_empty_input(self, cli_invocation, output, client):
        self.assertEquals('{}\n', output)

    @cli_test(["variable", "get", "foo", "bar"], get_many_output={"foo": "A", "bar": "B"})
    def test_cli_variable_get_with_multiple_vars_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('{\n    "foo": "A",\n    "bar": "B"\n}\n', output)

    @cli_test(["policy"])
    def test_cli_policy_parser_doesnt_break_without_action(self, cli_invocation, output, client):
        self.assertIn("Usage:", output)

    @cli_test(["policy", "apply", "foo", "foopolicy"])
    def test_cli_invokes_policy_apply_correctly(self, cli_invocation, output, client):
        client.apply_policy_file.assert_called_once_with('foo', 'foopolicy')

    @cli_test(["policy", "apply", "foo", "foopolicy"], policy_change_output={})
    def test_cli_policy_apply_doesnt_break_on_empty_input(self, cli_invocation, output, client):
        self.assertEquals('{}\n', output)

    @cli_test(["policy", "apply", "foo", "foopolicy"], policy_change_output={"foo": "A", "bar": "B"})
    def test_cli_policy_apply_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('{\n    "foo": "A",\n    "bar": "B"\n}\n', output)

    @cli_test(["policy", "replace", "foo", "foopolicy"])
    def test_cli_invokes_policy_replace_correctly(self, cli_invocation, output, client):
        client.replace_policy_file.assert_called_once_with('foo', 'foopolicy')

    @cli_test(["policy", "replace", "foo", "foopolicy"], policy_change_output={})
    def test_cli_policy_replace_doesnt_break_on_empty_input(self, cli_invocation, output, client):
        self.assertEquals('{}\n', output)

    @cli_test(["policy", "replace", "foo", "foopolicy"], policy_change_output={"foo": "A", "bar": "B"})
    def test_cli_policy_replace_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('{\n    "foo": "A",\n    "bar": "B"\n}\n', output)

    @cli_test(["policy", "delete", "foo", "foopolicy"])
    def test_cli_invokes_policy_delete_correctly(self, cli_invocation, output, client):
        client.delete_policy_file.assert_called_once_with('foo', 'foopolicy')

    @cli_test(["policy", "delete", "foo", "foopolicy"], policy_change_output={})
    def test_cli_policy_delete_doesnt_break_on_empty_input(self, cli_invocation, output, client):
        self.assertEquals('{}\n', output)

    @cli_test(["policy", "delete", "foo", "foopolicy"], policy_change_output={"foo": "A", "bar": "B"})
    def test_cli_policy_delete_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('{\n    "foo": "A",\n    "bar": "B"\n}\n', output)

    @cli_test(["list"], list_output=RESOURCE_LIST)
    def test_cli_invokes_resource_listing_correctly(self, cli_invocation, output, client):
        client.list.assert_called_once_with()

    @cli_test(["list"], list_output=RESOURCE_LIST)
    def test_cli_resource_listing_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('[\n    "some_id1",\n    "some_id2"\n]\n', output)

    @cli_test(["whoami"], whoami_output=WHOAMI_RESPONSE)
    def test_cli_invokes_whoami_correctly(self, cli_invocation, output, client):
        client.whoami.assert_called_once_with()

    @cli_test(["whoami"], whoami_output=WHOAMI_RESPONSE)
    def test_cli_invokes_whoami_outputs_formatted_json(self, cli_invocation, output, client):
        self.assertEquals('{\n    "account": "myaccount"\n}\n', output)
