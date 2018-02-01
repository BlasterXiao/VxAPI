import argparse
from argparse import ArgumentParser
from constants import ACTION_GET_ENVIRONMENTS
from constants import ACTION_GET_NSSF_LIST


class CliArgumentBuilder:

    def __init__(self, parser: ArgumentParser):
        self.parser = parser

    def add_sha256_argument(self):
        self.parser.add_argument('sha256', type=str, help='Sample sha256 hash')

    def add_submit_name_argument(self):
        self.parser.add_argument('--submitname', '-sn', type=str, help='\'submission name\' field that will be used for file type detection and analysis')

    def add_comment_argument(self):
        self.parser.add_argument('--comment', '-c', type=str, help='Add comment (e.g. #hashtag) to sample')

    def add_priority_argument(self):
        def check_value_range(value):
            forced_int_value = int(value)
            if forced_int_value < 0 or forced_int_value > 100:
                raise argparse.ArgumentTypeError('{} is not a value between 0 and 100'.format(value))
            return forced_int_value

        self.parser.add_argument('--priority', '-pr', type=check_value_range, help='Priority value between 0 (default) and 100 (highest)')

    def add_hash_argument(self):
        self.parser.add_argument('hash', type=str, help='Sample hash (md5, sha1 or sha256)')

    def add_dropped_file_name_argument(self):
        self.parser.add_argument('fileName', type=str, help='Dropped file name')

    def add_environment_id_argument(self, required: bool = False):
        environment_id_help = 'Sample Environment ID (use \'{}\' action to fetch all available)'.format(ACTION_GET_ENVIRONMENTS)
        if required is False:
            self.parser.add_argument('--environmentId', '-env', type=int, help=environment_id_help)
        else:
            self.parser.add_argument('environmentId', type=int, help=environment_id_help)

    def add_nosharevt_argument(self):
        self.parser.add_argument('--private', '-pv', help='Keep it private or share with community', type=str, choices=['yes', 'no'], default='yes', dest="nosharevt")

    def add_days_argument(self):
        self.parser.add_argument('days', type=str, help='Days')

    def add_file_type_argument(self):
        self.parser.add_argument('--type', '-t', type=str, choices=['bin', 'json', 'pdf', 'crt', 'maec', 'misp', 'misp-json', 'openioc', 'html', 'pcap', 'memory', 'xml'], default='xml', help='File type to return')

    def add_cli_output_argument(self):
        self.parser.add_argument('--cli_output', '-o', type=str, default='output', help='Output path')

    def add_query_search_argument(self):
        self.parser.add_argument('query', type=str, help='Search query. Once you want to search by multiple terms, wrap it into quotes e.g. \'python3 vxapi.py search "filetype_tag:doc filename:invoice"\'')

    def add_submit_file_argument(self):
        self.parser.add_argument('file', type=argparse.FileType('rb'), help='File to submit')

    def add_submitted_document_password_argument(self):
        self.parser.add_argument('--document-password', '-dp', type=str, help='Password used for archive extraction', dest="documentPassword")

    def add_analyze_url_argument(self):
        self.parser.add_argument('analyzeurl', type=str, help='Url which contains file')

    def add_url_file_argument(self):
        self.parser.add_argument('fileurl', type=str, help='Url which contains file')

    def add_url_hash_argument(self):
        self.parser.add_argument('url', type=str, help='Url to hash')

    def add_verbose_argument(self):
        self.parser.add_argument('--verbose', '-v', help="Run command in verbose mode", action='store_true')

    def add_help_argument(self):
        self.parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    def add_quiet_argument(self):
        self.parser.add_argument('--quiet', '-q',  action='store_true', default=False, help='Suppress all prompts and warnings')

    def add_hash_format_argument(self):
        self.parser.add_argument('--hash-format', '-hf', choices=['md5', 'sha1', 'sha256', 'sha256'], default='md5', help='Type of returned hash', dest="format")

    def add_visibility_argument(self):
        self.parser.add_argument('--visibility', '-vs', choices=['all', 'private', 'public'], default='public', help='Samples visibility')

    def add_verdict_format_argument(self):
        self.parser.add_argument('--verdict-format', '-vf', choices=['all', 'malicious', 'clean'], default='all', help='Samples verdict format', dest="type")

    def add_from_date_argument(self):
        self.parser.add_argument('--from-date', '-fd', type=str, help='Filter from date - ISO format', dest="from")

    def add_to_date_argument(self):
        self.parser.add_argument('--to-date', '-td', type=str, help='Filter to date - ISO format', dest="to")

    def add_file_with_hash_list(self):
        self.parser.add_argument('hash_list', type=argparse.FileType('r'), help='Path to file containing list of sample hashes(can be generated by \'{}\' action)'.format(ACTION_GET_NSSF_LIST))

    def add_file_with_hash_list_with_envs(self):
        self.parser.add_argument('hash_list_with_envs', type=argparse.FileType('r'), help='Path to file containing list of sample hashes with environment IDs (hash:envId)')

