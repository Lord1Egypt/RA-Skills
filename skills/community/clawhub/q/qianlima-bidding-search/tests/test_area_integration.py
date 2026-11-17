import json
import os
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as r
from complex_query_plan import preflight_complex_plan


class AreaIntegrationTests(unittest.TestCase):
    def queries(self):
        return [
            (r.normalize_project_search_query, {'keywordGroups': [{'keywords': ['设备'], 'matchScopes': [2, 9]}]}),
            (r.normalize_purchase_search_query, {'keywords': ['设备']}),
            (r.normalize_expiring_search_query, {'keywords': ['设备']}),
        ]

    def test_invalid_ids_rejected_in_all_sources(self):
        for normalize, query in self.queries():
            for value in ([999999], [-1], [0], [True], [3316.9], False, None, ['3316.0']):
                with self.subTest(source=normalize.__name__, value=value):
                    with self.assertRaises(r.SkillError):
                        normalize(dict(query, areaIds=value))

    def test_clear_removes_area_key_in_all_sources(self):
        for normalize, query in self.queries():
            with self.subTest(source=normalize.__name__):
                self.assertNotIn('areaIds', normalize(dict(query, areaIds=[]))[0])

    def test_valid_legacy_ids_never_rewritten(self):
        for normalize, query in self.queries():
            self.assertEqual(normalize(dict(query, areaIds=[1274, 1252, '3181', 3181]))[0]['areaIds'], [1274, 1252, 3181])

    def test_low_level_guard_has_no_validation_bypass(self):
        for path, query in [('/api/search', self.queries()[0][1]),
                            ('/api/search/purchase', {'keywords': ['设备'], 'currentPage': 1, 'numPerPage': 5}),
                            ('/api/search/expiring', {'keywords': ['设备'], 'currentPage': 1, 'numPerPage': 5})]:
            with self.subTest(path=path), self.assertRaises(r.SkillError):
                r.validate_endpoint_request('POST', path, dict(query, areaIds=[True]))

    def test_complex_preflight_blocks_unknown_ids(self):
        for source in ['project', 'purchase_intention', 'expiring_project']:
            plan = {'conditions': [{'id': 'k', 'type': 'keyword', 'value': '设备'},
                                  {'id': 'a', 'type': 'area', 'value': [999999]}],
                    'operations': [{'id': 's', 'action': 'search', 'data_source': source}]}
            p = preflight_complex_plan(plan, r.normalize_complex_operation)
            self.assertFalse(p['ok'], p)
            self.assertEqual(p['approved_operations'], [])

    def test_index_node_is_not_a_district_expansion(self):
        self.assertIsNone(r.district_area_expansion({'areaIds': [1274]}))
        self.assertEqual(r.district_area_expansion({'areaIds': [3320]})['refine_query'], {'areaIds': [2]})
        self.assertEqual(r.district_area_expansion({'areaIds': [2807]})['refine_query'], {'areaIds': [316]})
        self.assertIsNone(r.district_area_expansion({'areaIds': [618]}))

    def test_refine_clear_replace_append_and_next_preserve_other_fields(self):
        def request(client, method, path, query=None):
            calls.append(dict(query))
            client.last_request_path, client.last_request_query = path, dict(query)
            return {'rowCount': 100, 'pageCount': 4, 'list': []}
        for kind, (normalize, query) in zip(['project','purchase_intention','expiring_project'], self.queries()):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as state, patch.dict(os.environ, {'QIANLIMA_API_KEY':'offline-regression-key', 'QIANLIMA_SKILL_STATE_DIR':state}):
                original, _ = normalize(dict(query, areaIds=[2807], excludeWords=['维修']))
                snap = r.save_search_snapshot(session_id=str(uuid.uuid4()), result_type=kind,
                    effective_query=original, viewed_cards=[], total_count=100, page_count=4)
                ctx = ['--session-id',snap['session_id'],'--result-set-id',snap['result_set_id']]
                for area_ids in [[], [2806], [2807, 2806]]:
                    calls = []
                    args = r.build_parser().parse_args(['refine', *ctx, '--query-json', json.dumps({'areaIds': area_ids})])
                    with patch.object(r.ApiClient, '_request', request):
                        p = args.func(args)
                    self.assertTrue(p['ok'], p)
                    expected = dict(original)
                    if area_ids:expected['areaIds'] = area_ids
                    else:expected.pop('areaIds')
                    self.assertEqual(calls, [expected])
                calls = []
                args = r.build_parser().parse_args(['next', *ctx])
                with patch.object(r.ApiClient, '_request', request):
                    p = args.func(args)
                self.assertTrue(p['ok'], p)
                self.assertEqual(calls, [dict(original, currentPage=2)])

    def test_complex_clear_survives_patch_normalization(self):
        with tempfile.TemporaryDirectory() as state, patch.dict(os.environ, {'QIANLIMA_API_KEY':'offline-regression-key', 'QIANLIMA_SKILL_STATE_DIR':state}):
            query, _ = r.normalize_project_search_query(dict(self.queries()[0][1], areaIds=[2807]))
            snap = r.save_search_snapshot(session_id=str(uuid.uuid4()), result_type='project',
                effective_query=query, viewed_cards=[], total_count=0, page_count=0)
            operation = {'session_id':snap['session_id'],'result_set_id':snap['result_set_id']}
            p, _ = r.normalize_complex_operation('project','refine',{'areaIds':[]},operation)
            self.assertEqual(p, {'areaIds':[]})


if __name__ == '__main__':unittest.main()
