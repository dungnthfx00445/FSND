
import json

from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    header = request.headers.get("Authorization", None)
    if not header:
        raise AuthError(
            error={
                "code": "authorization_header_missing",
                "description": "Authorization header is expected."
            },
            status_code=401
        )
    token = header.split()
    if token[0].lower() != "bearer":
        raise AuthError(
            error={
                "code": "invalid_header",
                "description": 'Authorization header must start with "Bearer".'
            },
            status_code=401
        )
    elif len(token) == 1:
        raise AuthError(
            error={
                "code": "invalid_header",
                "description": "Token not found."
            },
            status_code=401
        )
    elif len(token) > 2:
        raise AuthError(
            error={
                "code": "invalid_header",
                "description": "Authorization header must be bearer token."
            },
            status_code=401
        )
    return token[1]

def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            error={
                "code": "invalid_claims",
                "description": "Permissions not included in JWT."
            },
            status_code=400
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            error={
                "code": "unauthorized",
                "description": "Permission not found."
            },
            status_code=403
        )
    return True

def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_keys = {}
    if "kid" not in unverified_header:
        raise AuthError(
            error={
                "code": "invalid_header",
                "description": "Authorization malformed."
            },
            status_code=401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_keys = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_keys:
        try:
            payload = jwt.decode(
                token=token,
                key=rsa_keys,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                error={
                    "code": "token_expired",
                    "description": "Token expired."
                },
                status_code=401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                error={
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer."},
                status_code=401)
        except Exception:
            raise AuthError(
                error={
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                },
                status_code=400
            )
    raise AuthError(
        error={
            "code": "invalid_header",
            "description": "Unable to find the appropriate key."
        },
        status_code=403
    )

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as error:
                abort(code=error.status_code)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator