import sys
from sys import platform

try:
    import colorama
    from colorama import init
except ImportError as exc:
    print('\nScript need \'colorama\' module to work. Read README.md to resolve the issue \n')
    exit(1)

if platform == 'win32':
    init()

from colors import Color

if sys.version_info < (3, 4, 0):
    print(Color.error('\nYou need python 3.4 or later to run this script. Possibly you should start the command from calling \'python3\' instead of \'python\'\n'))
    exit(1)

try:
    import requests
except ImportError as exc:
    print(Color.error('\nScript need \'requests\' module to work. Read README.md to resolve the issue \n'))
    exit(1)

try:  # Suppress requests warning connected with disabled verify. Needed only in python 3.5. In python 3.4 that package doesn't exist and message is not visible
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError as exc:
    pass

import argparse

from api_classes.api_submit_url import ApiSubmitUrl
from api_classes.api_submit_file import ApiSubmitFile
from api_classes.api_quota import ApiQuota
from api_classes.api_state import ApiState
from api_classes.api_scan import ApiScan
from api_classes.api_summary import ApiSummary
from api_classes.api_search import ApiSearch
from api_classes.api_relationships import ApiRelationships
from api_classes.api_feed import ApiFeed
from api_classes.api_system_stats import ApiSystemStats
from api_classes.api_system_state import ApiSystemState
from api_classes.api_system_backend import ApiSystemBackend
from api_classes.api_system_queue_size import ApiSystemQueueSize
from api_classes.api_system_in_progress import ApiSystemInProgress
from api_classes.api_system_heartbeat import ApiSystemHeartbeat
from api_classes.api_result import ApiResult
from api_classes.api_reanalyze import ApiReanalyze
from api_classes.api_dropped_file_submit import ApiDroppedFileSubmit
from api_classes.api_sample_dropped_files import ApiSampleDroppedFiles
from api_classes.api_sample_screenshots import ApiSampleScreenshots
from api_classes.api_api_key_data import ApiApiKeyData

from cli_classes.cli_quota import CliQuota
from cli_classes.cli_state import CliState
from cli_classes.cli_scan import CliScan
from cli_classes.cli_summary import CliSummary
from cli_classes.cli_search import CliSearch
from cli_classes.cli_relationships import CliRelationships
from cli_classes.cli_feed import CliFeed
from cli_classes.cli_system_stats import CliSystemStats
from cli_classes.cli_system_state import CliSystemState
from cli_classes.cli_system_heartbeat import CliSystemHeartbeat
from cli_classes.cli_system_backend import CliSystemBackend
from cli_classes.cli_system_in_progress import CliSystemInProgress
from cli_classes.cli_system_queue_size import CliSystemQueueSize
from cli_classes.cli_result import CliResult
from cli_classes.cli_submit_file import CliSubmitFile
from cli_classes.cli_submit_url_file import CliSubmitUrlFile
from cli_classes.cli_submit_url import CliSubmitUrl
from cli_classes.cli_reanalyze import CliReanalyze
from cli_classes.cli_dropped_file_submit import CliDroppedFileSubmit
from cli_classes.cli_sample_dropped_files import CliSampleDroppedFiles
from cli_classes.cli_sample_screenshots import CliSampleScreenshots

from exceptions import MissingConfigurationError
from exceptions import RetrievingApiKeyDataError

import datetime
import os.path

from collections import OrderedDict
from cli_classes.cli_argument_builder import CliArgumentBuilder

def main():
    try:
        if os.path.exists('config.py'):
            from config import get_config
            config = get_config()
        else:
            raise MissingConfigurationError('Configuration is missing. Before running CLI, please copy the file \'config_tpl.pl\' from current dir, rename it to \'config.pl\', and fill')
    
        program_name = 'VxWebService Python API Connector'
        program_version = '1.00'


        if config['server'].endswith('/'):
            config['server'] = config['server'][:-1]

        map_of_available_actions = OrderedDict([
            ('get_feed', CliFeed(ApiFeed(config['api_key'], config['api_secret'], config['server']))),
            ('get_relationships', CliRelationships(ApiRelationships(config['api_key'], config['api_secret'], config['server']))),
            ('get_result', CliResult(ApiResult(config['api_key'], config['api_secret'], config['server']))),
            ('get_sample_dropped_files', CliSampleDroppedFiles(ApiSampleDroppedFiles(config['api_key'], config['api_secret'], config['server']))),
            ('get_sample_screenshots', CliSampleScreenshots(ApiSampleScreenshots(config['api_key'], config['api_secret'], config['server']))),
            ('get_scan', CliScan(ApiScan(config['api_key'], config['api_secret'], config['server']))),
            ('get_state', CliState(ApiState(config['api_key'], config['api_secret'], config['server']))),
            ('get_summary', CliSummary(ApiSummary(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_backend', CliSystemBackend(ApiSystemBackend(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_in_progress', CliSystemInProgress(ApiSystemInProgress(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_heartbeat', CliSystemHeartbeat(ApiSystemHeartbeat(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_state', CliSystemState(ApiSystemState(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_stats', CliSystemStats(ApiSystemStats(config['api_key'], config['api_secret'], config['server']))),
            ('get_system_queue_size', CliSystemQueueSize(ApiSystemQueueSize(config['api_key'], config['api_secret'], config['server']))),
            ('get_quota', CliQuota(ApiQuota(config['api_key'], config['api_secret'], config['server']))),
            ('reanalyze_sample', CliReanalyze(ApiReanalyze(config['api_key'], config['api_secret'], config['server']))),
            ('search', CliSearch(ApiSearch(config['api_key'], config['api_secret'], config['server']))),
            ('submit_dropped_file', CliDroppedFileSubmit(ApiDroppedFileSubmit(config['api_key'], config['api_secret'], config['server']))),
            ('submit_file', CliSubmitFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            ('submit_url_file', CliSubmitUrlFile(ApiSubmitFile(config['api_key'], config['api_secret'], config['server']))),
            ('submit_url', CliSubmitUrl(ApiSubmitUrl(config['api_key'], config['api_secret'], config['server']))),
        ])

        api_object_api_key_data = ApiApiKeyData(config['api_key'], config['api_secret'], config['server'])
        api_object_api_key_data.call()
        if api_object_api_key_data.get_response_status_code() != 200 or api_object_api_key_data.get_response_json()['response_code'] != 0:
            raise RetrievingApiKeyDataError('Can\'t retrieve data for api_key \'{}\' in the webservice: \'{}\'. Response status code: \'{}\''.format(config['api_key'], config['server'], api_object_api_key_data.get_response_status_code()))

        used_api_key_data = api_object_api_key_data.get_response_json()['response']
        parser = argparse.ArgumentParser(description=program_name, formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
        parser.add_argument('--version', '-ver', action='version', version='{} - version {}'.format(program_name, program_version))
        CliArgumentBuilder(parser).add_help_argument()
    
        subparsers = parser.add_subparsers(help='Action names for \'{}\' auth level'.format(used_api_key_data['auth_level_name']), dest="chosen_action")
    
        for name, cli_object in map_of_available_actions.items():
            if cli_object.api_object.endpoint_auth_level <= used_api_key_data['auth_level']:
                child_parser = subparsers.add_parser(name=name, help=cli_object.help_description, add_help=False)
                cli_object.add_parser_args(child_parser)
    
        args = vars(parser.parse_args())

        if args['chosen_action'] is not None:
            cli_object = map_of_available_actions[args['chosen_action']]
            cli_object.attach_args(args)
            if args['verbose'] is True:
                cli_object.init_verbose_mode()
                print(Color.control('Running \'{}\' in version \'{}\''.format(program_name, program_version)))

                print(Color.control('Started checking used API Key at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                print('API Key: {}'.format(used_api_key_data['api_key']))
                print('Auth Level: {}'.format(used_api_key_data['auth_level_name']))
                if used_api_key_data['user'] is not None:
                    print('User: {} ({})'.format(used_api_key_data['user']['name'], used_api_key_data['user']['email']))

                print(Color.control('Request was sent at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                print('Endpoint URL: {}'.format(cli_object.api_object.get_full_endpoint_url()))
                print('HTTP Method: {}'.format(cli_object.api_object.request_method_name.upper()))
                print('Sent GET params: {}'.format(cli_object.api_object.params))
                print('Sent POST params: {}'.format(cli_object.api_object.data))
                print('Sent files: {}'.format(cli_object.api_object.files))

            cli_object.api_object.call()
            if args['verbose'] is True:
                print(Color.control('Received response at ' + '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                print('Response status code: {}'.format(cli_object.get_colored_response_status_code()))
                print('Message: {}'.format(cli_object.get_colored_prepared_response_msg()))
                print(Color.control('Showing response'))

            print(cli_object.get_result_msg())
            cli_object.do_post_processing()

            if args['verbose'] is True:
                print('\n')
        else:
            print(Color.control('No option was selected. To check CLI options, run script in help mode: \'{} -h\''.format(__file__)))
    except Exception as exc:
        print(Color.control('During the code execution, error has occurred. Please try again or contact the support.'))
        print(Color.error('Message: \'{}\'.').format(str(exc)) + '\n')

if __name__ == "__main__":
    main()
