# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from h.schemas import JSONSchema


class TestJWTBearerPayload(object):
    def test_valid(self, schema, payload):
        schema.validate(payload)

    def test_requires_assertion(self, schema, payload):
        del payload['assertion']
        schema.validate(payload)

    @pytest.fixture
    def schema(self):
        return JSONSchema('h/schemas/api_token.json')

    @pytest.fixture
    def payload(self):
        return {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': 'eyJh_.eyJ_.VRSspS_',
        }
