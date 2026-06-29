#!/usr/bin/env python3
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('SAGE_ROUTER_DARIO_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART', '0')

import router  # noqa: E402


class ToolCallLeakTests(unittest.TestCase):

    def test_default_thinking_is_high(self):
        self.assertEqual(router.ThinkingLevel.HIGH, router.DEFAULT_THINKING_LEVEL)
        self.assertEqual(router.ThinkingLevel.HIGH, router.normalize_thinking(None))
        self.assertEqual(router.ThinkingLevel.HIGH, router.normalize_thinking({}))
        self.assertEqual(router.ThinkingLevel.LOW, router.normalize_thinking('low'))
        self.assertEqual(router.ThinkingLevel.MEDIUM, router.normalize_thinking('medium'))

    def test_detects_visible_tool_code_blocks(self):
        self.assertTrue(router.looks_like_visible_tool_call('tool_code\nmessage(action="delete")'))
        self.assertTrue(router.looks_like_visible_tool_call('```tool_code\n{"tool":"message","arguments":{}}\n```'))
        self.assertTrue(router.looks_like_visible_tool_call('functions.exec(command="ls")'))

    def test_does_not_reject_normal_text_or_structured_tool_calls(self):
        payload = {'tools': [{'type': 'function', 'function': {'name': 'message'}}]}
        self.assertEqual('', router.reject_visible_tool_call_leak(payload, 'I can help with that.', []))
        self.assertEqual('', router.reject_visible_tool_call_leak({}, 'tool_code\nmessage(action="send")', []))
        self.assertEqual('', router.reject_visible_tool_call_leak(payload, 'tool_code\nmessage(action="send")', [{'id': 'call_1'}]))



    def test_discord_public_profile_preserves_model_denies(self):
        payload = {
            'profile': 'discord-public',
            'model': 'openai-codex/gpt-5.4-mini',
            'messages': [{'role': 'user', 'content': 'discord-public test'}],
            'tools': [{'type': 'function', 'function': {'name': 'exec', 'parameters': {'type': 'object'}}}],
        }
        self.assertEqual('discord-public', router.apply_router_profile(payload))
        self.assertTrue(router.apply_discord_public_route_profile(payload))
        req = router.normalize_requirements(payload, router.normalize_thinking(payload.get('thinking')))
        self.assertIn('*-mini*', req.get('denyModels', []))
        self.assertFalse(router.model_meets_requirements(router.Provider('openai-codex', 'openai-codex-responses', '', '', ['gpt-5.4-mini']), 'gpt-5.4-mini', req, 100)[0])


    def test_model_prefix_is_opt_in_by_default(self):
        response = router.build_openai_completion('ollama', 'qwen3-coder-next:cloud', 'req1', 'hello')
        content = response['choices'][0]['message']['content']
        self.assertEqual('hello', content)
        self.assertNotIn('[ollama/qwen3-coder-next:cloud]', content)

    def test_model_prefix_dedupes_existing_prefix_and_aliases(self):
        old_show_model_prefix = router.SHOW_MODEL_PREFIX
        router.SHOW_MODEL_PREFIX = True
        router._PREFIX_SEEN.clear()
        try:
            first = router.build_openai_completion(
                'ollama-cloud',
                'qwen3-coder-next:cloud',
                '1520266336406732954',
                '[ollama/qwen3-coder-next] already prefixed',
            )
            second = router.build_openai_completion(
                'ollama-cyber',
                'qwen3-coder-next-cloud',
                '1520266336406732954',
                'second answer',
            )
        finally:
            router.SHOW_MODEL_PREFIX = old_show_model_prefix
            router._PREFIX_SEEN.clear()

        first_content = first['choices'][0]['message']['content']
        second_content = second['choices'][0]['message']['content']
        self.assertEqual('[ollama/qwen3-coder-next] already prefixed', first_content)
        self.assertEqual(1, first_content.count('[ollama/qwen3-coder-next]'))
        self.assertEqual('second answer', second_content)

    def test_repeated_upstream_model_prefixes_are_stripped(self):
        text = '[ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code]'
        self.assertEqual('', router.strip_leading_model_prefixes(text, 'ollama-2', 'kimi-k2.7-code'))

    def test_repeated_model_prefixes_around_tool_call_omissions_are_stripped(self):
        text = (
            '[ollama-2/kimi-k2.5] [tool calls omitted]\n'
            '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]'
        )
        self.assertEqual('', router.strip_leading_model_prefixes(text, 'ollama-2', 'kimi-k2.5'))

    def test_assistant_replay_noise_strips_thousand_placeholder_prefixes(self):
        replay = '\n'.join(
            '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]'
            for _ in range(1000)
        )
        messages = [
            {'role': 'system', 'content': 'system instructions'},
            {'role': 'assistant', 'content': replay},
            {'role': 'user', 'content': 'Bug report: [tool calls omitted] should stay literal here.'},
        ]

        sanitized = router.sanitize_replay_messages(messages)

        self.assertEqual(2, len(sanitized))
        self.assertEqual('system instructions', sanitized[0]['content'])
        self.assertEqual('Bug report: [tool calls omitted] should stay literal here.', sanitized[1]['content'])
        self.assertNotIn('ollama-2/kimi-k2.5', json.dumps(sanitized))

    def test_assistant_replay_noise_strips_same_line_placeholder_prefixes(self):
        replay = ' '.join(
            '[ollama-2/kimi-k2.5] [tool calls omitted]'
            for _ in range(1000)
        )
        messages = [
            {'role': 'assistant', 'content': replay},
            {'role': 'user', 'content': 'Bug report: [tool calls omitted] should stay literal here.'},
        ]

        sanitized = router.sanitize_replay_messages(messages)

        self.assertEqual(1, len(sanitized))
        self.assertEqual('Bug report: [tool calls omitted] should stay literal here.', sanitized[0]['content'])
        self.assertNotIn('ollama-2/kimi-k2.5', json.dumps(sanitized))

    def test_assistant_replay_noise_preserves_structured_tool_calls(self):
        messages = [{
            'role': 'assistant',
            'content': '[ollama-2/kimi-k2.5] [tool calls omitted]',
            'tool_calls': [{
                'id': 'call_1',
                'type': 'function',
                'function': {'name': 'lookup', 'arguments': {'path': '/tmp'}},
            }],
        }]

        sanitized = router.sanitize_replay_messages(messages)

        self.assertEqual('', sanitized[0]['content'])
        self.assertEqual('lookup', sanitized[0]['tool_calls'][0]['function']['name'])

    def test_stream_strips_late_model_prefixes_and_tool_call_omissions(self):
        state = {'prefix_open': True, 'prefix_pending': ''}
        self.assertEqual(
            'visible text',
            router.sanitize_stream_content_fragment('visible text', 'ollama-2', 'kimi-k2.5', state=state),
        )
        self.assertEqual(
            '',
            router.sanitize_stream_content_fragment(
                '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]',
                'ollama-2',
                'kimi-k2.5',
                state=state,
            ),
        )

    def test_stream_strips_late_fragmented_model_prefix_after_visible_text(self):
        state = {'prefix_open': True, 'prefix_pending': ''}
        self.assertEqual(
            'visible text',
            router.sanitize_stream_content_fragment('visible text', 'ollama-2', 'kimi-k2.5', state=state),
        )
        fragments = [
            '[ollama-2/',
            'kimi-k2.5] ',
            '[tool calls omitted]',
            '[ollama-2/kimi-k2.5] ',
            '[tool calls omitted]',
        ]
        cleaned = [
            router.sanitize_stream_content_fragment(fragment, 'ollama-2', 'kimi-k2.5', state=state)
            for fragment in fragments
        ]
        self.assertEqual(['', '', '', '', ''], cleaned)

    def test_stream_strips_late_fragmented_tool_call_omission_after_visible_text(self):
        state = {'prefix_open': True, 'prefix_pending': ''}
        self.assertEqual(
            'visible text',
            router.sanitize_stream_content_fragment('visible text', 'ollama-2', 'kimi-k2.5', state=state),
        )
        fragments = [
            '[ollama-2/kimi-k2.5] ',
            '[tool calls ',
            'omitted]',
            '[ollama-2/kimi-k2.5] [tool calls ',
            'omitted]',
        ]
        cleaned = [
            router.sanitize_stream_content_fragment(fragment, 'ollama-2', 'kimi-k2.5', state=state)
            for fragment in fragments
        ]
        self.assertEqual(['', '', '', '', ''], cleaned)

    def test_openai_compat_stream_strips_repeated_prefix_chunks(self):
        raw = (
            'data: {"id":"chatcmpl-1","choices":[{"index":0,'
            '"delta":{"role":"assistant","content":"[ollama-2/kimi-k2.7-code] '
            '[ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code]"},"finish_reason":null}]}\n'
        ).encode()
        sanitized = router.sanitize_openai_compat_stream_line(raw, 'ollama-2', 'kimi-k2.7-code')
        chunk = json.loads(sanitized.decode().split('data: ', 1)[1])
        self.assertEqual('', chunk['choices'][0]['delta']['content'])

    def test_openai_compat_stream_strips_repeated_prefix_message_chunks(self):
        raw = (
            'data: {"id":"chatcmpl-1","choices":[{"index":0,'
            '"message":{"role":"assistant","content":"[ollama-2/kimi-k2.5] '
            '[ollama-2/kimi-k2.5] [tool calls omitted]"},"finish_reason":null}]}\n'
        ).encode()
        sanitized = router.sanitize_openai_compat_stream_line(raw, 'ollama-2', 'kimi-k2.5')
        chunk = json.loads(sanitized.decode().split('data: ', 1)[1])
        self.assertEqual('', chunk['choices'][0]['message']['content'])

    def test_openai_compat_stream_strips_same_line_message_prefix_storm(self):
        raw = (
            'data: ' + json.dumps({
                'id': 'chatcmpl-1',
                'choices': [{
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': ' '.join(
                            '[ollama-2/kimi-k2.5] [tool calls omitted]'
                            for _ in range(1000)
                        ),
                    },
                    'finish_reason': None,
                }],
            }) + '\n'
        ).encode()
        sanitized = router.sanitize_openai_compat_stream_line(raw, 'ollama-2', 'kimi-k2.5')
        chunk = json.loads(sanitized.decode().split('data: ', 1)[1])
        self.assertEqual('', chunk['choices'][0]['message']['content'])

    def test_openai_compat_stream_keeps_tool_call_delta_while_stripping_prefix(self):
        raw = (
            'data: {"id":"chatcmpl-1","choices":[{"index":0,'
            '"delta":{"content":"[ollama-2/kimi-k2.7-code] ",'
            '"tool_calls":[{"index":0,"id":"call_1","type":"function",'
            '"function":{"name":"lookup","arguments":"{}"}}]},"finish_reason":null}]}\n'
        ).encode()
        sanitized = router.sanitize_openai_compat_stream_line(raw, 'ollama-2', 'kimi-k2.7-code')
        chunk = json.loads(sanitized.decode().split('data: ', 1)[1])
        delta = chunk['choices'][0]['delta']
        self.assertEqual('', delta['content'])
        self.assertEqual('lookup', delta['tool_calls'][0]['function']['name'])

    def test_openai_compat_stream_strips_fragmented_prefix_before_tool_call(self):
        state = {'prefix_open': True, 'prefix_pending': ''}
        lines = [
            'data: {"choices":[{"delta":{"role":"assistant","content":"[ollama-2/"}}]}\n',
            'data: {"choices":[{"delta":{"content":"kimi-k2.7-code] "}}]}\n',
            'data: {"choices":[{"delta":{"content":"[ollama-2/kimi-k2.7-code] "}}]}\n',
            (
                'data: {"choices":[{"delta":{"content":"[ollama-2/kimi-k2.7-code] ",'
                '"tool_calls":[{"index":0,"id":"call_1","type":"function",'
                '"function":{"name":"lookup","arguments":"{}"}}]}}]}\n'
            ),
        ]
        chunks = [
            json.loads(
                router.sanitize_openai_compat_stream_line(
                    line.encode(),
                    'ollama-2',
                    'kimi-k2.7-code',
                    state=state,
                ).decode().split('data: ', 1)[1]
            )
            for line in lines
        ]

        self.assertEqual(['', '', '', ''], [
            ((chunk['choices'][0]['delta']).get('content') or '')
            for chunk in chunks
        ])
        self.assertEqual('lookup', chunks[-1]['choices'][0]['delta']['tool_calls'][0]['function']['name'])

    def test_openai_compat_stream_strips_fragmented_tool_call_omission(self):
        state = {'prefix_open': True, 'prefix_pending': ''}
        lines = [
            'data: {"choices":[{"delta":{"role":"assistant","content":"visible text"}}]}\n',
            'data: {"choices":[{"delta":{"content":"[ollama-2/kimi-k2.5] "}}]}\n',
            'data: {"choices":[{"delta":{"content":"[tool calls "}}]}\n',
            'data: {"choices":[{"delta":{"content":"omitted]"}}]}\n',
        ]
        chunks = [
            json.loads(
                router.sanitize_openai_compat_stream_line(
                    line.encode(),
                    'ollama-2',
                    'kimi-k2.5',
                    state=state,
                ).decode().split('data: ', 1)[1]
            )
            for line in lines
        ]

        self.assertEqual('visible text', chunks[0]['choices'][0]['delta']['content'])
        self.assertEqual(['', '', ''], [
            ((chunk['choices'][0]['delta']).get('content') or '')
            for chunk in chunks[1:]
        ])

    def test_wrapped_sse_strips_stale_prefix_content_before_tool_call(self):
        class FakeHandler:
            def __init__(self):
                self.writes = []

            def send_response(self, _code):
                pass

            def send_header(self, _key, _value):
                pass

            def end_headers(self):
                pass

            def routing_headers(self, _payload, _request_id):
                return {}

            @property
            def wfile(self):
                outer = self

                class W:
                    def write(self, data):
                        outer.writes.append(data)

                    def flush(self):
                        pass

                return W()

        handler = FakeHandler()
        router.write_openai_completion_as_sse(handler, {
            'id': 'chatcmpl-1',
            'created': 1,
            'model': 'ollama-2/kimi-k2.7-code',
            'choices': [{
                'message': {
                    'content': '[ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code]',
                    'tool_calls': [{
                        'id': 'call_1',
                        'type': 'function',
                        'function': {'name': 'lookup', 'arguments': '{}'},
                    }],
                },
                'finish_reason': 'tool_calls',
            }],
        }, 'req-wrapped-tools')
        body = b''.join(handler.writes).decode()
        self.assertNotIn('[ollama-2/kimi-k2.7-code]', body)
        self.assertIn('"tool_calls"', body)
        self.assertIn('"finish_reason": "tool_calls"', body)

    def test_router_profile_wrapped_sse_keeps_profile_model_for_tool_calls(self):
        class FakeHandler:
            def __init__(self):
                self.writes = []

            def send_response(self, _code):
                pass

            def send_header(self, _key, _value):
                pass

            def end_headers(self):
                pass

            def routing_headers(self, _payload, _request_id):
                return {}

            @property
            def wfile(self):
                outer = self

                class W:
                    def write(self, data):
                        outer.writes.append(data)

                    def flush(self):
                        pass

                return W()

        result = router.build_openai_completion(
            'ollama-2',
            'kimi-k2.5',
            'req-profile-tools',
            '',
            [{
                'id': 'call_1',
                'type': 'function',
                'function': {'name': 'lookup', 'arguments': '{}'},
            }],
            'tool_calls',
        )
        result['upstream_model'] = result['model']
        result['model'] = router.client_visible_model_for_request({'model': 'sage-router/frontier'}, None, 'sage-router/frontier')

        handler = FakeHandler()
        router.write_openai_completion_as_sse(handler, result, 'req-profile-tools')
        body = b''.join(handler.writes).decode()
        chunks = [
            json.loads(line[len('data: '):])
            for line in body.splitlines()
            if line.startswith('data: ') and line != 'data: [DONE]'
        ]

        self.assertTrue(chunks)
        self.assertTrue(all(chunk['model'] == 'sage-router/frontier' for chunk in chunks))
        self.assertNotIn('"model": "ollama-2/kimi-k2.5"', body)
        self.assertIn('"tool_calls"', body)

    def test_wrapped_chat_sse_ignores_client_disconnect(self):
        class FakeHandler:
            def __init__(self):
                self.status = None

            def send_response(self, code):
                self.status = code

            def send_header(self, _key, _value):
                pass

            def end_headers(self):
                pass

            def routing_headers(self, _payload, _request_id):
                return {}

            @property
            def wfile(self):
                class W:
                    def write(self, _data):
                        raise BrokenPipeError()

                    def flush(self):
                        raise BrokenPipeError()

                return W()

        handler = FakeHandler()
        router.write_openai_completion_as_sse(handler, {
            'id': 'chatcmpl-1',
            'created': 1,
            'model': 'sage-router/frontier',
            'choices': [{
                'message': {'content': 'OK'},
                'finish_reason': 'stop',
            }],
        }, 'req-disconnect')
        self.assertEqual(200, handler.status)

    def test_responses_sse_ignores_client_disconnect(self):
        class FakeHandler:
            def __init__(self):
                self.status = None

            def send_response(self, code):
                self.status = code

            def send_header(self, _key, _value):
                pass

            def send_cors_headers(self):
                pass

            def end_headers(self):
                pass

            @property
            def wfile(self):
                class W:
                    def write(self, _data):
                        raise BrokenPipeError()

                    def flush(self):
                        raise BrokenPipeError()

                return W()

        handler = FakeHandler()
        router.write_responses_as_sse(handler, {
            'id': 'resp-1',
            'object': 'response',
            'created_at': 1,
            'model': 'sage-router/frontier',
            'output': [{
                'id': 'msg-1',
                'type': 'message',
                'role': 'assistant',
                'content': [{'type': 'output_text', 'text': 'OK'}],
            }],
        }, 'req-responses-disconnect')
        self.assertEqual(200, handler.status)

    def test_native_ollama_stream_strips_fragmented_prefix_before_tool_call(self):
        class FakeHandler:
            def __init__(self):
                self.writes = []

            def send_response(self, _code):
                pass

            def send_header(self, _key, _value):
                pass

            def end_headers(self):
                pass

            def routing_headers(self, _payload, _request_id):
                return {}

            @property
            def wfile(self):
                outer = self

                class W:
                    def write(self, data):
                        outer.writes.append(data)

                    def flush(self):
                        pass

                return W()

        class FakeResponse:
            def __init__(self, lines):
                self.lines = [line.encode() for line in lines]

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def readline(self):
                if self.lines:
                    return self.lines.pop(0)
                return b''

        lines = [
            json.dumps({'message': {'content': '[ollama-2/'}, 'done': False}) + '\n',
            json.dumps({'message': {'content': 'kimi-k2.7-code] '}, 'done': False}) + '\n',
            json.dumps({'message': {
                'content': '[ollama-2/kimi-k2.7-code] ',
                'tool_calls': [{
                    'id': 'call_1',
                    'type': 'function',
                    'function': {'name': 'lookup', 'arguments': {'id': 'abc'}},
                }],
            }, 'done': True}) + '\n',
        ]
        old_open = router.open_upstream_with_credential_failover
        try:
            router.open_upstream_with_credential_failover = lambda *_args, **_kwargs: (FakeResponse(lines), '')
            handler = FakeHandler()
            router.stream_ollama_to_client(
                handler,
                router.Provider('ollama-2', 'ollama', 'http://ollama.example', '', ['kimi-k2.7-code']),
                'kimi-k2.7-code',
                {'messages': [{'role': 'user', 'content': 'lookup abc'}], 'tools': [{'type': 'function'}]},
                'req-native-tools',
            )
        finally:
            router.open_upstream_with_credential_failover = old_open

        body = b''.join(handler.writes).decode()
        self.assertNotIn('[ollama-2/kimi-k2.7-code]', body)
        self.assertNotIn('[ollama-2/', body)
        self.assertIn('"tool_calls"', body)
        self.assertIn('"finish_reason": "tool_calls"', body)

    def test_provider_prefixed_model_id_does_not_double_display_provider(self):
        self.assertEqual(
            'ollama-2/kimi-k2.7-code',
            router.display_model_id('ollama-2', 'ollama-2/kimi-k2.7-code'),
        )

    def test_repeated_upstream_model_prefixes_are_stripped_across_aliases(self):
        text = '[ollama-2/kimi-k2.7-code] [ollama-2/kimi-k2.7-code] tool result ready'
        self.assertEqual(
            'tool result ready',
            router.strip_leading_model_prefixes(text, 'ollama', 'kimi-k2.7-code'),
        )

    def test_upstream_model_prefix_is_stripped_before_visible_content(self):
        text = '[ollama-2/kimi-k2.7-code] tool result ready'
        self.assertEqual(
            'tool result ready',
            router.strip_leading_model_prefixes(text, 'ollama-2', 'kimi-k2.7-code'),
        )

    def test_debug_prefix_dedupes_against_model_prefix(self):
        router._PREFIX_SEEN.clear()
        try:
            prefixed = router.model_prefix_once('ollama-cloud', 'glm-5.1:cloud', '1520266336406732954', 'first')
            debug_prefix = router.streaming_debug_prefix('ollama-cyber', 'glm-5.1-cloud', '1520266336406732954')
        finally:
            router._PREFIX_SEEN.clear()

        self.assertEqual('[ollama/glm-5.1] first', prefixed)
        self.assertEqual('', debug_prefix)

    def test_structured_tool_calls_never_include_visible_narration(self):
        response = router.build_openai_completion(
            'ollama',
            'qwen3-coder-next:cloud',
            'req1',
            'I will check this first.',
            [{'function': {'name': 'message', 'arguments': {'action': 'read'}}}],
        )
        message = response['choices'][0]['message']
        self.assertEqual('', message['content'])
        self.assertEqual('tool_calls', response['choices'][0]['finish_reason'])
        self.assertIn('tool_calls', message)

    def test_detects_codex_inline_tool_leaks(self):
        noisy = '''I’ll pull the records.
{"cmd":"cd /data/.openclaw/workspace-discord-public && find EARLCoin -maxdepth 4 -type f", "yieldMs":1000}
{"path":"/home/umbrel/.openclaw/workspace-discord-public/AGENTS.md"}
to=exec {"cmd":"cd /data/.openclaw/workspace-discord-public && pwd"}
 I can calculate it, but need source records.'''
        self.assertTrue(router.looks_like_visible_tool_call(noisy))

    def test_rejects_codex_inline_tool_leaks_when_tools_present(self):
        payload = {'tools': [{'type': 'function', 'function': {'name': 'exec'}}]}
        text = 'I will inspect it. {"cmd":"cd /data/.openclaw/workspace-discord-public && ls EARLCoin"}'
        self.assertEqual(
            'provider leaked tool call as visible text instead of structured tool_calls',
            router.reject_visible_tool_call_leak(payload, text, []),
        )


    def test_sanitizes_thinking_without_raw_fallback(self):
        self.assertEqual('final answer', router.sanitize_visible_output('<think>private chain</think> final answer'))
        self.assertEqual('', router.sanitize_visible_output('<think>private chain only</think>'))
        self.assertEqual('', router.sanitize_visible_output('<think>unterminated private chain'))

    def test_sanitizes_channel_tagged_analysis(self):
        raw = '<|channel|>analysis<|message|>private reasoning<|channel|>final<|message|>public answer'
        self.assertEqual('public answer', router.sanitize_visible_output(raw))

    def test_visible_output_strips_repeated_model_prefix_tool_placeholders(self):
        raw = (
            '[ollama-2/kimi-k2.5] [tool calls omitted]\n'
            '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]\n'
            'final answer'
        )
        self.assertEqual('final answer', router.sanitize_visible_output(raw))

    def test_visible_output_strips_thousand_model_prefix_tool_placeholders(self):
        raw = '\n'.join(
            '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]'
            for _ in range(1000)
        )
        self.assertEqual('', router.sanitize_visible_output(raw))

    def test_visible_output_strips_thousand_model_prefix_only_placeholders(self):
        raw = '\n'.join(
            '[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5]'
            for _ in range(1000)
        )
        self.assertEqual('', router.sanitize_visible_output(raw))

    def test_visible_output_strips_prefix_only_partial_tail(self):
        self.assertEqual('', router.sanitize_visible_output('[ollama-2/glm'))

    def test_visible_output_strips_same_line_model_prefix_tool_placeholders(self):
        raw = ' '.join(
            '[ollama-2/kimi-k2.5] [tool calls omitted]'
            for _ in range(1000)
        )
        self.assertEqual('', router.sanitize_visible_output(raw))

    def test_visible_output_strips_same_line_model_prefix_only_placeholders(self):
        raw = ' '.join(
            '[ollama-2/kimi-k2.5]'
            for _ in range(1000)
        )
        self.assertEqual('', router.sanitize_visible_output(raw))

    def test_visible_output_strips_suffix_model_prefix_tool_placeholder_storm(self):
        raw = 'final answer ' + ' '.join(
            '[ollama-2/kimi-k2.5] [tool calls omitted]'
            for _ in range(1000)
        )
        self.assertEqual('final answer', router.sanitize_visible_output(raw))

    def test_visible_output_strips_suffix_model_prefix_only_storm(self):
        raw = 'final answer ' + ' '.join(
            '[ollama-2/kimi-k2.5]'
            for _ in range(1000)
        )
        self.assertEqual('final answer', router.sanitize_visible_output(raw))

    def test_visible_output_strips_plain_repeated_model_prefix_before_text(self):
        raw = ' '.join('[ollama-2/glm-5.2]' for _ in range(1000)) + ' The goal is already complete. No further action needed.'
        self.assertEqual(
            'The goal is already complete. No further action needed.',
            router.sanitize_visible_output(raw),
        )

    def test_detects_structured_json_tool_leaks(self):
        leaked = '{"recipient_name":"functions.exec","parameters":{"command":"ls"}}'
        self.assertTrue(router.looks_like_visible_tool_call(leaked))

    def test_normalized_tool_arguments_stay_openai_compatible(self):
        call = {'function': {'name': 'message', 'arguments': {'action': 'send', 'message': 'hi'}}}
        converted = router.openai_tool_calls([call])
        args = converted[0]['function']['arguments']
        self.assertIsInstance(args, str)
        self.assertEqual(json.loads(args)['action'], 'send')

    def test_responses_tool_definition_converts_chat_completion_function_schema(self):
        converted = router.responses_tool_definition({
            'type': 'function',
            'function': {
                'name': 'lookup_record',
                'description': 'Look up a record.',
                'parameters': {'type': 'object', 'properties': {'id': {'type': 'string'}}},
                'strict': True,
            },
        })
        self.assertEqual({
            'type': 'function',
            'name': 'lookup_record',
            'description': 'Look up a record.',
            'parameters': {'type': 'object', 'properties': {'id': {'type': 'string'}}},
            'strict': True,
        }, converted)

    def test_responses_tool_choice_converts_named_function_choice(self):
        self.assertEqual(
            {'type': 'function', 'name': 'lookup_record'},
            router.responses_tool_choice({'type': 'function', 'function': {'name': 'lookup_record'}}),
        )
        self.assertEqual('required', router.responses_tool_choice('required'))
        self.assertIsNone(router.responses_tool_choice('auto'))

    def test_goal_slash_command_becomes_agent_objective_context(self):
        payload = {
            'model': 'sage-router/frontier',
            'messages': [{'role': 'user', 'content': '/goal ship the activation funnel'}],
        }

        self.assertTrue(router.apply_goal_compat(payload))

        self.assertEqual('best', payload['route'])
        self.assertEqual({'effort': 'high'}, payload['thinking'])
        self.assertTrue(payload['requirements']['agentic'])
        self.assertTrue(payload['requirements']['reasoning'])
        self.assertTrue(payload['requirements']['longContext'])
        self.assertTrue(payload['metadata']['codexGoalMode'])
        self.assertIn('Codex/OpenClaw goal mode is active', payload['messages'][0]['content'])
        self.assertIn('ship the activation funnel', payload['messages'][0]['content'])
        self.assertNotIn('/goal ship the activation funnel', json.dumps(payload['messages']))

    def test_codex_internal_goal_context_is_normalized_for_responses_payload(self):
        chat_payload = router.responses_payload_to_chat_payload({
            'model': 'sage-router/frontier',
            'input': [{
                'role': 'user',
                'content': [{
                    'type': 'input_text',
                    'text': (
                        '<codex_internal_context source="goal">'
                        '<objective>make sage-router compatible with Codex goals</objective>'
                        '</codex_internal_context>\n'
                        'Continue from the newest request.'
                    ),
                }],
            }],
        })

        self.assertTrue(router.apply_goal_compat(chat_payload))

        self.assertEqual('Continue from the newest request.', chat_payload['messages'][1]['content'])
        self.assertIn('make sage-router compatible with Codex goals', chat_payload['messages'][0]['content'])
        self.assertNotIn('codex_internal_context', json.dumps(chat_payload['messages']))
        self.assertTrue(chat_payload['requirements']['frontierOrReasoningTools'])
        self.assertTrue(chat_payload['requirements']['suppressToolCallContent'])

    def test_parse_responses_stream_returns_function_calls(self):
        lines = [
            b'event: response.output_item.added\n',
            b'data: {"type":"response.output_item.added","item":{"id":"fc_1","type":"function_call","call_id":"call_1","name":"lookup_record","arguments":""}}\n',
            b'event: response.function_call_arguments.delta\n',
            b'data: {"type":"response.function_call_arguments.delta","item_id":"fc_1","delta":"{\\"id\\":"}\n',
            b'event: response.function_call_arguments.done\n',
            b'data: {"type":"response.function_call_arguments.done","item_id":"fc_1","arguments":"{\\"id\\":\\"abc\\"}"}\n',
            b'data: [DONE]\n',
        ]
        text, tool_calls = router.parse_responses_stream(lines)
        self.assertEqual('', text)
        self.assertEqual('call_1', tool_calls[0]['id'])
        self.assertEqual('lookup_record', tool_calls[0]['function']['name'])
        self.assertEqual('{"id":"abc"}', tool_calls[0]['function']['arguments'])

    def test_responses_input_to_chat_messages_drops_non_message_items(self):
        messages = router.responses_input_to_chat_messages([
            {'type': 'web_search_call', 'id': 'ws_1', 'status': 'completed'},
            {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'hello'}]},
            {'type': 'function_call', 'call_id': 'call_1', 'name': 'lookup_record', 'arguments': '{"id":"abc"}'},
            {'type': 'function_call_output', 'call_id': 'call_1', 'output': 'record'},
        ], instructions='be brief')
        self.assertEqual('system', messages[0]['role'])
        self.assertEqual('user', messages[1]['role'])
        self.assertEqual('hello', messages[1]['content'])
        self.assertEqual('assistant', messages[2]['role'])
        self.assertEqual('lookup_record', messages[2]['tool_calls'][0]['function']['name'])
        self.assertEqual('tool', messages[3]['role'])
        self.assertEqual('call_1', messages[3]['tool_call_id'])

    def test_responses_input_to_chat_messages_drops_orphan_tool_outputs(self):
        messages = router.responses_input_to_chat_messages([
            {'type': 'function_call_output', 'call_id': '', 'output': 'orphan'},
            {'type': 'function_call_output', 'output': 'orphan'},
            {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'continue'}]},
        ])

        self.assertEqual([{'role': 'user', 'content': 'continue'}], messages)

    def test_responses_input_to_chat_messages_drops_assistant_prefix_storms(self):
        storm = ' '.join('[ollama-2/kimi-k2.5] [tool calls omitted]' for _ in range(1000))
        messages = router.responses_input_to_chat_messages([
            {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': storm}]},
            {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'continue'}]},
        ])

        self.assertEqual([{'role': 'user', 'content': 'continue'}], messages)

    def test_chat_messages_to_responses_input_drops_assistant_prefix_storms(self):
        storm = ' '.join('[ollama-2/kimi-k2.5] [tool calls omitted]' for _ in range(1000))
        items = router.chat_messages_to_responses_input([
            {'role': 'assistant', 'content': storm},
            {'role': 'user', 'content': 'continue'},
        ])

        self.assertEqual([{'role': 'user', 'content': 'continue'}], items)

    def test_chat_messages_to_responses_input_never_emits_empty_call_ids(self):
        items = router.chat_messages_to_responses_input([
            {
                'role': 'assistant',
                'content': '',
                'tool_calls': [{'id': '', 'function': {'name': 'lookup_record', 'arguments': '{"id":"abc"}'}}],
            },
            {'role': 'tool', 'tool_call_id': '', 'content': 'orphan result'},
        ])

        self.assertEqual(1, len(items))
        self.assertEqual('function_call', items[0]['type'])
        self.assertTrue(items[0]['call_id'])
        self.assertNotEqual('', items[0]['call_id'])

    def test_responses_tool_schema_converts_to_chat_schema(self):
        converted = router.responses_tools_to_chat_tools([{
            'type': 'function',
            'name': 'lookup_record',
            'description': 'Look up a record.',
            'parameters': {'type': 'object', 'properties': {'id': {'type': 'string'}}},
            'strict': True,
        }])
        self.assertEqual('function', converted[0]['type'])
        self.assertEqual('lookup_record', converted[0]['function']['name'])
        self.assertTrue(converted[0]['function']['strict'])

    def test_chat_completion_translates_to_responses_output(self):
        chat = router.build_openai_completion(
            'ollama',
            'qwen3',
            'req1',
            'hello',
            [{'id': 'call_1', 'function': {'name': 'lookup_record', 'arguments': '{"id":"abc"}'}}],
        )
        response = router.openai_chat_completion_to_responses(chat, {'model': 'sage-router/frontier'}, 'req1')
        self.assertEqual('response', response['object'])
        self.assertEqual('ollama/qwen3', response['model'])
        self.assertEqual('function_call', response['output'][0]['type'])
        self.assertEqual('lookup_record', response['output'][0]['name'])

    def test_responses_output_sanitizes_client_visible_model_prefix_replay(self):
        chat = {
            'id': 'chatcmpl-test',
            'created': 1,
            'model': 'sage-router/frontier',
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': '[ollama-2/glm-5.2] [ollama-2/glm-5.2] The goal is already complete. No further action needed.',
                },
                'finish_reason': 'stop',
            }],
            'usage': {},
        }

        response = router.openai_chat_completion_to_responses(chat, {'model': 'sage-router/frontier'}, 'req1')

        self.assertEqual('sage-router/frontier', response['model'])
        self.assertEqual('The goal is already complete. No further action needed.', response['output_text'])
        self.assertEqual(response['output_text'], response['output'][0]['content'][0]['text'])

    def test_responses_sse_sanitizes_raw_prefix_storm_payload(self):
        class FakeHandler:
            def __init__(self):
                self.writes = []

            def send_response(self, _code):
                pass

            def send_header(self, _key, _value):
                pass

            def send_cors_headers(self):
                pass

            def end_headers(self):
                pass

            @property
            def wfile(self):
                outer = self

                class W:
                    def write(self, data):
                        outer.writes.append(data)

                    def flush(self):
                        pass

                return W()

        storm = ' '.join('[ollama-2/kimi-k2.5] [tool calls omitted]' for _ in range(1000))
        response = {
            'id': 'resp-prefix-storm',
            'object': 'response',
            'created_at': 1,
            'model': 'sage-router/frontier',
            'output_text': storm,
            'output': [{
                'id': 'msg-prefix-storm',
                'type': 'message',
                'status': 'completed',
                'role': 'assistant',
                'content': [{'type': 'output_text', 'text': storm, 'annotations': []}],
            }],
        }

        handler = FakeHandler()
        router.write_responses_as_sse(handler, response, 'req-prefix-storm')
        body = b''.join(handler.writes).decode()

        self.assertNotIn('[ollama-2/kimi-k2.5]', body)
        self.assertNotIn('[tool calls omitted]', body)

    def test_direct_codex_scoring_is_not_capped_as_recursive_gateway(self):
        debug_scores = []
        provider = router.Provider('openai-codex', 'openai-codex-responses', 'https://codex.example/v1', 'token', ['gpt-5-codex'])
        router.score_provider_model(
            provider,
            'gpt-5-codex',
            router.Intent.CODE,
            router.Complexity.SIMPLE,
            debug_scores=debug_scores,
            requirements={'agentic': True},
        )
        contributions = [name for name, _ in debug_scores[0]['contributions']]
        self.assertNotIn('openclaw_gateway_recursive_cap', contributions)
        self.assertNotIn('openclaw_gateway_penalty', contributions)
        self.assertIn('agentic_code_codex_bonus', contributions)

    def test_anthropic_max_tokens_maps_to_length_and_back(self):
        self.assertEqual('length', router.anthropic_stop_reason_to_openai_finish_reason('max_tokens'))
        self.assertEqual('max_tokens', router.openai_finish_reason_to_anthropic_stop_reason('length'))

        response = router.build_openai_completion('dario', 'claude-sonnet-4', 'req1', 'partial', finish_reason='length')
        anthropic = router.openai_to_anthropic_response(response, 'claude-sonnet-4')
        self.assertEqual('max_tokens', anthropic['stop_reason'])

    def test_anthropic_end_turn_still_maps_to_openai_stop(self):
        self.assertEqual('stop', router.anthropic_stop_reason_to_openai_finish_reason('end_turn'))
        self.assertEqual('end_turn', router.openai_finish_reason_to_anthropic_stop_reason('stop'))

    def test_google_max_tokens_maps_to_length(self):
        self.assertEqual('length', router.google_finish_reason_to_openai_finish_reason('MAX_TOKENS'))
        self.assertEqual('stop', router.google_finish_reason_to_openai_finish_reason('STOP'))

    def test_google_payload_includes_function_declarations_and_tool_results(self):
        payload = router.build_google_generate_payload(
            [
                {'role': 'user', 'content': 'List files'},
                {'role': 'assistant', 'content': '', 'tool_calls': [{
                    'id': 'call_123',
                    'type': 'function',
                    'function': {'name': 'exec', 'arguments': '{"command":"ls"}'},
                }]},
                {'role': 'tool', 'tool_call_id': 'call_123', 'content': 'README.md'},
            ],
            tools=[{
                'type': 'function',
                'function': {
                    'name': 'exec',
                    'description': 'Run a shell command.',
                    'parameters': {'type': 'object', 'properties': {'command': {'type': 'string'}}},
                },
            }],
            tool_choice='required',
        )
        declaration = payload['tools'][0]['functionDeclarations'][0]
        self.assertEqual('exec', declaration['name'])
        self.assertEqual({'type': 'object', 'properties': {'command': {'type': 'string'}}}, declaration['parameters'])
        self.assertEqual('ANY', payload['toolConfig']['functionCallingConfig']['mode'])
        self.assertEqual(['exec'], payload['toolConfig']['functionCallingConfig']['allowedFunctionNames'])
        self.assertEqual({'name': 'exec', 'args': {'command': 'ls'}}, payload['contents'][1]['parts'][0]['functionCall'])
        self.assertEqual({'name': 'exec', 'response': {'result': 'README.md'}}, payload['contents'][2]['parts'][0]['functionResponse'])

    def test_google_function_call_response_maps_to_openai_tool_calls(self):
        body = {
            'candidates': [{
                'content': {'parts': [{'functionCall': {'name': 'exec', 'args': {'command': 'find /tmp -maxdepth 1'}}}]},
                'finishReason': 'STOP',
            }]
        }
        calls = router.parse_google_generate_tool_calls(body)
        self.assertEqual(1, len(calls))
        self.assertTrue(calls[0]['id'].startswith('call_'))
        self.assertEqual('exec', calls[0]['function']['name'])
        self.assertEqual({'command': 'find /tmp -maxdepth 1'}, calls[0]['function']['arguments'])

    def test_google_completion_returns_structured_tool_calls(self):
        response_body = {
            'candidates': [{
                'content': {'parts': [{'functionCall': {'name': 'exec', 'args': {'command': 'ls -la /'}}}]},
                'finishReason': 'STOP',
            }]
        }

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return json.dumps(response_body).encode()

        old_urlopen = router.urllib.request.urlopen
        captured = {}

        def fake_urlopen(req, timeout=None):
            captured['payload'] = json.loads(req.data.decode())
            captured['timeout'] = timeout
            return FakeResponse()

        router.urllib.request.urlopen = fake_urlopen
        try:
            ok, completion = router.call_google_completion(
                'https://generativelanguage.googleapis.com',
                'gemini-2.5-flash',
                {
                    'messages': [{'role': 'user', 'content': 'inspect root'}],
                    'tools': [{'type': 'function', 'function': {'name': 'exec', 'parameters': {'type': 'object'}}}],
                    'tool_choice': 'auto',
                },
                api_key='test-key',
                request_id='req-google-tools',
            )
        finally:
            router.urllib.request.urlopen = old_urlopen

        self.assertTrue(ok)
        self.assertIn('tools', captured['payload'])
        self.assertEqual('AUTO', captured['payload']['toolConfig']['functionCallingConfig']['mode'])
        self.assertEqual('tool_calls', completion['choices'][0]['finish_reason'])
        message = completion['choices'][0]['message']
        self.assertEqual('', message['content'])
        self.assertEqual('exec', message['tool_calls'][0]['function']['name'])
        self.assertEqual({'command': 'ls -la /'}, json.loads(message['tool_calls'][0]['function']['arguments']))

    def test_google_models_are_tool_capable_for_agentic_fallback(self):
        provider = router.Provider('google', 'google-generative-language', 'https://generativelanguage.googleapis.com/v1beta', 'key', ['gemini-2.5-flash'])
        self.assertTrue(router.model_capabilities(provider, 'gemini-2.5-flash')['tools'])

    def test_google_ignores_stale_host_servable_metadata(self):
        provider = router.Provider(
            'google',
            'google-generative-language',
            'https://generativelanguage.googleapis.com/v1beta',
            'key',
            ['gemini-2.5-flash'],
            model_meta={'gemini-2.5-flash': {'servable': False, 'supportsTools': True}},
        )
        ok, reason = router.model_meets_requirements(provider, 'gemini-2.5-flash', {'tools': True}, 100)
        self.assertTrue(ok, reason)

    def test_explicit_google_prefix_is_not_reassigned_to_openrouter(self):
        old_providers = router.PROVIDERS
        old_disabled = set(router.DISABLED_PROVIDERS)
        try:
            router.PROVIDERS = {
                'google': router.Provider('google', 'google-generative-language', 'https://generativelanguage.googleapis.com/v1beta', 'key', ['gemini-2.5-flash']),
                'openrouter': router.Provider('openrouter', 'openai-completions', 'https://openrouter.example/v1', 'key', ['gemini-2.5-flash']),
            }
            router.DISABLED_PROVIDERS.clear()
            provider, model = router.resolve_requested_provider_model({'model': 'google/gemini-2.5-flash'})
            self.assertEqual(('google', 'gemini-2.5-flash'), (provider, model))
            _, _, _, _, chain = router.prepare_route(
                [{'role': 'user', 'content': 'call a tool'}],
                requirements={'tools': True},
                force_provider=provider,
                requested_model=model,
            )
            self.assertEqual([('google', 'gemini-2.5-flash')], chain[:1])
        finally:
            router.PROVIDERS = old_providers
            router.DISABLED_PROVIDERS.clear()
            router.DISABLED_PROVIDERS.update(old_disabled)


if __name__ == '__main__':
    unittest.main()
