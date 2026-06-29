#!/usr/bin/env python3
"""Image/vision routing: image requests must go to image-capable models, never GLM*."""
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('SAGE_ROUTER_DARIO_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART', '0')

import router  # noqa: E402


def _img_msg():
    return [{'role': 'user', 'content': [
        {'type': 'text', 'text': 'describe this image'},
        {'type': 'image_url', 'image_url': {'url': 'https://x/y.png'}},
    ]}]


class ImageDetectionTests(unittest.TestCase):
    def test_glm_family_detected(self):
        for m in ['glm-5', 'glm-5.2:cloud', 'glm-5:cloud', 'glm-4v', 'AutoGLM-Phone-9B', 'glmocr']:
            self.assertTrue(router.is_glm_model(m), m)
        for m in ['gpt-5.4', 'gpt-4o', 'claude-sonnet-4', 'gemini-2.5-pro', 'qwen3-vl']:
            self.assertFalse(router.is_glm_model(m), m)

    def test_image_in_chat_message_content(self):
        payload = {'messages': _img_msg()}
        self.assertTrue(router.payload_vision_signal(payload))

    def test_image_in_responses_input(self):
        payload = {'input': [{'role': 'user', 'content': [
            {'type': 'input_text', 'text': 'describe'},
            {'type': 'input_image', 'image_url': 'https://x/y.jpg'},
        ]}]}
        self.assertTrue(router.payload_vision_signal(payload))

    def test_image_inside_tool_result(self):
        payload = {'messages': [{'role': 'tool', 'content': [
            {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,iVBORw0KG'}},
        ]}]}
        self.assertTrue(router.payload_vision_signal(payload))

    def test_text_only_no_vision_signal(self):
        payload = {'messages': [{'role': 'user', 'content': 'just text, no images'}]}
        self.assertFalse(router.payload_vision_signal(payload))


class VisionRoutingTests(unittest.TestCase):
    def setUp(self):
        self._old_providers = router.PROVIDERS
        self._old_disabled = set(router.DISABLED_PROVIDERS)
        self._old_fetch = router.fetch_ollama_models
        self._old_reach = router.provider_endpoint_reachable
        self._old_blocks = dict(router.TEMP_MODEL_BLOCKS)
        router.DISABLED_PROVIDERS.clear()
        router.fetch_ollama_models = lambda provider: provider.models
        router.provider_endpoint_reachable = lambda provider: True
        router.TEMP_MODEL_BLOCKS.clear()
        glm_meta = lambda: {'input': ['text'], 'supportsVision': False, 'supportsChat': True,
                            'supportsTools': True, 'supportsJson': True, 'reasoning': True}
        vis_meta = lambda: {'input': ['text', 'image'], 'supportsVision': True, 'supportsChat': True,
                            'supportsTools': True, 'supportsJson': True, 'reasoning': True}
        aud_meta = lambda: {**vis_meta(), 'input': ['text', 'image', 'audio'], 'supportsAudio': True}
        vid_meta = lambda: {**vis_meta(), 'input': ['text', 'image', 'video'], 'supportsVideo': True}
        router.PROVIDERS = {
            'ollama-cloud': router.Provider(
                'ollama-cloud', 'ollama', 'https://ollama.com', 'k',
                ['glm-5.2:cloud', 'glm-5:cloud'],
                model_meta={'glm-5.2:cloud': glm_meta(), 'glm-5:cloud': glm_meta()},
            ),
            'openai': router.Provider(
                'openai', 'openai-completions', 'https://api.openai.com/v1', 'sk',
                ['gpt-5.4', 'gpt-4o', 'gpt-4o-audio', 'gpt-4o-video'],
                model_meta={
                    'gpt-5.4': vis_meta(),
                    'gpt-4o': {**vis_meta(), 'reasoning': False},
                    'gpt-4o-audio': aud_meta(),
                    'gpt-4o-video': vid_meta(),
                },
            ),
        }

    def tearDown(self):
        router.PROVIDERS = self._old_providers
        router.DISABLED_PROVIDERS.clear()
        router.DISABLED_PROVIDERS.update(self._old_disabled)
        router.fetch_ollama_models = self._old_fetch
        router.provider_endpoint_reachable = self._old_reach
        router.TEMP_MODEL_BLOCKS.clear()
        router.TEMP_MODEL_BLOCKS.update(self._old_blocks)

    def test_image_capable_glm_allowed_for_vision(self):
        # Image-capable GLM variants (e.g. glm-4v / glm-5v) may serve vision
        # requests again; only text-only GLM models are excluded.
        prov = router.PROVIDERS['ollama-cloud']
        prov.models.append('glm-5v:cloud')
        prov.model_meta['glm-5v:cloud'] = {**prov.model_meta['glm-5.2:cloud'], 'input': ['text', 'image'], 'supportsVision': True}
        ok, reason = router.model_meets_requirements(prov, 'glm-5v:cloud', {'vision': True}, 100)
        self.assertTrue(ok, f'image-capable GLM should be allowed for vision: {reason}')

    def test_non_vision_glm_rejected_for_vision(self):
        prov = router.PROVIDERS['ollama-cloud']
        ok, _ = router.model_meets_requirements(prov, 'glm-5.2:cloud', {'vision': True}, 100)
        self.assertFalse(ok)
        ok, reason2 = router.model_meets_requirements(prov, 'glm-5.2:cloud', {}, 100)
        self.assertTrue(ok, f'glm should be allowed for non-vision: {reason2}')

    def test_vision_model_allowed_for_vision(self):
        prov = router.PROVIDERS['openai']
        ok, reason = router.model_meets_requirements(prov, 'gpt-5.4', {'vision': True}, 100)
        self.assertTrue(ok, reason)

    def test_prepare_route_relaxes_when_forced_provider_only_has_glm(self):
        _m, _i, _c, _t, chain = router.prepare_route(
            _img_msg(),
            request_id='test-vision-forced',
            route_mode='best',
            requirements={'vision': True, 'allowProviders': ['ollama-cloud'],
                          'allowModels': ['*glm-5*'], 'frontierLargeOnly': True},
            force_provider='ollama-cloud',
            requested_model='glm-5.2:cloud',
        )
        self.assertTrue(chain, 'expected a vision fallback chain, got empty')
        # The forced provider only has text-only GLM, so the relaxed fallback
        # must land on a vision-capable non-text-glm model (openai).
        for pn, model in chain:
            caps = router.model_capabilities(router.PROVIDERS[pn], model)
            self.assertTrue(caps.get('vision'), f'non-vision model in image chain: {pn}/{model}')
        self.assertEqual(chain[0][0], 'openai')

    def test_prepare_route_auto_only_uses_vision_models(self):
        _m, _i, _c, _t, chain = router.prepare_route(
            _img_msg(),
            request_id='test-vision-auto',
            route_mode='best',
            requirements={'vision': True},
        )
        self.assertTrue(chain)
        for pn, model in chain:
            caps = router.model_capabilities(router.PROVIDERS[pn], model)
            self.assertTrue(caps.get('vision'), f'non-vision model in image chain: {pn}/{model}')

    def test_image_capable_models_summary_lists_vision_models(self):
        summary = router.image_capable_models_summary()
        self.assertIn('openai', summary)
        ids = [m['id'] for m in summary['openai']]
        self.assertIn('gpt-5.4', ids)
        # Text-only GLM models must NOT appear as image-capable.
        glm_text = [m for m in summary.get('ollama-cloud', []) if m['id'] in ('glm-5.2:cloud', 'glm-5:cloud')]
        self.assertEqual(glm_text, [])
        # An image-capable GLM variant should appear, flagged as glm.
        prov = router.PROVIDERS['ollama-cloud']
        prov.models.append('glm-5v:cloud')
        prov.model_meta['glm-5v:cloud'] = {**prov.model_meta['glm-5.2:cloud'], 'input': ['text', 'image'], 'supportsVision': True}
        summary2 = router.image_capable_models_summary()
        glm_vis = [m for m in summary2.get('ollama-cloud', []) if m['id'] == 'glm-5v:cloud']
        self.assertEqual(len(glm_vis), 1)
        self.assertTrue(glm_vis[0]['glm'])



class MultimodalInputTests(unittest.TestCase):
    def setUp(self):
        self._old_providers = router.PROVIDERS
        self._old_disabled = set(router.DISABLED_PROVIDERS)
        self._old_fetch = router.fetch_ollama_models
        self._old_reach = router.provider_endpoint_reachable
        self._old_blocks = dict(router.TEMP_MODEL_BLOCKS)
        router.DISABLED_PROVIDERS.clear()
        router.fetch_ollama_models = lambda provider: provider.models
        router.provider_endpoint_reachable = lambda provider: True
        router.TEMP_MODEL_BLOCKS.clear()
        txt = lambda: {'input': ['text'], 'supportsVision': False, 'supportsChat': True,
                       'supportsTools': True, 'supportsJson': True, 'reasoning': True}
        vis = lambda: {**txt(), 'input': ['text', 'image'], 'supportsVision': True}
        aud = lambda: {**vis(), 'input': ['text', 'image', 'audio'], 'supportsAudio': True}
        vid = lambda: {**vis(), 'input': ['text', 'image', 'video'], 'supportsVideo': True}
        router.PROVIDERS = {
            'ollama-cloud': router.Provider('ollama-cloud', 'ollama', 'https://ollama.com', 'k',
                                            ['glm-5.2:cloud'], model_meta={'glm-5.2:cloud': txt()}),
            'openai': router.Provider('openai', 'openai-completions', 'https://api.openai.com/v1', 'sk',
                                      ['gpt-5.4', 'gpt-4o-audio', 'gpt-4o-video'],
                                      model_meta={'gpt-5.4': vis(), 'gpt-4o-audio': aud(), 'gpt-4o-video': vid()}),
        }

    def tearDown(self):
        router.PROVIDERS = self._old_providers
        router.DISABLED_PROVIDERS.clear()
        router.DISABLED_PROVIDERS.update(self._old_disabled)
        router.fetch_ollama_models = self._old_fetch
        router.provider_endpoint_reachable = self._old_reach
        router.TEMP_MODEL_BLOCKS.clear()
        router.TEMP_MODEL_BLOCKS.update(self._old_blocks)

    def test_audio_input_detected(self):
        payload = {'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': 'transcribe'},
            {'type': 'input_audio', 'input_audio': {'data': 'data:audio/wav;base64,UklGR'}}]}]}
        self.assertTrue(router.payload_audio_signal(payload))
        req = router.normalize_requirements(payload, router.ThinkingLevel.LOW)
        self.assertTrue(req['audio'])

    def test_video_input_detected(self):
        payload = {'messages': [{'role': 'user', 'content': [
            {'type': 'input_video', 'video_url': 'https://x/clip.mp4'}]}]}
        self.assertTrue(router.payload_video_signal(payload))
        req = router.normalize_requirements(payload, router.ThinkingLevel.LOW)
        self.assertTrue(req['video'])

    def test_audio_routes_to_audio_capable_model(self):
        prov = router.PROVIDERS['openai']
        ok, _ = router.model_meets_requirements(prov, 'gpt-4o-audio', {'audio': True}, 100)
        self.assertTrue(ok)
        # text-only GLM cannot serve audio
        glm = router.PROVIDERS['ollama-cloud']
        ok2, reason = router.model_meets_requirements(glm, 'glm-5.2:cloud', {'audio': True}, 100)
        self.assertFalse(ok2)

    def test_auto_profile_relaxes_for_vision(self):
        # auto-style profile constraints restrict to ollama-cloud (text-only GLM);
        # a vision request must relax and route to a vision-capable provider.
        _m, _i, _c, _t, chain = router.prepare_route(
            [{'role': 'user', 'content': [
                {'type': 'text', 'text': 'describe this image'},
                {'type': 'image_url', 'image_url': {'url': 'https://x/y.png'}}]}],
            request_id='test-auto-vision',
            route_mode='best',
            requirements={'vision': True, 'allowProviders': ['ollama-cloud'], 'frontierLargeOnly': True},
        )
        self.assertTrue(chain)
        for pn, model in chain:
            self.assertTrue(router.model_capabilities(router.PROVIDERS[pn], model).get('vision'),
                            f'non-vision model in image chain: {pn}/{model}')
        self.assertEqual(chain[0][0], 'openai')

    def test_auto_profile_relaxes_for_audio(self):
        _m, _i, _c, _t, chain = router.prepare_route(
            [{'role': 'user', 'content': [
                {'type': 'text', 'text': 'transcribe this'},
                {'type': 'input_audio', 'input_audio': {'data': 'data:audio/wav;base64,UklGR'}}]}],
            request_id='test-auto-audio',
            route_mode='best',
            requirements={'audio': True, 'allowProviders': ['ollama-cloud']},
        )
        self.assertTrue(chain)
        for pn, model in chain:
            self.assertTrue(router.model_capabilities(router.PROVIDERS[pn], model).get('audio'),
                            f'non-audio model in audio chain: {pn}/{model}')
        self.assertEqual(chain[0][1], 'gpt-4o-audio')


if __name__ == '__main__':
    unittest.main()
