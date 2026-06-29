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


class ProviderSwitchingTests(unittest.TestCase):
    def setUp(self):
        self.old_providers = router.PROVIDERS
        self.old_disabled = set(router.DISABLED_PROVIDERS)
        self.old_fetch_ollama_models = router.fetch_ollama_models
        self.old_provider_endpoint_reachable = router.provider_endpoint_reachable
        self.old_temp_blocks = dict(router.TEMP_MODEL_BLOCKS)
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'http://ollama.invalid', '', ['glm-5']),
            'ollama-2': router.Provider('ollama-2', 'ollama', 'http://ollama-2.invalid', '', ['glm-5.2']),
            'ollama-cloud': router.Provider('ollama-cloud', 'ollama', 'https://ollama.com', 'test-key', ['glm-5.1:cloud']),
            'openai-codex': router.Provider('openai-codex', 'openclaw-gateway', 'ws://gateway.invalid', '', ['gpt-5.5', 'gpt-5.4']),
        }
        router.DISABLED_PROVIDERS.clear()
        router.fetch_ollama_models = lambda provider: provider.models
        router.provider_endpoint_reachable = lambda provider: True
        router.TEMP_MODEL_BLOCKS.clear()

    def tearDown(self):
        router.PROVIDERS = self.old_providers
        router.DISABLED_PROVIDERS.clear()
        router.DISABLED_PROVIDERS.update(self.old_disabled)
        router.fetch_ollama_models = self.old_fetch_ollama_models
        router.provider_endpoint_reachable = self.old_provider_endpoint_reachable
        router.TEMP_MODEL_BLOCKS.clear()
        router.TEMP_MODEL_BLOCKS.update(self.old_temp_blocks)

    def test_stale_ollama_prefix_switches_to_provider_that_has_model(self):
        provider, model = router.resolve_requested_provider_model({'model': 'ollama/gpt-5.5'})
        self.assertEqual('openai-codex', provider)
        self.assertEqual('gpt-5.5', model)

    def test_stale_provider_field_switches_to_provider_that_has_model(self):
        provider, model = router.resolve_requested_provider_model({'provider': 'ollama', 'model': 'gpt-5.5'})
        self.assertEqual('openai-codex', provider)
        self.assertEqual('gpt-5.5', model)

    def test_valid_ollama_model_keeps_ollama_provider(self):
        provider, model = router.resolve_requested_provider_model({'model': 'ollama/glm-5'})
        self.assertEqual('ollama', provider)
        self.assertEqual('glm-5', model)

    def test_forced_ollama_model_keeps_fallbacks_after_exact_attempt(self):
        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'hello'}],
            request_id='test-forced-ollama-fallback',
            force_provider='ollama',
            requested_model='glm-5',
        )
        self.assertGreaterEqual(len(chain), 2)
        self.assertEqual(('ollama', 'glm-5'), chain[0])
        self.assertIn(('ollama-2', 'glm-5.2'), chain[1:])

    def test_empty_forced_provider_chain_falls_back_to_working_provider(self):
        router.PROVIDERS['ollama-cloud'].models = ['nomic-embed-text:cloud']

        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'analyze this repository and use tools if needed'}],
            request_id='test-empty-forced-provider-fallback',
            thinking=router.ThinkingLevel.HIGH,
            route_mode='best',
            requirements={
                'document': True,
                'longContext': True,
                'preferTools': True,
                'agentic': True,
            },
            force_provider='ollama-cloud',
        )

        self.assertTrue(chain)
        self.assertNotEqual('ollama-cloud', chain[0][0])
        self.assertIn(('openai-codex', 'gpt-5.5'), chain)
        self.assertTrue(router.LAST_ROUTE_DEBUG.get('forcedProviderFallback'))

    def test_forced_ollama_cloud_chain_reserves_cross_provider_fallbacks(self):
        router.PROVIDERS['ollama-cloud'].models = [
            'glm-5.1:cloud',
            'glm-5.2:cloud',
            'kimi-k2.5:cloud',
            'deepseek-v4-pro:cloud',
            'qwen3.5:cloud',
            'minimax-m3:cloud',
        ]

        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'analyze this repository and use tools if needed'}],
            request_id='test-forced-ollama-cloud-cross-provider-fallback',
            thinking=router.ThinkingLevel.HIGH,
            route_mode='best',
            requirements={
                'document': True,
                'longContext': True,
                'preferTools': True,
                'agentic': True,
            },
            force_provider='ollama-cloud',
        )

        self.assertTrue(chain)
        self.assertEqual('ollama-cloud', chain[0][0])
        self.assertIn(('openai-codex', 'gpt-5.5'), chain)
        self.assertLess(
            sum(1 for provider, _model in chain if provider == 'ollama-cloud'),
            len(chain),
        )
        self.assertTrue(any(router.PROVIDERS[provider].api_type != 'ollama' for provider, _model in chain))

    def test_ollama_cloud_model_switches_to_hosted_provider(self):
        provider, model = router.resolve_requested_provider_model({'model': 'ollama/glm-5.1:cloud'})
        self.assertEqual('ollama-cloud', provider)
        self.assertEqual('glm-5.1:cloud', model)

    def test_unknown_ollama_prefix_switches_to_sibling_ollama_provider(self):
        provider, model = router.resolve_requested_provider_model({'model': 'ollama/kimi-k2.7-code'})
        self.assertEqual('ollama-2', provider)
        self.assertEqual('kimi-k2.7-code', model)

        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'hello'}],
            request_id='test-stale-ollama-prefix',
            force_provider=provider,
            requested_model=model,
        )
        self.assertTrue(chain)
        self.assertEqual(('ollama-2', 'glm-5.2'), chain[0])

    def test_unknown_ollama_provider_field_switches_to_sibling_ollama_provider(self):
        provider, model = router.resolve_requested_provider_model({'provider': 'ollama', 'model': 'kimi-k2.7-code'})
        self.assertEqual('ollama-2', provider)
        self.assertEqual('kimi-k2.7-code', model)

    def test_router_profile_model_does_not_force_self_provider(self):
        provider, model = router.resolve_requested_provider_model({'model': 'sage-router/balanced'})
        self.assertIsNone(provider)
        self.assertIsNone(model)

    def test_router_profile_provider_field_does_not_force_self_provider(self):
        provider, model = router.resolve_requested_provider_model({'provider': 'sage-router', 'model': 'balanced'})
        self.assertIsNone(provider)
        self.assertIsNone(model)

    def test_nested_sage_router_model_resolves_to_upstream_provider(self):
        router.PROVIDERS['google'] = router.Provider(
            'google',
            'google-generative-language',
            'https://google.invalid',
            'test-key',
            ['gemini-2.5-flash'],
        )
        provider, model = router.resolve_requested_provider_model({'model': 'sage-router/google/gemini-2.5-flash'})
        self.assertEqual('google', provider)
        self.assertEqual('gemini-2.5-flash', model)

    def test_discord_public_profile_defaults_include_google_provider_models(self):
        payload = {
            'model': 'sage-router/balanced',
            'metadata': {'agent': 'discord-public'},
            'messages': [{'role': 'user', 'content': 'hello from discord-public'}],
        }

        self.assertEqual('balanced', router.apply_router_profile(payload))
        self.assertTrue(router.apply_discord_public_route_profile(payload))

        requirements = payload['requirements']
        self.assertEqual('google', requirements['allowProviders'][0])
        self.assertNotIn('google', requirements['fallbackProviders'])
        self.assertIn('google/gemini-2.5-flash', requirements['allowModels'])
        self.assertIn('google/gemini-2.5-pro', requirements['allowModels'])
        self.assertNotIn('requiresReasoning', payload)
        self.assertFalse(router.normalize_requirements(payload)['reasoning'])
        self.assertFalse(requirements.get('frontierLargeOnly', False))

    def test_discord_public_explicit_google_flash_fallback_builds_chain(self):
        old_providers = router.PROVIDERS
        old_disabled = set(router.DISABLED_PROVIDERS)
        try:
            router.PROVIDERS = {
                'google': router.Provider(
                    'google',
                    'google-generative-language',
                    'https://generativelanguage.googleapis.com/v1beta',
                    'test-key',
                    ['gemini-2.5-flash'],
                ),
            }
            router.DISABLED_PROVIDERS.clear()
            payload = {
                'model': 'sage-router/google/gemini-2.5-flash',
                'metadata': {'agent': 'discord-public'},
                'messages': [{'role': 'user', 'content': 'summarize this public thread'}],
            }
            self.assertTrue(router.apply_discord_public_route_profile(payload))
            provider, model = router.resolve_requested_provider_model(payload)

            _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
                payload['messages'],
                request_id='test-discord-public-google-flash-fallback',
                thinking=router.ThinkingLevel.HIGH,
                route_mode='best',
                requirements=payload['requirements'],
                force_provider=provider,
                requested_model=model,
            )

            self.assertEqual([('google', 'gemini-2.5-flash')], chain)
        finally:
            router.PROVIDERS = old_providers
            router.DISABLED_PROVIDERS.clear()
            router.DISABLED_PROVIDERS.update(old_disabled)

    def test_discord_public_disabled_google_flash_fallback_allows_openrouter_equivalent(self):
        old_providers = router.PROVIDERS
        old_disabled = set(router.DISABLED_PROVIDERS)
        try:
            router.PROVIDERS = {
                'google': router.Provider(
                    'google',
                    'google-generative-language',
                    'https://generativelanguage.googleapis.com/v1beta',
                    'test-key',
                    ['gemini-2.5-flash'],
                ),
                'openrouter': router.Provider(
                    'openrouter',
                    'openai-completions',
                    'https://openrouter.ai/api/v1',
                    'test-key',
                    ['gemini-2.5-flash'],
                ),
            }
            router.DISABLED_PROVIDERS.clear()
            router.DISABLED_PROVIDERS.add('google')
            payload = {
                'model': 'sage-router/google/gemini-2.5-flash',
                'metadata': {'agent': 'discord-public'},
                'messages': [{'role': 'user', 'content': 'summarize this public thread'}],
            }
            self.assertTrue(router.apply_discord_public_route_profile(payload))
            provider, model = router.resolve_requested_provider_model(payload)

            _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
                payload['messages'],
                request_id='test-discord-public-google-flash-openrouter-fallback',
                thinking=router.ThinkingLevel.HIGH,
                route_mode='best',
                requirements=payload['requirements'],
                force_provider=provider,
                requested_model=model,
            )

            self.assertEqual([('openrouter', 'gemini-2.5-flash')], chain)
        finally:
            router.PROVIDERS = old_providers
            router.DISABLED_PROVIDERS.clear()
            router.DISABLED_PROVIDERS.update(old_disabled)

    def test_prepare_route_uses_inferred_provider_for_stale_forced_provider(self):
        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'hello'}],
            request_id='test-provider-switch',
            force_provider='ollama',
            requested_model='gpt-5.5',
        )
        self.assertEqual([('openai-codex', 'gpt-5.5')], chain[:1])

    def test_gpt_family_switches_to_openai_provider_even_if_catalog_is_incomplete(self):
        router.PROVIDERS['openai-codex'].models = ['gpt-5.4']
        provider, model = router.resolve_requested_provider_model({'model': 'ollama/gpt-5.5'})
        self.assertEqual('openai-codex', provider)
        self.assertEqual('gpt-5.5', model)

        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'hello'}],
            request_id='test-provider-family-switch',
            force_provider='ollama',
            requested_model='gpt-5.5',
        )
        self.assertEqual([('openai-codex', 'gpt-5.5')], chain[:1])

    def test_codex_subscription_beats_google_when_ollama_is_rate_limited(self):
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'http://ollama.invalid', '', ['glm-5']),
            'openai-codex': router.Provider('openai-codex', 'openai-codex-responses', 'https://codex.invalid', 'token', ['gpt-5.4']),
            'google': router.Provider('google', 'google-generative-language', 'https://google.invalid', 'key', ['gemini-2.5-pro']),
        }
        router.TEMP_MODEL_BLOCKS['ollama/glm-5'] = {
            'until': 9999999999,
            'reason': 'HTTP 429 Too Many Requests',
        }

        chain, scores, _rejections = router.select_model(
            router.Intent.ANALYSIS,
            router.Complexity.COMPLEX,
            router.ThinkingLevel.HIGH,
            'best',
            {'document': True, 'qualitySensitive': True},
            10000,
        )

        self.assertEqual(('openai-codex', 'gpt-5.4'), chain[0])
        codex_score = next(row for row in scores if row['provider'] == 'openai-codex')
        google_score = next(row for row in scores if row['provider'] == 'google')
        self.assertGreater(codex_score['score'], google_score['score'])
        self.assertIn(
            'user_pref_analysis_codex_subscription',
            [name for name, _value in codex_score['contributions']],
        )

    def test_balanced_route_reserves_public_chat_fallback_and_skips_nim_audio_models(self):
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'https://ollama.invalid', 'key', ['kimi-k2.5:cloud']),
            'openai': router.Provider('openai', 'openai-completions', 'https://openai.invalid/v1', 'key', ['gpt-5.4']),
            'openrouter': router.Provider('openrouter', 'openai-completions', 'https://openrouter.invalid/api/v1', 'key', ['gemini-2.5-flash']),
            'nvidia-nim': router.Provider('nvidia-nim', 'openai-completions', 'https://integrate.api.nvidia.com/v1', 'key', ['canary-asr', 'meta/llama-3.1-8b-instruct']),
        }

        self.assertFalse(router.is_chat_capable_model(router.PROVIDERS['nvidia-nim'], 'canary-asr'))

        chain, _scores, rejections = router.select_model(
            router.Intent.GENERAL,
            router.Complexity.SIMPLE,
            router.ThinkingLevel.MEDIUM,
            'balanced',
            {},
            100,
        )

        self.assertIn(('openrouter', 'gemini-2.5-flash'), chain)
        self.assertNotIn(('nvidia-nim', 'canary-asr'), chain)
        self.assertIn(
            {'provider': 'nvidia-nim', 'model': 'canary-asr', 'reason': 'not chat-capable'},
            rejections,
        )

    def test_balanced_route_reserves_openrouter_passthrough_fallback_when_catalog_is_sparse(self):
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'https://ollama.invalid', 'key', ['kimi-k2.5:cloud']),
            'openai': router.Provider('openai', 'openai-completions', 'https://openai.invalid/v1', 'key', ['gpt-5.4']),
            'openrouter': router.Provider('openrouter', 'openai-completions', 'https://openrouter.invalid/api/v1', 'key', ['anthropic/claude-sonnet-4.5']),
        }

        chain, _scores, _rejections = router.select_model(
            router.Intent.GENERAL,
            router.Complexity.SIMPLE,
            router.ThinkingLevel.MEDIUM,
            'balanced',
            {},
            100,
        )

        self.assertIn(('openrouter', 'gemini-2.5-flash'), chain)

    def test_frontier_route_reserves_reliable_plain_chat_fallback(self):
        router.PROVIDERS = {
            'ollama': router.Provider('ollama', 'ollama', 'https://ollama.invalid', 'key', ['glm-5:cloud']),
            'openrouter': router.Provider('openrouter', 'openai-completions', 'https://openrouter.invalid/api/v1', 'key', ['openai/gpt-5.4']),
        }
        requirements = {
            'qualitySensitive': True,
            'reasoning': True,
            'frontierLargeOnly': True,
            'allowProviders': ['ollama', 'openrouter'],
            'allowModels': ['*glm-5*', '*gpt-5*'],
        }

        chain, _scores, _rejections = router.select_model(
            router.Intent.GENERAL,
            router.Complexity.SIMPLE,
            router.ThinkingLevel.HIGH,
            'best',
            requirements,
            100,
        )

        self.assertIn(('openrouter', 'gemini-2.5-flash'), chain[:3])

    def test_fusion_selection_includes_reliable_plain_chat_fallback(self):
        router.PROVIDERS = {
            'openrouter': router.Provider(
                'openrouter',
                'openai-completions',
                'https://openrouter.invalid/api/v1',
                'key',
                ['x-ai/grok-4', 'anthropic/claude-sonnet-4.5', 'openai/gpt-5.4'],
                {'x-ai/grok-4', 'anthropic/claude-sonnet-4.5', 'openai/gpt-5.4'},
            ),
        }

        chain = router.select_fusion_panel_chain(
            [{'role': 'user', 'content': 'compare these choices'}],
            'test-fusion-reliable-fallback',
            router.ThinkingLevel.HIGH,
            'best',
            {'qualitySensitive': True, 'reasoning': True},
            False,
        )

        self.assertIn(('openrouter', 'gemini-2.5-flash'), chain)
        self.assertLess(chain.index(('openrouter', 'gemini-2.5-flash')), router.FUSION_PANEL_SIZE)

    def test_temp_model_blocks_are_honored_without_static_disabled_models(self):
        old_disabled_models = set(router.DISABLED_MODELS)
        try:
            router.DISABLED_MODELS = set()
            router.set_temp_model_block('ollama', 'glm-5', 3600, 'HTTP 429 Too Many Requests')

            self.assertIn('temporarily blocked', router.model_disabled_reason('ollama', 'glm-5'))

            chain, _scores, _rejections = router.select_model(
                router.Intent.ANALYSIS,
                router.Complexity.COMPLEX,
                router.ThinkingLevel.HIGH,
                'best',
                {'document': True, 'qualitySensitive': True},
                10000,
            )

            self.assertNotIn(('ollama', 'glm-5'), chain)
            self.assertIn(('openai-codex', 'gpt-5.5'), chain)
        finally:
            router.DISABLED_MODELS = old_disabled_models

    def test_ollama_payment_error_blocks_provider_models_temporarily(self):
        old_disabled_models = set(router.DISABLED_MODELS)
        try:
            router.DISABLED_MODELS = set()
            router.PROVIDERS['ollama-2'].models = ['glm-5.2', 'qwen3-next:80b']

            router.maybe_block_ollama_runtime_error(
                'ollama-2',
                'glm-5.2',
                'HTTP 403 Forbidden | {"error":"your subscription payment is past due. update your payment method"}',
            )

            self.assertIn('temporarily blocked', router.model_disabled_reason('ollama-2', 'glm-5.2'))
            self.assertIn('temporarily blocked', router.model_disabled_reason('ollama-2', 'qwen3-next:80b'))
        finally:
            router.DISABLED_MODELS = old_disabled_models

    def test_ranked_chain_reserves_slots_for_distinct_providers(self):
        router.PROVIDERS = {
            'openai-codex': router.Provider(
                'openai-codex',
                'openai-codex-responses',
                'https://codex.invalid',
                'token',
                ['gpt-5.5', 'gpt-5.4', 'gpt-5.3-codex', 'gpt-5.2-codex'],
            ),
            'openai': router.Provider(
                'openai',
                'openai-completions',
                'https://api.openai.invalid/v1',
                'token',
                ['gpt-5.4'],
            ),
            'ollama': router.Provider('ollama', 'ollama', 'http://ollama.invalid', '', ['glm-5']),
        }

        chain, _scores, _rejections = router.select_model(
            router.Intent.ANALYSIS,
            router.Complexity.COMPLEX,
            router.ThinkingLevel.HIGH,
            'best',
            {'document': True, 'longContext': True, 'preferTools': True, 'agentic': True},
            10000,
        )

        self.assertEqual('openai-codex', chain[0][0])
        self.assertIn('openai', [provider for provider, _model in chain])
        self.assertGreaterEqual(len({provider for provider, _model in chain[:3]}), 2)

    def test_balanced_profile_is_explicit_non_frontier_ollama_first(self):
        payload = {'model': 'sage-router/balanced', 'messages': [{'role': 'user', 'content': 'hello'}]}
        profile = router.apply_router_profile(payload)

        self.assertEqual('balanced', profile)
        self.assertEqual('sage-router/auto', payload['model'])
        self.assertEqual('balanced', payload['route'])
        self.assertEqual({'effort': 'medium'}, payload['thinking'])
        requirements = payload['requirements']
        self.assertEqual(['ollama-cyber', 'ollama'], requirements['allowProviders'][:2])
        self.assertIn('openai-codex', requirements['fallbackProviders'])
        self.assertIn('google', requirements['fallbackProviders'])
        self.assertFalse(requirements.get('frontierLargeOnly', False))
        self.assertFalse(requirements.get('reasoning', False))

    def test_discord_public_profile_allows_discovered_ollama_providers(self):
        payload = {
            'model': 'sage-router/frontier',
            'metadata': {'agentId': 'discord-public'},
            'messages': [{'role': 'user', 'content': 'hello'}],
        }

        self.assertTrue(router.apply_discord_public_route_profile(payload))

        requirements = payload['requirements']
        self.assertIn('ollama-2', requirements['allowProviders'])

    def test_tool_safe_profile_relaxes_when_strict_catalog_filter_is_empty(self):
        router.PROVIDERS = {
            'ollama-2': router.Provider('ollama-2', 'ollama', 'http://ollama-2.invalid', '', ['devstral-2:123b-cloud']),
        }
        requirements = {
            'qualitySensitive': True,
            'suppressToolCallContent': True,
            'frontierLargeOnly': True,
            'allowModels': ['*gpt-5*'],
            'allowProviders': ['ollama-2'],
        }

        _messages, _intent, _complexity, _tokens, chain = router.prepare_route(
            [{'role': 'user', 'content': 'analyze this and use tools if needed'}],
            request_id='test-tool-safe-relaxed-fallback',
            thinking=router.ThinkingLevel.HIGH,
            route_mode='best',
            requirements=requirements,
        )

        self.assertEqual([('ollama-2', 'devstral-2:123b-cloud')], chain)

    def test_stale_hosted_auto_profile_keeps_cloud_fallbacks(self):
        old_load_router_profiles = router.load_router_profiles
        try:
            router.load_router_profiles = lambda: {
                'auto': {
                    'route': 'best',
                    'thinking': 'high',
                    'requiresQuality': True,
                    'requiresReasoning': True,
                    'allowProviders': ['ollama-cloud', 'ollama'],
                    'fallbackProviders': ['ollama'],
                    'frontierLargeOnly': True,
                }
            }
            payload = {'model': 'auto', 'messages': [{'role': 'user', 'content': 'hello'}]}

            profile = router.apply_router_profile(payload)
        finally:
            router.load_router_profiles = old_load_router_profiles

        self.assertEqual('auto', profile)
        self.assertEqual('google/gemini-2.5-flash', payload['model'])
        requirements = payload['requirements']
        self.assertIn('google', requirements['allowProviders'])
        self.assertIn('openrouter', requirements['allowProviders'])
        self.assertIn('google', requirements['fallbackProviders'])
        self.assertFalse(requirements.get('frontierLargeOnly', False))
        self.assertFalse(requirements.get('reasoning', False))
        self.assertIn('*gemini-2.5-flash*', requirements['allowModels'])

    def test_google_tool_declarations_strip_unsupported_schema_keys(self):
        tools = [{
            'type': 'function',
            'function': {
                'name': 'lookup',
                'parameters': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'filters': {
                            'type': 'object',
                            'additionalProperties': {'type': 'string'},
                            'properties': {
                                'query': {'type': 'string'},
                                'mode': {
                                    'any_of': [
                                        {'const': 'fast', 'type': 'string'},
                                        {'const': 'deep', 'type': 'string'},
                                    ],
                                },
                                'count': {
                                    'type': ['integer', 'null'],
                                    'exclusiveMinimum': 0,
                                },
                            },
                        },
                    },
                },
            },
        }]

        declarations = router.google_tool_declarations(tools)

        parameters = declarations[0]['parameters']
        self.assertNotIn('additionalProperties', parameters)
        self.assertNotIn('additionalProperties', parameters['properties']['filters'])
        self.assertNotIn('any_of', parameters['properties']['filters']['properties']['mode'])
        self.assertNotIn('const', parameters['properties']['filters']['properties']['mode'])
        self.assertNotIn('exclusiveMinimum', parameters['properties']['filters']['properties']['count'])
        self.assertEqual('integer', parameters['properties']['filters']['properties']['count']['type'])
        self.assertEqual('string', parameters['properties']['filters']['properties']['query']['type'])


if __name__ == '__main__':
    unittest.main()
