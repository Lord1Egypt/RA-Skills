import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import runtime_bootstrap as rb
import oa_utils as api

class SecurityRevisionTests(unittest.TestCase):
    def test_probe_does_not_inherit_credentials(self):
        with patch.dict(os.environ, {'OA_ENC_KEY': 'synthetic-key', 'UNRELATED_SECRET': 'synthetic', 'HTTPS_PROXY': 'http://fixture:fictional@example.invalid'}), patch.object(rb.subprocess, 'run') as run:
            rb._has_modules(sys.executable, ['requests'])
            self.assertIsNotNone(run.call_args.kwargs.get('env'))
            self.assertNotIn('OA_ENC_KEY', run.call_args.kwargs['env'])
            self.assertNotIn('UNRELATED_SECRET', run.call_args.kwargs['env'])
            self.assertNotIn('HTTPS_PROXY', run.call_args.kwargs['env'])

    def test_runtime_environment_is_allowlisted(self):
        with patch.dict(os.environ, {'OA_ENC_KEY': 'synthetic-key', 'UNRELATED_SECRET': 'synthetic', 'HTTPS_PROXY': 'http://example.invalid'}):
            self.assertTrue(hasattr(rb, 'runtime_environment'))
            env = rb.runtime_environment(credentials=True)
            self.assertEqual(env['OA_ENC_KEY'], 'synthetic-key')
            self.assertEqual(env['HTTPS_PROXY'], 'http://example.invalid')
            self.assertNotIn('UNRELATED_SECRET', env)

    def test_openssl_secret_uses_pipe_not_argv_or_environment(self):
        original = api.subprocess.run
        def inspect(args, **kwargs):
            self.assertNotIn('pass:synthetic-key', args)
            self.assertTrue(args[-1].startswith('fd:'))
            self.assertNotIn('OA_ENC_KEY', kwargs['env'])
            return original(args, **kwargs)
        with patch.object(api, 'get_enc_key', return_value='synthetic-key'), patch.object(api.subprocess, 'run', side_effect=inspect):
            encrypted = api.openssl_cipher('-e', b'fictional fixture')
            self.assertEqual(api.openssl_cipher('-d', encrypted), b'fictional fixture')

    def test_openssl_rejects_overlong_utf8_passphrase_before_subprocess(self):
        for key in ('a' * 1023, '密' * 341):
            for mode in ('-e', '-d'):
                with self.subTest(bytes=len(key.encode('utf-8')), mode=mode):
                    with patch.object(api, 'get_enc_key', return_value=key), patch.object(api.subprocess, 'run') as run:
                        try:
                            with self.assertRaisesRegex(ValueError, '1022'):
                                api.openssl_cipher(mode, b'synthetic fixture')
                        finally:
                            run.assert_not_called()

    def test_openssl_accepts_1022_utf8_bytes_without_truncation(self):
        key = '密' * 340 + 'ab'
        with patch.object(api, 'get_enc_key', return_value=key):
            encrypted = api.openssl_cipher('-e', b'synthetic boundary fixture')
            self.assertEqual(api.openssl_cipher('-d', encrypted), b'synthetic boundary fixture')
        with patch.object(api, 'get_enc_key', return_value=key[:-1] + 'c'):
            with self.assertRaises(ValueError):
                api.openssl_cipher('-d', encrypted)

    def test_legacy_openssl_ciphertext_remains_readable(self):
        ciphertext = b'U2FsdGVkX1+9DxiBSgPpkxBYfO/OJuDM6yJBB30I2Ofz/N48kRiLsKo2jSbhUpdJ\n'
        with patch.object(api, 'get_enc_key', return_value='synthetic-key'):
            self.assertEqual(api.openssl_cipher('-d', ciphertext), b'fictional legacy fixture\n')

if __name__ == '__main__': unittest.main()
