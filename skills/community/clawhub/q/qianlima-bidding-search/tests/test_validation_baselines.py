from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import Any
from protocol_migration import project_query


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
RUNTIME = ROOT / "scripts" / "qianlima_skill.py"
LIVE_VALIDATE = ROOT / "scripts" / "live_validate.py"
SEMANTIC_RETEST = ROOT / "scripts" / "retest_semantic_fields.py"
DETAIL_RETEST = ROOT / "scripts" / "retest_detail_followups.py"
LIVE_CASES = ROOT / "tests" / "live_validation_cases.json"
FIXTURES = ROOT / "tests" / "fixtures"
RELEASE_VERSION = json.loads((ROOT / "manifest.json").read_text())["version"]
RELEASE_PACKAGE = Path(os.environ.get("QIANLIMA_TEST_PACKAGE", str(ROOT.parent / "dist" / f"qianlima-bidding-search-v{RELEASE_VERSION}.zip")))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidationBaselineTests(unittest.TestCase):
    def follow_up_payload(self, fixtures: Path, state_dir: Path, *args: str) -> dict[str, Any]:
        env = {key: value for key, value in os.environ.items() if not key.startswith("QIANLIMA_")}
        env["QIANLIMA_API_KEY"] = "offline-baseline-key"
        env["QIANLIMA_SKILL_STATE_DIR"] = str(state_dir)
        proc = subprocess.run(
            [sys.executable, str(RUNTIME), "--mock-dir", str(fixtures), *args],
            env=env, text=True, capture_output=True, check=False,
        )
        self.assertIn(proc.returncode, (0, 2), proc.stderr)
        return json.loads(proc.stdout)

    def test_live_safe_failure_rejects_matched_api_business_failures(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_safe_business_errors")
        for code in (10005, 10007):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as tmp:
                fixtures = Path(tmp) / "fixtures"
                shutil.copytree(FIXTURES, fixtures)
                state = Path(tmp) / "state"
                first = self.follow_up_payload(
                    fixtures, state, "search", "--query-json",
                    json.dumps({"keywordGroups": [{"keywords": ["实验室"], "matchScopes": [2, 9]}]}),
                )
                (fixtures / "detail_101.json").write_text(json.dumps({
                    "code": code, "msg": "详情不存在" if code == 10005 else "无权查看详情",
                    "data": {}, "success": False,
                }))
                failed = self.follow_up_payload(
                    fixtures, state, "detail", "--result-set-id", first["follow_up"]["result_set_id"],
                    "--project-ref", "第1条", "--fields", "budgetAmount",
                )
                self.assertFalse(failed["ok"])
                self.assertEqual(failed["error_code"], str(code))
                self.assertEqual(failed["resolution"]["status"], "matched")
                self.assertEqual(failed["api_responses"][0]["path"], "/api/detail/101")
                self.assertFalse(live.is_safe_follow_up_failure(failed))

    def test_live_safe_failure_accepts_unresolved_objects_without_api(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_safe_object_resolution")
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            first = self.follow_up_payload(
                FIXTURES, state, "search", "--query-json",
                json.dumps({"keywordGroups": [{"keywords": ["实验室"], "matchScopes": [2, 9]}]}),
            )
            for ref, status in (("实验室", "ambiguous"), ("第99条", "not_found")):
                with self.subTest(ref=ref):
                    failed = self.follow_up_payload(
                        FIXTURES, state, "detail", "--result-set-id", first["follow_up"]["result_set_id"],
                        "--project-ref", ref,
                    )
                    self.assertFalse(failed["ok"])
                    self.assertEqual(failed["resolution"]["status"], status)
                    self.assertFalse(failed.get("api_responses"))
                    self.assertTrue(live.is_safe_follow_up_failure(failed))

    def test_live_safe_failure_accepts_missing_query_without_api(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_safe_missing_context")
        with tempfile.TemporaryDirectory() as tmp:
            failed = self.follow_up_payload(FIXTURES, Path(tmp) / "state", "next")
        self.assertFalse(failed["ok"])
        self.assertFalse(failed.get("api_responses"))
        self.assertTrue(failed["needs_clarification"])
        self.assertTrue(live.is_safe_follow_up_failure(failed))

    def test_live_safe_failure_rejects_api_calls_even_with_clarification_labels(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_safe_actual_call_guard")
        response = {"path": "/api/detail/101", "response": {"code": 10005, "msg": "详情不存在", "data": {}}}
        for fields in ({}, {"resolution": {"status": "not_found"}}, {
            "retry_policy": "restore_explicit_context_or_clarify_missing_fields", "needs_clarification": True,
        }):
            with self.subTest(fields=fields):
                self.assertFalse(live.is_safe_follow_up_failure({
                    "ok": False, "error_code": "10005", "api_responses": [response], **fields,
                }))

    def test_live_safe_failure_requires_an_actual_failure_and_missing_context(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_safe_failure_shape")
        for payload in (
            {"ok": True, "resolution": {"status": "not_found"}},
            {"ok": False, "error_code": "10005"},
            {"ok": False, "resolution": {"status": "matched"}},
            {"ok": False, "retry_policy": "restore_explicit_context_or_clarify_missing_fields"},
        ):
            with self.subTest(payload=payload):
                self.assertFalse(live.is_safe_follow_up_failure(payload))

    def run_skill(self, command: str, query: dict[str, Any], *extra: str) -> dict[str, Any]:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, QIANLIMA_API_KEY="offline-baseline-key")
            env["QIANLIMA_SKILL_STATE_DIR"] = str(Path(tmp) / "state")
            env.pop("QIANLIMA_SKILL_STATE", None)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUNTIME),
                    "--mock-dir",
                    str(FIXTURES),
                    command,
                    *extra,
                    "--query-json",
                    json.dumps(project_query(query) if command == "search" else query, ensure_ascii=False),
                ],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        return json.loads(proc.stdout or "{}")

    def test_project_search_rejects_procurement_intention_info_type(self) -> None:
        payload = self.run_skill(
            "search",
            {"keywords": ["数字化"], "infoTypes": {"99": []}, "numPerPage": 2},
        )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertIn("search-purchase", payload["user_message"])
        self.assertNotIn("request_query", payload)

    def test_runtime_reports_actual_route_metadata(self) -> None:
        cases = [
            (
                "search",
                {"keywords": ["实验室设备"], "numPerPage": 2},
                (),
                "search-projects",
                "project",
                "/api/search",
            ),
            (
                "search-purchase",
                {"keywords": ["实验室设备"], "numPerPage": 2},
                (),
                "search-purchase-intentions",
                "purchase_intention",
                "/api/search/purchase",
            ),
            (
                "search-expiring",
                {"keywords": ["物业"], "numPerPage": 1},
                (),
                "search-expiring-projects",
                "expiring_project",
                "/api/search/expiring",
            ),
            (
                "enterprise",
                {"companyName": "千里马科技股份有限公司"},
                ("--kind", "business-info"),
                "enterprise-intel",
                "enterprise_business_info",
                "/api/enterprise/businessInfo",
            ),
        ]

        for command, query, extra, capability, result_type, api_path in cases:
            with self.subTest(command=command):
                payload = self.run_skill(command, query, *extra)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["capability"], capability)
                self.assertEqual(payload["result_type"], result_type)
                self.assertEqual(payload["request_api_path"], api_path)

    def test_live_cases_declare_all_route_expectations(self) -> None:
        payload = json.loads(LIVE_CASES.read_text(encoding="utf-8"))
        route_types = {"search", "purchase_intention", "expiring_project", "enterprise"}
        route_cases = [case for case in payload["cases"] if case["type"] in route_types]
        required = {"expected_command", "expected_capability", "expected_api_path", "expected_result_type"}

        self.assertTrue(route_cases)
        for case in route_cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(required.issubset(case))
                self.assertNotEqual(case.get("expected_query", {}).get("infoTypes"), {"99": []})

        self.assertTrue(any(case["type"] == "purchase_intention" for case in route_cases))
        self.assertTrue(any(case["type"] == "expiring_project" for case in route_cases))
        self.assertTrue(any(case["type"] == "enterprise" for case in route_cases))

    def test_validation_expected_requests_use_source_specific_date_normalization(self) -> None:
        live = load_module(LIVE_VALIDATE, "live_validate_date_contract")
        query = {"keywordGroups": [{"keywords": ["空调"], "matchScopes": [2]}], "beginTime": "2026-01-31"}
        expected = live.normalized_expected_query(query)
        self.assertEqual(expected["beginTime"], "2026-01-31 00:00:00")
        self.assertEqual(expected["endTime"], "2026-02-28 23:59:59")
        purchase = live.normalized_expected_query({"keywords": ["空调"], "beginTime": "2026-01-31"}, "purchase_intention")
        self.assertEqual(purchase["beginTime"], "2026-01-31")
        for filename, method in [("retest_all_search_fields.py", "expected_request"), ("retest_semantic_fields.py", "normalized"), ("retest_multiturn_state.py", "expected_with")]:
            module = load_module(ROOT / "scripts" / filename, filename[:-3] + "_date_test")
            self.assertEqual(getattr(module, method)(query), expected)

    def test_grouped_summary_preserves_groups_scopes_and_zero_filters(self) -> None:
        query = {"keywordGroups": [{"keywords": ["空调", "新风"], "matchScopes": [2]}, {"keywords": ["安装"], "matchScopes": [8]}], "hasAnnex": 0}
        for path in [LIVE_VALIDATE, ROOT / "scripts" / "retest_all_search_fields.py"]:
            module = load_module(path, path.stem + "_summary_test")
            summary = module.compact_query(query)
            for value in ["空调", "新风", "安装", "标题", "正文", "AND", "OR", "无附件"]:
                self.assertIn(value, summary)

    def test_visible_group_checks_do_not_turn_hidden_fields_into_matches(self) -> None:
        semantic = load_module(SEMANTIC_RETEST, "semantic_visible_groups_test")
        query = {"keywordGroups": [{"keywords": ["空调"], "matchScopes": [2]}, {"keywords": ["安装"], "matchScopes": [8]}]}
        partial = semantic.visible_checks(query, [{"title": "空调项目"}])
        self.assertEqual(partial["关键词可见命中"], "0/1")
        self.assertEqual(partial["关键词不可完整核验"], 1)
        self.assertFalse(partial["完整可见核验"])
        wrong = semantic.visible_checks(query, [{"title": "物业项目"}])
        self.assertFalse(wrong["通过"])

    def test_visible_dates_compare_seconds_and_mark_date_only_precision_unknown(self) -> None:
        module = load_module(ROOT / "scripts" / "retest_all_search_fields.py", "retest_timestamp_precision")
        query = {"keywordGroups": [{"keywords": ["空调"], "matchScopes": [2]}], "beginTime": "2026-09-01 12:00:00", "endTime": "2026-09-01 18:00:00"}
        result = module.visible_accuracy(query, {"cards": [{"title": "空调", "publishTime": "2026-09-01 10:00:00"}]})
        self.assertEqual(result["可见字段"]["发布时间匹配"], "0/1")
        self.assertTrue(any("发布时间不匹配" in text for text in result["前5个问题"]))
        unknown = module.visible_accuracy(query, {"cards": [{"title": "空调", "publishTime": "2026-09-01"}]})
        self.assertEqual(unknown["日期不可见"], 1)

    def test_shifted_live_cases_keep_timestamp_precision(self) -> None:
        import datetime as dt
        live = load_module(LIVE_VALIDATE, "live_shift_timestamp")
        yesterday = dt.date.today() - dt.timedelta(days=1)
        shifted = live.shift_dates_to_today({"current_date": str(yesterday), "cases": [{"expected_query": {"beginTime": f"{yesterday} 12:34:56"}}]})
        self.assertEqual(shifted["cases"][0]["expected_query"]["beginTime"], f"{dt.date.today()} 12:34:56")

    def test_static_project_validation_queries_pass_runtime_contract(self) -> None:
        runtime = load_module(RUNTIME, "runtime_validation_static_queries")
        candidates = []
        payload = json.loads(LIVE_CASES.read_text(encoding="utf-8"))
        candidates += [(case["id"], case["expected_query"]) for case in payload["cases"] if case["type"] == "search"]
        for path in sorted((ROOT / "scripts").glob("retest_*.py")):
            module = load_module(path, path.stem + "_static_queries")
            cases = getattr(module, "CASES", [])
            cases += [case for group in getattr(module, "CASE_GROUPS", []) for case in group["cases"]]
            cases += list(getattr(module, "CONTEXTS", {}).values())
            for case in cases:
                if isinstance(case, dict) and "query" in case and case.get("command", "search") == "search":
                    candidates.append((str(case.get("id")), case["query"]))
            initial = getattr(module, "INITIAL_QUERY", None)
            if initial:
                candidates.append((path.name, initial))
        self.assertGreater(len(candidates), 20)
        for name, query in candidates:
            with self.subTest(case=name):
                self.assertFalse(set(query) & {"keywords", "keywordsSearchType", "matchScopes", "procurementMethod"})
                try:
                    runtime.normalize_project_search_query(query)
                except runtime.SkillError as exc:
                    self.assertEqual(exc.code, "AREA_SCOPE_UNSUPPORTED")
                    self.assertTrue(query.get("areaIds"))
                    runtime.normalize_project_search_query({k:v for k,v in query.items() if k != "areaIds"})

    def test_live_validator_dispatches_and_rejects_wrong_routes(self) -> None:
        module = load_module(LIVE_VALIDATE, "live_validate_for_route_test")
        case = {
            "type": "purchase_intention",
            "expected_command": "search-purchase",
            "expected_capability": "search-purchase-intentions",
            "expected_api_path": "/api/search/purchase",
            "expected_result_type": "purchase_intention",
            "expected_query": {"keywords": ["数字化"]},
        }

        self.assertEqual(module.search_case_args(case)[:1], ["search-purchase"])
        ok, note = module.route_matches_expected(
            case,
            actual_command="search",
            payload={
                "capability": "search-projects",
                "result_type": "project",
                "request_api_path": "/api/search",
            },
        )
        self.assertFalse(ok)
        self.assertIn("命令", note)
        self.assertIn("接口路径", note)

    def test_live_report_declares_host_agent_route_boundary(self) -> None:
        module = load_module(LIVE_VALIDATE, "live_validate_for_report_boundary_test")
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            module.write_report(
                report,
                cases_payload={"current_date": "2026-04-15"},
                entries=[],
                passed=0,
                total=0,
                quota=None,
            )
            content = report.read_text(encoding="utf-8")

        self.assertIn("宿主 Agent 自主路由未验证", content)
        self.assertIn(
            "复杂查询完成率需使用答案隔离的三轮 Host Agent 新旧对照证明；本脚本只验证运行时契约，不能替代该证据。",
            content,
        )

    def test_legacy_acceptance_scripts_do_not_use_project_stage_99(self) -> None:
        paths = [
            ROOT / "scripts" / "retest_procurement_intention.py",
            ROOT / "scripts" / "retest_semantic_fields.py",
            ROOT / "scripts" / "retest_all_search_fields.py",
            ROOT / "scripts" / "retest_detail_followups.py",
        ]
        pattern = re.compile(r'"infoTypes"\s*:\s*\{\s*"99"')

        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")))

    def test_semantic_retest_marks_visible_mismatches_as_failure(self) -> None:
        module = load_module(SEMANTIC_RETEST, "semantic_retest_for_failure_test")
        result = module.visible_checks(
            {
                "keywords": ["数字化"],
                "excludeWords": ["运维"],
                "infoTypes": {"0": []},
                "beginAmount": 1000000,
            },
            [
                {
                    "title": "物业服务公告",
                    "purchasingUnit": "某单位",
                    "areaName": "北京",
                    "infoType": "中标公告",
                    "budgetAmount": "500000",
                }
            ],
        )

        self.assertFalse(result["通过"])

    def test_detail_retest_fails_when_any_case_is_not_executed(self) -> None:
        module = load_module(DETAIL_RETEST, "detail_retest_for_exit_gate_test")
        results = [
            {"后端返回准确性": {"符合预期": True}}
            for _ in range(7)
        ]
        results.append({"未执行原因": "前置能力路由不正确。"})

        self.assertEqual(module.validation_exit_code(results, expected_count=8), 1)

    def test_purchase_and_expiring_page_fixtures_share_one_pagination_baseline(self) -> None:
        pairs = [
            ("search_purchase_page_1.json", "search_purchase_page_2.json", 3, 2),
            ("search_expiring_page_1.json", "search_expiring_page_2.json", 2, 2),
        ]

        for first_name, second_name, row_count, page_count in pairs:
            with self.subTest(first=first_name):
                first = json.loads((FIXTURES / first_name).read_text(encoding="utf-8"))["data"]
                second = json.loads((FIXTURES / second_name).read_text(encoding="utf-8"))["data"]
                self.assertEqual(first["rowCount"], row_count)
                self.assertEqual(second["rowCount"], row_count)
                self.assertEqual(first["pageCount"], page_count)
                self.assertEqual(second["pageCount"], page_count)

    def test_release_package_matches_route_baseline_source_files(self) -> None:
        critical_paths = [
            "SKILL.md",
            "scripts/qianlima_skill.py",
            "scripts/complex_query_plan.py",
            "scripts/live_validate.py",
            "scripts/package_skill.py",
            "scripts/retest_procurement_intention.py",
            "scripts/retest_semantic_fields.py",
            "scripts/retest_all_search_fields.py",
            "scripts/retest_detail_followups.py",
            "tests/live_validation_cases.json",
            "tests/test_qianlima_skill.py",
            "tests/test_validation_baselines.py",
            "tests/test_api_v3.py",
            "tests/test_wallet_v3.py",
            "tests/test_docs_v3.py",
            "tests/test_complex_query_v3.py",
            "tests/protocol_migration.py",
            "references/api-project-resources.md",
            "references/api-entitlement.md",
            "references/api-enterprise-intel.md",
            "references/capabilities/enterprise-intelligence.md",
            "tests/fixtures/fullText_101.json",
            "tests/fixtures/attachments_101.json",
            "tests/fixtures/timeline_101.json",
            "tests/fixtures/entitlement.json",
            "tests/fixtures/search_purchase_page_1.json",
            "tests/fixtures/search_expiring_page_1.json",
            "references/enums.md",
            "references/area.json",
            "tests/test_area_flat.py",
            "tests/test_area_granularity.py",
            "scripts/area_resolver.py",
            "references/api.md",
            "references/capabilities/project-search.md",
            "references/capabilities/purchase-intentions.md",
            "references/capabilities/expiring-projects.md",
            "references/capabilities/query-strategy.md",
            "references/capabilities/follow-up-and-results.md",
            "references/execution-patterns.md",
            "references/nl_parsing_examples.md",
            "references/usage-examples.md",
            "references/api-purchase-intentions.md",
        ]

        if not RELEASE_PACKAGE.exists():
            self.skipTest("未指定候选包且外层候选路径不存在，包一致性在交付轮次单独校验。")
        with zipfile.ZipFile(RELEASE_PACKAGE) as archive:
            # Account changes must be present in the candidate as well as routing.
            critical_paths += [
                "scripts/qianlima_account.py",
                "references/account-access.md",
                "references/credential-configuration.md",
                "references/faq.md",
                "tests/test_account_key_output.py",
            ]
            # Text-only onboarding must not ship dormant card instructions or tools.
            for relative in (
                "references/registration-cards.md", "scripts/render_registration_card.py",
                "assets/phone.html", "tests/test_registration_cards.py",
                "tests/test_registration_cards.cjs",
            ):
                self.assertNotIn(f"{ROOT.name}/{relative}", archive.namelist())
            manifest = json.loads(archive.read(f"{ROOT.name}/manifest.json"))
            for script in manifest["runtime"]["scripts"]:
                self.assertIn(f"{ROOT.name}/{script}", archive.namelist())
            for relative in critical_paths:
                archived = f"{ROOT.name}/{relative}"
                with self.subTest(path=relative):
                    self.assertEqual(archive.read(archived), (ROOT / relative).read_bytes())

    def test_release_package_has_no_conflicting_district_expansion_rules(self) -> None:
        if not RELEASE_PACKAGE.exists():
            self.skipTest("发布包不存在，仅在发布目录校验安装内容。")

        with zipfile.ZipFile(RELEASE_PACKAGE) as archive:
            markdown_text = "\n".join(
                archive.read(name).decode("utf-8")
                for name in archive.namelist()
                if name.endswith(".md")
            )

        for forbidden in (
            "查询时按市级或省级范围保障召回",
            "不传区/县级 ID",
            "上收地区",
            "地区上收",
        ):
            self.assertNotIn(forbidden, markdown_text)
        for phrase in ("区县第一次只查区县", "零结果需用户同意", "未回复或已有结果时不扩大", "其他条件不变"):
            self.assertIn(phrase, markdown_text)
        self.assertIn("keywordGroups", markdown_text)
        self.assertIn("组内 OR", markdown_text)
        self.assertIn("组间 AND", markdown_text)


if __name__ == "__main__":
    unittest.main()
