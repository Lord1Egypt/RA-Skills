#!/usr/bin/env python3
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('SAGE_ROUTER_DARIO_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART', '0')

import router  # noqa: E402


class AudioProxyTests(unittest.TestCase):
    def setUp(self):
        self.old_providers = router.PROVIDERS
        self.old_stt = router.AUDIO_STT_PROVIDER
        self.old_tts = router.AUDIO_TTS_PROVIDER
        router.PROVIDERS = {
            'openai': router.Provider(
                'openai',
                'openai-completions',
                'https://api.openai.test/v1',
                'sk-test',
                ['gpt-4o-mini-transcribe', 'gpt-4o-mini-tts'],
            )
        }
        router.AUDIO_STT_PROVIDER = 'openai'
        router.AUDIO_TTS_PROVIDER = 'openai'

    def tearDown(self):
        router.PROVIDERS = self.old_providers
        router.AUDIO_STT_PROVIDER = self.old_stt
        router.AUDIO_TTS_PROVIDER = self.old_tts

    def test_audio_endpoint_kind_accepts_v1_and_short_paths(self):
        self.assertEqual('stt', router.audio_endpoint_kind('/v1/audio/transcriptions'))
        self.assertEqual('stt', router.audio_endpoint_kind('/audio/transcriptions?x=1'))
        self.assertEqual('tts', router.audio_endpoint_kind('/v1/audio/speech'))
        self.assertEqual('tts', router.audio_endpoint_kind('/audio/speech'))
        self.assertEqual('', router.audio_endpoint_kind('/v1/chat/completions'))

    def test_audio_proxy_uses_configured_openai_compatible_provider(self):
        provider, error = router.audio_proxy_provider('stt')
        self.assertEqual('', error)
        self.assertEqual('openai', provider.name)
        self.assertEqual(
            'https://api.openai.test/v1/audio/transcriptions',
            router.upstream_audio_url(provider, 'stt'),
        )
        self.assertEqual(
            'https://api.openai.test/v1/audio/speech',
            router.upstream_audio_url(provider, 'tts'),
        )

    def test_audio_proxy_rejects_missing_or_non_openai_provider(self):
        router.AUDIO_STT_PROVIDER = 'missing'
        provider, error = router.audio_proxy_provider('stt')
        self.assertIsNone(provider)
        self.assertEqual('audio_stt_provider_not_configured', error)

        router.PROVIDERS['local'] = router.Provider('local', 'ollama', 'http://localhost:11434', 'x', ['whisper'])
        router.AUDIO_STT_PROVIDER = 'local'
        provider, error = router.audio_proxy_provider('stt')
        self.assertIsNone(provider)
        self.assertEqual('audio_stt_provider_not_openai_compatible', error)


if __name__ == '__main__':
    unittest.main()
