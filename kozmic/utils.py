"""
kozmic.utils
~~~~~~~~~~~~
"""
import json
import github3

from sqlalchemy import types


def get_pull_request_url(payload):
    try:
        return github3.pulls.PullRequest(payload.get('pull_request', {})).html_url
    except:
        return ''


class JSONEncodedDict(types.TypeDecorator):
    """Represents an immutable structure as a JSON-encoded string."""
    impl = types.LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
