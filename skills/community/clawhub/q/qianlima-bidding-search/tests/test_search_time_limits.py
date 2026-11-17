"""Calendar-span limits are enforced before requests, including continuations."""
import copy
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as r
from complex_query_plan import preflight_complex_plan


class SearchTimeLimitTests(unittest.TestCase):
    # source, command, path, begin/end, maximum years, semantic condition
    cases = [
        ('project', 'search', '/api/search', 'beginTime', 'endTime', 3, 'publish_time'),
        ('expiring_project', 'search-expiring', '/api/search/expiring',
         'beginServiceExpireTime', 'endServiceExpireTime', 5, 'service_expiry'),
        ('purchase_intention', 'search-purchase', '/api/search/purchase', 'beginTime', 'endTime', 3, 'publish_time'),
        ('purchase_intention', 'search-purchase', '/api/search/purchase',
         'startPlanPurchaseDate', 'endPlanPurchaseDate', 3, 'planned_purchase_date'),
    ]

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        env = patch.dict(os.environ, {'QIANLIMA_SKILL_STATE_DIR': tmp.name, 'QIANLIMA_API_KEY': 'test-only'})
        env.start(); self.addCleanup(env.stop)
        network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Offline test must not access network'))
        network.start(); self.addCleanup(network.stop)

    def date_value(self, case, value):
        return value[:7] if case[6] == 'planned_purchase_date' else value

    def query(self, case, start=None, end=None):
        source, _, _, begin_field, end_field, _, _ = case
        query = {'currentPage': 1, 'numPerPage': 5, 'areaIds': [3320], 'excludeWords': ['维修']}
        query.update({'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 9]}]}
                     if source == 'project' else {'keywords': ['设备']})
        if start is not None:
            query[begin_field] = self.date_value(case, start)
        if end is not None:
            query[end_field] = self.date_value(case, end)
        return query

    def normalize(self, case, query):
        return r.SEARCH_CAPABILITIES[case[0]].normalize_query(query)[0]

    def command(self, argv):
        output = io.StringIO()
        with redirect_stdout(output):
            r.main(argv)
        return json.loads(output.getvalue())

    def rejected(self, callback, code='TIME_SPAN_EXCEEDED'):
        with self.assertRaises(r.SkillError) as caught:
            callback()
        self.assertEqual(caught.exception.code, code)

    def test_calendar_boundaries_and_leap_day(self):
        for case in self.cases:
            if case[6] == 'planned_purchase_date':
                continue  # Month boundaries are covered separately.
            years = case[5]
            for start, end, allowed in [
                ('2024-02-29', f'{2024 + years}-02-27', True),
                ('2024-02-29', f'{2024 + years}-02-28', True),
                ('2024-02-29', f'{2024 + years}-03-01', False),
                ('2023-10-28', f'{2023 + years}-10-28', True),
                ('2023-10-28', f'{2023 + years}-10-29', False),
                ('2000-01-01', '2001-01-01', True),  # Span, not historical retention.
                ('9998-01-01', '9999-12-31', True),
            ]:
                with self.subTest(source=case[0], start=start, end=end):
                    query = self.query(case, start, end)
                    original = copy.deepcopy(query)
                    if allowed:
                        normalized = self.normalize(case, query)
                        self.assertEqual(self.normalize(case, normalized), normalized)
                        r.validate_endpoint_request('POST', case[2], normalized)
                        for field in ('areaIds', 'excludeWords'):
                            self.assertEqual(normalized[field], query[field])
                    else:
                        self.rejected(lambda: self.normalize(case, query))
                        self.rejected(lambda: r.validate_endpoint_request('POST', case[2], query))
                    self.assertEqual(query, original)

    def test_project_explicit_times_compare_at_second_precision(self):
        case = self.cases[0]
        for end, allowed in [('2027-02-28 12:30:00', True), ('2027-02-28 12:30:01', False)]:
            query = self.query(case, '2024-02-29 12:30:00', end)
            if allowed:
                self.assertEqual(self.normalize(case, query)['endTime'], end)
            else:
                self.rejected(lambda: self.normalize(case, query))

    def test_defaults_single_endpoints_and_invalid_dates(self):
        for case in self.cases:
            normalized = self.normalize(case, self.query(case))
            self.assertNotIn(case[3], normalized)
            self.assertNotIn(case[4], normalized)
            pairs = [('2026-13', '2027-01'), ('2026-04', '2026-03')] if case[6] == 'planned_purchase_date' else [('2026-02-30', '2026-03-01'), ('2026-03-02', '2026-03-01')]
            for start, end in pairs:
                self.rejected(lambda: self.normalize(case, self.query(case, start, end)), 'INVALID_QUERY')
        case = self.cases[0]
        query = self.normalize(case, self.query(case, '2024-01-31'))
        self.assertEqual(query['endTime'], '2024-02-29 23:59:59')
        query = self.normalize(case, self.query(case, end='2024-03-31'))
        self.assertEqual(query['beginTime'], '2024-02-29 00:00:00')
        self.rejected(lambda: self.normalize(self.cases[1], self.query(self.cases[1], '2026-01-01')),
                      'AGENT_QUERY_CORRECTION_REQUIRED')

    def test_over_limit_search_never_builds_client_or_mutates_scope(self):
        for case in self.cases:
            query = self.query(case, '2024-01-01', f'{2024 + case[5]}-02-01')
            args = r.build_parser().parse_args([case[1], '--query-json', json.dumps(query)])
            with self.subTest(source=case[0]), patch.object(r, 'build_client') as client:
                result = args.func(args)
                self.assertFalse(result['ok'])
                self.assertEqual(result['error_code'], 'TIME_SPAN_EXCEEDED')
                self.assertIn(str(case[5]), result['user_message'])
                client.assert_not_called()

    def test_complex_preflight_rejects_only_over_limit(self):
        for case in self.cases:
            for end, allowed in [(f'{2024 + case[5]}-01-01', True), (f'{2024 + case[5]}-02-01', False)]:
                plan = {'conditions': [
                    {'id': 'k', 'type': 'keyword', 'value': '设备'},
                    {'id': 't', 'type': case[6], 'value': {'start': self.date_value(case, '2024-01-01'), 'end': self.date_value(case, end)}},
                ], 'operations': [{'id': 's', 'action': 'search', 'data_source': case[0]}]}
                result = preflight_complex_plan(plan, r.normalize_complex_operation)
                self.assertEqual(result['ok'], allowed, result)
                if not allowed:
                    self.assertEqual(result['approved_operations'], [])

    def test_historical_span_can_be_repaired_but_cannot_be_paged(self):
        for case in self.cases:
            old_query = self.query(case, '2024-01-01', f'{2024 + case[5]}-02-01')
            snapshot = r.save_search_snapshot(session_id=str(uuid.uuid4()), result_type=case[0],
                effective_query=old_query, viewed_cards=[], total_count=20, page_count=4)
            contexts = [
                ['--session-id', snapshot['session_id'], '--result-set-id', snapshot['result_set_id']],
                ['--context-json', json.dumps({'result_type': case[0], 'effective_query': old_query, 'page_count': 4})],
            ]
            for context in contexts:
                with self.subTest(source=case[0], context=context[0]):
                    for command in [['next', *context], ['refine', *context, '--query-json', '{"excludeWords":["保洁"]}']]:
                        args = r.build_parser().parse_args(command)
                        with patch.object(r, 'build_client') as client:
                            result = self.command(command)
                            self.assertIn(str(case[5]), result["user_message"])
                            self.assertEqual(result['error_code'], 'TIME_SPAN_EXCEEDED', result)
                            client.assert_not_called()
                    calls = []
                    def request(client, method, path, query=None):
                        r.validate_endpoint_request(method, path, query)
                        calls.append(dict(query))
                        client.last_request_path, client.last_request_query = path, dict(query)
                        return {'rowCount': 20, 'pageCount': 4, 'list': []}
                    patch_query = {case[4]: self.date_value(case, f'{2024 + case[5]}-01-01')}
                    args = r.build_parser().parse_args(['refine', *context, '--query-json', json.dumps(patch_query)])
                    with patch.object(r.ApiClient, '_request', request):
                        result = args.func(args)
                        self.assertTrue(result['ok'], result)
                        follow = result['follow_up']
                        args = r.build_parser().parse_args(['next', '--session-id', follow['session_id'],
                                                          '--result-set-id', follow['result_set_id']])
                        self.assertTrue(args.func(args)['ok'])
                    self.assertEqual([q['currentPage'] for q in calls], [1, 2])
                    for query in calls:
                        self.assertEqual(query['areaIds'], [3320])
                        self.assertEqual(query['excludeWords'], ['维修'])
                        self.assertEqual(query[case[4]][:10], patch_query[case[4]])

    def test_refine_cannot_expand_valid_query_past_limit(self):
        for case in self.cases:
            query = self.normalize(case, self.query(case, '2024-01-01', '2025-01-01'))
            snapshot = r.save_search_snapshot(session_id=str(uuid.uuid4()), result_type=case[0],
                effective_query=query, viewed_cards=[], total_count=20, page_count=4)
            patch_query = {case[4]: self.date_value(case, f'{2024 + case[5]}-02-01')}
            with self.subTest(source=case[0]), patch.object(r, 'build_client') as client:
                result = self.command(['refine', '--session-id', snapshot['session_id'],
                                       '--result-set-id', snapshot['result_set_id'],
                                       '--query-json', json.dumps(patch_query)])
                self.assertEqual(result['error_code'], 'TIME_SPAN_EXCEEDED')
                client.assert_not_called()

    def test_complex_refine_can_repair_historical_span(self):
        for case in self.cases:
            query = self.query(case, '2024-01-01', f'{2024 + case[5]}-02-01')
            snapshot = r.save_search_snapshot(session_id=str(uuid.uuid4()), result_type=case[0],
                effective_query=query, viewed_cards=[], total_count=20, page_count=4)
            operation = {'session_id': snapshot['session_id'], 'result_set_id': snapshot['result_set_id']}
            normalized, _ = r.normalize_complex_operation(case[0], 'refine', {case[4]: self.date_value(case, '2025-01-01')}, operation)
            self.assertEqual(normalized[case[4]][:10], self.date_value(case, '2025-01-01'))
            self.rejected(lambda: r.normalize_complex_operation(case[0], 'refine', {'excludeWords': ['保洁']}, operation))

    def test_query_cannot_disable_time_span_validation(self):
        for case in self.cases:
            query = dict(self.query(case, '2024-01-01', f'{2024 + case[5]}-02-01'), check_time_span=False)
            with self.subTest(source=case[0]), self.assertRaises(r.SkillError):
                self.normalize(case, query)

    def test_purchase_month_boundaries(self):
        case = self.cases[3]
        for end, allowed in [('2027-01', True), ('2027-02', True), ('2027-03', False)]:
            query = self.query(case, '2024-02', end)
            if allowed:
                self.assertEqual(self.normalize(case, query)['endPlanPurchaseDate'], end)
                r.validate_endpoint_request('POST', case[2], query)
            else:
                self.rejected(lambda: self.normalize(case, query))
                self.rejected(lambda: r.validate_endpoint_request('POST', case[2], query))

    def test_purchase_time_pairs_are_independent(self):
        case = self.cases[2]
        # The gap between publication and purchase is not a queried span.
        query = dict(self.query(case, '2020-01-01', '2023-01-01'),
                     startPlanPurchaseDate='2026-01', endPlanPurchaseDate='2029-01')
        self.assertEqual(self.normalize(case, query), query)
        for patch_query, label in [({'endTime': '2023-01-02'}, '公告发布时间'),
                                   ({'endPlanPurchaseDate': '2029-02'}, '预计采购时间')]:
            result = self.command(['search-purchase', '--query-json', json.dumps({**query, **patch_query})])
            self.assertEqual(result['error_code'], 'TIME_SPAN_EXCEEDED')
            self.assertIn(label, result['user_message'])
            self.assertIn(list(patch_query.values())[0], result['user_message'])
            self.assertIn('未执行搜索', result['user_message'])

    def test_purchase_single_endpoint_does_not_invent_other_endpoint(self):
        for case in self.cases[2:]:
            query = self.query(case, '2024-01-01')
            normalized = self.normalize(case, query)
            self.assertEqual(normalized[case[3]], query[case[3]])
            self.assertNotIn(case[4], normalized)

    def test_contract_period_enum_is_independent(self):
        case = self.cases[1]
        query = dict(self.query(case, '2026-01-01', '2031-01-01'), contractPeriodType=6)
        self.assertEqual(self.normalize(case, query)['contractPeriodType'], 6)


if __name__ == '__main__':
    unittest.main()
