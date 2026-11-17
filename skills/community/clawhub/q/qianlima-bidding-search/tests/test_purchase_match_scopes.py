"""Purchase scopes: real CLI/HTTP boundary, synthetic credentials, no network."""
import contextlib
import copy
import io
import itertools
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlparse
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as r

ALLOWED = [1, 2, 8, 10]
INVALID = [[n] for n in (0, 3, 4, 5, 6, 7, 9, 11, -1)] + [
    [], None, [None], [2, None], [2, 9], [True], [False], [2.5],
    {}, [[2]],
]
COMPATIBLE_INPUTS = [2, '2', ['2'], [2.0]]
HISTORY = json.loads((Path(__file__).parent / 'fixtures' / 'purchase_match_scopes_history.json').read_text())
QUERY = {'keywords': ['物业'], 'startPlanPurchaseDate': '2026-11',
         'endPlanPurchaseDate': '2027-01', 'areaIds': [2],
         'excludeWords': ['电梯'], 'currentPage': 1, 'numPerPage': 2}
PATH = '/api/search/purchase'


class PurchaseMatchScopesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / 'state'
        env = patch.dict(os.environ, {
            'QIANLIMA_API_KEY': 'synthetic-offline-key',
            'QIANLIMA_SKILL_STATE_DIR': str(self.state),
            'QIANLIMA_MOCK_DIR': '', 'QIANLIMA_SKILL_SESSION_ID': '',
        })
        env.start()
        self.addCleanup(env.stop)
        network = patch('socket.socket', side_effect=AssertionError('External network forbidden'))
        network.start()
        self.addCleanup(network.stop)

    def call(self, argv, response=None):
        calls = []
        def receive(request, **kwargs):
            calls.append({'path': urlparse(request.full_url).path,
                          'query': json.loads(request.data) if request.data else None})
            body = response if response is not None else {
                'code': 200, 'msg': '合成成功', 'success': True,
                'data': {'rowCount': 4, 'pageCount': 2, 'list': [
                    {'id': 201, 'title': '合成采购意向', 'url': 'https://example.invalid/201'}]}}
            return io.BytesIO(json.dumps(body).encode())
        output = io.StringIO()
        with patch('urllib.request.urlopen', receive), contextlib.redirect_stdout(output):
            r.main(['--base-url', 'https://offline.invalid', *argv])
        return json.loads(output.getvalue()), calls

    def search(self, query):
        return self.call(['search-purchase', '--query-json', json.dumps(query)])

    def seed(self, scopes):
        return r.save_search_snapshot(
            session_id=str(uuid.uuid4()), result_type='purchase_intention',
            effective_query={**QUERY, 'matchScopes': scopes},
            viewed_cards=[{'id': 201, 'title': '合成采购意向'}], total_count=4, page_count=2)

    def ref(self, snapshot):
        return ['--session-id', snapshot['session_id'], '--result-set-id', snapshot['result_set_id']]

    def assert_blocked(self, result, calls):
        self.assertFalse(result['ok'], result)
        self.assertEqual(calls, [], 'Invalid query must not reach HTTP or entitlement diagnosis')

    def test_all_15_nonempty_scope_combinations_reach_http_unchanged(self):
        for size in range(1, 5):
            for values in itertools.combinations(ALLOWED, size):
                with self.subTest(scopes=values):
                    result, calls = self.search({**QUERY, 'matchScopes': list(values)})
                    self.assertTrue(result['ok'], result)
                    self.assertEqual(calls, [{'path': PATH, 'query': {**QUERY, 'matchScopes': list(values)}}])
                    self.assertEqual(result['effective_query']['matchScopes'], list(values))

    def test_omission_uses_api_default_without_inserting_all_scope(self):
        result, calls = self.search(QUERY)
        self.assertTrue(result['ok'], result)
        self.assertNotIn('matchScopes', calls[0]['query'])
        self.assertNotIn('matchScopes', result['effective_query'])

    def test_invalid_values_fail_before_http_and_do_not_create_state(self):
        for scopes in INVALID:
            with self.subTest(scopes=scopes):
                result, calls = self.search({**QUERY, 'matchScopes': scopes})
                self.assert_blocked(result, calls)
                self.assertEqual(result['error_code'], 'AGENT_QUERY_CORRECTION_REQUIRED')
        self.assertFalse(list(self.state.rglob('*.json')))

    def test_compatible_inputs_normalize_before_http(self):
        for scopes in COMPATIBLE_INPUTS:
            with self.subTest(scopes=scopes):
                result, calls = self.search({**QUERY, 'matchScopes': scopes})
                self.assertTrue(result['ok'], result)
                self.assertEqual(calls, [{'path': PATH, 'query': {**QUERY, 'matchScopes': [2]}}])
                self.assertEqual(result['effective_query']['matchScopes'], [2])

    def test_transport_guard_cannot_be_bypassed(self):
        # The transport receives normalized arrays, never permissive raw CLI input.
        for scopes in INVALID + COMPATIBLE_INPUTS:
            with self.subTest(scopes=scopes), self.assertRaises(r.SkillError):
                r.validate_endpoint_request('POST', PATH, {**QUERY, 'matchScopes': scopes})

    def test_next_and_refine_preserve_filters_and_use_purchase_endpoint(self):
        initial, _ = self.search({**QUERY, 'matchScopes': [2, 8, 10]})
        follow = initial['follow_up']
        next_result, calls = self.call(['next', *self.ref(follow)])
        self.assertTrue(next_result['ok'], next_result)
        self.assertEqual(calls, [{'path': PATH, 'query': {**QUERY, 'matchScopes': [2, 8, 10], 'currentPage': 2}}])
        result, calls = self.call(['refine', *self.ref(next_result['follow_up']),
                                   '--query-json', json.dumps({'matchScopes': [10]})])
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls, [{'path': PATH, 'query': {**QUERY, 'matchScopes': [10]}}])

    def test_invalid_refine_leaves_original_snapshot_unchanged(self):
        snapshot = self.seed([2])
        before = copy.deepcopy(r.load_snapshot(snapshot['session_id'], snapshot['result_set_id']))
        for scopes in INVALID:
            with self.subTest(scopes=scopes):
                result, calls = self.call(['refine', *self.ref(snapshot), '--query-json', json.dumps({'matchScopes': scopes})])
                self.assert_blocked(result, calls)
                self.assertEqual(r.load_snapshot(snapshot['session_id'], snapshot['result_set_id']), before)

    def test_historical_invalid_snapshot_cannot_be_replayed_or_silently_widened(self):
        snapshot = self.seed([2, 9])
        for command in ('next', 'refine'):
            args = [command, *self.ref(snapshot)]
            if command == 'refine':
                args += ['--query-json', json.dumps({'keywords': ['设备']})]
            result, calls = self.call(args)
            self.assert_blocked(result, calls)
        # Explicit repair is permitted; there is no automatic substitution.
        result, calls = self.call(['refine', *self.ref(snapshot), '--query-json', '{"matchScopes":[2,8]}'])
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls[0]['query']['matchScopes'], [2, 8])

    def assert_historical_scenario(self, scenario_id):
        matches = [case for case in HISTORY['scenarios'] if case['id'] == scenario_id]
        self.assertEqual(len(matches), 1, 'One regression case per distinct historical query')
        case = matches[0]
        original = copy.deepcopy(case['query'])
        self.assertEqual(original['matchScopes'], [2, 9])
        result, calls = self.search(original)
        self.assert_blocked(result, calls)
        self.assertEqual(result['error_code'], 'AGENT_QUERY_CORRECTION_REQUIRED')
        self.assertFalse(list(self.state.rglob('*.json')))
        self.assertEqual(original, case['query'], 'Invalid query must not be silently rewritten')

        # A deliberate test choice, NOT a 9 -> 8 automatic or semantic mapping.
        selected_query = {**copy.deepcopy(original), 'matchScopes': [2, 8]}
        result, calls = self.search(selected_query)
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls, [{'path': case['path'], 'query': selected_query}])
        self.assertEqual(result['effective_query'], selected_query)
        for key, value in original.items():
            if key != 'matchScopes':
                self.assertEqual(calls[0]['query'][key], value, key)
        return result, calls

    def test_history_obs_267_01_endoscopes_two_publication_days(self):
        self.assert_historical_scenario('OBS-267-01')

    def test_history_obs_267_02_operating_room_two_publication_days(self):
        self.assert_historical_scenario('OBS-267-02')

    def test_history_obs_267_03_operating_room_with_purchase_months(self):
        self.assert_historical_scenario('OBS-267-03')

    def test_full_context_recovery_validates_scope(self):
        for scopes in ([2, 8], [3], [2, 9]):
            context = {'result_type': 'purchase_intention', 'effective_query': {**QUERY, 'matchScopes': scopes}}
            result, calls = self.call(['next', '--context-json', json.dumps(context)])
            if scopes == [2, 8]:
                self.assertTrue(result['ok'], result)
                self.assertEqual(calls[0]['query'], {**QUERY, 'matchScopes': scopes, 'currentPage': 2})
            else:
                self.assert_blocked(result, calls)

    def test_preflight_uses_real_runtime_contract_and_no_scope_fallback(self):
        for scope in range(1, 11):
            plan = {'conditions': [
                {'id': 'kw', 'type': 'keyword', 'value': ['物业']},
                {'id': 'scope', 'type': 'match_scope', 'value': [scope]}],
                'operations': [{'id': 'purchase', 'action': 'search', 'data_source': 'purchase_intention'}]}
            result, calls = self.call(['preflight-complex', '--plan-json', json.dumps(plan)])
            self.assertEqual(calls, [])
            if scope in ALLOWED:
                self.assertTrue(result['ok'], result)
                self.assertEqual(result['approved_operations'][0]['query']['matchScopes'], [scope])
            else:
                self.assertFalse(result['ok'], result)
                self.assertEqual(result['approved_operations'], [])
                self.assertEqual(result['approved_business_calls'], 0)

    def test_other_sources_keep_all_10_scopes(self):
        scopes = list(range(1, 11))
        for command, query, path in (
            ('search', {'keywordGroups': [{'keywords': ['物业'], 'matchScopes': scopes}]}, '/api/search'),
            ('search-expiring', {'keywords': ['物业'], 'matchScopes': scopes}, '/api/search/expiring')):
            result, calls = self.call([command, '--query-json', json.dumps(query)])
            self.assertTrue(result['ok'], result)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]['path'], path)
            sent = calls[0]['query']
            self.assertEqual(sent.get('matchScopes', sent.get('keywordGroups', [{}])[0].get('matchScopes')), scopes)

    def test_multisource_preflight_blocks_only_invalid_purchase_branch(self):
        plan = {'conditions': [
            {'id': 'kw', 'type': 'keyword', 'value': ['物业']},
            {'id': 'scope', 'type': 'match_scope', 'value': [9]}],
            'operations': [{'id': source, 'action': 'search', 'data_source': source}
                           for source in ('project', 'purchase_intention', 'expiring_project')]}
        result, calls = self.call(['preflight-complex', '--plan-json', json.dumps(plan)])
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls, [])
        self.assertEqual([op['data_source'] for op in result['approved_operations']], ['project', 'expiring_project'])
        self.assertTrue(any(item.get('operation_id') == 'purchase_intention' for item in result['unresolved_conditions']))

    def test_preflight_refine_validates_merged_scope(self):
        snapshot = self.seed([2])
        operation = {'session_id': snapshot['session_id'], 'result_set_id': snapshot['result_set_id']}
        for scopes in ([3], [9], [2, 9], [], [None]):
            with self.subTest(scopes=scopes), self.assertRaises(r.SkillError):
                r.normalize_complex_operation('purchase_intention', 'refine', {'matchScopes': scopes}, operation)
        approved, _ = r.normalize_complex_operation('purchase_intention', 'refine', {'matchScopes': [8, 10]}, operation)
        result, calls = self.call(['refine', *self.ref(snapshot), '--query-json', json.dumps(approved)])
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls[0]['query'], {**QUERY, 'matchScopes': [8, 10]})

    def test_unsupported_semantic_positions_do_not_turn_into_general_search(self):
        for kind, value in [('project_id', 'QLM-2026-001'),
                            ('organization_role', {'role': 'purchasing_unit', 'keywords': ['某医院']})]:
            plan = {'conditions': [{'id': 'position', 'type': kind, 'value': value}],
                    'operations': [{'id': 'purchase', 'action': 'search', 'data_source': 'purchase_intention'}]}
            result, calls = self.call(['preflight-complex', '--plan-json', json.dumps(plan)])
            self.assert_blocked(result, calls)
            self.assertEqual(result['approved_operations'], [])

    def test_valid_scope_order_duplicates_and_zero_results_are_preserved(self):
        query = {**QUERY, 'matchScopes': [10, 2, 2]}
        response = {'code': 200, 'success': True, 'msg': '成功',
                    'data': {'rowCount': 0, 'pageCount': 0, 'list': []}}
        result, calls = self.call(['search-purchase', '--query-json', json.dumps(query)], response)
        self.assertTrue(result['ok'], result)
        self.assertEqual(calls, [{'path': PATH, 'query': query}])
        self.assertEqual(result['api_responses'][0]['response'], response)

    def test_api_errors_preserved_once_without_retry_or_entitlement_lookup(self):
        # Synthetic failures: not claimed to be the historical admin responses.
        for code in (10004, 500):
            response = {'code': code, 'msg': '合成错误', 'data': None, 'success': False}
            result, calls = self.call(['search-purchase', '--query-json', json.dumps(QUERY)], response)
            self.assertFalse(result['ok'], result)
            self.assertEqual(len(calls), 1)
            self.assertEqual(result['api_responses'][0]['response'], response)


if __name__ == '__main__':
    unittest.main()
