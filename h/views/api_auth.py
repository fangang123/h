# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from h.auth.services import TOKEN_TTL
from h.exceptions import OAuthTokenError
from h.schemas import JSONSchema, ValidationError
from h.util.view import json_view


log = logging.getLogger(__name__)

ACCESS_TOKEN_SCHEMA = None


@json_view(route_name='token', request_method='POST')
def access_token(request):
    schema = get_access_token_schema()
    appstruct = schema.validate(request.json_body)

    svc = request.find_service(name='oauth')

    user, authclient = svc.verify_jwt_bearer(
        assertion=appstruct.get('assertion'),
        grant_type=appstruct.get('grant_type'))
    token = svc.create_token(user, authclient)

    return {
        'access_token': token.value,
        'token_type': 'bearer',
        'expires_in': TOKEN_TTL.total_seconds(),
    }


@json_view(context=OAuthTokenError)
def api_token_error(context, request):
    """Handle an expected/deliberately thrown API exception."""
    return _render_oauth_error(request, context.type, context.message, context.status_code)


@json_view(context=ValidationError)
def validation_error(context, request):
    """Handle an expected/deliberately thrown API exception."""
    return _render_oauth_error(request, 'invalid_request', context.message, 400)


def get_access_token_schema():
    global ACCESS_TOKEN_SCHEMA

    if ACCESS_TOKEN_SCHEMA is None:
        ACCESS_TOKEN_SCHEMA = JSONSchema('h/schemas/api_token.json')
    return ACCESS_TOKEN_SCHEMA


def _render_oauth_error(request, type_, message, status_code=400):
    request.response.status_code = status_code
    resp = {'error': type_}
    if message:
        resp['error_description'] = message
    return resp
