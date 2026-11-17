from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from complex_query_plan import preflight_complex_plan, sanitize_query_match_scopes


class ComplexQueryV3Tests(unittest.TestCase):
    def run_plan(self, conditions, groups=None, source="project", user_text="查符合条件的项目"):
        plan = {"conditions": conditions, "operations": [{"id": "op", "action": "search", "data_source": source}]}
        if groups:
            plan.update(logic_groups=groups, root_group_id="root")
        return preflight_complex_plan(plan, lambda source, action, query, operation: (query, []), user_text=user_text)

    def query(self, conditions, **kwargs):
        result = self.run_plan(conditions, **kwargs)
        self.assertTrue(result["ok"], result)
        query = result["approved_operations"][0]["query"]
        if kwargs.get("source", "project") == "project":
            self.assertFalse(set(query) & {"keywords", "keywordsSearchType", "matchScopes", "procurementMethod"})
        return query

    def test_keyword_groups_preserve_independent_scopes_and_and_relation(self):
        query = self.query([
            {"id": "a", "type": "keyword_group", "value": {"keywords": ["空调", "新风"], "matchScopes": [2, 9]}},
            {"id": "b", "type": "keyword_group", "value": {"keywords": ["安装", "改造"], "matchScopes": [8, 10]}},
        ])
        self.assertEqual(query["keywordGroups"], [
            {"keywords": ["空调", "新风"], "matchScopes": [2, 9]},
            {"keywords": ["安装", "改造"], "matchScopes": [8, 10]},
        ])

    def test_semantic_keyword_title_id_and_role_have_distinct_scopes(self):
        query = self.query([
            {"id": "a", "type": "keyword", "value": "物业"},
            {"id": "b", "type": "project_title", "value": "维修"},
            {"id": "c", "type": "project_id", "value": "QLM-123"},
            {"id": "d", "type": "organization_role", "value": {"role": "winning_unit", "keywords": ["甲公司"]}},
        ])
        self.assertEqual([g["matchScopes"] for g in query["keywordGroups"]], [[2, 9], [2], [8, 10], [5]])

    def test_nested_or_and_compiles_equivalent_cnf(self):
        conditions = [{"id": key, "type": "keyword", "value": key} for key in "abc"]
        groups = [
            {"id": "root", "operator": "OR", "condition_ids": ["a"], "group_ids": ["both"]},
            {"id": "both", "operator": "AND", "condition_ids": ["b", "c"]},
        ]
        query = self.query(conditions, groups=groups)
        self.assertEqual(query["keywordGroups"], [
            {"keywords": ["a", "b"], "matchScopes": [2, 9]},
            {"keywords": ["a", "c"], "matchScopes": [2, 9]},
        ])

    def test_non_equivalent_scoped_or_and_filter_or_are_blocked(self):
        for second in [
            {"id": "b", "type": "project_title", "value": "改造"},
            {"id": "b", "type": "area", "value": [2]},
        ]:
            with self.subTest(second=second):
                result = self.run_plan([
                    {"id": "a", "type": "keyword", "value": "空调"}, second,
                ], groups=[{"id": "root", "operator": "OR", "condition_ids": ["a", "b"]}])
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["approved_operations"], [])
                self.assertTrue(result.get("unresolved_conditions"), result)

    def test_project_filters_are_not_keywords(self):
        mappings = {
            "procurement_category": ([1, 3], "procurementCategories"),
            "procurement_method": ([0, 2], "procurementMethods"),
            "funds_source": ([1, 5], "fundsSources"),
            "has_annex": (0, "hasAnnex"),
            "has_agency": (1, "hasAgency"),
            "registration_status": (0, "registrationStatus"),
            "has_bidding_phone": (1, "hasBiddingPhone"),
            "has_winning_phone": (0, "hasWinningPhone"),
        }
        conditions = [{"id": "kw", "type": "keyword", "value": "空调"}]
        conditions += [{"id": key, "type": key, "value": value} for key, (value, _) in mappings.items()]
        query = self.query(conditions)
        for value, field in mappings.values():
            self.assertEqual(query[field], value)
        self.assertEqual(query["keywordGroups"], [{"keywords": ["空调"], "matchScopes": [2, 9]}])

    def test_single_endpoint_and_seconds_only_for_project(self):
        for value in [{"start": "2026-09-01 12:34:56"}, {"end": "2026-09-14"}, ["2026-09-01 12:34:56", "2026-09-14 18:00:01"]]:
            conditions = [{"id": "a", "type": "keyword", "value": "空调"}, {"id": "t", "type": "publish_time", "value": value}]
            query = self.query(conditions)
            self.assertTrue("beginTime" in query or "endTime" in query)
            self.assertFalse(self.run_plan(conditions, source="purchase_intention")["ok"])

    def test_scope_conditions_survive_without_literal_scope_words(self):
        query = self.query([
            {"id": "a", "type": "keyword", "value": "空调"},
            {"id": "s", "type": "match_scope", "value": [4, 9]},
        ])
        self.assertEqual(query["keywordGroups"][0]["matchScopes"], [4, 9])
        self.assertEqual(sanitize_query_match_scopes({"keywords": ["甲公司"], "matchScopes": [5]}, "查甲公司的项目")["matchScopes"], [5])

    def test_other_sources_keep_legacy_keywords_and_all_scope_values(self):
        for source in ["purchase_intention", "expiring_project"]:
            query = self.query([
                {"id": "a", "type": "keyword", "value": "空调"},
                {"id": "s", "type": "match_scope", "value": list(range(1, 11))},
            ], source=source)
            self.assertEqual(query["keywords"], ["空调"])
            self.assertEqual(query["matchScopes"], list(range(1, 11)))
            self.assertNotIn("keywordGroups", query)

    def test_expiring_procurement_method_stays_scalar(self):
        query = self.query([
            {"id": "a", "type": "keyword", "value": "空调"},
            {"id": "m", "type": "procurement_method", "value": 2},
        ], source="expiring_project")
        self.assertEqual(query["procurementMethod"], 2)

    def test_nested_filter_or_and_nested_not_never_drop_logic(self):
        conditions = [{"id": "a", "type": "keyword", "value": "空调"}, {"id": "b", "type": "area", "value": [2]}]
        for source in ["project", "purchase_intention", "expiring_project"]:
            for operator in ["OR", "NOT"]:
                result = self.run_plan(conditions, source=source, groups=[
                    {"id": "root", "operator": operator, "group_ids": ["left", "right"]},
                    {"id": "left", "operator": "AND", "condition_ids": ["a"]},
                    {"id": "right", "operator": "AND", "condition_ids": ["b"]},
                ])
                self.assertFalse(result["ok"], (source, operator, result))

    def test_representable_scoped_or_and_method_or(self):
        for atoms, field, expected in [
            ([{"id":"a","type":"keyword_group","value":{"keywords":["空调"],"matchScopes":[2]}},{"id":"b","type":"keyword_group","value":{"keywords":["空调"],"matchScopes":[8]}}], "keywordGroups", [{"keywords":["空调"],"matchScopes":[2,8]}]),
            ([{"id":"a","type":"procurement_method","value":0},{"id":"b","type":"procurement_method","value":2}], "procurementMethods", [0,2]),
        ]:
            result=self.query(atoms,groups=[{"id":"root","operator":"OR","condition_ids":["a","b"]}])
            self.assertEqual(result[field],expected)

    def test_repeated_expression_is_simplified_incrementally(self):
        conditions=[{"id":x,"type":"keyword","value":x} for x in ["a","b"]]
        groups=[{"id":"root","operator":"OR","group_ids":[f"g{i}" for i in range(18)]}]
        groups += [{"id":f"g{i}","operator":"AND","condition_ids":["a","b"]} for i in range(18)]
        self.assertEqual(len(self.query(conditions,groups=groups)["keywordGroups"]),2)

    def test_scope_only_refine_preserves_existing_words(self):
        from unittest.mock import patch
        import uuid
        import qianlima_skill as runtime
        sid,rid=str(uuid.uuid4()),str(uuid.uuid4())
        snapshot={"result_type":"project","effective_query":{"keywordGroups":[{"keywords":["空调"],"matchScopes":[2,8]}],"currentPage":1}}
        plan={"conditions":[{"id":"s","type":"match_scope","value":[2]},{"id":"m","type":"amount_min","value":5000000}],"operations":[{"id":"op","action":"refine","data_source":"project","session_id":sid,"result_set_id":rid}]}
        with patch.object(runtime,"load_snapshot",return_value=snapshot):
            result=preflight_complex_plan(plan,runtime.normalize_complex_operation)
        self.assertTrue(result["ok"],result)
        query=result["approved_operations"][0]["query"]
        self.assertEqual(query["keywordGroups"],[{"keywords":["空调"],"matchScopes":[2]}])
        self.assertNotIn("matchScopes",query)




    def test_project_output_passes_actual_runtime_normalizer(self):
        from qianlima_skill import normalize_project_search_query
        result = preflight_complex_plan({
            "conditions": [
                {"id": "a", "type": "keyword_group", "value": {"keywords": ["空调", "新风"], "matchScopes": [4, 9]}},
                {"id": "t", "type": "publish_time", "value": {"start": "2026-01-31 12:34:56"}},
                {"id": "m", "type": "procurement_method", "value": [0, 2]},
            ],
            "operations": [{"id": "op", "action": "search", "data_source": "project"}],
        }, lambda source, action, query, operation: normalize_project_search_query(query))
        self.assertTrue(result["ok"], result)
        query = result["approved_operations"][0]["query"]
        self.assertEqual(query["beginTime"], "2026-01-31 12:34:56")
        self.assertEqual(query["endTime"], "2026-02-28 12:34:56")
        self.assertEqual(query["keywordGroups"][0]["matchScopes"], [4, 9])


if __name__ == "__main__":
    unittest.main()
