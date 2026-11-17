from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as runtime


def project(**fields):
    return {'keywordGroups': [{'keywords': ['空调'], 'matchScopes': [2, 9]}], **fields}


class FiveApiRuntimeTests(unittest.TestCase):
    def test_result_parent_label_does_not_claim_all_notices_are_awards(self):
        self.assertEqual(runtime.info_type_names({'3': []}), ['结果公示'])

    def test_inquiry_search_and_detail_are_valid(self):
        try:
            query, _ = runtime.normalize_query(project(procurementMethods=[4]))
            detail = runtime.validate_detail_response({'id': 101, 'zhaoBiaoType': '询价'})
        except runtime.SkillError as exc:
            self.fail(f'已支持的询价被拒绝：{exc}')
        self.assertEqual(query['procurementMethods'], [4])
        self.assertEqual(detail['zhaoBiaoType'], '询价')
        self.assertIn('询价', runtime.user_query_sentence(query))

    def test_clear_patch_survives_preflight_and_actual_refine(self):
        with tempfile.TemporaryDirectory() as state_dir, patch.dict(os.environ, {'QIANLIMA_API_KEY':'offline-regression-key', 'QIANLIMA_SKILL_STATE_DIR': state_dir}):
            original, _ = runtime.normalize_query(project(
                areaIds=[2], beginAmount=5000000, procurementMethods=[0], hasAnnex=1,
                registrationStatus=0, beginTime='2026-08-15', endTime='2026-09-15'))
            snapshot = runtime.save_search_snapshot(
                session_id=str(uuid.uuid4()), result_type='project', effective_query=original,
                viewed_cards=[{'id': 101, 'title': '空调采购'}], total_count=2, page_count=1)
            operation = {'session_id': snapshot['session_id'], 'result_set_id': snapshot['result_set_id']}
            deletion = {'procurementMethods': None, 'hasAnnex': None}
            approved, _ = runtime.normalize_complex_operation('project', 'refine', deletion, operation)
            self.assertEqual(approved, deletion, '清除键不能在发给 refine 之前消失')
            calls = []
            def request(client, method, path, query=None):
                calls.append((method, path, query))
                client.last_request_path, client.last_request_query = path, query
                return {'rowCount': 0, 'pageCount': 0, 'list': []}
            args = runtime.build_parser().parse_args([
                'refine', '--session-id', snapshot['session_id'], '--result-set-id', snapshot['result_set_id'],
                '--query-json', json.dumps(approved)])
            with patch.object(runtime.ApiClient, '_request', request):
                result = args.func(args)
            self.assertTrue(result['ok'], result)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][:2], ('POST', '/api/search'))
            expected = {k: v for k, v in original.items() if k not in deletion}
            self.assertEqual(calls[0][2], expected)
            self.assertEqual(result['effective_query'], expected)

    def test_zero_and_independent_multiselect_filters_survive(self):
        raw = project(hasAnnex=0, registrationStatus=0, procurementCategories=[1, 2],
                      procurementMethods=[0, 1], fundsSources=[1, 5])
        query, _ = runtime.normalize_query(raw)
        for field, value in raw.items():
            self.assertEqual(query[field], value)

    def test_visible_logic_includes_actual_scopes_and_amount_basis(self):
        query = project(beginAmount=5000000, registrationStatus=0)
        query['keywordGroups'][0]['matchScopes'] = [2, 8]
        for text in (runtime.user_query_sentence(query), '\n'.join(runtime.user_query_lines(query))):
            self.assertIn('标题', text)
            self.assertIn('正文', text)
            self.assertIn('预算或中标金额', text)
            self.assertIn('有记录', text)

    def test_empty_search_does_not_offer_unbounded_time_or_blind_stage_parent(self):
        text = '\n'.join(runtime.zero_result_reflection(project(
            beginTime='2026-01-01', endTime='2026-09-15', infoTypes={'3': [11, 12]})))
        for misleading in ('去掉时间限制', '放宽到一级阶段', '减少限定词'):
            self.assertNotIn(misleading, text)

    def test_role_only_queries_preserve_name_and_scope(self):
        for scope in (4, 5, 6):
            raw = {'keywordGroups': [{'keywords': ['北京某单位有限公司'], 'matchScopes': [scope]}]}
            query, _ = runtime.normalize_query(raw)
            self.assertEqual(query['keywordGroups'], raw['keywordGroups'])
            self.assertNotIn('areaIds', query)
            self.assertNotIn('companyId', query)
            self.assertNotIn('infoTypes', query)

    def test_counts_remain_exactly_as_returned(self):
        for field in ('rowCount', 'pageCount'):
            for value in (None, True, '0', -1, 0.5):
                data = {'rowCount': 0, 'pageCount': 0, 'list': [], field: value}
                with self.subTest(field=field, value=value):
                    self.assertEqual(runtime.validate_search_response(data),data)
                    self.assertIs(type(runtime.validate_search_response(data)[field]),type(value))
        self.assertEqual(runtime.validate_search_response(
            {'rowCount': 0, 'pageCount': 0, 'list': []})['rowCount'], 0)


if __name__ == '__main__':
    unittest.main()
