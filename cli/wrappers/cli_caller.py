from api.callers.api_caller import ApiCaller
from exceptions import FilesSavingMethodNotDeclaredError
from exceptions import ResponseTextContentTypeError
from colors import Color
import errno
import os
import json
from cli.arguments_builders.default_cli_arguments import DefaultCliArguments
import datetime
from cli.cli_file_writer import CliFileWriter


class CliCaller:

    api_object = None
    action_name = None
    help_description = ''
    given_args = {}
    result_msg_for_files = 'Response contains files. They were saved in the output folder ({}).'
    result_msg_for_json = '{}'
    cli_output_folder = ''
    args_to_prevent_from_being_send = ['chosen_action', 'verbose', 'quiet']

    def __init__(self, api_object: ApiCaller, action_name: str):
        self.api_object = api_object
        self.action_name = action_name
        self.help_description = self.help_description.format(self.api_object.endpoint_url)

    def init_verbose_mode(self):
        self.result_msg_for_json = 'JSON:\n\n{}'

    def build_argument_builder(self, child_parser):
        return DefaultCliArguments(child_parser)

    def add_parser_args(self, child_parser):
        parser_argument_builder = self.build_argument_builder(child_parser)
        parser_argument_builder.add_verbose_argument()
        parser_argument_builder.add_help_argument()
        parser_argument_builder.add_quiet_argument()

        return parser_argument_builder

    def attach_args(self, args):
        self.given_args = args.copy()
        args_to_send = args.copy()
        for arg_to_remove in self.args_to_prevent_from_being_send:
            if arg_to_remove in args_to_send:
                del args_to_send[arg_to_remove]

        if 'output' in args:
            self.cli_output_folder = args['output']
            del args_to_send['output']

        args_to_send = {k: v for k, v in args_to_send.items() if v not in [None, '']}  # Removing some 'empty' elements from dictionary

        if 'file' in args:
            del args_to_send['file'] # attaching file is handled by separated method

        for param in ['no_share_third_party', 'allowCommunityAccess']:
            if param in args:
                args_to_send[param] = 1 if args[param] == 'yes' else 0

        if self.api_object.request_method_name == ApiCaller.CONST_REQUEST_METHOD_GET:
            self.api_object.attach_params(args_to_send)
        else:  # POST
            self.api_object.attach_data(args_to_send)

    def attach_file(self, file_handler):
        self.api_object.attach_files({'file': file_handler})  # it's already stored as file handler

    def get_colored_response_status_code(self):
        response_code = self.api_object.get_response_status_code()

        return Color.success(response_code) if self.api_object.if_request_success() is True else Color.error(response_code)

    def get_colored_prepared_response_msg(self):
        response_msg = self.api_object.get_prepared_response_msg()

        return Color.success(response_msg) if self.api_object.if_request_success() is True else Color.error(response_msg)

    def get_result_msg(self):
        if self.api_object.api_response.headers['Content-Type'] == 'text/html':
            raise ResponseTextContentTypeError('Can\'t print result, since it\'s \'text/html\' instead of expected content type with \'{}\' on board.'.format(self.api_object.api_expected_data_type))

        if self.api_object.api_expected_data_type == ApiCaller.CONST_EXPECTED_DATA_TYPE_JSON:
            return self.result_msg_for_json.format(json.dumps(self.api_object.get_response_json(), indent=4, sort_keys=True, ensure_ascii=False))
        elif self.api_object.api_expected_data_type == ApiCaller.CONST_EXPECTED_DATA_TYPE_FILE:
            if self.api_object.if_request_success() is True:
                return self.get_result_msg_for_files()
            else:
                error_msg = 'Error has occurred and your files were not saved.'
                if self.given_args['verbose'] is False:
                    error_msg += ' To get more information, please run command in verbose mode. (add \'-v\')'

                return error_msg

    def get_processed_output_path(self):
        output_path = self.cli_output_folder
        if output_path.startswith('/') is True:  # Given path is absolute
            final_output_path = output_path
        else:
            prepared_file_path = os.path.dirname(os.path.realpath(__file__)).split('/')[:-2] + [self.cli_output_folder]
            final_output_path = '/'.join(prepared_file_path)

        return final_output_path

    def get_result_msg_for_files(self):
        return self.result_msg_for_files.format(self.get_processed_output_path())

    def do_post_processing(self):
        if self.api_object.api_expected_data_type == ApiCaller.CONST_EXPECTED_DATA_TYPE_FILE and self.api_object.if_request_success() is True:
            self.save_files()

    def get_date_string(self):
        now = datetime.datetime.now()
        return '{}_{}_{}_{}_{}_{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)

    def convert_file_hashes_to_array(self, args, file_arg='hash_list', key_of_array_arg='hashes'):
        with args[file_arg] as file:
            hashes = file.read().splitlines()

            if not hashes:
                raise Exception('Given file does not contain any data.')

            for key, value in enumerate(hashes):
                args['{}[{}]'.format(key_of_array_arg, key)] = value

        del args[file_arg]

        return args

    def save_files(self):
        api_response = self.api_object.api_response
        identifier = None
        if 'id' in self.given_args:
            identifier = self.given_args['id']
        elif 'sha256' in self.given_args:
            identifier = self.given_args['sha256']

        filename = '{}-{}-{}'.format(self.action_name, identifier, api_response.headers['Vx-Filename']) if identifier is not None else '{}-{}'.format(self.action_name, api_response.headers['Vx-Filename'])

        return CliFileWriter.write(self.cli_output_folder, filename, api_response.content)