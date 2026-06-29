#!/usr/bin/env python3
"""Credential-pool failover tests (non-streaming + streaming open path)."""
import os
import sys
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('SAGE_ROUTER_DARIO_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART', '0')

import router  # noqa: E402


def _http_error(code, reason, body=b''):
    return urllib.error.HTTPError(
        url='https://example.test/v1/chat/completions',
        code=code, msg=reason, hdrs=None, fp=None,
    )


class CredentialFailoverTests(unittest.TestCase):
    def setUp(self):
        self._old_urlopen = router.urllib.request.urlopen
        self._old_providers = router.PROVIDERS
        router.PROVIDERS = {
            'openai': router.Provider(
                'openai', 'openai-completions', 'https://api.openai.com/v1', 'sk-primary',
                ['gpt-4o-mini'],
                credentials=[
                    {'type': 'api_key', 'label': 'primary', 'key': 'sk-primary'},
                    {'type': 'api_key', 'label': 'backup', 'key': 'sk-backup'},
                ],
            ),
        }
        self.calls = []

    def tearDown(self):
        router.urllib.request.urlopen = self._old_urlopen
        router.PROVIDERS = self._old_providers

    def _make_urlopen(self, responses):
        """responses: list keyed by credential string -> outcome.

        Each outcome is either an HTTPError instance or a fake response object.
        """
        def _fake(req, timeout=None):
            key = None
            auth = req.headers.get('Authorization') if hasattr(req, 'headers') else None
            if auth and auth.startswith('Bearer '):
                key = auth[len('Bearer '):]
            # For google-style query keys
            if key is None and '?key=' in (req.full_url if hasattr(req, 'full_url') else ''):
                key = req.full_url.split('?key=')[1]
            self.calls.append(key)
            outcome = responses.get(key)
            if isinstance(outcome, urllib.error.HTTPError):
                raise outcome
            return outcome
        return _fake

    def test_non_streaming_failover_on_429(self):
        class Resp:
            def read(self):
                return b'{"choices":[{"message":{"content":"hi"}}]}'
            def __enter__(self): return self
            def __exit__(self, *a): return False

        router.urllib.request.urlopen = self._make_urlopen({
            'sk-primary': _http_error(429, 'Too Many Requests', b'rate limited'),
            'sk-backup': Resp(),
        })
        # Force the openai-completions path with a minimal payload.
        ok, result = router.call_provider_completion_once(
            'openai', 'gpt-4o-mini',
            {'messages': [{'role': 'user', 'content': 'hi'}]},
            'req-1', router.ThinkingLevel.LOW,
        )
        self.assertTrue(ok, f'expected success after failover, got {result}')
        self.assertEqual(self.calls, ['sk-primary', 'sk-backup'])

    def test_non_streaming_no_failover_on_hard_error(self):
        router.urllib.request.urlopen = self._make_urlopen({
            'sk-primary': _http_error(400, 'Bad Request', b'malformed'),
        })
        ok, result = router.call_provider_completion_once(
            'openai', 'gpt-4o-mini',
            {'messages': [{'role': 'user', 'content': 'hi'}]},
            'req-2', router.ThinkingLevel.LOW,
        )
        self.assertFalse(ok)
        # Only the first credential should have been attempted.
        self.assertEqual(self.calls, ['sk-primary'])

    def test_streaming_open_failover_on_429(self):
        class StreamResp:
            def readline(self):
                return b''
            def __enter__(self): return self
            def __exit__(self, *a): return False

        router.urllib.request.urlopen = self._make_urlopen({
            'sk-primary': _http_error(429, 'Too Many Requests'),
            'sk-backup': StreamResp(),
        })

        class FakeHandler:
            def __init__(self): self.written = []
            def send_response(self, c): self.written.append(('status', c))
            def send_header(self, k, v): self.written.append(('header', k, v))
            def end_headers(self): self.written.append(('end',))
            def routing_headers(self, payload, rid): return {}
            @property
            def wfile(self):
                w = self
                class W:
                    def write(self, data): w.written.append(('data', data))
                    def flush(self): pass
                return W()

        handler = FakeHandler()
        provider = router.PROVIDERS['openai']
        ret = router.stream_openai_compat_to_client(
            handler, provider, 'gpt-4o-mini',
            {'messages': [{'role': 'user', 'content': 'hi'}]},
            'req-stream', thinking=router.ThinkingLevel.LOW,
        )
        self.assertTrue(ret)
        # Failover happened before committing to the client: the 429 key was
        # tried first, then the backup key opened the stream.
        self.assertEqual(self.calls, ['sk-primary', 'sk-backup'])

    def test_single_key_provider_no_failover(self):
        router.PROVIDERS['solo'] = router.Provider(
            'solo', 'openai-completions', 'https://api.example.com/v1', 'sk-only', ['m1'],
        )
        router.urllib.request.urlopen = self._make_urlopen({
            'sk-only': _http_error(429, 'Too Many Requests'),
        })

        def _build(key):
            req = urllib.request.Request('https://api.example.com/v1', data=b'{}')
            req.add_header('Authorization', f'Bearer {key}')
            return req

        with self.assertRaises(urllib.error.HTTPError):
            router.open_upstream_with_credential_failover(
                router.PROVIDERS['solo'], _build, 5,
            )
        self.assertEqual(self.calls, ['sk-only'])


if __name__ == '__main__':
    unittest.main()


class CredentialLoadBalancingTests(unittest.TestCase):
    def setUp(self):
        self._old_state = dict(router.CREDENTIAL_STATE)
        self._old_rr = dict(router.CREDENTIAL_RR_INDEX)
        router.CREDENTIAL_STATE.clear()
        router.CREDENTIAL_RR_INDEX.clear()
        self._old_providers = router.PROVIDERS
        router.PROVIDERS = {
            'lb': router.Provider(
                'lb', 'openai-completions', 'https://api.example.com/v1', 'k0',
                ['m1'],
                credentials=[
                    {'type': 'api_key', 'label': 'a', 'key': 'kA'},
                    {'type': 'api_key', 'label': 'b', 'key': 'kB'},
                    {'type': 'api_key', 'label': 'c', 'key': 'kC'},
                ],
                credential_strategy='round-robin',
            ),
        }

    def tearDown(self):
        router.CREDENTIAL_STATE.clear()
        router.CREDENTIAL_RR_INDEX.clear()
        router.CREDENTIAL_STATE.update(self._old_state)
        router.CREDENTIAL_RR_INDEX.update(self._old_rr)
        router.PROVIDERS = self._old_providers

    def test_round_robin_rotates_starting_key(self):
        picks = [router.select_credential_keys(router.PROVIDERS['lb'])[0] for _ in range(6)]
        # Starting key should cycle through the pool: kA, kB, kC, kA, kB, kC
        self.assertEqual(picks, ['kA', 'kB', 'kC', 'kA', 'kB', 'kC'])

    def test_cooldown_deprioritizes_key(self):
        prov = router.PROVIDERS['lb']
        # Force credential 'a' (kA) into cooldown.
        router.mark_credential_error('lb', 'a')
        order = router.select_credential_keys(prov)
        # kA must be last while in cooldown; the rest stay in rotation order.
        self.assertEqual(order[-1], 'kA')
        self.assertNotEqual(order[0], 'kA')

    def test_lru_picks_least_recently_used(self):
        router.PROVIDERS['lb'].credential_strategy = 'lru'
        prov = router.PROVIDERS['lb']
        # Use 'a' then 'b' so 'c' is least recently used.
        router.mark_credential_used('lb', 'a')
        router.mark_credential_used('lb', 'b')
        first = router.select_credential_keys(prov)[0]
        self.assertEqual(first, 'kC')

    def test_failover_keeps_primary_first(self):
        router.PROVIDERS['lb'].credential_strategy = 'failover'
        prov = router.PROVIDERS['lb']
        # Primary api_key (k0) must come first, ahead of the pool.
        order = router.select_credential_keys(prov)
        self.assertEqual(order[0], 'k0')

    def test_strategy_persisted_to_config(self):
        import json, tempfile, os
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        tmp.write(json.dumps({'models': {'providers': {
            'lb': {'api': 'openai-completions', 'baseUrl': 'https://api.example.com/v1',
                   'apiKeys': [{'label': 'a', 'key': 'kA'}]}}}}))
        tmp.close()
        old_cfg_path = router.APP_PROVIDER_CONFIG
        old_reload = router.reload_configured_providers
        router.APP_PROVIDER_CONFIG = tmp.name
        router.reload_configured_providers = lambda: None
        try:
            res = router.set_setup_credential_strategy({'provider': 'lb', 'strategy': 'round-robin'})
            self.assertEqual(res['strategy'], 'round-robin')
            cfg = json.load(open(tmp.name))
            self.assertEqual(cfg['models']['providers']['lb']['credentialStrategy'], 'round-robin')
        finally:
            router.APP_PROVIDER_CONFIG = old_cfg_path
            router.reload_configured_providers = old_reload
            os.unlink(tmp.name)

    def test_new_provider_credential_requires_endpoint_for_unknown_api(self):
        import json, tempfile, os
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        tmp.write(json.dumps({'models': {'providers': {}}}))
        tmp.close()
        old_cfg_path = router.APP_PROVIDER_CONFIG
        old_reload = router.reload_configured_providers
        router.APP_PROVIDER_CONFIG = tmp.name
        router.reload_configured_providers = lambda: None
        try:
            with self.assertRaises(ValueError) as ctx:
                router.save_setup_credential({
                    'provider': 'custom-work',
                    'api': 'custom-api',
                    'key': 'sk-test',
                })
            self.assertEqual(str(ctx.exception), 'provider_endpoint_required')
        finally:
            router.APP_PROVIDER_CONFIG = old_cfg_path
            router.reload_configured_providers = old_reload
            os.unlink(tmp.name)

    def test_new_provider_credential_normalizes_dashboard_api_aliases(self):
        import json, tempfile, os
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        tmp.write(json.dumps({'models': {'providers': {}}}))
        tmp.close()
        old_cfg_path = router.APP_PROVIDER_CONFIG
        old_reload = router.reload_configured_providers
        router.APP_PROVIDER_CONFIG = tmp.name
        router.reload_configured_providers = lambda: None
        try:
            res = router.save_setup_credential({
                'provider': 'ollama-team-b',
                'api': 'ollama-cloud',
                'baseUrl': 'https://ollama.com',
                'key': 'ollama-key',
                'credentialStrategy': 'round-robin',
            })
            self.assertEqual(res['provider'], 'ollama-team-b')
            self.assertEqual(res['slot'], 'apiKeys')
            cfg = json.load(open(tmp.name))
            provider_cfg = cfg['models']['providers']['ollama-team-b']
            self.assertEqual(provider_cfg['api'], 'ollama')
            self.assertEqual(provider_cfg['baseUrl'], 'https://ollama.com')
            self.assertEqual(provider_cfg['credentialStrategy'], 'round-robin')
            self.assertEqual(provider_cfg['apiKeys'][0]['key'], 'ollama-key')
        finally:
            router.APP_PROVIDER_CONFIG = old_cfg_path
            router.reload_configured_providers = old_reload
            os.unlink(tmp.name)

    def test_existing_ollama_credential_uses_provider_defaults_without_endpoint(self):
        import json, tempfile, os
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        tmp.write(json.dumps({'models': {'providers': {}}}))
        tmp.close()
        old_cfg_path = router.APP_PROVIDER_CONFIG
        old_reload = router.reload_configured_providers
        old_providers = router.PROVIDERS
        router.APP_PROVIDER_CONFIG = tmp.name
        router.reload_configured_providers = lambda: None
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'https://ollama.com', '', ['glm-5.1:cloud'])
        }
        try:
            router.save_setup_credential({
                'provider': 'ollama',
                'api': 'ollama',
                'key': 'second-ollama-key',
            })
            cfg = json.load(open(tmp.name))
            provider_cfg = cfg['models']['providers']['ollama']
            self.assertEqual(provider_cfg['api'], 'ollama')
            self.assertEqual(provider_cfg['baseUrl'], 'https://ollama.com')
            self.assertNotIn('models', provider_cfg)
            self.assertEqual(provider_cfg['apiKeys'][0]['key'], 'second-ollama-key')
        finally:
            router.APP_PROVIDER_CONFIG = old_cfg_path
            router.reload_configured_providers = old_reload
            router.PROVIDERS = old_providers
            os.unlink(tmp.name)

    def test_dashboard_enablement_updates_config_disabled_lists(self):
        import json, tempfile, os
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        tmp.write(json.dumps({'models': {'providers': {}}}))
        tmp.close()
        old_cfg_path = router.APP_PROVIDER_CONFIG
        old_reload = router.reload_configured_providers
        old_disabled_providers = set(router.DISABLED_PROVIDERS)
        old_disabled_models = set(router.DISABLED_MODELS)
        router.APP_PROVIDER_CONFIG = tmp.name
        router.reload_configured_providers = lambda: router._apply_dashboard_disabled_sets(router._load_app_provider_config_safe())
        try:
            router.set_setup_provider_enabled({'provider': 'google', 'enabled': False})
            router.set_setup_model_enabled({'provider': 'ollama', 'model': 'glm-5.1:cloud', 'enabled': False})
            cfg = json.load(open(tmp.name))
            self.assertIn('google', cfg['disabledProviders'])
            self.assertIn('ollama/glm-5.1:cloud', cfg['disabledModels'])
            self.assertIn('google', router.DISABLED_PROVIDERS)
            self.assertTrue(router.model_disabled_reason('ollama', 'glm-5.1:cloud'))

            router.set_setup_provider_enabled({'provider': 'google', 'enabled': True})
            router.set_setup_model_enabled({'provider': 'ollama', 'model': 'glm-5.1:cloud', 'enabled': True})
            cfg = json.load(open(tmp.name))
            self.assertNotIn('google', cfg['disabledProviders'])
            self.assertNotIn('ollama/glm-5.1:cloud', cfg['disabledModels'])
        finally:
            router.APP_PROVIDER_CONFIG = old_cfg_path
            router.reload_configured_providers = old_reload
            router.DISABLED_PROVIDERS = old_disabled_providers
            router.DISABLED_MODELS = old_disabled_models
            os.unlink(tmp.name)
