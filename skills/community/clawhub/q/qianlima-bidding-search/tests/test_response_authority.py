"""Exercise real transport decoding and command output without external calls."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('authority_runtime', ROOT/'scripts/qianlima_skill.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

def data(name):
    return json.loads((ROOT/'tests/fixtures'/f'{name}.json').read_text())['data']

QUERY = {'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2]}]}

class ResponseAuthorityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        env = patch.dict(os.environ, {'QIANLIMA_SKILL_STATE_DIR': temp.name, 'QIANLIMA_API_KEY': 'offline-dummy', 'QIANLIMA_MOCK_DIR': ''})
        env.start(); self.addCleanup(env.stop)
        seed, _ = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': data('search_page_1')})
        self.context = ['--session-id', seed['follow_up']['session_id'], '--result-set-id', seed['follow_up']['result_set_id'], '--project-ref', '第1条']

    def call(self, argv, routes, envelopes=False):
        calls = []
        def receive(req, **kwargs):
            path = urlparse(req.full_url).path
            calls.append(path)
            if path not in routes:
                raise AssertionError('Unexpected extra request: ' + path)
            payload = routes[path] if envelopes else {'code': 200, 'msg': '成功', 'data': routes[path], 'extraEnvelopeField': False}
            return io.BytesIO(json.dumps(payload, ensure_ascii=False).encode())
        out = io.StringIO()
        with patch('urllib.request.urlopen', receive), patch('socket.socket', side_effect=AssertionError('Network forbidden')), contextlib.redirect_stdout(out):
            r.main(['--base-url', 'https://offline.invalid', *argv])
        return json.loads(out.getvalue()), calls

    def assert_raw(self, out, path, value):
        self.assertTrue(out['ok'], out)
        self.assertEqual(out['api_responses'][0]['path'], path)
        self.assertEqual(out['api_responses'][0]['response'], {'code': 200, 'msg': '成功', 'data': value, 'extraEnvelopeField': False})

    def test_unrequested_detail_fields_never_reject_success(self):
        for fields in [{'biddingCandidates': None}, {'zhaoBiaoType': ''}, {'xmNumber': 123}, {'id': 999}, {'threeLevelClassification': '设备'}, {'newField': {'values': [0, False, None]}}]:
            value = {**data('detail_101'), **fields}
            with self.subTest(fields=fields):
                out, calls = self.call(['detail', *self.context, '--fields', 'title'], {'/api/detail/101': value})
                self.assert_raw(out, '/api/detail/101', value)
                self.assertEqual(calls, ['/api/detail/101'])

    def test_empty_or_unusual_resource_data_remains_successful(self):
        for command, path, values in [('full-text', '/api/fullText/101', [None, {'projectId': 999, 'content': ''}]), ('attachments', '/api/attachments/101', [None, [], [{**data('attachments_101')[0], 'fileSize': '125.5', 'new': None}]]), ('timeline', '/api/timeline/101', [None, [], [None]])]:
            for value in values:
                with self.subTest(command=command, value=value):
                    out, calls = self.call([command, *self.context], {path: value})
                    self.assert_raw(out, path, value)
                    self.assertEqual(calls, [path])

    def test_attachment_size_uses_api_value_without_inventing_numeric_kb(self):
        original = data('attachments_101')[0]
        for size, expected in [(125.5, '125.5 KB'), ('125.5', '125.5 KB'), (0, '0 KB'), (None, '大小未公示')]:
            with self.subTest(size=size):
                value = [{**original, 'fileSize': size}]
                out, calls = self.call(['attachments', *self.context], {'/api/attachments/101': value})
                self.assert_raw(out, '/api/attachments/101', value)
                self.assertIn(expected, out['user_message'])
                self.assertEqual(calls, ['/api/attachments/101'])
        for size in [True, False, {'value': 12}, [12]]:
            with self.subTest(size=size):
                value = [{**original, 'fileSize': size}]
                out, calls = self.call(['attachments', *self.context], {'/api/attachments/101': value})
                self.assert_raw(out, '/api/attachments/101', value)
                self.assertNotIn('KB', out['user_message'])
                self.assertEqual(calls, ['/api/attachments/101'])

    def test_enterprise_without_api_total_reports_only_returned_batch(self):
        value = {'list': []}
        out, calls = self.call(
            ['enterprise', '--kind', 'partners', '--query-json', '{"companyName":"测试有限公司"}'],
            {'/api/enterprise/partners': value},
        )
        self.assert_raw(out, '/api/enterprise/partners', value)
        self.assertIsNone(out['total_count'])
        self.assertEqual(out['returned_count'], 0)
        self.assertEqual(calls, ['/api/enterprise/partners'])

    def test_explicit_project_dates_stay_fixed_on_next_page(self):
        dated_query = {**QUERY, 'beginTime': '2026-08-21', 'endTime': '2026-09-21'}
        first, first_calls = self.call(
            ['search', '--query-json', json.dumps(dated_query)],
            {'/api/search': data('search_page_1')},
        )
        self.assert_raw(first, '/api/search', data('search_page_1'))
        self.assertEqual(first_calls, ['/api/search'])
        context = ['--session-id', first['follow_up']['session_id'], '--result-set-id', first['follow_up']['result_set_id']]
        second, second_calls = self.call(['next', *context], {'/api/search': data('search_page_2')})
        self.assert_raw(second, '/api/search', data('search_page_2'))
        self.assertEqual(second_calls, ['/api/search'])
        for result in (first, second):
            self.assertEqual(result['request_query'].get('beginTime'), '2026-08-21 00:00:00')
            self.assertEqual(result['request_query'].get('endTime'), '2026-09-21 23:59:59')
        self.assertEqual(second['request_query']['currentPage'], 2)

    def test_redirect_does_not_forward_api_key_to_other_host(self):
        captured = []
        def receive(req, **kwargs):
            captured.append(req)
            return io.BytesIO(json.dumps({'code': 200, 'data': {}}).encode())
        client = r.ApiClient('https://original.invalid', 'synthetic-key')
        with patch('urllib.request.urlopen', receive):
            client._request('GET', '/api/user/verify')
        original = captured[0]
        redirected = urllib.request.HTTPRedirectHandler().redirect_request(
            original, io.BytesIO(), 302, 'Found', {}, 'https://other.invalid/elsewhere'
        )
        self.assertEqual(dict(original.header_items()).get('Qianlimaapikey'), 'synthetic-key')
        self.assertNotIn('Qianlimaapikey', dict(redirected.header_items()))

    def test_search_rows_counts_and_new_fields_are_preserved(self):
        for command, path in [('search', '/api/search'), ('search-purchase', '/api/search/purchase'), ('search-expiring', '/api/search/expiring')]:
            query = QUERY if command == 'search' else {'keywords': ['设备']}
            for value in [None, {}, {'rowCount': '2', 'pageCount': None, 'list': [None, {'id': 101, 'title': '设备', 'hasAnnex': 1, 'new': '保留'}]}]:
                with self.subTest(command=command, value=value):
                    out, calls = self.call([command, '--query-json', json.dumps(query)], {path: value})
                    self.assert_raw(out, path, value)
                    self.assertEqual(calls, [path])

    def test_other_apis_preserve_success_and_unknown_fields(self):
        cases = [(['verify'], '/api/user/verify'), (['entitlement'], '/api/user/entitlement'), (['search-company', '--query-json', '{"companyName":"测试"}'], '/api/searchCompany'), (['enterprise', '--kind', 'partners', '--query-json', '{"companyName":"测试有限公司"}'], '/api/enterprise/partners'), (['detail', *self.context, '--fields', 'sourceUrl'], '/api/sourceUrl/101')]
        for argv, path in cases:
            for value in [None, {}, {'newField': [False, None, '']}]:
                with self.subTest(argv=argv, value=value):
                    out, calls = self.call(argv, {path: value})
                    self.assert_raw(out, path, value)
                    self.assertEqual(calls, [path])

    def test_empty_fields_are_undisclosed_not_missing(self):
        value = {**data('detail_101'), 'purchasingUnitLinkPhone': None, 'zhaoBiaoType': '', 'biddingCandidates': None}
        out, _ = self.call(['detail', *self.context, '--fields', 'purchasingUnitLinkPhone,zhaoBiaoType,biddingCandidates'], {'/api/detail/101': value})
        self.assert_raw(out, '/api/detail/101', value)
        self.assertIn('未公示', out['user_message'])
        self.assertNotIn('未返回', out['user_message'])
        self.assertNotIn('接口未提供', out['user_message'])

    def test_api_failure_preserves_envelope_data_and_status(self):
        response = {'code': 10005, 'msg': '项目不存在', 'data': {'newField': '保留'}, 'success': False}
        out, calls = self.call(['detail', *self.context], {'/api/detail/101': response}, envelopes=True)
        self.assertFalse(out['ok'])
        self.assertEqual(out['error_code'], '10005')
        self.assertEqual(out['api_responses'][0]['response'], response)
        self.assertEqual(calls, ['/api/detail/101'])

    def test_local_save_failure_keeps_received_success(self):
        value = data('search_page_1')
        with patch.object(r, 'save_search_snapshot', side_effect=OSError('disk unavailable')):
            out, calls = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': value})
        self.assert_raw(out, '/api/search', value)
        self.assertEqual(calls, ['/api/search'])
        self.assertNotIn('follow_up', out)

    def test_response_context_does_not_leak_into_later_command(self):
        self.call(['detail', *self.context], {'/api/detail/101': data('detail_101')})
        out, calls = self.call(['search', '--query-json', '{}'], {})
        self.assertFalse(out['ok'])
        self.assertEqual(calls, [])
        self.assertNotIn('api_responses', out)

    def test_partial_resources_keep_each_api_outcome(self):
        routes = {'/api/detail/101': {'code': 200, 'data': data('detail_101')}, '/api/sourceUrl/101': {'code': 10011, 'msg': '原文不存在', 'data': None}}
        out, calls = self.call(['detail', *self.context, '--fields', 'title,sourceUrl'], routes, envelopes=True)
        self.assertFalse(out['ok'])
        self.assertTrue(out['partial_success'])
        self.assertEqual([item['response']['code'] for item in out['api_responses']], [200, 10011])
        self.assertEqual(calls, list(routes))

    def test_transport_failure_after_detail_does_not_become_full_success(self):
        calls = []
        def receive(req, **kwargs):
            path = urlparse(req.full_url).path
            calls.append(path)
            if path == '/api/detail/101':
                return io.BytesIO(json.dumps({'code': 200, 'data': data('detail_101')}).encode())
            raise urllib.error.URLError('offline')
        output = io.StringIO()
        with patch('urllib.request.urlopen', receive), contextlib.redirect_stdout(output):
            r.main(['detail', *self.context, '--fields', 'title,sourceUrl'])
        out = json.loads(output.getvalue())
        self.assertFalse(out['ok'])
        self.assertTrue(out['partial_success'])
        self.assertEqual(out['api_responses'][0]['response']['code'], 200)
        self.assertEqual(out['api_responses'][1]['transport_error']['code'], 'NETWORK_ERROR')
        self.assertEqual(len(calls), 2)

    def test_unknown_count_never_becomes_zero_or_claims_safe_paging(self):
        value = {**data('search_page_1'), 'rowCount': None, 'pageCount': None}
        out, _ = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': value})
        self.assert_raw(out, '/api/search', value)
        self.assertIsNone(out.get('total_count'))
        self.assertNotIn('next', out.get('follow_up', {}).get('allowed_actions', []))

    def test_unknown_fields_survive_cards_and_full_detail(self):
        value = {**data('detail_101'), 'newField': False}
        out, _ = self.call(['detail', *self.context], {'/api/detail/101': value})
        self.assertEqual(out['full_detail'], value)
        value = data('search_page_1'); value['list'][0]['newField'] = None
        out, _ = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': value})
        self.assertEqual(out['cards'], value['list'])

    def test_followup_search_commands_preserve_changed_shapes(self):
        context = self.context[:4]
        for argv in [['next', *context], ['refine', *context, '--query-json', '{"numPerPage":2}']]:
            value = {'rowCount': None, 'pageCount': '2', 'list': [None], 'new': False}
            out, calls = self.call(argv, {'/api/search': value})
            self.assert_raw(out, '/api/search', value)
            self.assertEqual(calls, ['/api/search'])

    def test_other_source_details_and_all_enterprise_routes(self):
        for command, path, fixture, detail_path in [('search-purchase', '/api/search/purchase', 'search_purchase_page_1', '/api/purchase/detail/201'), ('search-expiring', '/api/search/expiring', 'search_expiring_page_1', '/api/expiring/detail/301')]:
            seed, _ = self.call([command, '--query-json', '{"keywords":["设备"]}'], {path: data(fixture)})
            context = ['--session-id', seed['follow_up']['session_id'], '--result-set-id', seed['follow_up']['result_set_id'], '--project-ref', '第1条']
            out, calls = self.call(['detail', *context], {detail_path: {'id': None, 'biddingCandidates': None, 'new': 0}})
            self.assert_raw(out, detail_path, {'id': None, 'biddingCandidates': None, 'new': 0})
            self.assertEqual(calls, [detail_path])
        for kind, endpoint in [('partners', 'partners'), ('principals', 'principals'), ('area-distribution', 'areaDistribution'), ('winning-area-distribution', 'winningAreaDistribution'), ('co-bidder-competitors', 'coBidderCompetitors'), ('potential-competitors', 'potentialCompetitors'), ('business-info', 'businessInfo'), ('contacts', 'contacts')]:
            path = '/api/enterprise/' + endpoint
            out, calls = self.call(['enterprise', '--kind', kind, '--query-json', '{"companyName":"测试有限公司"}'], {path: None})
            self.assert_raw(out, path, None)
            self.assertEqual(calls, [path])

    def test_wallet_diagnosis_does_not_override_api_failure(self):
        routes = {'/api/detail/101': {'code': 10028, 'msg': '地区权限不足', 'data': {'new': None}}, '/api/user/entitlement': {'code': 200, 'data': None}}
        out, calls = self.call(['detail', *self.context], routes, envelopes=True)
        self.assertFalse(out['ok'])
        self.assertEqual(out['error_code'], '10028')
        self.assertEqual(out['api_responses'][0]['response'], routes['/api/detail/101'])
        self.assertEqual(calls, list(routes))

    def test_mock_and_transport_share_response_semantics(self):
        response = {'code': 200, 'data': {'username': '', 'new': [None, 0, False]}}
        real, _ = self.call(['verify'], {'/api/user/verify': response}, envelopes=True)
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'verify.json').write_text(json.dumps(response))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                r.main(['--mock-dir', folder, 'verify'])
            mocked = json.loads(output.getvalue())
        self.assertEqual(real, mocked)

    def test_bad_json_is_transport_issue_not_api_business_failure(self):
        output = io.StringIO()
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'not json')), contextlib.redirect_stdout(output):
            r.main(['verify'])
        out = json.loads(output.getvalue())
        self.assertFalse(out['ok'])
        self.assertEqual(out['api_responses'][0]['transport_error']['code'], 'API_RESPONSE_UNREADABLE')
        self.assertNotIn('response', out['api_responses'][0])

    def test_missing_url_and_empty_candidate_fields_are_undisclosed(self):
        value = {**data('detail_101'), 'url': None, 'biddingCandidates': None}
        out, _ = self.call(['detail', *self.context, '--fields', 'url,biddingCandidates'], {'/api/detail/101': value})
        self.assertTrue(out['ok'])
        self.assertNotIn('未提供', out['user_message'])
        self.assertNotIn('未返回', out['user_message'])
        self.assertIn('未公示', out['user_message'])

    def test_zero_and_false_are_not_rendered_as_undisclosed(self):
        self.assertNotEqual(r.clean_user_value(0), '未公示')
        self.assertNotEqual(r.clean_user_value(False), '未公示')
        self.assertNotEqual(r.detail_display_value('biddingCandidates', False), '未公示')

    def test_null_project_id_does_not_advertise_detail_action(self):
        value = data('search_page_1'); value['list'][0]['id'] = None
        out, _ = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': value})
        self.assert_raw(out, '/api/search', value)
        self.assertNotIn('detail', out.get('follow_up', {}).get('allowed_actions', []))

    def test_company_null_counts_are_undisclosed_and_wrong_page_cannot_continue(self):
        value = data('searchCompany_page_1')
        value['currentPage'] = 9
        value['list'][0]['winningCount'] = None
        out, _ = self.call(['search-company', '--query-json', '{"companyName":"测试","pageSize":1}'], {'/api/searchCompany': value})
        self.assert_raw(out, '/api/searchCompany', value)
        self.assertNotIn('None', out['user_message'])
        self.assertIn('中标 未公示', out['user_message'])
        self.assertNotIn('search-company --next', out.get('follow_up', {}).get('allowed_actions', []))

    def test_null_list_is_not_zero_results(self):
        for command, path, query in [('search', '/api/search', QUERY), ('search-purchase', '/api/search/purchase', {'keywords': ['设备']}), ('search-expiring', '/api/search/expiring', {'keywords': ['设备']})]:
            value = {'rowCount': 2, 'pageCount': 1, 'list': None}
            out, _ = self.call([command, '--query-json', json.dumps(query)], {path: value})
            self.assert_raw(out, path, value)
            self.assertNotIn('没查到', out['user_message'])
            self.assertIn('未公示', out['user_message'])
            self.assertNotIn('follow_up', out)
            self.assertIsNone(out['cards'])

    def test_missing_id_followup_stops_before_network_but_preserves_original_success(self):
        value = data('search_page_1'); value['list'][0]['id'] = None
        first, _ = self.call(['search', '--query-json', json.dumps(QUERY)], {'/api/search': value})
        context = ['--session-id', first['follow_up']['session_id'], '--result-set-id', first['follow_up']['result_set_id'], '--project-ref', '第1条']
        for command in ['detail', 'full-text', 'attachments', 'timeline']:
            out, calls = self.call([command, *context], {})
            self.assertEqual(calls, [])
            self.assertEqual(out['error_code'], 'FOLLOW_UP_UNAVAILABLE')
        self.assert_raw(first, '/api/search', value)

    def test_candidate_null_rank_is_undisclosed(self):
        display = r.detail_display_value('biddingCandidates', [{'ranking': None, 'providerName': None, 'amount': None}])
        self.assertNotIn('None', display)
        self.assertIn('未公示', display)

    def test_failed_detail_does_not_prevent_requested_source_url(self):
        routes = {'/api/detail/101': {'code': 10005, 'msg': '详情不存在', 'data': None}, '/api/sourceUrl/101': {'code': 200, 'data': {'sourceUrl': 'https://example.invalid/source'}}}
        out, calls = self.call(['detail', *self.context, '--fields', 'title,sourceUrl'], routes, envelopes=True)
        self.assertFalse(out['ok'])
        self.assertTrue(out['partial_success'])
        self.assertEqual(calls, list(routes))
        self.assertIn('https://example.invalid/source', out['user_message'])
        self.assertEqual(out['successful_resources'], ['sourceUrl'])

    def test_empty_wallet_diagnosis_does_not_interrupt_remaining_resource(self):
        routes = {'/api/detail/101': {'code': 10028, 'msg': '地区权限不足', 'data': None}, '/api/user/entitlement': {'code': 200, 'data': None}, '/api/sourceUrl/101': {'code': 200, 'data': {'sourceUrl': 'https://example.invalid/source'}}}
        out, calls = self.call(['detail', *self.context, '--fields', 'title,sourceUrl'], routes, envelopes=True)
        self.assertEqual(calls, list(routes))
        self.assertFalse(out['ok'])
        self.assertEqual(out['error_code'], '10028')
        self.assertTrue(out['partial_success'])
        self.assertIn('https://example.invalid/source', out['user_message'])
        self.assertIn('未公示', out['user_message'])

if __name__ == '__main__':
    unittest.main()
