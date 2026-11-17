import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from oauth_login import OAuthCredentials, OAuthError
import teleskopiq

ENDPOINT = 'https://teleskopiq.com/api/graphql'


def token(suffix='a'):
    return {'access_token': 'tso_' + suffix * 43, 'refresh_token': 'tsr_' + suffix * 43,
            'resource': ENDPOINT, 'scope': 'scripts:read', 'channel_id': 'channel-a',
            'token_type': 'Bearer', 'expires_in': 900}


class OAuthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.oauth = OAuthCredentials(ENDPOINT, Path(self.temp.name) / 'oauth.json')

    def save(self, value=None):
        with self.oauth.locked():
            return self.oauth.save(value or token())

    def test_private_storage_and_status_never_returns_tokens(self):
        self.save()
        self.assertEqual(self.oauth.path.stat().st_mode & 0o777, 0o600)
        status = self.oauth.status()
        self.assertEqual(status['channelId'], 'channel-a')
        self.assertNotIn('access_token', status)
        self.assertNotIn('refresh_token', status)

    def test_rejects_wrong_audience_and_unsafe_endpoints(self):
        self.save()
        with self.assertRaises(OAuthError):
            OAuthCredentials('https://other.test/api/graphql', self.oauth.path).token()
        for endpoint in ['http://other.test/api/graphql', 'https://user@teleskopiq.com/api/graphql',
                         ENDPOINT + '?secret=x', 'https://teleskopiq.com/other']:
            with self.assertRaises(OAuthError):
                OAuthCredentials(endpoint)
        with self.assertRaises(OAuthError):
            self.save({**token(), 'resource': 'https://other.test/api/graphql'})

    def test_rejects_world_readable_credentials_and_symlinks(self):
        self.save()
        self.oauth.path.chmod(0o644)
        with self.assertRaises(OAuthError):
            self.oauth.read()
        real = self.oauth.path.with_suffix('.real')
        self.oauth.path.rename(real)
        self.oauth.path.symlink_to(real)
        with self.assertRaises(OSError):
            self.oauth.read()

    def test_refreshes_expired_credentials_and_saves_rotation(self):
        self.save({**token(), 'expires_in': 1})
        with patch.object(self.oauth, 'post', return_value=token('b')) as post:
            self.assertEqual(self.oauth.token()['access_token'], token('b')['access_token'])
            self.assertEqual(self.oauth.token()['access_token'], token('b')['access_token'])
            self.assertEqual(post.call_count, 1)
            self.assertEqual(post.call_args.args[1]['resource'], ENDPOINT)

    def test_ambiguous_refresh_is_not_replayed(self):
        self.save({**token(), 'expires_in': 1})
        with patch.object(self.oauth, 'post', side_effect=OAuthError('timeout')) as post:
            with self.assertRaisesRegex(OAuthError, 'interrupted'):
                self.oauth.token()
            self.assertTrue(self.oauth.path.exists())
            self.assertTrue(self.oauth.read()['requires_login'])
            with self.assertRaisesRegex(OAuthError, 'Run login'):
                self.oauth.token()
            self.assertEqual(post.call_count, 1)

    def test_revocation_deletes_cache_only_after_server_accepts_it(self):
        self.save()
        with patch.object(self.oauth, 'post', side_effect=OAuthError('timeout')):
            with self.assertRaises(OAuthError):
                self.oauth.logout()
        self.assertTrue(self.oauth.path.exists())
        with patch.object(self.oauth, 'post', return_value={}) as post:
            self.oauth.logout()
            self.assertEqual(post.call_args.args[0], 'revoke')
        self.assertFalse(self.oauth.path.exists())

    def test_device_flow_waits_for_consent_and_honors_slow_down(self):
        start = {'device_code': 'private-device-code', 'user_code': 'ABCDE-FG234', 'expires_in': 600,
                 'interval': 5, 'verification_uri_complete': 'https://teleskopiq.com/oauth/authorize?user_code=ABCDE-FG234'}
        stderr = io.StringIO()
        with patch.object(self.oauth, 'post', side_effect=[start, {'error': 'authorization_pending'},
                {'error': 'slow_down'}, token()]), patch('oauth_login.time.sleep') as sleep, redirect_stderr(stderr):
            result = self.oauth.login(no_browser=True)
        self.assertTrue(result['authenticated'])
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [5, 5, 10])
        self.assertNotIn('private-device-code', stderr.getvalue())
        self.assertNotIn(token()['access_token'], stderr.getvalue())

    def test_no_browser_redirect_to_untrusted_origin(self):
        with patch.object(self.oauth, 'post', return_value={
            'verification_uri_complete': 'https://attacker.test/oauth/authorize'}):
            with self.assertRaises(OAuthError):
                self.oauth.login()

    def test_client_refreshes_before_content_request_without_replaying_mutation(self):
        self.save()
        client = teleskopiq.Client('', oauth=self.oauth)
        client.session = Mock()
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.ok = False
        response.status_code = 401
        response.json.return_value = {'errors': [{'message': 'expired'}]}
        client.session.post.return_value = response
        with self.assertRaises(teleskopiq.APIError):
            client.gql('mutation { deleteScript(id:"x") { success } }')
        self.assertEqual(client.session.post.call_count, 1)
        self.assertEqual(client.channel_id, 'channel-a')


if __name__ == '__main__':
    unittest.main()
