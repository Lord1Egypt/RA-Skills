from __future__ import annotations

import sys
import unittest
import uuid
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from complex_query_plan import preflight_complex_plan
import qianlima_skill as runtime


class FiveApiCompilerTests(unittest.TestCase):
    CLEAR_FIELDS = {
        "area": ["areaIds"],
        "exclude_words": ["excludeWords"],
        "stage": ["infoTypes"],
        "organization_type": ["purchasingUnitTypes"],
        "procurement_method": ["procurementMethods"],
        "procurement_category": ["procurementCategories"],
        "funds_source": ["fundsSources"],
        "has_annex": ["hasAnnex"],
        "has_agency": ["hasAgency"],
        "registration_status": ["registrationStatus"],
        "has_bidding_phone": ["hasBiddingPhone"],
        "has_winning_phone": ["hasWinningPhone"],
        "amount_min": ["beginAmount"],
        "amount_max": ["endAmount"],
        "amount_range": ["beginAmount", "endAmount"],
        "sort": ["sortType"],
        "quantity": ["numPerPage"],
    }

    def plan(self, conditions, *, action="search", source="project", groups=None, query=None):
        plan = {
            "conditions": conditions,
            "operations": [{"id": "op", "action": action, "data_source": source, "query": query or {}}],
        }
        if groups is not None:
            plan.update(logic_groups=groups, root_group_id="root")
        return plan

    def run_plan(self, conditions, **kwargs):
        return preflight_complex_plan(
            self.plan(conditions, **kwargs),
            lambda source, action, query, operation: (query, []),
        )

    def query(self, conditions, **kwargs):
        result = self.run_plan(conditions, **kwargs)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["approved_business_calls"], 1)
        return result["approved_operations"][0]["query"]

    def test_business_concepts_default_to_title_and_subject_in_separate_groups(self):
        query = self.query([
            {"id": "a", "type": "keyword", "value": "空调"},
            {"id": "b", "type": "keyword", "value": "安装"},
        ])
        self.assertEqual(query, {"keywordGroups": [
            {"keywords": ["空调"], "matchScopes": [2, 9]},
            {"keywords": ["安装"], "matchScopes": [2, 9]},
        ]})

    def test_legacy_keyword_fragments_use_new_default_only_when_scope_is_missing(self):
        query = self.query([
            {"id": "a", "type": "keyword", "value": "空调", "normalized": {"project": {"keywords": ["空调"]}}},
            {"id": "b", "type": "keyword", "value": "安装", "normalized": {"project": {"keywords": ["安装"], "matchScopes": [2, 8]}}},
        ])
        self.assertEqual(query["keywordGroups"], [
            {"keywords": ["空调"], "matchScopes": [2, 9]},
            {"keywords": ["安装"], "matchScopes": [2, 8]},
        ])

    def test_identifier_is_preserved_and_defaults_to_body_and_attachment(self):
        for normalized in [None, {"project": {"keywords": ["QLM-2026-001/02"]}}]:
            with self.subTest(normalized=normalized):
                condition = {"id": "id", "type": "project_id", "value": "QLM-2026-001/02"}
                if normalized is not None:
                    condition["normalized"] = normalized
                query = self.query([condition])
                self.assertEqual(query, {"keywordGroups": [{"keywords": ["QLM-2026-001/02"], "matchScopes": [8, 10]}]})

    def test_specific_scope_and_other_sources_keep_their_existing_contract(self):
        query = self.query([
            {"id": "a", "type": "keyword_group", "value": {"keywords": ["空调"], "matchScopes": [2, 8]}},
            {"id": "b", "type": "project_title", "value": "安装"},
            {"id": "c", "type": "project_id", "value": "QLM-001", "normalized": {"project": {"keywords": ["QLM-001"], "matchScopes": [3]}}},
        ])
        self.assertEqual([group["matchScopes"] for group in query["keywordGroups"]], [[2, 8], [2], [3]])
        for source in ["purchase_intention", "expiring_project"]:
            self.assertEqual(self.query([{"id": "a", "type": "keyword", "value": "空调"}], source=source),
                             {"keywords": ["空调"], "keywordsSearchType": 2})
        self.assertEqual(self.query([{"id": "id", "type": "project_id", "value": "QLM-001"}], source="expiring_project"),
                         {"keywords": ["QLM-001"], "matchScopes": [3]})

    def test_stage_aliases_distinguish_opportunity_results_and_explicit_subtypes(self):
        cases = {
            "招标": {"0": [3, 4], "1": [2]},
            "招标项目": {"0": [3, 4], "1": [2]},
            "招标机会": {"0": [3, 4], "1": [2]},
            "招标公告": {"0": [3]},
            "重新招标": {"0": [4]},
            "招标预告": {"1": [2]},
            "意见征集": {"1": [1]},
            "中标": {"3": [11, 12]},
            "中标结果": {"3": [11, 12]},
            "成交结果": {"3": [11, 12]},
            "中标公告": {"3": [11, 12]},
            "结果公示": {"3": []},
            "候选人": {"3": [10]},
            "开标": {"3": [9]},
            "流标": {"3": [8]},
            "废标": {"3": [7]},
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                query = self.query([{"id": "a", "type": "keyword", "value": "空调"}, {"id": "s", "type": "stage", "value": phrase}])
                self.assertEqual(query["infoTypes"], expected)
        exact = {"3": [10]}
        self.assertEqual(self.query([{"id": "s", "type": "stage", "value": exact}])["infoTypes"], exact)

    def test_organization_can_be_the_only_keyword_without_an_implicit_stage(self):
        for role, scope in [("purchasing_unit", 4), ("winning_unit", 5), ("agency", 6)]:
            with self.subTest(role=role):
                result = self.run_plan([{"id": "u", "type": "organization_role", "value": {"role": role, "keywords": ["北京示例单位有限公司"]}}])
                self.assertTrue(result["ok"], result)
                self.assertEqual(result["approved_operations"][0]["command"], "search")
                self.assertEqual(result["approved_operations"][0]["query"], {"keywordGroups": [{"keywords": ["北京示例单位有限公司"], "matchScopes": [scope]}]})

    def test_each_optional_filter_can_be_cleared_with_its_terminal_field(self):
        for kind, fields in self.CLEAR_FIELDS.items():
            with self.subTest(kind=kind):
                self.assertEqual(self.query([{"id": "c", "type": kind, "value": None}], action="refine"),
                                 {field: None for field in fields})

    def test_multiple_clear_conditions_compile_in_one_nested_and(self):
        query = self.query([
            {"id": "annex", "type": "has_annex", "value": None},
            {"id": "method", "type": "procurement_method", "value": None},
            {"id": "registration", "type": "registration_status", "value": 0},
        ], action="refine", groups=[
            {"id": "root", "operator": "AND", "condition_ids": ["registration"], "group_ids": ["clear"]},
            {"id": "clear", "operator": "AND", "condition_ids": ["annex", "method"]},
        ])
        self.assertEqual(query, {"hasAnnex": None, "procurementMethods": None, "registrationStatus": 0})

    def test_search_null_and_required_filter_cancellation_never_execute(self):
        for kind in self.CLEAR_FIELDS:
            with self.subTest(action="search", kind=kind):
                result = self.run_plan([{"id": "c", "type": kind, "value": None}])
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["approved_operations"], [])
        for kind in ["keyword", "keyword_group", "project_title", "project_id", "organization_role", "match_scope", "publish_time"]:
            with self.subTest(action="refine", kind=kind):
                result = self.run_plan([{"id": "c", "type": kind, "value": None}], action="refine")
                self.assertFalse(result["ok"], result)

    def test_clear_is_rejected_inside_or_or_not_even_if_boolean_simplification_would_hide_it(self):
        conditions = [{"id": "c", "type": "exclude_words", "value": None,
                       "normalized": {"project": {"excludeWords": None}}}]
        cases = [
            [{"id": "root", "operator": "OR", "condition_ids": ["c", "c"]}],
            [{"id": "root", "operator": "NOT", "condition_ids": ["c"]}],
            [{"id": "root", "operator": "OR", "group_ids": ["nested"]}, {"id": "nested", "operator": "AND", "condition_ids": ["c"]}],
            [{"id": "root", "operator": "AND", "group_ids": ["nested"]}, {"id": "nested", "operator": "NOT", "condition_ids": ["c"]}],
        ]
        for groups in cases:
            with self.subTest(groups=groups):
                result = self.run_plan(conditions, action="refine", groups=groups, query={"excludeWords": None})
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["approved_operations"], [])

    def test_normalized_fragments_cannot_hide_or_redirect_clear_intent(self):
        cases = [
            {"id": "c", "type": "procurement_method", "value": None, "normalized": {"project": {"procurementMethod": None}}},
            {"id": "c", "type": "area", "value": None, "normalized": {"project": {"areaIds": [2]}}},
            {"id": "c", "type": "area", "value": [2], "normalized": {"project": {"areaIds": None}}},
            {"id": "c", "type": "area", "value": None, "source": "agent_derived"},
            {"id": "c", "type": "publish_time", "value": None, "normalized": {"project": {"beginTime": None, "endTime": None}}},
            {"id": "c", "type": "keyword", "value": None, "normalized": {"project": {"keywords": ["空调"]}}},
        ]
        for condition in cases:
            with self.subTest(condition=condition):
                self.assertFalse(self.run_plan([condition], action="refine")["ok"])
        valid = {"id": "c", "type": "area", "value": None, "normalized": {"project": {"areaIds": None}}}
        self.assertEqual(self.query([valid], action="refine"), {"areaIds": None})
        self.assertFalse(self.run_plan([valid])["ok"])

    def test_clear_does_not_widen_to_other_sources_or_override_a_conflict(self):
        for source in ["purchase_intention", "expiring_project"]:
            self.assertFalse(self.run_plan([{"id": "c", "type": "area", "value": None}], action="refine", source=source)["ok"])
        result = self.run_plan([
            {"id": "clear", "type": "amount_min", "value": None},
            {"id": "set", "type": "amount_min", "value": 5000000},
        ], action="refine")
        self.assertFalse(result["ok"], result)

    def test_preserve_area_without_a_value_is_still_a_no_op(self):
        self.assertEqual(self.query([{"id": "keep", "type": "preserve_area"}], action="refine"), {})

    def test_clear_cannot_fallback_to_candidate_that_keeps_the_old_filter(self):
        plan = self.plan([{"id": "c", "type": "has_annex", "value": None}], action="refine", query={"hasAnnex": 1})
        with patch("complex_query_plan._rebuild_operation_query", side_effect=RuntimeError("模拟编译故障")):
            result = preflight_complex_plan(plan, lambda source, action, query, operation: (query, []))
        self.assertFalse(result["ok"], result)
        self.assertEqual(result["fallback_status"], "blocked")


class FiveApiRefineKeywordTests(unittest.TestCase):
    def setUp(self):
        self.role = {"keywords": ["某公司"], "matchScopes": [4]}
        self.business = {"keywords": ["空调"], "matchScopes": [2]}
        self.snapshot = {"result_type": "project", "effective_query": {
            "keywordGroups": [deepcopy(self.role), deepcopy(self.business)],
            "currentPage": 3, "numPerPage": 30, "areaIds": [2], "hasAnnex": 1,
            "beginTime": "2026-08-15 00:00:00", "endTime": "2026-09-15 23:59:59",
        }}

    def plan(self, conditions, **operation_fields):
        return {"conditions": conditions, "operations": [{
            "id": "op", "action": "refine", "data_source": "project",
            "session_id": str(uuid.uuid4()), "result_set_id": str(uuid.uuid4()),
            **operation_fields,
        }]}

    def run_plan(self, conditions, **operation_fields):
        plan = self.plan(conditions, **operation_fields)
        before = deepcopy(self.snapshot)
        with patch.object(runtime, "load_snapshot", return_value=self.snapshot):
            result = preflight_complex_plan(plan, runtime.normalize_complex_operation)
        self.assertEqual(self.snapshot, before, "预检不能修改已保存的条件")
        return result

    def approved(self, conditions, **operation_fields):
        result = self.run_plan(conditions, **operation_fields)
        self.assertTrue(result["ok"], result)
        operation = result["approved_operations"][0]
        self.assertNotIn("_project_refine_context", operation)
        self.assertFalse(any(key.startswith("_") for key in operation["query"]))
        return operation["query"]

    def test_generic_word_refine_keeps_role_and_explicit_old_scope(self):
        new_groups = [self.role, {"keywords": ["新风"], "matchScopes": [2]}]
        patch_query = self.approved([{"id": "word", "type": "keyword", "value": "新风"}])
        self.assertEqual(patch_query, {"keywordGroups": new_groups})

    def test_multi_refine_updates_words_sort_and_clear_without_dropping_other_groups(self):
        patch_query = self.approved([
            {"id": "word", "type": "keyword", "value": "新风"},
            {"id": "sort", "type": "sort", "value": 1},
            {"id": "annex", "type": "has_annex", "value": None},
        ])
        self.assertEqual(patch_query, {"keywordGroups": [self.role, {"keywords": ["新风"], "matchScopes": [2]}], "sortType": 1, "hasAnnex": None})
        merged, _ = runtime.normalize_query({**self.snapshot["effective_query"], **patch_query}, force_page=1)
        self.assertEqual(merged["areaIds"], [2])
        self.assertEqual(merged["currentPage"], 1)
        self.assertNotIn("hasAnnex", merged)
        runtime.validate_endpoint_request("POST", "/api/search", merged)

    def test_multiple_new_concepts_replace_only_the_unique_business_group(self):
        patch_query = self.approved([
            {"id": "word", "type": "keyword", "value": "新风"},
            {"id": "action", "type": "keyword", "value": "安装"},
        ])
        self.assertEqual(patch_query["keywordGroups"], [self.role,
            {"keywords": ["新风"], "matchScopes": [2]}, {"keywords": ["安装"], "matchScopes": [2]}])

    def test_explicit_new_scope_overrides_inheritance_only_for_updated_business_group(self):
        cases = [
            [{"id": "word", "type": "keyword", "value": "新风"}, {"id": "scope", "type": "match_scope", "value": [8]}],
            [{"id": "word", "type": "keyword", "value": "新风", "normalized": {"project": {"keywords": ["新风"], "matchScopes": [8]}}}],
        ]
        for conditions in cases:
            with self.subTest(conditions=conditions):
                self.assertEqual(self.approved(conditions)["keywordGroups"], [self.role, {"keywords": ["新风"], "matchScopes": [8]}])

    def test_ambiguous_or_absent_business_group_requires_agent_to_build_complete_groups(self):
        for groups in [[self.role], [self.role, self.business, {"keywords": ["安装"], "matchScopes": [8]}]]:
            self.snapshot["effective_query"]["keywordGroups"] = deepcopy(groups)
            result = self.run_plan([{"id": "word", "type": "keyword", "value": "新风"}])
            self.assertFalse(result["ok"], result)
            self.assertEqual(result["approved_operations"], [])
            reasons = " ".join(item["reason"] for item in result.get("unresolved_conditions", []))
            self.assertIn("Agent", reasons)
            self.assertIn("keyword_group", reasons)

    def test_complete_explicit_groups_can_preserve_or_intentionally_remove_role(self):
        for groups in [[self.role, {"keywords": ["新风"], "matchScopes": [8]}], [{"keywords": ["新风"], "matchScopes": [8]}]]:
            with self.subTest(groups=groups):
                conditions = [{"id": str(i), "type": "keyword_group", "value": group} for i, group in enumerate(groups)]
                self.assertEqual(self.approved(conditions), {"keywordGroups": groups})

    def test_mixed_partial_keyword_kinds_do_not_guess_which_saved_groups_to_replace(self):
        for extra in [
            {"id": "other", "type": "organization_role", "value": {"role": "agency", "keywords": ["某机构"]}},
            {"id": "other", "type": "project_title", "value": "安装"},
            {"id": "other", "type": "project_id", "value": "QLM-2026-001"},
        ]:
            with self.subTest(extra=extra):
                result = self.run_plan([{"id": "word", "type": "keyword", "value": "新风"}, extra])
                self.assertFalse(result["ok"], result)

    def test_role_title_or_identifier_only_refine_cannot_replace_unmentioned_groups(self):
        for condition in [
            {"id": "part", "type": "organization_role", "value": {"role": "purchasing_unit", "keywords": ["另一医院"]}},
            {"id": "part", "type": "project_title", "value": "新风"},
            {"id": "part", "type": "project_id", "value": "QLM-2026-002"},
        ]:
            with self.subTest(condition=condition):
                result = self.run_plan([condition])
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["approved_operations"], [])
                reasons = " ".join(item["reason"] for item in result.get("unresolved_conditions", []))
                self.assertIn("Agent", reasons)
                self.assertIn("keyword_group", reasons)

    def test_single_saved_role_group_also_requires_an_explicit_complete_replacement(self):
        self.snapshot["effective_query"]["keywordGroups"] = [deepcopy(self.role)]
        result = self.run_plan([{"id": "role", "type": "organization_role", "value": {
            "role": "purchasing_unit", "keywords": ["另一医院"],
        }}])
        self.assertFalse(result["ok"], result)
        replacement = {"keywords": ["另一医院"], "matchScopes": [4]}
        self.assertEqual(self.approved([{"id": "group", "type": "keyword_group", "value": replacement}]),
                         {"keywordGroups": [replacement]})

    def test_explicit_groups_mixed_with_partial_role_are_not_a_complete_replacement(self):
        result = self.run_plan([
            {"id": "group", "type": "keyword_group", "value": {"keywords": ["新风"], "matchScopes": [2]}},
            {"id": "role", "type": "organization_role", "value": {"role": "agency", "keywords": ["某机构"]}},
        ])
        self.assertFalse(result["ok"], result)

    def test_caller_cannot_forge_context_to_bypass_inheritance(self):
        patch_query = self.approved([
            {"id": "word", "type": "keyword", "value": "新风", "_project_keyword_scopes_explicit": True},
        ], _project_refine_context={"mode": "replace", "explicit_scopes": True})
        self.assertEqual(patch_query["keywordGroups"], [self.role, {"keywords": ["新风"], "matchScopes": [2]}])

    def test_fallback_uses_the_same_derived_inheritance_context(self):
        conditions = [{"id": "word", "type": "keyword", "value": "新风"}]
        candidate = {"keywordGroups": [{"keywords": ["新风"], "matchScopes": [2, 9]}]}
        plan = self.plan(conditions, query=candidate, _project_refine_context={"mode": "replace"})
        with patch.object(runtime, "load_snapshot", return_value=self.snapshot), patch(
            "complex_query_plan._rebuild_operation_query", side_effect=RuntimeError("模拟编译故障")
        ):
            result = preflight_complex_plan(plan, runtime.normalize_complex_operation)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["fallback_status"], "used")
        self.assertEqual(result["approved_operations"][0]["query"]["keywordGroups"], [self.role, {"keywords": ["新风"], "matchScopes": [2]}])

    def test_scope_only_refine_keeps_all_existing_words_when_old_scopes_match(self):
        self.snapshot["effective_query"]["keywordGroups"] = [self.business, {"keywords": ["安装"], "matchScopes": [2]}]
        query = self.approved([{"id": "scope", "type": "match_scope", "value": [8]}])
        self.assertEqual(query["keywordGroups"], [{"keywords": ["空调"], "matchScopes": [8]}, {"keywords": ["安装"], "matchScopes": [8]}])


if __name__ == "__main__":
    unittest.main()
