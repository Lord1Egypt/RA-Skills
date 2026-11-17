"""Fixed package attribution; invented accounts, no network or native config."""
import io
import json
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

from test_account_flow import FakeAPI, FakeConfig, LoginAPI, account, inputs
from qianlima_skill import AUTH_ERROR_RULES


SOURCE = 'bb3b4102f584028c3830df37'


class SourceContractTests(unittest.TestCase):
    def test_login_payload_and_existing_request_sequence(self):
        for new in (True, False):
            with self.subTest(new=new):
                api = LoginAPI(new=new)
                data = inputs(action='verify', smsCode='012345', configVersion='fake-v')
                result = account.register(data, api, FakeConfig())
                self.assertEqual(result['status'], 'configuration_saved')
                logins = [c for c in api.calls if c[1] == '/api/auth/login']
                self.assertEqual(len(logins), 1)
                expected = {k: data[k] for k in
                            ('phone', 'smsCode')}
                self.assertEqual(logins[0][2], dict(expected, sourceCode=SOURCE, agreementVersion='test-v1', privacyVersion='test-v1'))
                paths = ['/api/legal?type=TERMS', '/api/legal?type=PRIVACY', '/api/auth/login']
                if not new:
                    paths.append('/api/api-keys/7/reveal')
                self.assertEqual([c[1] for c in api.calls],
                                 paths + ['/api/points/account', '/api/auth/logout'])
                for _, path, body, token in api.calls:
                    if path != '/api/auth/login':
                        self.assertNotIn('sourceCode', body or {})
                    self.assertNotIn(SOURCE, token or '')
                self.assertNotIn(SOURCE, api.secret)

    def test_stdin_cannot_override_package_source_and_guidance_matches(self):
        api = LoginAPI()
        data = inputs(action='verify', smsCode='012345', configVersion='fake-v',
                      source='external-page', sourceCode='other-package')
        with patch.object(account, 'AccountAPI', return_value=api), \
             patch.object(account, 'CodexConfig') as config, \
             patch.object(sys, 'argv', ['account', 'register', '--input-stdin']), \
             patch.object(sys, 'stdin', io.StringIO(json.dumps(data))), \
             patch.object(sys, 'stdout', io.StringIO()) as output:
            config.return_value.preflight.return_value = None
            config.return_value.save.return_value = None
            self.assertEqual(account.main(config_factory=account.CodexConfig), 0)
            self.assertEqual(json.loads(output.getvalue())['status'], 'configuration_saved')
        body = next(c[2] for c in api.calls if c[1] == '/api/auth/login')
        self.assertEqual(body['sourceCode'], SOURCE)
        self.assertNotIn('source', body)
        guidance = account.prepare(FakeAPI())['guidance']
        urls = re.findall(r'https://[^\s)]+', guidance)
        sources = [parse_qs(urlsplit(u).query)['source'][0] for u in urls
                   if 'source' in parse_qs(urlsplit(u).query)]
        self.assertEqual(sources, [body['sourceCode']])
        self.assertIn('https://ai.qianlima.com/?source=' + SOURCE, guidance)
        production = '\n'.join(AUTH_ERROR_RULES['10001']['next_steps'])
        self.assertIn('https://ai.qianlima.com/?source=' + SOURCE, production)

    def test_guidance_keeps_approved_copy_weight_and_source_in_every_variant(self):
        expected_guidance = (
            '**千里马AI 数据平台**\\\n'
            '让你的AI 即刻拥有4.5 亿+招投标数据，注册即赠 500 积分\n\n'
            '**注册流程：**\\\n'
            '① 回复 11 位手机号 → ② 输入短信验证码 → ③ 自动获取并配置 API Key\n\n'
            '[前往官网](https://ai.qianlima.com/?source=' + SOURCE + ')'
            '  · 已有 API Key 可直接在会话提供'
        )
        self.assertEqual(AUTH_ERROR_RULES['MISSING_API_KEY']['next_steps'],
                         [expected_guidance])
        for pending_query in (True, False):
            for has_key in (True, False):
                with self.subTest(pending_query=pending_query, has_key=has_key):
                    api = FakeAPI()
                    guidance = account.prepare(api, pending_query=pending_query,
                                               has_key=has_key)['guidance']
                    self.assertEqual(guidance, expected_guidance)
                    self.assertNotIn('```', guidance)
                    self.assertNotIn('\n>', guidance)
                    links = re.findall(r'\[([^\]]+)\]\((https://[^)]+)\)', guidance)
                    self.assertEqual(len(links), 1)
                    self.assertEqual({label for label, _ in links}, {'前往官网'})
                    for label, url in links:
                        parsed = urlsplit(url)
                        self.assertEqual((parsed.scheme, parsed.netloc, parsed.path),
                                         ('https', 'ai.qianlima.com', '/'))
                        query = {'source': [SOURCE]}
                        self.assertEqual(parse_qs(parsed.query), query)
                        self.assertEqual(parsed.fragment, '')
                    self.assertEqual(api.calls, [])

    def test_skill_entry_is_a_markdown_link_to_package_source(self):
        text = (Path(__file__).resolve().parents[1] / 'SKILL.md').read_text()
        links = re.findall(r'\[([^\]]+)\]\((https://ai\.qianlima\.com/[^)]*)\)', text)
        self.assertEqual(len(links), 1)
        label, url = links[0]
        # Account-access allows a Chinese site name; the complete target and source remain mandatory.
        self.assertTrue(label.strip())
        urls = [url]
        self.assertEqual(len(urls), 1)
        self.assertEqual(parse_qs(urlsplit(urls[0]).query), {'source': [SOURCE]})
        self.assertNotIn('`https://ai.qianlima.com/', text)

    def test_send_does_not_propagate_source(self):
        api = FakeAPI()
        result = account.register(inputs(sourceCode='external', source='external'), api)
        self.assertEqual(result['status'], 'sms_sent')
        self.assertEqual(api.calls[-1], ('POST', '/api/auth/sms/send',
                                       {'phone': '19900000001'}, None))
        self.assertEqual(len(api.calls), 1)

    def test_login_failure_keeps_source_without_retry_or_write(self):
        api, config = LoginAPI(), FakeConfig()
        api.fail['/api/auth/login'] = account.AccountError('request_failed')
        result = account.register(inputs(action='verify', smsCode='012345'), api, config)
        self.assertEqual(result['status'], 'request_failed')
        self.assertEqual(config.writes, 0)
        self.assertEqual(len(api.calls), 3)
        self.assertEqual(api.calls[-1][2]['sourceCode'], SOURCE)


if __name__ == '__main__':
    unittest.main()
