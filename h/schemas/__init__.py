# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy
import json
import jsonschema
from jsonschema.exceptions import best_match


class ValidationError(Exception):
    pass


class JSONSchema(object):
    """
    Validate data according to a Draft 4 JSON Schema.
    Inherit from this class and override the `schema` class property with a
    valid JSON schema.
    """

    def __init__(self, path):
        schema = self.load(path)
        self.validator = jsonschema.Draft4Validator(schema)

    def validate(self, data):
        """
        Validate `data` according to the current schema.
        :param data: The data to be validated
        :return: valid data
        :raises ValidationError: if the data is invalid
        """
        # Take a copy to ensure we don't modify what we were passed.
        appstruct = copy.deepcopy(data)
        for e in self.validator.iter_errors(appstruct):
            print(e)
            print('---')
        error = best_match(self.validator.iter_errors(appstruct))
        if error is not None:
            print(_format_jsonschema_error(error))
            raise ValidationError(_format_jsonschema_error(error))
        return appstruct

    def load(self, path):
        with open(path) as fp:
            return json.load(fp)


def _format_jsonschema_error(error):
    """Format a :py:class:`jsonschema.ValidationError` as a string."""
    if error.path:
        dotted_path = '.'.join([str(c) for c in error.path])
        return '{path}: {message}'.format(path=dotted_path,
                                          message=error.message)
    return error.message
