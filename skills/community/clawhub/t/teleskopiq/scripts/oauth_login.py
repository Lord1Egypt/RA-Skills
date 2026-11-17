"""Browser authorization and private, audience-bound OAuth credentials for the CLI."""
import contextlib
try:
    import fcntl
except ImportError:
    fcntl = None
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.parse import urlparse
import webbrowser

import requests

CLIENT_ID = 'teleskopiq-skill'
DEVICE_GRANT = 'urn:ietf:params:oauth:grant-type:device_code'
DEFAULT_SCOPES = 'scripts:read scripts:write thumbnails:write channel:read'


class OAuthError(RuntimeError):
    pass


def validate_endpoint(endpoint):
    parsed = urlparse(endpoint)
    if (parsed.scheme != 'https' and not (parsed.scheme == 'http' and
            parsed.hostname in {'localhost', '127.0.0.1', '::1'})):
        raise OAuthError('Use HTTPS (HTTP is allowed only for localhost)')
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path != '/api/graphql':
        raise OAuthError('OAuth requires an endpoint like https://teleskopiq.com/api/graphql')
    return f'{parsed.scheme}://{parsed.netloc}'


class OAuthCredentials:
    def __init__(self, endpoint, path=None, session=None):
        self.endpoint = endpoint
        self.issuer = validate_endpoint(endpoint)
        self.path = Path(path or os.environ.get('TELESKOPIQ_OAUTH_FILE', '~/.config/teleskopiq/oauth.json')).expanduser()
        self.session = session or requests.Session()

    @contextlib.contextmanager
    def locked(self):
        if fcntl is None:
            raise OAuthError('Browser OAuth login currently supports Linux and macOS')
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        lock_path = self.path.with_suffix('.lock')
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            os.fchmod(fd, 0o600)
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            os.close(fd)

    def read(self):
        if not self.path.exists():
            return None
        fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd) as file:
            if os.fstat(file.fileno()).st_mode & 0o077:
                raise OAuthError('OAuth credential file must have mode 0600')
            try:
                value = json.load(file)
            except ValueError:
                raise OAuthError('Invalid OAuth credential file; run login again') from None
        if not isinstance(value, dict) or value.get('resource') != self.endpoint:
            raise OAuthError('Saved OAuth login belongs to a different endpoint; use a separate TELESKOPIQ_OAUTH_FILE')
        if (not re.fullmatch(r'tso_[A-Za-z0-9_-]{43}', str(value.get('access_token', ''))) or
                not re.fullmatch(r'tsr_[A-Za-z0-9_-]{43}', str(value.get('refresh_token', ''))) or
                not isinstance(value.get('channel_id'), str) or not isinstance(value.get('scope'), str) or
                not isinstance(value.get('expires_at'), (int, float)) or not math.isfinite(value['expires_at'])):
            raise OAuthError('Invalid OAuth credential file; run login again')
        return value

    def save(self, data):
        if (not isinstance(data, dict) or data.get('resource') != self.endpoint or
                not re.fullmatch(r'tso_[A-Za-z0-9_-]{43}', str(data.get('access_token', ''))) or
                not re.fullmatch(r'tsr_[A-Za-z0-9_-]{43}', str(data.get('refresh_token', ''))) or
                not isinstance(data.get('channel_id'), str) or not data['channel_id'] or
                not isinstance(data.get('scope'), str) or not isinstance(data.get('token_type'), str) or
                data['token_type'].lower() != 'bearer' or
                not isinstance(data.get('expires_in'), (int, float)) or not math.isfinite(data['expires_in']) or
                data['expires_in'] <= 0):
            raise OAuthError('Authorization server returned invalid credentials')
        value = {key: data[key] for key in ('resource', 'access_token', 'refresh_token', 'channel_id', 'scope')}
        value['expires_at'] = time.time() + data['expires_in']
        return self.write(value)

    def write(self, value):
        fd, name = tempfile.mkstemp(prefix='.oauth-', dir=self.path.parent)
        try:
            with os.fdopen(fd, 'w') as file:
                json.dump(value, file)
                file.flush()
                os.fsync(file.fileno())
            os.replace(name, self.path)
        finally:
            if os.path.exists(name):
                os.unlink(name)
        return value

    def post(self, path, data):
        try:
            response = self.session.post(self.issuer + '/api/oauth/' + path, data=data,
                                         timeout=(10, 30), allow_redirects=False)
            try:
                result = response.json()
            except ValueError:
                raise OAuthError(f'OAuth endpoint returned HTTP {response.status_code}; verify the OAuth server is deployed') from None
            if not isinstance(result, dict) or (not response.ok and not result.get('error')):
                raise OAuthError(f'OAuth endpoint returned HTTP {response.status_code}')
            if 300 <= response.status_code < 400:
                raise OAuthError('OAuth redirects are not accepted for credential requests')
            return result
        except requests.RequestException:
            raise OAuthError('OAuth request failed; no credentials were displayed and the request was not retried') from None

    def login(self, no_browser=False, scope=DEFAULT_SCOPES):
        started = self.post('device', {'client_id': CLIENT_ID, 'scope': scope, 'resource': self.endpoint})
        if started.get('error'):
            raise OAuthError('Could not start login: ' + str(started['error']))
        url = started.get('verification_uri_complete', '')
        parsed = urlparse(url)
        if f'{parsed.scheme}://{parsed.netloc}' != self.issuer or parsed.path != '/oauth/authorize':
            raise OAuthError('Authorization server returned an unexpected login address')
        print(f'Open {url}\nCheck code: {started["user_code"]}', file=sys.stderr, flush=True)
        if not no_browser:
            try:
                webbrowser.open(url)
            except webbrowser.Error:
                print('Open the link above in your browser.', file=sys.stderr)
        deadline = time.monotonic() + min(float(started['expires_in']), 3600)
        interval = max(float(started.get('interval', 5)), 5)
        while time.monotonic() < deadline:
            time.sleep(interval)
            result = self.post('token', {'client_id': CLIENT_ID, 'grant_type': DEVICE_GRANT,
                'device_code': started['device_code'], 'resource': self.endpoint})
            error = result.get('error')
            if error == 'authorization_pending':
                continue
            if error == 'slow_down':
                interval += 5
                continue
            if error:
                raise OAuthError('Login was declined or expired; start login again')
            with self.locked():
                self.save(result)
            return {'authenticated': True, 'channelId': result['channel_id'], 'scopes': result['scope'].split()}
        raise OAuthError('Login expired; start login again')

    def token(self):
        # Serialize refresh rotation across CLI processes and reread after taking the lock.
        with self.locked():
            data = self.read()
            if not data or data.get('requires_login'):
                raise OAuthError('Run login to connect Teleskopiq')
            if data.get('expires_at', 0) > time.time() + 60:
                return data
            # Persist intent first: even a killed process must not replay a rotating refresh token.
            self.write({**data, 'requires_login': True})
            try:
                result = self.post('token', {'client_id': CLIENT_ID, 'grant_type': 'refresh_token',
                    'refresh_token': data['refresh_token'], 'resource': self.endpoint})
            except OAuthError:
                # A lost refresh response is ambiguous: do not replay a consumed rotating token.
                raise OAuthError('Token refresh was interrupted. Run login again; no content request was retried') from None
            if result.get('error'):
                raise OAuthError('Your connection expired or was revoked. Run login again')
            return self.save(result)

    def logout(self):
        with self.locked():
            data = self.read()
            if data:
                result = self.post('revoke', {'client_id': CLIENT_ID, 'token': data['refresh_token']})
                if result.get('error'):
                    raise OAuthError('Could not revoke the connection. Retry logout or use Settings → Connected apps')
                self.path.unlink(missing_ok=True)
        return {'authenticated': False}

    def status(self):
        with self.locked():
            data = self.read()
        return {'authenticated': bool(data and not data.get('requires_login')), 'verified': False,
                **({'channelId': data['channel_id'], 'scopes': data['scope'].split()} if data else {})}
