import json
import decimal
import datetime
import time
import urllib
import urllib.parse as urlparse

import requests

from sa import app


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return datetime.datetime.strftime(obj, "%m/%d/%Y")
        return json.JSONEncoder.default(self, obj)


def call_api(method, rule, user_data=None):
    IDEMPOTENT_METHODS = ("GET", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH")
    if not user_data:
        user_data = {}
    elif not isinstance(user_data, dict):
        user_data = dict(user_data)

    method = str(method).strip().lower()
    payload = {
        "app_token": app.config["APP_TOKEN"],
        "timestamp": time.time(),
        **user_data,
    }

    if method.upper() in IDEMPOTENT_METHODS:
        request_data = {"params": payload}
    else:
        request_data = {"data": json.dumps(payload, cls=Encoder)}

    if rule.startswith("/"):
        rule = rule[1:]

    if not rule.endswith("/"):
        rule = "".join([rule, "/"])

    route = app.config["API_URL"].format(rule)

    response = getattr(requests, method)(route, **request_data)
    print(response.json())
    response.raise_for_status()
    return response.json()
    
def sign_in_url():
    url_parts = list(urlparse.urlparse(app.config["O365_AUTH_URL"]))
    auth_params = {
        'response_type': 'code',
        'redirect_uri': app.config["O365_REDIRECT_URI"],
        'client_id': app.config["O365_APP_ID"]
    }
    print(app.config["O365_REDIRECT_URI"])
    url_parts[4] = urllib.parse.urlencode(auth_params)
    return urlparse.urlunparse(url_parts)


def get_oauth_token(code):
    token_params = {
        'grant_type': 'authorization_code',
        'redirect_uri': app.config["O365_REDIRECT_URI"],
        'client_id': app.config["O365_APP_ID"],
        'client_secret': app.config["O365_APP_KEY"],
        'code': code,
        'resource': 'https://graph.microsoft.com/'
    }

    r = requests.post(app.config["O365_TOKEN_URL"], data=token_params)

    return r.json()


def get_jwt_from_id_token(id_token):
    encoded_jwt = id_token.split('.')[1]
    if len(encoded_jwt) % 4 == 2:
        encoded_jwt += '=='
    else:
        encoded_jwt += '='

    return json.loads(base64.b64decode(encoded_jwt))
    
    
def dict_without(d, *keys):
   prohibited = set(keys)
   return {k: v for k, v in d.items() if k not in prohibited}