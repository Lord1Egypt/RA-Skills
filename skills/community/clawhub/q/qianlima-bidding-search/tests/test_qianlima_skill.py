from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import importlib.util
import re
import shutil
import datetime as dt
import uuid
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from protocol_migration import cli_args, project_query, query_field


ROOT = Path(__file__).resolve().parents[1]
SKILL_DOC = ROOT / "SKILL.md"
MANIFEST = ROOT / "manifest.json"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
SCRIPT = ROOT / "scripts" / "qianlima_skill.py"
COMPLEX_PLAN_MODULE = ROOT / "scripts" / "complex_query_plan.py"
API_REF = ROOT / "references" / "api.md"
ACCOUNT_REF = ROOT / "references" / "account-access.md"
ENTITLEMENT_REF = ROOT / "references" / "api-entitlement.md"
FAQ_REF = ROOT / "references" / "faq.md"
ENTERPRISE_REF = ROOT / "references" / "api-enterprise-intel.md"
LIVE_VALIDATE = ROOT / "scripts" / "live_validate.py"
PACKAGE_SCRIPT = ROOT / "scripts" / "package_skill.py"
FIXTURES = ROOT / "tests" / "fixtures"
ERROR_FIXTURES = ROOT / "tests" / "fixtures" / "search_error"
EMPTY_FIXTURES = ROOT / "tests" / "fixtures" / "search_empty"
ENTITLEMENT_ERROR_FIXTURES = ROOT / "tests" / "fixtures" / "search_entitlement_error"
ENTITLEMENT_ERROR_NO_DIAG_FIXTURES = ROOT / "tests" / "fixtures" / "search_entitlement_error_no_diagnosis"
ABNORMAL_EMPTY_FIXTURES = ROOT / "tests" / "fixtures" / "search_abnormal_empty"
LIVE_CASES = ROOT / "tests" / "live_validation_cases.json"
NL_EXAMPLES = ROOT / "references" / "nl_parsing_examples.md"
EXECUTION_PATTERNS = ROOT / "references" / "execution-patterns.md"
USAGE_EXAMPLES = ROOT / "references" / "usage-examples.md"
QUERY_STRATEGY = ROOT / "references" / "capabilities" / "query-strategy.md"
PROJECT_CAPABILITY_REF = ROOT / "references" / "capabilities" / "project-search.md"
FOLLOW_UP_REF = ROOT / "references" / "capabilities" / "follow-up-and-results.md"
DOC_FILES = [
    SKILL_DOC,
    API_REF,
    ACCOUNT_REF,
    ENTITLEMENT_REF,
    FAQ_REF,
    ROOT / "references" / "api-projects.md",
    ROOT / "references" / "api-purchase-intentions.md",
    ROOT / "references" / "api-expiring-projects.md",
    ENTERPRISE_REF,
    ROOT / "references" / "enums.md",
    NL_EXAMPLES,
    EXECUTION_PATTERNS,
    USAGE_EXAMPLES,
]

EXPECTED_SKILL_DESCRIPTION = (
    "当用户查询以下招投标数据时使用本 Skill：中标数据、中标公告、中标项目、中标结果、成交公告、成交结果、候选人公示、查标讯、招标项目、采购意向、临期项目、合同快到期、临期续约机会、某公司/某企业中标项目、企业合作供应商、合作甲方、采购/中标地区分布、直接或潜在竞争对手、企业工商信息、企业联系人、企业电话；"
    "当用户追问当前结果详情时也使用：普通项目和临期项目支持联系人、截止时间、标的物、金额、代理机构、详情页或原文；采购意向支持预算、预计采购时间、采购需求和详情页；"
    "当用户查询当前账号版本、服务地区、已开通权益、已用额度、剩余额度或权益重置时间时也使用。"
    "仅在需要调用项目、采购意向、临期项目、企业情报或当前权益接口查询事实时使用；不要凭模型记忆回答。"
)
EXPECTED_DISPLAY_NAME = "招投标商机情报（千里马）"
EXPECTED_BASE_URL = "https://skills.qianlima.com"


def subtract_one_month(value: dt.date) -> dt.date:
    month_index = value.month - 2
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return value.replace(year=year, month=month, day=min(value.day, month_lengths[month - 1]))


class QianlimaSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self._follow_up_by_state: dict[str, dict[str, str]] = {}
        credentials = mock.patch.dict(os.environ, {"QIANLIMA_API_KEY": "offline-regression-key"})
        credentials.start()
        self.addCleanup(credentials.stop)

    def complex_project_plan(self) -> dict:
        return {
            "conditions": [
                {
                    "id": "c1",
                    "type": "keyword",
                    "source": "user_explicit",
                    "value": ["物业"],
                    "normalized": {"project": {"keywords": ["物业"]}},
                    "applies_to": ["project"],
                },
                {
                    "id": "c2",
                    "type": "amount_min",
                    "source": "user_explicit",
                    "value": 5000000,
                    "normalized": {"project": {"beginAmount": 5000000}},
                    "applies_to": ["project"],
                },
            ],
            "logic_groups": [
                {"id": "root", "operator": "AND", "condition_ids": ["c1", "c2"]}
            ],
            "root_group_id": "root",
            "operations": [
                {
                    "id": "op1",
                    "action": "search",
                    "data_source": "project",
                    "condition_ids": ["c1", "c2"],
                    "query": {"keywords": ["物业"], "beginAmount": 500},
                }
            ],
            "unresolved_conditions": [],
            "planned_business_calls": 1,
        }

    def test_preflight_complex_repairs_amount_without_business_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "preflight-complex",
                "--plan-json",
                json.dumps(self.complex_project_plan(), ensure_ascii=False),
                state_path=state,
            )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["approved_business_calls"], 1)
        self.assertEqual(payload["approved_operations"][0]["query"]["beginAmount"], 5000000)
        self.assertNotIn("request_query", payload)
        self.assertNotIn("request_api_path", payload)
        self.assertNotIn("user_message", payload)

    def test_preflight_complex_keeps_unspecified_stage_amount_as_one_project_call(self) -> None:
        plan = self.complex_project_plan()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "preflight-complex",
                "--plan-json",
                json.dumps(plan, ensure_ascii=False),
                state_path=state,
            )
        operation = payload["approved_operations"][0]
        self.assertEqual(operation["data_source"], "project")
        self.assertEqual(operation["command"], "search")
        self.assertNotIn("infoTypes", operation["query"])
        self.assertEqual(payload["approved_business_calls"], 1)

    def test_preflight_complex_drops_unrequested_match_scope_from_user_text(self) -> None:
        plan = {
            "conditions": [
                {"id": "c1", "type": "keyword", "value": ["物业"]},
                {"id": "c2", "type": "match_scope", "value": [2, 8]},
            ],
            "operations": [{"id": "op1", "action": "search", "data_source": "project"}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_skill(
                "preflight-complex",
                "--plan-json",
                json.dumps(plan, ensure_ascii=False),
                "--user-text",
                "查北京 500 万以上的物业项目",
                state_path=Path(tmp) / "state.json",
            )

        self.assertTrue(payload["ok"])
        self.assertNotIn("matchScopes", payload["approved_operations"][0]["query"])

    def test_search_removes_match_scope_missing_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "matchScopes": [2, 8]}, ensure_ascii=False),
                "--user-text",
                "查物业项目",
                state_path=Path(tmp) / "state.json",
            )

        self.assertTrue(payload["ok"])
        self.assertNotIn("matchScopes", payload["effective_query"])
        self.assertNotIn("matchScopes", payload["request_query"])

    def test_search_preserves_supplied_match_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "matchScopes": [2, 8, 10]}, ensure_ascii=False),
                "--user-text",
                "查标题和正文都包含物业的项目",
                state_path=Path(tmp) / "state.json",
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'matchScopes'), [2, 8, 10])

    def test_project_id_scope_is_supported_for_expiring_but_not_purchase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expiring = self.run_skill(
                "search-expiring",
                "--query-json",
                json.dumps(
                    {"keywords": ["QLM-2026-001"], "matchScopes": [3]},
                    ensure_ascii=False,
                ),
                "--user-text",
                "查项目 ID QLM-2026-001 的临期项目",
                state_path=Path(tmp) / "expiring.json",
            )
            purchase = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps(
                    {"keywords": ["QLM-2026-001"], "matchScopes": [3]},
                    ensure_ascii=False,
                ),
                "--user-text",
                "查项目 ID QLM-2026-001 的采购意向",
                state_path=Path(tmp) / "purchase.json",
            )

        self.assertTrue(expiring["ok"])
        self.assertEqual(query_field(expiring["request_query"], 'matchScopes'), [3])
        self.assertFalse(purchase["ok"])
        self.assertEqual(purchase["error_code"], "AGENT_QUERY_CORRECTION_REQUIRED")


    def test_preflight_complex_accepts_compact_semantic_plan(self) -> None:
        plan = {
            "current_date": "2026-04-15",
            "conditions": [
                {"id": "c1", "type": "keyword", "value": ["设备"]},
                {"id": "c2", "type": "area", "value": [2]},
                {
                    "id": "c3",
                    "type": "planned_purchase_date",
                    "value": {"relative": "future_months", "count": 3},
                },
            ],
            "operations": [
                {"id": "op1", "action": "search", "data_source": "purchase_intention"}
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.run_skill(
                "preflight-complex",
                "--plan-json",
                json.dumps(plan, ensure_ascii=False),
                state_path=Path(tmp) / "state.json",
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["approved_business_calls"], 1)
        self.assertEqual(
            payload["approved_operations"][0]["query"],
            {
                "keywords": ["设备"],
                "areaIds": [2],
                "startPlanPurchaseDate": "2026-05",
                "endPlanPurchaseDate": "2026-07",
                "currentPage": 1,
                "numPerPage": 30,
            },
        )

    def test_manifest_declares_complex_preflight_runtime_dependency(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertIn("scripts/complex_query_plan.py", manifest["runtime"]["scripts"])

    def test_preflight_complex_refine_uses_current_result_type_without_calling_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search-expiring",
                "--query-json",
                json.dumps(
                    {"keywords": ["物业"], "areaIds": [2805], "numPerPage": 1},
                    ensure_ascii=False,
                ),
                state_path=state,
            )
            plan = {
                "conditions": [
                    {
                        "id": "c1",
                        "type": "contract_amount_min",
                        "source": "user_explicit",
                        "value": 5000000,
                        "normalized": {
                            "expiring_project": {"beginContractAmount": 5000000}
                        },
                        "applies_to": ["expiring_project"],
                    },
                    {
                        "id": "c2",
                        "type": "preserve_area",
                        "source": "user_explicit",
                        "value": "地区不变",
                        "normalized": {"expiring_project": {}},
                        "applies_to": ["expiring_project"],
                    },
                ],
                "logic_groups": [
                    {"id": "root", "operator": "AND", "condition_ids": ["c1", "c2"]}
                ],
                "root_group_id": "root",
                "operations": [
                    {
                        "id": "op1",
                        "action": "refine",
                        "data_source": "expiring_project",
                        "condition_ids": ["c1", "c2"],
                        "session_id": first["follow_up"]["session_id"],
                        "result_set_id": first["follow_up"]["result_set_id"],
                        "query": {"beginAmount": 5000000, "areaIds": [305]},
                    }
                ],
                "unresolved_conditions": [],
                "planned_business_calls": 1,
            }
            payload = self.run_skill(
                "preflight-complex",
                "--plan-json",
                json.dumps(plan, ensure_ascii=False),
                state_path=state,
            )
        operation = payload["approved_operations"][0]
        self.assertEqual(operation["query"], {"beginContractAmount": 5000000})
        self.assertEqual(operation["data_source"], "expiring_project")
        self.assertNotIn("request_api_path", payload)

    def test_simple_search_command_remains_direct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "beginAmount": 5000000}, ensure_ascii=False),
                state_path=state,
            )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["request_api_path"], "/api/search")
        self.assertNotIn("complex_preflight", payload)

    def _state_dir_for_test(self, state_path: Path) -> Path:
        return state_path.parent / f"{state_path.name}.state"

    def _session_id_for_test(self, state_path: Path) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, str(state_path.resolve())))

    def prepare_test_args(self, args: tuple[str, ...], state_path: Path) -> list[str]:
        command = args[0]
        prepared = list(args)
        context = self._follow_up_by_state.get(str(state_path))
        if command in {"search", "search-purchase", "search-expiring"} and "--session-id" not in prepared:
            session_id = (context or {}).get("session_id") or self._session_id_for_test(state_path)
            prepared[1:1] = ["--session-id", session_id]
        elif command in {"next", "refine", "detail"} and "--session-id" not in prepared and context:
            prepared[1:1] = [
                "--session-id",
                context["session_id"],
                "--result-set-id",
                context["result_set_id"],
            ]
        return prepared

    def record_test_follow_up(self, state_path: Path, payload: dict) -> None:
        follow_up = payload.get("follow_up")
        if isinstance(follow_up, dict) and follow_up.get("session_id") and follow_up.get("result_set_id"):
            self._follow_up_by_state[str(state_path)] = {
                "session_id": str(follow_up["session_id"]),
                "result_set_id": str(follow_up["result_set_id"]),
            }

    def current_snapshot_path(self, state_path: Path) -> Path:
        context = self._follow_up_by_state[str(state_path)]
        return self._state_dir_for_test(state_path) / context["session_id"] / f"{context['result_set_id']}.json"

    def entitlement_profile(
        self,
        *,
        version_name: str,
        version_status: str,
        expire_time: str | None,
        rights: list[dict],
        area: str = "北京",
    ) -> dict:
        return {
            "version": {
                "name": version_name,
                "status": version_status,
                "subscribeTime": "2026-07-09 16:28:29",
                "expireTime": expire_time,
            },
            "area": area,
            "rights": rights,
        }

    def entitlement_right(
        self,
        name: str,
        *,
        status: str = "可用",
        period: str = "每日",
        total: int | str | None = 100,
        used: int | None = 0,
        remaining: int | str | None = 100,
        unit: str = "次",
        reset_at: str | None = "2026-07-15 00:00:00",
    ) -> dict:
        return {
            "name": name,
            "status": status,
            "period": period,
            "total": total,
            "used": used,
            "remaining": remaining,
            "unit": unit,
            "resetAt": reset_at,
        }

    def heading_titles(self, text: str, level: int) -> list[str]:
        return re.findall(rf"^{'#' * level} (.+)$", text, re.M)

    def assert_markdown_link(self, message: str, label: str, expected_url: str) -> None:
        match = re.search(rf"\[{re.escape(label)}\]\(([^)]+)\)", message)
        self.assertIsNotNone(match, f"缺少可点击链接：{label}")
        assert match is not None
        self.assertEqual(match.group(1), expected_url)

    def assert_url_only_appears_as_link_target(self, message: str, url: str) -> None:
        self.assertIn(url, message)
        visible_text = re.sub(r"\[[^\]]+\]\([^)]+\)", "", message)
        self.assertNotIn(url, visible_text)

    def run_skill(self, *args: str, state_path: Path) -> dict:
        env = os.environ.copy()
        env["QIANLIMA_MOCK_DIR"] = str(FIXTURES)
        env["QIANLIMA_SKILL_STATE_DIR"] = str(self._state_dir_for_test(state_path))
        env.pop("QIANLIMA_SKILL_STATE", None)
        prepared_args = cli_args(self.prepare_test_args(args, state_path), self._state_dir_for_test(state_path))
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *prepared_args],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise AssertionError(proc.stdout + proc.stderr) from exc
        if proc.returncode != 0:
            raise AssertionError(payload)
        self.record_test_follow_up(state_path, payload)
        return payload

    def run_skill_with_fixtures(self, fixtures: Path, *args: str, state_path: Path) -> tuple[int, dict]:
        env = os.environ.copy()
        env["QIANLIMA_MOCK_DIR"] = str(fixtures)
        env["QIANLIMA_SKILL_STATE_DIR"] = str(self._state_dir_for_test(state_path))
        env.pop("QIANLIMA_SKILL_STATE", None)
        prepared_args = cli_args(self.prepare_test_args(args, state_path), self._state_dir_for_test(state_path))
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *prepared_args],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(proc.stdout)
        self.record_test_follow_up(state_path, payload)
        return proc.returncode, payload

    def run_skill_raw(self, fixtures: Path, *args: str, state_path: Path, extra_env: dict[str, str] | None = None) -> tuple[int, dict]:
        env = os.environ.copy()
        env["QIANLIMA_MOCK_DIR"] = str(fixtures)
        env["QIANLIMA_SKILL_STATE_DIR"] = str(self._state_dir_for_test(state_path))
        env.pop("QIANLIMA_SKILL_STATE", None)
        if extra_env:
            env.update(extra_env)
        prepared_args = cli_args(self.prepare_test_args(args, state_path), self._state_dir_for_test(state_path))
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *prepared_args],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            payload = {"stdout": proc.stdout, "stderr": proc.stderr}
        self.record_test_follow_up(state_path, payload)
        return proc.returncode, payload

    def run_v2_cli(
        self,
        fixtures: Path,
        *args: str,
        state_dir: Path,
        cwd: Path | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> tuple[int, dict]:
        env = os.environ.copy()
        env["QIANLIMA_MOCK_DIR"] = str(fixtures)
        env["QIANLIMA_SKILL_STATE_DIR"] = str(state_dir)
        env.pop("QIANLIMA_SKILL_STATE", None)
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *cli_args(args, state_dir)],
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            payload = {"stdout": proc.stdout, "stderr": proc.stderr}
        return proc.returncode, payload

    def copy_fixtures(self, parent: Path) -> Path:
        fixtures = parent / "fixtures"
        shutil.copytree(FIXTURES, fixtures)
        return fixtures

    def load_runtime_module(self, name: str = "qianlima_skill_contract_tests"):
        spec = importlib.util.spec_from_file_location(name, SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def write_api_error_fixture(self, path: Path, code: str, message: str) -> None:
        path.write_text(
            json.dumps({"code": int(code), "msg": message, "data": {}, "success": False}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )



    def test_parameter_mapping_contract_is_documented_without_user_text_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["空调"], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "北京政府 500 万以上空调中标，不要维修",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["空调"])
        for field in ("areaIds", "beginAmount", "infoTypes", "purchasingUnitTypes", "excludeWords"):
            self.assertNotIn(field, payload["effective_query"])
            self.assertNotIn(field, payload["request_query"])

    def test_unspecified_project_stage_amount_uses_one_backend_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "beginAmount": 5000000, "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "查 500 万以上的物业项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["request_query"], 'keywords'), ["物业"])
        self.assertEqual(payload["request_query"]["beginAmount"], 5000000)
        self.assertNotIn("infoTypes", payload["effective_query"])
        self.assertNotIn("infoTypes", payload["request_query"])

    def test_unspecified_stage_amount_calls_project_backend_exactly_once(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill_single_search", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        client = SimpleNamespace(last_request_path=None, last_request_query=None)
        backend_queries: list[dict] = []

        def counting_search(fake_client: SimpleNamespace, query: dict) -> dict:
            backend_queries.append(dict(query))
            fake_client.last_request_path = "/api/search"
            fake_client.last_request_query = dict(query)
            return {"rowCount": 0, "pageCount": 0, "list": []}

        capability = module.SEARCH_CAPABILITIES["project"]
        with tempfile.TemporaryDirectory() as tmp:
            with (
                mock.patch.dict(os.environ, {"QIANLIMA_SKILL_STATE_DIR": str(Path(tmp) / "state")}),
                mock.patch.object(capability, "search_call", counting_search),
                mock.patch.object(module, "build_client", return_value=client),
            ):
                payload = module.run_search(
                    capability,
                    project_query({"keywords": ["物业"], "beginAmount": 5000000}),
                    SimpleNamespace(session_id=str(uuid.uuid4())),
                )

        self.assertTrue(payload["ok"])
        self.assertEqual(len(backend_queries), 1)
        self.assertEqual(query_field(backend_queries[0], "keywords"), ["物业"])
        self.assertEqual(backend_queries[0]["beginAmount"], 5000000)
        self.assertNotIn("infoTypes", backend_queries[0])












    def test_search_capability_registry_declares_shared_contract(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        expected_slots = (
            "result_type",
            "success_stage",
            "stage_label",
            "search_call",
            "detail_call",
            "normalize_query",
            "card_view",
            "list_renderer",
            "message_renderer",
            "refine_aliases",
            "include_stage_on_success",
        )
        self.assertEqual(module.SearchCapabilitySpec.__slots__, expected_slots)
        self.assertEqual(set(module.SEARCH_CAPABILITIES), {"project", "purchase_intention", "expiring_project"})

        expectations = {
            "project": ("search", "detail", (), False),
            "purchase_intention": (
                "search_purchase",
                "purchase_detail",
                (("beginAmount", "startPlanPurchaseAmount"), ("endAmount", "endPlanPurchaseAmount")),
                True,
            ),
            "expiring_project": (
                "search_expiring",
                "expiring_detail",
                (("beginAmount", "beginContractAmount"), ("endAmount", "endContractAmount")),
                True,
            ),
        }
        for result_type, (search_name, detail_name, aliases, include_stage) in expectations.items():
            capability = module.SEARCH_CAPABILITIES[result_type]
            self.assertEqual(capability.result_type, result_type)
            self.assertEqual(capability.search_call.__name__, search_name)
            self.assertEqual(capability.detail_call.__name__, detail_name)
            self.assertEqual(capability.refine_aliases, aliases)
            self.assertEqual(capability.include_stage_on_success, include_stage)
            for attr in ("normalize_query", "card_view", "list_renderer", "message_renderer"):
                self.assertTrue(callable(getattr(capability, attr)), f"{result_type}.{attr} must be callable")

    def test_search_capabilities_share_search_detail_next_refine_flow(self) -> None:
        cases = [
            {
                "command": "search",
                "query": {"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2},
                "first_id": 101,
                "expected_stage": None,
                "source_phrase": "北京学校实验室设备采购中标通知",
                "forbidden_phrase": "采购意向",
                "detail_field": "budgetAmount",
                "amount_field": "beginAmount",
                "amount": 1000000,
            },
            {
                "command": "search-purchase",
                "query": {"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2},
                "first_id": 201,
                "expected_stage": "purchase_intention",
                "source_phrase": "采购意向",
                "forbidden_phrase": "中标通知",
                "detail_field": "purchaseContent",
                "amount_field": "startPlanPurchaseAmount",
                "amount": 1000000,
            },
            {
                "command": "search-expiring",
                "query": {"keywords": ["物业"], "areaIds": [305], "numPerPage": 1},
                "first_id": 301,
                "expected_stage": "expiring_project",
                "source_phrase": "临期项目",
                "forbidden_phrase": "中标通知",
                "detail_field": "contractAmount",
                "amount_field": "beginContractAmount",
                "amount": 2000000,
            },
        ]
        for case in cases:
            with self.subTest(command=case["command"]):
                with tempfile.TemporaryDirectory() as tmp:
                    state = Path(tmp) / "state.json"
                    first = self.run_skill(
                        case["command"],
                        "--query-json",
                        json.dumps(case["query"], ensure_ascii=False),
                        state_path=state,
                    )
                    detail = self.run_skill(
                        "detail",
                        "--project-ref",
                        "第1条",
                        "--fields",
                        case["detail_field"],
                        state_path=state,
                    )
                    next_page = self.run_skill("next", state_path=state)
                    refined = self.run_skill(
                        "refine",
                        "--query-json",
                        json.dumps({"beginAmount": case["amount"]}, ensure_ascii=False),
                        state_path=state,
                    )

                self.assertTrue(first["ok"])
                self.assertEqual(first["cards"][0]["id"], case["first_id"])
                if case["expected_stage"] is None:
                    self.assertNotIn("stage", first)
                    self.assertNotIn("stage", next_page)
                else:
                    self.assertEqual(first["stage"], case["expected_stage"])
                    self.assertEqual(next_page["stage"], case["expected_stage"])
                    self.assertEqual(refined["stage"], case["expected_stage"])

                self.assertTrue(detail["ok"])
                self.assertEqual(detail["resolution"]["method"], "ordinal")
                self.assertEqual(detail["full_detail"]["id"], case["first_id"])
                self.assertIn(case["detail_field"], detail["detail"])
                self.assertEqual(next_page["effective_query"]["currentPage"], 2)
                self.assertIn(case["source_phrase"], next_page["user_message"])
                self.assertNotIn(case["forbidden_phrase"], next_page["user_message"])
                self.assertEqual(refined["effective_query"][case["amount_field"]], case["amount"])
                self.assertEqual(refined["request_query"][case["amount_field"]], case["amount"])
                if case["amount_field"] != "beginAmount":
                    self.assertNotIn("beginAmount", refined["effective_query"])
                    self.assertNotIn("beginAmount", refined["request_query"])

    def test_search_purchase_intentions_returns_business_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stage"], "purchase_intention")
        self.assertEqual(payload["total_count"], 3)
        self.assertEqual(payload["page_count"], 2)
        self.assertEqual(payload["cards"][0]["id"], 201)
        self.assertIn("采购意向", payload["user_message"])
        self.assertIn("北京市第一医院实验室设备采购意向公告", payload["user_message"])
        self.assertIn("北京市第一医院", payload["user_message"])
        self.assertIn("北京市 / 东城区", payload["user_message"])
        self.assertIn("180.00", payload["user_message"])
        self.assert_markdown_link(payload["user_message"], "查看详情", "https://www.qianlima.com/purchase-201.html")
        self.assertIn("2026-08", payload["user_message"])
        self.assertNotIn("联系电话", payload["user_message"])

    def test_search_purchase_requires_non_empty_keywords_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps({"keywords": ["  ", ""], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertNotIn("request_query", payload)
        self.assertIn("关键词不能为空", payload["user_message"])

    def test_search_expiring_projects_returns_renewal_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search-expiring",
                "--query-json",
                json.dumps({"keywords": ["物业"], "areaIds": [305], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stage"], "expiring_project")
        self.assertEqual(payload["cards"][0]["id"], 301)
        self.assertIn("临期项目", payload["user_message"])
        self.assertIn("深圳市某区机关物业服务合同公告", payload["user_message"])
        self.assertIn("深圳市某区机关事务管理局", payload["user_message"])
        self.assertIn("广东省 / 深圳市 / 福田区", payload["user_message"])
        self.assertIn("360.00", payload["user_message"])
        self.assert_markdown_link(payload["user_message"], "查看详情", "https://www.qianlima.com/expiring-301.html")
        self.assertIn("2026-11-30", payload["user_message"])
        self.assertIn("深圳市城市服务有限公司", payload["user_message"])

    def test_search_expiring_requires_non_empty_keywords_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search-expiring",
                "--query-json",
                json.dumps({"numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertNotIn("request_query", payload)
        self.assertIn("关键词不能为空", payload["user_message"])

    def test_enterprise_intel_contacts_is_explicit_paid_followup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "enterprise",
                "--kind",
                "contacts",
                "--query-json",
                json.dumps({"companyName": "深圳市城市服务有限公司", "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stage"], "enterprise_contacts")
        self.assertTrue(payload["paid_sensitive"])
        self.assertEqual(
            payload["effective_query"],
            {"companyName": "深圳市城市服务有限公司", "numPerPage": 2, "currentPage": 1},
        )
        self.assertEqual(payload["request_query"], payload["effective_query"])
        self.assertEqual(payload["warnings"], [])
        self.assertIn("企业联系电话", payload["user_message"])
        self.assertIn("张经理", payload["user_message"])
        self.assertIn("手机", payload["user_message"])
        self.assertIn("13800000000", payload["user_message"])
        enterprise_capability = (
            ROOT / "references" / "capabilities" / "enterprise-intelligence.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "企业联系电话属于高敏付费数据；只在用户明确索要联系人、电话或联系方式时调用",
            enterprise_capability,
        )

    def test_enterprise_intel_all_kinds_have_fixture_backed_outputs(self) -> None:
        company_name = "深圳市城市服务有限公司"
        cases = [
            {
                "kind": "partners",
                "query": {"companyName": company_name, "sortType": "2"},
                "stage": "enterprise_partners",
                "row_key": "companyName",
                "row_value": "深圳市绿城物业服务有限公司",
                "message_parts": ["合作供应商", "深圳市绿城物业服务有限公司", "合作次数", "12", "368.00"],
                "warnings": ["未传时间参数，企业情报接口默认按近一年查询。"],
            },
            {
                "kind": "principals",
                "query": {"companyName": company_name, "beginTime": "2026-01-01", "endTime": "2026-12-31"},
                "stage": "enterprise_principals",
                "row_key": "companyName",
                "row_value": "深圳市某区机关事务管理局",
                "message_parts": ["合作甲方", "深圳市某区机关事务管理局", "合作次数", "5", "820.00"],
                "warnings": [],
            },
            {
                "kind": "area-distribution",
                "query": {"companyName": company_name},
                "stage": "enterprise_area_distribution",
                "row_key": "areaName",
                "row_value": "广东省 / 深圳市",
                "message_parts": ["采购地区分布", "广东省 / 深圳市", "次数", "18", "960.00"],
                "warnings": ["未传时间参数，企业情报接口默认按近一年查询。"],
            },
            {
                "kind": "winning-area-distribution",
                "query": {"companyName": company_name, "beginTime": "2026-01-01", "endTime": "2026-12-31"},
                "stage": "enterprise_winning_area_distribution",
                "row_key": "areaName",
                "row_value": "广东省 / 深圳市",
                "message_parts": ["中标地区分布", "广东省 / 深圳市", "次数", "7", "430.00"],
                "warnings": [],
            },
            {
                "kind": "co-bidder-competitors",
                "query": {"companyName": company_name},
                "stage": "enterprise_co_bidder_competitors",
                "row_key": "competitorName",
                "row_value": "深圳市鹏城物业管理有限公司",
                "message_parts": ["直接竞争对手", "深圳市鹏城物业管理有限公司", "同场竞标次数", "9", "中标次数", "3", "210.00", "高级"],
                "warnings": ["未传时间参数，企业情报接口默认按近一年查询。"],
            },
            {
                "kind": "potential-competitors",
                "query": {"companyName": company_name},
                "stage": "enterprise_potential_competitors",
                "row_key": "competitorName",
                "row_value": "广东城服科技有限公司",
                "message_parts": ["潜在竞争对手", "广东城服科技有限公司", "中标次数", "4", "180.00", "中级"],
                "warnings": ["未传时间参数，企业情报接口默认按近一年查询。"],
            },
            {
                "kind": "business-info",
                "query": {"companyName": company_name},
                "stage": "enterprise_business_info",
                "row_key": "name",
                "row_value": company_name,
                "message_parts": ["工商信息", "经营状态：存续", "法定代表人：王某某", "注册资本：5000万元"],
                "warnings": [],
            },
            {
                "kind": "contacts",
                "query": {"companyName": company_name},
                "stage": "enterprise_contacts",
                "row_key": "linkMan",
                "row_value": "张经理",
                "message_parts": ["企业联系电话", "张经理", "电话类型", "手机", "联系电话", "13800000000"],
                "warnings": [],
                "paid_sensitive": True,
                "expected_query": {"companyName": company_name, "currentPage": 1, "numPerPage": 30},
            },
        ]

        for case in cases:
            with self.subTest(kind=case["kind"]):
                with tempfile.TemporaryDirectory() as tmp:
                    state = Path(tmp) / "state.json"
                    payload = self.run_skill(
                        "enterprise",
                        "--kind",
                        case["kind"],
                        "--query-json",
                        json.dumps(case["query"], ensure_ascii=False),
                        state_path=state,
                    )

                expected_query = case.get("expected_query", case["query"])
                if "sortType" in expected_query:
                    expected_query = {**expected_query, "sortType": int(expected_query["sortType"])}
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["stage"], case["stage"])
                self.assertEqual(payload["paid_sensitive"], case.get("paid_sensitive", False))
                self.assertEqual(payload["effective_query"], expected_query)
                self.assertEqual(payload["request_query"], expected_query)
                self.assertEqual(payload["warnings"], case["warnings"])
                self.assertGreaterEqual(payload["returned_count"], 1)
                self.assertEqual(payload["rows"][0][case["row_key"]], case["row_value"])
                for message_part in case["message_parts"]:
                    self.assertIn(message_part, payload["user_message"])











    def test_entitlement_uses_get_without_query_parameters(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        client = module.ApiClient("https://skills.qianlima.com", "dummy")
        captured: dict[str, object] = {}

        def capture_request(method: str, path: str, query=None) -> dict:
            captured.update({"method": method, "path": path, "query": query})
            return {"version": {}, "area": "", "rights": []}

        client._request = capture_request
        client.entitlement()

        self.assertEqual(captured, {"method": "GET", "path": "/api/user/entitlement", "query": None})

    def test_entitlement_mapping_covers_all_nine_rights(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cases = {
            ("search", "project", None): "标讯查询",
            ("detail", "project", None): "标讯详情",
            ("search", "purchase_intention", None): "采购意向查询",
            ("detail", "purchase_intention", None): "采购意向详情",
            ("search", "expiring_project", None): "临期项目查询",
            ("detail", "expiring_project", None): "临期项目详情",
            ("enterprise", None, "partners"): "企业情报",
            ("source_url", "project", None): "源网址",
            ("enterprise", None, "contacts"): "企业联系电话",
        }
        for (operation, result_type, enterprise_kind), expected in cases.items():
            with self.subTest(operation=operation, result_type=result_type, enterprise_kind=enterprise_kind):
                self.assertEqual(
                    module.entitlement_right_name(
                        operation=operation,
                        result_type=result_type,
                        enterprise_kind=enterprise_kind,
                    ),
                    expected,
                )













    def test_missing_api_key_has_user_friendly_message(self) -> None:
        env = os.environ.copy()
        env.pop("QIANLIMA_API_KEY", None)
        env["QIANLIMA_SKILL_STATE_DIR"] = str(Path(tempfile.gettempdir()) / "qianlima_missing_key_test_state")
        env.pop("QIANLIMA_SKILL_STATE", None)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "verify"],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(proc.stdout)

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "MISSING_API_KEY")
        self.assertIn("[前往官网](https://ai.qianlima.com/?source=bb3b4102f584028c3830df37)", payload["user_message"])
        self.assertIn("使用账号积分", payload["user_message"])
        self.assertNotIn("注册流程", payload["user_message"])

    def test_invalid_api_key_has_user_friendly_message(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        message = module.permission_user_message(module.SkillError("10001", "无效KEY"), "verify")

        self.assertIn("API Key", message)
        self.assertIn("没有通过验证", message)
        self.assertIn("手机号验证码登录后重新配置", message)
        self.assertIn("https://ai.qianlima.com/?source=bb3b4102f584028c3830df37", message)
        self.assertNotIn("千里马官网", message)
        self.assertNotIn("www.qianlima.com", message)
        self.assertIn("提供其他 API Key", message)
        self.assertNotIn("Skill 配置入口", message)
        self.assertNotIn("无效KEY", message)


    def test_http_429_is_classified_as_rate_limit_without_raw_http_details(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def raise_http_429(*_args, **_kwargs):
            raise module.urllib.error.HTTPError(
                "https://skills.qianlima.com/api/search",
                429,
                "Too Many Requests",
                {},
                None,
            )

        original_urlopen = module.urllib.request.urlopen
        module.urllib.request.urlopen = raise_http_429
        try:
            client = module.ApiClient("https://skills.qianlima.com", "dummy")
            with self.assertRaises(module.SkillError) as ctx:
                client.search(project_query({"keywords": ["实验室设备"], "currentPage": 1, "numPerPage": 30}))
        finally:
            module.urllib.request.urlopen = original_urlopen

        self.assertEqual(ctx.exception.code, "429")
        payload = module.failure_payload(
            stage="search",
            error=ctx.exception,
            effective_query={"keywords": ["实验室设备"]},
        )
        self.assertIn("请求有点频繁", payload["user_message"])
        self.assertIn("不要连续重复提交同一个查询", payload["user_message"])
        self.assertIn("减少每次查询的数据量", payload["user_message"])
        self.assertNotIn("HTTP 429", payload["user_message"])
        self.assertNotIn("Too Many Requests", payload["user_message"])
        self.assert_public_error_text_is_safe(payload)

    def assert_public_error_text_is_safe(self, payload: dict) -> None:
        public_text = "\n".join(
            [
                str(payload.get("message", "")),
                str(payload.get("user_message", "")),
                "；".join(str(item) for item in payload.get("warnings", [])),
            ]
        )
        for forbidden in (
            "Traceback",
            "JSONDecodeError",
            "line 1 column",
            "搜索接口参数异常",
            "Connection refused",
            "HTTP 500",
            "Internal Server Error",
            "badField",
            "keywords",
            "excludeWords",
        ):
            self.assertNotIn(forbidden, public_text)
        self.assertIn("user_message", payload)
        self.assertTrue(payload["user_message"].strip())

    def test_malformed_query_json_returns_structured_user_safe_error(self) -> None:
        commands = [
            ["search", "--query-json", "{not-json}", "--user-text", "查北京实验室设备项目"],
            ["search-purchase", "--query-json", "{not-json}", "--user-text", "查北京实验室设备采购意向"],
            ["search-expiring", "--query-json", "{not-json}", "--user-text", "查深圳物业临期项目"],
            ["enterprise", "--kind", "contacts", "--query-json", "{not-json}"],
        ]
        for args in commands:
            with self.subTest(command=args[0]), tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp) / "state.json"
                code, payload = self.run_skill_raw(FIXTURES, *args, state_path=state)

            self.assertEqual(code, 2)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error_code"], "INVALID_JSON")
            self.assertIn("查询条件格式不正确", payload["user_message"])
            self.assertIn("重新发起查询", payload["user_message"])
            self.assert_public_error_text_is_safe(payload)

        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            self.assertTrue(first["ok"])
            code, payload = self.run_skill_raw(
                FIXTURES,
                "refine",
                "--query-json",
                "{not-json}",
                "--user-text",
                "金额改成 500 万以上",
                state_path=state,
            )

        self.assertEqual(code, 2)
        self.assertEqual(payload["error_code"], "INVALID_JSON")
        self.assertIn("查询条件格式不正确", payload["user_message"])
        self.assert_public_error_text_is_safe(payload)

    def test_backend_parameter_error_is_translated_with_next_steps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(
                ERROR_FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertIn("接口参数异常", payload["user_message"])
        self.assertIn("Agent 按当前接口契约修正参数", payload["user_message"])
        self.assertNotIn("这次查询暂时没有处理成功", payload["user_message"])
        self.assert_public_error_text_is_safe(payload)

    def test_network_and_http_errors_are_translated_without_raw_details(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        errors = [
            module.SkillError("NETWORK_ERROR", "[Errno 61] Connection refused"),
            module.SkillError("HTTP_ERROR", "HTTP 500: Internal Server Error"),
        ]
        for error in errors:
            with self.subTest(error_code=error.code):
                payload = module.failure_payload(stage="search", error=error, effective_query={"keywords": ["实验室设备"]})

            self.assertIn("数据服务暂时不可用", payload["user_message"])
            self.assertIn("稍后重试", payload["user_message"])
            self.assertIn("确认本地网络可用", payload["user_message"])
            self.assertIn("登录 https://ai.qianlima.com/?source=bb3b4102f584028c3830df37 检查 API Key", payload["user_message"])
            self.assert_public_error_text_is_safe(payload)

    def test_enterprise_failure_always_has_user_message(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        payload = module.failure_payload(
            stage="enterprise",
            error=module.SkillError("MOCK_FILE_NOT_FOUND", "缺少 mock 文件：enterprise_contacts.json"),
            effective_query={"companyName": "测试公司"},
        )

        self.assertIn("user_message", payload)
        self.assertIn("稍后重试", payload["user_message"])
        self.assert_public_error_text_is_safe(payload)

    def test_word_list_warnings_do_not_expose_internal_field_names(self) -> None:
        keywords = [f"关键词{i}" for i in range(12)]
        excludes = [f"排除{i}" for i in range(12)]
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": keywords, "excludeWords": excludes, "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        warning_text = "；".join(payload["warnings"])
        self.assertFalse(payload["ok"])
        self.assertIn("排除词最多支持 10 个", warning_text)
        self.assertIn("不能丢弃部分条件", warning_text)
        self.assert_public_error_text_is_safe({"message": "", "warnings": payload["warnings"], "user_message": payload["user_message"]})

    def test_invalid_detail_fields_tell_user_which_details_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            self.assertTrue(first["ok"])
            code, payload = self.run_skill_raw(
                FIXTURES,
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "badField",
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "AGENT_DETAIL_CORRECTION_REQUIRED")
        self.assertTrue(payload["requires_agent_correction"])
        self.assertFalse(payload["requires_user_confirmation"])
        self.assertIn("badField", payload["agent_instruction"])
        self.assertNotIn("不能确定", payload["user_message"])
        self.assert_public_error_text_is_safe(payload)

    def test_bad_field_types_return_user_safe_errors_without_traceback(self) -> None:
        commands = [
            (
                "keywords-number",
                ["search", "--query-json", json.dumps({"keywords": 123, "numPerPage": 2}, ensure_ascii=False)],
                "关键词需要是文字",
            ),
            (
                "exclude-number",
                ["search", "--query-json", json.dumps({"keywords": ["实验室设备"], "excludeWords": 123, "numPerPage": 2}, ensure_ascii=False)],
                "排除词需要是文字",
            ),
            (
                "search-area-invalid",
                ["search", "--query-json", json.dumps({"keywords": ["实验室设备"], "areaIds": ["abc"], "numPerPage": 2}, ensure_ascii=False)],
                "地区编号必须是目录内的正整数",
            ),
            (
                "purchase-area-invalid",
                ["search-purchase", "--query-json", json.dumps({"keywords": ["实验室设备"], "areaIds": ["abc"], "numPerPage": 2}, ensure_ascii=False)],
                "地区编号必须是目录内的正整数",
            ),
        ]
        for name, args, expected in commands:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp) / "state.json"
                code, payload = self.run_skill_raw(FIXTURES, *args, state_path=state)

            self.assertEqual(code, 0)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error_code"], "INVALID_QUERY")
            self.assertIn(expected, payload["user_message"])
            self.assertNotIn("Traceback", json.dumps(payload, ensure_ascii=False))
            self.assert_public_error_text_is_safe(payload)

    def test_search_returns_required_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["total_count"], 3)
        self.assertEqual(payload["returned_count"], 2)
        self.assertEqual(payload["effective_query"]["currentPage"], 1)
        self.assertIn("warnings", payload)
        self.assertEqual(payload["cards"][0]["id"], 101)

    def test_search_user_message_uses_readable_chinese_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        message = payload["user_message"]
        self.assertIn("北京市第一医院实验室设备采购招标公告", message)
        self.assertIn("北京市第一医院", message)
        self.assertIn("北京市 / 东城区", message)
        self.assertIn("2026-04-10", message)
        self.assertIn("招标公告", message)
        self.assertIn("120.00", message)
        self.assertNotIn("中标金额（万元）", message)
        self.assertIn("120.00", message)
        self.assertIn("招标公告", message)
        self.assertNotIn("公告-招标公告", message)
        self.assertIn("[北京市第一医院实验室设备采购招标公告](https://www.qianlima.com/bid-101.html)", message)
        self.assertIn("我按北京", message)
        self.assertNotIn("本次生效条件", message)
        self.assertNotIn("- 关键词：", message)
        self.assertIn("本批最新发布时间", message)
        self.assertIn("您可以继续说", message)
        self.assertNotIn("提醒：无", message)
        for card in payload["cards"]:
            self.assertIn(card["title"], message)

    def test_empty_user_value_displays_as_not_disclosed(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(module.clean_user_value(""), "未公示")
        self.assertEqual(module.format_amount_wan(""), "未公示")
        self.assertEqual(module.format_detail_link(""), "未公示")

    def test_broad_info_type_words_use_parent_stage_names(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(module.info_type_names({"0": []}), ["招标公告"])
        self.assertEqual(module.info_type_names({"3": []}), ["结果公示"])
        self.assertEqual(module.info_type_names({"0": [4]}), ["重新招标"])
        self.assertEqual(module.info_type_names({"3": [11]}), ["中标通知"])
        self.assertEqual(module.info_type_names({"3": [12]}), ["合同公告"])
        self.assertIn("只看结果公示", module.user_query_sentence({"infoTypes": {"3": []}}))

    def test_user_query_sentence_separates_last_condition_from_action(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(
            module.user_query_sentence(
                {
                    "areaIds": [3320],
                    "keywords": ["食堂"],
                    "beginTime": "2026-07-18",
                    "endTime": "2026-07-24",
                }
            ),
            "我按北京市-海淀区，关键词“食堂”，时间 2026-07-18 至 2026-07-24，查询了项目。",
        )

    def test_search_does_not_rewrite_ai_extracted_query_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps(
                    {
                        "keywords": ["学校", "空调"],
                        "areaIds": [24],
                        "infoTypes": {"0": []},
                        "numPerPage": 2,
                    },
                    ensure_ascii=False,
                ),
                "--user-text",
                "北京学校空调中标，不要保洁",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["学校", "空调"])
        self.assertEqual(payload["effective_query"]["areaIds"], [24])
        self.assertEqual(payload["effective_query"]["infoTypes"], {"0": []})
        self.assertNotIn("excludeWords", payload["effective_query"])
        self.assertNotIn("purchasingUnitTypes", payload["effective_query"])
        self.assertNotIn("review_status", payload)
        self.assertNotIn("corrections", payload)

    def test_keywords_search_type_passes_through_when_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps(
                    {"keywords": ["空调", "新风"], "keywordsSearchType": 2, "numPerPage": 2},
                    ensure_ascii=False,
                ),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywordsSearchType'), 2)
        self.assertEqual(query_field(payload["request_query"], 'keywordsSearchType'), 2)
        self.assertIn("关键词需同时命中", payload["user_message"])


    def test_search_does_not_correct_keywords_search_type_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps(
                    {"keywords": ["空调", "新风"], "keywordsSearchType": 2, "numPerPage": 2},
                    ensure_ascii=False,
                ),
                "--user-text",
                "查空调或者新风项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywordsSearchType'), 2)
        self.assertEqual(query_field(payload["request_query"], 'keywordsSearchType'), 2)
        self.assertNotIn("review_status", payload)
        self.assertNotIn("corrections", payload)

    def test_search_does_not_infer_keywords_search_type_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["空调", "安装"], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "找空调安装项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertNotIn("keywordsSearchType", payload["effective_query"])
        self.assertNotIn("keywordsSearchType", payload["request_query"])
        self.assertNotIn("review_status", payload)

    def test_plain_multiple_terms_do_not_force_keywords_search_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["学校", "空调"], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "学校空调项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["学校", "空调"])
        self.assertNotIn("purchasingUnitTypes", payload["effective_query"])
        self.assertNotIn("keywordsSearchType", payload["effective_query"])
        self.assertNotIn("keywordsSearchType", payload["request_query"])

    def test_search_does_not_correct_area_mismatch_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "areaIds": [24], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "看一下朝阳区物业招标",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["effective_query"]["areaIds"], [24])
        self.assertNotIn("review_status", payload)

    def test_search_does_not_block_ambiguous_user_text_when_query_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "新区最近的物业招标看看",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertNotIn("review_status", payload)
        self.assertNotIn("clarification_questions", payload)
        self.assertIn("request_query", payload)

    def test_search_requires_non_empty_keywords_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "只看千万级项目",
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertNotIn("request_query", payload)
        self.assertIn("关键词不能为空", payload["user_message"])

    def test_search_keeps_missing_time_for_backend_default(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "帮我看看北京实验室设备项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertNotIn("beginTime", payload["effective_query"])
        self.assertNotIn("endTime", payload["effective_query"])
        self.assertNotIn("beginTime", payload["request_query"])
        self.assertNotIn("endTime", payload["request_query"])
        self.assertIn("接口默认按近一个月", "；".join(payload["warnings"]))


    def test_followup_suggestions_match_project_stage(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def suggestion_for(stage: str, query: dict | None = None) -> str:
            lines = module.followup_lines(
                query or {"beginTime": "2026-01-01", "endTime": "2026-04-16"},
                total_count=5,
                returned_count=2,
                cards=[
                    {"infoType": stage, "title": "第一条"},
                    {"infoType": stage, "title": "第二条"},
                ],
            )
            return "\n".join(lines)

        tender = suggestion_for("公告-招标公告", {"beginAmount": 1000000})
        self.assertIn("投标截止时间和联系人", tender)
        self.assertNotIn("中标单位", tender)
        self.assertNotIn("中标金额", tender)

        failed = suggestion_for("结果-废标公告")
        self.assertIn("联系人和代理机构", failed)
        self.assertIn("把项目阶段放宽一点", failed)
        self.assertNotIn("报名截止时间", failed)
        self.assertNotIn("投标截止时间", failed)
        self.assertNotIn("中标单位", failed)
        self.assertNotIn("公告原文", failed)
        self.assertNotIn("废标原因", failed)
        self.assertNotIn("只看 100 万以上", failed)

        flowed = suggestion_for("结果-流标公告")
        self.assertIn("联系人和代理机构", flowed)
        self.assertNotIn("报名截止时间", flowed)
        self.assertNotIn("投标截止时间", flowed)
        self.assertNotIn("公告原文", flowed)
        self.assertNotIn("流标原因", flowed)

        changed = suggestion_for("变更-信息变更")
        self.assertIn("联系人和代理机构", changed)
        self.assertNotIn("报名截止时间", changed)
        self.assertNotIn("公告原文", changed)
        self.assertNotIn("变更内容", changed)

        answered = suggestion_for("变更-答疑公告")
        self.assertIn("联系人和代理机构", answered)
        self.assertNotIn("公告原文", answered)
        self.assertNotIn("答疑内容", answered)

        awarded = suggestion_for("结果-中标通知")
        self.assertIn("中标单位联系人和代理机构", awarded)
        self.assertNotIn("中标金额", awarded)

        contract = suggestion_for("结果-合同公告")
        self.assertIn("中标单位联系人和代理机构", contract)
        self.assertNotIn("合同金额", contract)
        self.assertNotIn("中标金额", contract)

        intention = suggestion_for("采购意向")
        self.assertIn("联系人和标的物", intention)
        self.assertNotIn("标的关键词", intention)
        self.assertNotIn("标的物关键词", intention)

        forecast = suggestion_for("预告-招标预告")
        self.assertIn("联系人和标的物", forecast)
        self.assertNotIn("标的关键词", forecast)
        self.assertNotIn("标的物关键词", forecast)

    def test_followup_rules_only_use_supported_non_card_fields(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for stage, rule in module.FOLLOWUP_STAGE_RULES.items():
            with self.subTest(stage=stage):
                self.assertTrue(module.followup_rule_is_valid(rule))
                fields = rule["fields"]
                self.assertTrue(all(field in module.DETAIL_FIELD_SET for field in fields))
                self.assertFalse(all(field in module.CARD_VISIBLE_FIELDS for field in fields))

    def test_search_query_amount_uses_wan_and_displays_backend_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "beginAmount": 1000000, "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["returned_count"], 2)
        self.assertIn("金额 100.00 万元以上", payload["user_message"])
        self.assertIn("北京市第一医院实验室设备采购招标公告", payload["user_message"])
        self.assertIn("北京市第二医院实验室仪器采购招标公告", payload["user_message"])
        self.assertEqual(payload["rejected_count"], 0)
        self.assertNotIn("与本次查询条件不一致", "；".join(payload["warnings"]))

    def test_search_blocks_suspicious_amount_unit_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "beginAmount": 500, "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "看一下 500 万以上的物业项目",
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "AMOUNT_UNIT_SELF_CHECK_REQUIRED")
        self.assertEqual(payload["returned_count"], 0)
        self.assertEqual(payload["cards"], [])
        self.assertNotIn("request_query", payload)
        self.assertTrue(payload["requires_agent_correction"])
        self.assertFalse(payload["requires_user_confirmation"])
        self.assertIn("接口金额单位是元", payload["agent_instruction"])
        self.assertIn("5000000", payload["agent_instruction"])
        self.assertNotIn("请您确认", payload["user_message"])

    def test_search_accepts_yuan_amount_after_unit_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "beginAmount": 5000000, "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "看一下 500 万以上的物业项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["effective_query"]["beginAmount"], 5000000)
        self.assertEqual(payload["request_query"]["beginAmount"], 5000000)
        self.assertIn("金额 500.00 万元以上", payload["user_message"])

    def test_search_blocks_invalid_date_range_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps(
                    {"keywords": ["物业"], "beginTime": "2026-04-20", "endTime": "2026-04-01", "numPerPage": 2},
                    ensure_ascii=False,
                ),
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertNotIn("request_query", payload)
        self.assertIn("开始时间不能晚于结束时间", payload["user_message"])

    def test_search_blocks_invalid_info_types_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "infoTypes": {"3": [999]}, "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertNotIn("request_query", payload)
        self.assertIn("项目阶段条件不在支持范围内", payload["user_message"])

    def test_search_normalizes_bad_page_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "currentPage": "abc", "numPerPage": 200}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["effective_query"]["currentPage"], 1)
        self.assertEqual(payload["effective_query"]["numPerPage"], 100)
        self.assertIn("页码无法识别，已改为 1", "；".join(payload["warnings"]))
        self.assertIn("每页数量超过接口上限 100，已改为 100", "；".join(payload["warnings"]))

    def test_search_displays_backend_cards_without_result_interception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["returned_count"], 2)
        self.assertEqual(payload["api_returned_count"], 2)
        self.assertEqual(payload["rejected_count"], 0)
        self.assertIn("北京市第一医院实验室设备采购招标公告", payload["user_message"])
        self.assertIn("北京市第二医院实验室仪器采购招标公告", payload["user_message"])
        self.assertNotIn("已先不展示", payload["user_message"])

    def test_search_does_not_infer_missing_amount_or_time_from_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                "--user-text",
                "看一下今天朝阳区 500 万以上的物业项目",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["effective_query"]["areaIds"], [2])
        self.assertEqual(payload["request_query"]["areaIds"], [2])
        self.assertNotIn("review_status", payload)
        self.assertNotIn("corrections", payload)
        self.assertNotIn("beginAmount", payload["effective_query"])
        self.assertNotIn("beginTime", payload["effective_query"])
        self.assertIn("我按北京", payload["user_message"])

    def test_next_page_keeps_query_conditions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            payload = self.run_skill("next", state_path=state)

        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["实验室设备"])
        self.assertEqual(payload["effective_query"]["areaIds"], [2])
        self.assertEqual(payload["effective_query"]["currentPage"], 2)
        self.assertIn("当前查询条件未变", payload["query_notice"])
        self.assertIn("当前查询条件未变", payload["user_message"])
        self.assertNotIn("本次按这些条件查", payload["user_message"])
        self.assertNotIn("关键词：实验室设备", payload["user_message"])
        self.assertIn("北京学校实验室设备采购中标通知", payload["user_message"])
        self.assertIn("北京市示范学校", payload["user_message"])
        self.assertIn("中标通知", payload["user_message"])
        self.assertIn("138.00", payload["user_message"])
        self.assertIn("中标通知", payload["user_message"])
        self.assertNotIn("结果-中标通知", payload["user_message"])

    def test_detail_resolves_current_result_before_api_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            payload = self.run_skill(
                "detail",
                "--project-ref",
                "第1个",
                "--fields",
                "budgetAmount,biddingEndTime,sourceUrl",
                "--source-url",
                state_path=state,
            )

        self.assertEqual(payload["total_count"], 1)
        self.assertEqual(payload["returned_count"], 1)
        self.assertEqual(payload["resolution"]["method"], "ordinal")
        self.assertEqual(payload["detail"]["budgetAmount"], "1200000.00")
        self.assertEqual(payload["detail"]["sourceUrl"], "https://example.gov.cn/source/101")
        self.assertEqual(payload["full_detail"]["agencyUnit"], "北京采购代理有限公司")
        self.assertIn("定位到的项目：北京市第一医院实验室设备采购招标公告", payload["user_message"])
        self.assertNotIn("定位方式", payload["user_message"])
        self.assertIn("## 您关心的信息", payload["user_message"])
        self.assertIn("## 项目补充信息", payload["user_message"])
        self.assertIn("### 项目概况", payload["user_message"])
        self.assertIn("### 相关单位", payload["user_message"])
        self.assertIn("- 预算金额（万元）：120.00", payload["user_message"])
        self.assertIn("- 投标截止时间：2026-04-25 09:30:00", payload["user_message"])
        self.assertIn("- 原文链接：[查看原文](https://example.gov.cn/source/101)（https://example.gov.cn/source/101）", payload["user_message"])
        self.assertIn("- 采购单位：北京市第一医院", payload["user_message"])
        self.assertIn("- 代理机构：北京采购代理有限公司", payload["user_message"])
        self.assertIn("您可以直接[查看项目详情](https://www.qianlima.com/bid-101.html)", payload["user_message"])
        self.assert_markdown_link(payload["user_message"], "查看项目详情", payload["full_detail"]["url"])
        self.assert_markdown_link(payload["user_message"], "查看原文", payload["detail"]["sourceUrl"])
        self.assert_url_only_appears_as_link_target(payload["user_message"], payload["full_detail"]["url"])
        self.assertNotIn("原文链接：https://example.gov.cn/source/101", payload["user_message"])
        self.assertNotIn("详情页链接：https://www.qianlima.com/bid-101.html", payload["user_message"])
        self.assertNotIn("url：", payload["user_message"])
        self.assertNotIn("URL：", payload["user_message"])
        self.assertEqual(payload["user_message"].count("预算金额（万元）："), 1)
        self.assertEqual(payload["user_message"].count("投标截止时间："), 1)

    def test_detail_target_keywords_uses_plain_user_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            payload = self.run_skill(
                "detail",
                "--project-ref",
                "第1个",
                "--fields",
                "targetKeywords",
                state_path=state,
            )

        self.assertEqual(payload["detail"]["targetKeywords"], ["实验室设备", "仪器"])
        self.assertIn("## 您关心的信息", payload["user_message"])
        self.assertIn("- 标的物：实验室设备、仪器", payload["user_message"])
        self.assertIn("您可以直接[查看项目详情](https://www.qianlima.com/bid-101.html)", payload["user_message"])
        self.assert_markdown_link(payload["user_message"], "查看项目详情", payload["full_detail"]["url"])
        self.assert_url_only_appears_as_link_target(payload["user_message"], payload["full_detail"]["url"])
        self.assertNotIn("标的关键词", payload["user_message"])
        self.assertNotIn("标的物关键词", payload["user_message"])
        self.assertEqual(payload["user_message"].count("标的物："), 1)

    def test_project_detail_returns_open_biding_time_with_user_facing_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            payload = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "openBidingTime",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["detail"]["openBidingTime"], "2026-04-25 10:00:00")
        self.assertEqual(payload["full_detail"]["openBidingTime"], "2026-04-25 10:00:00")
        self.assertIn("- 开标日期：2026-04-25 10:00:00", payload["user_message"])
        self.assertEqual(payload["user_message"].count("开标日期："), 1)

    def test_title_fragment_with_ordinal_word_is_not_treated_as_result_index(self) -> None:
        spec = importlib.util.spec_from_file_location("qianlima_skill", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cards = [
            {"id": 101, "title": "婺源县第二批学校心理咨询室建设设备采购项目询价公告"},
            {"id": 102, "title": "高坡幼儿园五寨园区监控设备采购竞价公告"},
        ]
        resolution = module.resolve_project("婺源县第二批学校心理咨询室建", cards)

        self.assertEqual(resolution["status"], "matched")
        self.assertEqual(resolution["method"], "text")
        self.assertEqual(resolution["matches"][0]["id"], 101)

    def test_ambiguous_project_reference_does_not_guess(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            code, payload = self.run_skill_with_fixtures(
                FIXTURES,
                "detail",
                "--project-ref",
                "北京市",
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["total_count"], 2)
        self.assertEqual(payload["returned_count"], 0)
        self.assertIn("多个候选", payload["warnings"][0])
        self.assertIn("可能相关的项目", payload["user_message"])
        self.assertNotIn("本次当前结果来自这些查询条件", payload["user_message"])
        self.assertIn("北京市第一医院实验室设备采购招标公告", payload["user_message"])
        self.assertIn("北京市第一医院", payload["user_message"])
        self.assertNotIn("中标金额（万元）", payload["user_message"])

    def test_search_error_preserves_effective_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(
                ERROR_FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["stage"], "search")
        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["实验室设备"])
        self.assertEqual(payload["effective_query"]["areaIds"], [2])
        self.assertIn("user_message", payload)
        self.assertIn("我按北京市，标题/正文含“实验室设备”，查询了项目。", payload["user_message"])
        self.assertNotIn("本次生效条件", payload["user_message"])
        self.assertIn("没有自动改用其他网站", payload["user_message"])
        self.assertIn("接口参数异常", payload["user_message"])
        self.assertIn("Agent 按当前接口契约修正参数", payload["user_message"])
        for forbidden_websearch_prompt in ("WebSearch", "互联网公开信息", "改用互联网"):
            self.assertNotIn(forbidden_websearch_prompt, payload["user_message"])

    def test_empty_first_search_suggests_supported_refinements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(
                EMPTY_FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["5G基站"], "beginAmount": 3000000, "numPerPage": 5}, ensure_ascii=False),
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["returned_count"], 0)
        self.assertIn("zero_result_reflection", payload)
        self.assertLessEqual(len(payload["zero_result_reflection"]), 3)
        self.assertIn("暂时没查到符合这些条件的项目", payload["user_message"])
        self.assertIn("放宽金额范围", payload["user_message"])
        self.assertIn("关键词拆分、组合与搜索位置", payload["user_message"])
        self.assertNotIn("单位名称", payload["user_message"])

    def test_empty_first_search_without_amount_does_not_suggest_adding_amount(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(
                EMPTY_FIXTURES,
                "search",
                "--query-json",
                json.dumps(
                    {
                        "keywords": ["5G基站"],
                        "excludeWords": ["监理"],
                        "beginTime": "2025-10-15",
                        "endTime": "2026-04-15",
                        "purchasingUnitTypes": [7],
                        "infoTypes": {"0": [4]},
                        "numPerPage": 5,
                    },
                    ensure_ascii=False,
                ),
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["returned_count"], 0)
        self.assertIn("zero_result_reflection", payload)
        self.assertLessEqual(len(payload["zero_result_reflection"]), 3)
        self.assertIn("发布时间的起止范围", payload["user_message"])
        self.assertIn("可能误删", payload["user_message"])
        self.assertNotIn("增加金额范围", payload["user_message"])

    def test_district_zero_result_requires_confirmation_before_city_expansion(self) -> None:
        empty_payload = (EMPTY_FIXTURES / "search_page_1.json").read_text(encoding="utf-8")
        cases = [
            ("search", "search_page_1.json", "项目"),
            ("search-purchase", "search_purchase_page_1.json", "采购意向"),
            ("search-expiring", "search_expiring_page_1.json", "临期项目"),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixtures = root / "fixtures"
            fixtures.mkdir()
            for _, fixture_name, _ in cases:
                (fixtures / fixture_name).write_text(empty_payload, encoding="utf-8")

            for index, (command, _, stage_label) in enumerate(cases, start=1):
                with self.subTest(command=command):
                    state = root / f"state-{index}.json"
                    code, payload = self.run_skill_with_fixtures(
                        fixtures,
                        command,
                        "--query-json",
                        json.dumps({"keywords": ["食堂"], "areaIds": [2807]}, ensure_ascii=False),
                        state_path=state,
                    )

                    self.assertEqual(code, 0)
                    self.assertTrue(payload["ok"])
                    self.assertEqual(payload["total_count"], 0)
                    self.assertEqual(payload["effective_query"]["areaIds"], [2807])
                    self.assertEqual(payload["request_query"]["areaIds"], [2807])
                    self.assertEqual(
                        payload["area_expansion"],
                        {
                            "from_area_id": 2807,
                            "from_area_name": "广东省-深圳市-南山区",
                            "to_area_id": 316,
                            "to_area_name": "广东省-深圳市",
                            "requires_confirmation": True,
                            "refine_query": {"areaIds": [316]},
                        },
                    )
                    self.assertIn("南山区", payload["user_message"])
                    self.assertIn("是否扩大到广东省-深圳市", payload["user_message"])
                    self.assertIn("同意", payload["user_message"])
                    self.assertIn(stage_label, payload["user_message"])

    def test_city_refine_after_district_zero_result_preserves_other_conditions(self) -> None:
        initial_query = {
            "keywords": ["食堂"],
            "excludeWords": ["外包"],
            "areaIds": [2807],
            "beginTime": "2026-07-18",
            "endTime": "2026-07-24",
            "purchasingUnitTypes": [3],
            "infoTypes": {"3": []},
            "beginAmount": 500000,
            "currentPage": 4,
            "numPerPage": 5,
        }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.json"
            fixtures = root / "fixtures"
            fixtures.mkdir()
            empty_payload = (EMPTY_FIXTURES / "search_page_1.json").read_text(encoding="utf-8")
            (fixtures / "search_page_1.json").write_text(empty_payload, encoding="utf-8")
            (fixtures / "search_page_4.json").write_text(empty_payload, encoding="utf-8")
            code, first = self.run_skill_with_fixtures(
                fixtures,
                "search",
                "--query-json",
                json.dumps(initial_query, ensure_ascii=False),
                state_path=state,
            )
            self.assertEqual(code, 0)
            self.assertEqual(first["effective_query"]["areaIds"], [2807])
            self.assertEqual(first["effective_query"]["currentPage"], 4)

            code, refined = self.run_skill_with_fixtures(
                fixtures,
                "refine",
                "--query-json",
                json.dumps({"areaIds": [316]}, ensure_ascii=False),
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertEqual(refined["effective_query"]["areaIds"], [316])
        self.assertEqual(refined["effective_query"]["currentPage"], 1)
        for field in (
            "keywords",
            "excludeWords",
            "beginTime",
            "endTime",
            "purchasingUnitTypes",
            "infoTypes",
            "beginAmount",
            "numPerPage",
        ):
            self.assertEqual(query_field(refined["effective_query"], field), initial_query[field])

    def test_city_refine_preserves_capability_specific_conditions_for_all_searches(self) -> None:
        empty_payload = (EMPTY_FIXTURES / "search_page_1.json").read_text(encoding="utf-8")
        cases = [
            (
                "search",
                "search_page",
                {
                    "keywords": ["食堂"],
                    "excludeWords": ["外包"],
                    "areaIds": [2807],
                    "beginTime": "2026-07-18",
                    "endTime": "2026-07-24",
                    "purchasingUnitTypes": [3],
                    "infoTypes": {"3": []},
                    "beginAmount": 500000,
                    "currentPage": 2,
                    "numPerPage": 5,
                },
            ),
            (
                "search-purchase",
                "search_purchase_page",
                {
                    "keywords": ["食堂"],
                    "excludeWords": ["外包"],
                    "areaIds": [2807],
                    "startPlanPurchaseDate": "2026-08",
                    "endPlanPurchaseDate": "2026-10",
                    "startPlanPurchaseAmount": 500000,
                    "currentPage": 2,
                    "numPerPage": 5,
                },
            ),
            (
                "search-expiring",
                "search_expiring_page",
                {
                    "keywords": ["食堂"],
                    "excludeWords": ["外包"],
                    "areaIds": [2807],
                    "beginServiceExpireTime": "2026-08-01",
                    "endServiceExpireTime": "2026-10-31",
                    "beginContractAmount": 500000,
                    "currentPage": 2,
                    "numPerPage": 5,
                },
            ),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, (command, fixture_prefix, initial_query) in enumerate(cases, start=1):
                with self.subTest(command=command):
                    fixtures = root / f"fixtures-{index}"
                    fixtures.mkdir()
                    (fixtures / f"{fixture_prefix}_1.json").write_text(empty_payload, encoding="utf-8")
                    (fixtures / f"{fixture_prefix}_2.json").write_text(empty_payload, encoding="utf-8")
                    state = root / f"state-{index}.json"

                    code, first = self.run_skill_with_fixtures(
                        fixtures,
                        command,
                        "--query-json",
                        json.dumps(initial_query, ensure_ascii=False),
                        state_path=state,
                    )
                    self.assertEqual(code, 0)
                    self.assertEqual(first["request_query"]["areaIds"], [2807])
                    self.assertTrue(first["area_expansion"]["requires_confirmation"])

                    code, refined = self.run_skill_with_fixtures(
                        fixtures,
                        "refine",
                        "--query-json",
                        json.dumps({"areaIds": [316]}, ensure_ascii=False),
                        state_path=state,
                    )
                    self.assertEqual(code, 0)
                    self.assertEqual(refined["request_query"]["areaIds"], [316])
                    self.assertEqual(refined["effective_query"]["currentPage"], 1)
                    for field, value in initial_query.items():
                        if field not in {"areaIds", "currentPage"}:
                            self.assertEqual(query_field(refined["effective_query"], field), value)

    def test_refine_updates_current_query_and_resets_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "currentPage": 2, "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            payload = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"beginAmount": 1000000}, ensure_ascii=False),
                "--user-text",
                "只看 100 万以上的",
                state_path=state,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(query_field(payload["effective_query"], 'keywords'), ["实验室设备"])
        self.assertEqual(payload["effective_query"]["beginAmount"], 1000000)
        self.assertEqual(payload["effective_query"]["currentPage"], 1)
        self.assertIn("金额 100.00 万元以上", payload["user_message"])

    @staticmethod
    def current_project_expected(query):
        import qianlima_skill
        return qianlima_skill.normalize_query(project_query(query))[0]

    def test_multiturn_next_and_refine_keep_unmodified_query_fields(self) -> None:
        initial_query = {
            "keywords": ["空调"],
            "excludeWords": ["维修"],
            "areaIds": [2],
            "beginTime": "2026-03-15",
            "endTime": "2026-04-15",
            "purchasingUnitTypes": [3],
            "infoTypes": {"3": [11]},
            "beginAmount": 500000,
            "numPerPage": 2,
        }
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search",
                "--query-json",
                json.dumps(initial_query, ensure_ascii=False),
                state_path=state,
            )
            next_page = self.run_skill("next", state_path=state)
            refined_amount = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"beginAmount": 1000000}, ensure_ascii=False),
                "--user-text",
                "只看 100 万以上的",
                state_path=state,
            )
            next_after_refine = self.run_skill("next", state_path=state)
            refined_exclude = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"excludeWords": ["维修", "维保"]}, ensure_ascii=False),
                "--user-text",
                "再排除维保",
                state_path=state,
            )
            refined_keyword = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"keywords": ["设备"]}, ensure_ascii=False),
                "--user-text",
                "换成设备",
                state_path=state,
            )

        self.assertEqual(first["effective_query"]["currentPage"], 1)
        for key, value in initial_query.items():
            self.assertEqual(query_field(first["effective_query"], key), value)

        for key, value in initial_query.items():
            self.assertEqual(query_field(next_page["effective_query"], key), value)
        self.assertEqual(next_page["effective_query"]["currentPage"], 2)

        expected_after_amount = dict(initial_query)
        expected_after_amount["beginAmount"] = 1000000
        expected_after_amount["currentPage"] = 1
        self.assertEqual(refined_amount["effective_query"], self.current_project_expected(expected_after_amount))

        expected_next_after_refine = dict(expected_after_amount)
        expected_next_after_refine["currentPage"] = 2
        self.assertEqual(next_after_refine["effective_query"], self.current_project_expected(expected_next_after_refine))

        expected_after_exclude = dict(expected_after_amount)
        expected_after_exclude["excludeWords"] = ["维修", "维保"]
        self.assertEqual(refined_exclude["effective_query"], self.current_project_expected(expected_after_exclude))

        expected_after_keyword = dict(expected_after_exclude)
        expected_after_keyword["keywords"] = ["设备"]
        self.assertEqual(refined_keyword["effective_query"], self.current_project_expected(expected_after_keyword))

    def test_purchase_intention_next_and_refine_keep_purchase_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            next_page = self.run_skill("next", state_path=state)
            refined = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"beginAmount": 1000000}, ensure_ascii=False),
                "--user-text",
                "只看 100 万以上的采购意向",
                state_path=state,
            )

        self.assertEqual(first["stage"], "purchase_intention")
        self.assertEqual(next_page["stage"], "purchase_intention")
        self.assertEqual(next_page["effective_query"]["currentPage"], 2)
        self.assertEqual(next_page["cards"][0]["id"], 203)
        self.assertIn("采购意向", next_page["user_message"])
        self.assertNotIn("中标通知", next_page["user_message"])
        self.assertEqual(refined["stage"], "purchase_intention")
        self.assertEqual(refined["effective_query"]["startPlanPurchaseAmount"], 1000000)
        self.assertNotIn("beginAmount", refined["effective_query"])

    def test_expiring_project_next_and_refine_keep_expiring_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search-expiring",
                "--query-json",
                json.dumps({"keywords": ["物业"], "areaIds": [305], "numPerPage": 1}, ensure_ascii=False),
                state_path=state,
            )
            next_page = self.run_skill("next", state_path=state)
            refined = self.run_skill(
                "refine",
                "--query-json",
                json.dumps({"beginAmount": 2000000}, ensure_ascii=False),
                "--user-text",
                "只看 200 万以上的临期项目",
                state_path=state,
            )

        self.assertEqual(first["stage"], "expiring_project")
        self.assertEqual(next_page["stage"], "expiring_project")
        self.assertEqual(next_page["effective_query"]["currentPage"], 2)
        self.assertEqual(next_page["cards"][0]["id"], 302)
        self.assertIn("临期项目", next_page["user_message"])
        self.assertNotIn("中标通知", next_page["user_message"])
        self.assertEqual(refined["stage"], "expiring_project")
        self.assertEqual(refined["effective_query"]["beginContractAmount"], 2000000)
        self.assertNotIn("beginAmount", refined["effective_query"])

    def test_area_region_phrase_preserves_explicit_group_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, payload = self.run_skill_with_fixtures(
                FIXTURES, "area", "--name", "大湾区内地九市", "--limit", "20",
                state_path=Path(tmp) / "state.json")
        self.assertEqual(code, 0)
        self.assertEqual(payload["resolution_status"], "resolved")
        self.assertEqual(len(payload["areas"]), 9)

    def test_area_ambiguous_phrase_returns_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, payload = self.run_skill_with_fixtures(
                FIXTURES, "area", "--name", "朝阳区", "--limit", "5",
                state_path=Path(tmp) / "state.json")
        self.assertEqual(code, 0)
        self.assertEqual(payload["resolution_status"], "ambiguous")
        self.assertGreater(len(payload["candidates"]), 1)
        self.assertNotIn("effective_query", payload)
        self.assertIn("请确认", payload["user_message"])

    def test_area_known_municipality_district_has_executable_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, payload = self.run_skill_with_fixtures(
                FIXTURES, "area", "--name", "海淀区", state_path=Path(tmp) / "state.json")
        self.assertEqual(code, 0)
        self.assertEqual(payload["effective_query"]["areaIds"], [3320])
        self.assertEqual(payload["resolution_status"], "resolved")
        self.assertNotIn("expansion_suggestion", payload)

    def test_area_scope_names_do_not_select_lower_same_name_entry(self) -> None:
        cases = {
            "北京": [2],
            "北京市": [2],
            "上海": [24],
            "上海市": [24],
            "广州": [305],
            "广州市": [305],
            "广东省": [5],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, (name, expected) in enumerate(cases.items(), start=1):
                with self.subTest(name=name):
                    code, payload = self.run_skill_with_fixtures(
                        FIXTURES,
                        "area",
                        "--name",
                        name,
                        state_path=root / f"state-{index}.json",
                    )
                    self.assertEqual(code, 0)
                    self.assertEqual(payload["effective_query"]["areaIds"], expected)

    def test_area_parent_qualified_district_phrase_resolves_uniquely(self) -> None:
        cases = {
            "北京朝阳区": [3316],
            "北京市朝阳区": [3316],
            "深圳南山": [2807],
            "广东省深圳市南山区": [2807],
            "杭州西湖": [2949],
            "南京玄武": [2724],
            "成都武侯": [3502],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, (name, expected) in enumerate(cases.items(), start=1):
                with self.subTest(name=name):
                    code, payload = self.run_skill_with_fixtures(
                        FIXTURES,
                        "area",
                        "--name",
                        name,
                        state_path=root / f"state-{index}.json",
                    )
                    self.assertEqual(code, 0)
                    self.assertEqual(payload["effective_query"]["areaIds"], expected)
                    self.assertEqual(len(payload["areas"]), 1)

    def test_purchase_search_rejects_inverted_planned_purchase_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            payload = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps(
                    {
                        "keywords": ["数字化"],
                        "startPlanPurchaseDate": "2026-07",
                        "endPlanPurchaseDate": "2026-05",
                    },
                    ensure_ascii=False,
                ),
                state_path=state,
            )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "INVALID_QUERY")
        self.assertIn("预计采购时间", payload["user_message"])

    def test_all_search_capabilities_preserve_district_area_id(self) -> None:
        cases = [
            "search",
            "search-purchase",
            "search-expiring",
        ]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, command in enumerate(cases, start=1):
                with self.subTest(command=command):
                    state = root / f"state-{index}.json"
                    payload = self.run_skill(
                        command,
                        "--query-json",
                        json.dumps({"keywords": ["食堂"], "areaIds": [2807]}, ensure_ascii=False),
                        state_path=state,
                    )
                    self.assertEqual(payload["effective_query"]["areaIds"], [2807])
                    self.assertEqual(payload["request_query"]["areaIds"], [2807])

    def test_next_page_without_current_search_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(FIXTURES, "next", state_path=state)

        self.assertEqual(code, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "RESULT_SET_ID_REQUIRED")
        self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")

    def test_v2_search_returns_follow_up_and_cross_cwd_detail_uses_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            search_cwd = root / "search"
            detail_cwd = root / "detail"
            search_cwd.mkdir()
            detail_cwd.mkdir()

            search_code, search = self.run_v2_cli(
                FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
                cwd=search_cwd,
            )
            follow_up = search["follow_up"]
            detail_code, detail = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--session-id",
                follow_up["session_id"],
                "--result-set-id",
                follow_up["result_set_id"],
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_dir=state_dir,
                cwd=detail_cwd,
            )

        self.assertEqual(search_code, 0)
        self.assertEqual(detail_code, 0)
        self.assertEqual(detail["full_detail"]["id"], 101)
        self.assertEqual(detail["follow_up"]["result_set_id"], follow_up["result_set_id"])
        self.assertEqual(detail["selected_project_id"], "101")

    def test_v2_two_sessions_in_one_state_directory_do_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            session_a = str(uuid.uuid4())
            session_b = str(uuid.uuid4())
            _, search_a = self.run_v2_cli(
                FIXTURES,
                "search",
                "--session-id",
                session_a,
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
            )
            _, search_b = self.run_v2_cli(
                FIXTURES,
                "search-purchase",
                "--session-id",
                session_b,
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
            )
            _, detail_a = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--session-id",
                session_a,
                "--result-set-id",
                search_a["follow_up"]["result_set_id"],
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_dir=state_dir,
            )
            _, detail_b = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--session-id",
                session_b,
                "--result-set-id",
                search_b["follow_up"]["result_set_id"],
                "--project-ref",
                "第1条",
                "--fields",
                "purchaseContent",
                state_dir=state_dir,
            )

        self.assertEqual(detail_a["full_detail"]["id"], 101)
        self.assertEqual(detail_b["full_detail"]["id"], 201)

    def test_v2_missing_follow_up_context_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, payload = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_dir=Path(tmp) / "state",
            )

        self.assertEqual(code, 2)
        self.assertEqual(payload["error_code"], "RESULT_SET_ID_REQUIRED")
        self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")
        self.assertTrue(payload["needs_clarification"])
        self.assertFalse(payload["requires_user_confirmation"])

    def test_v2_missing_result_requires_context_and_unavailable_store_keeps_api_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty_fixtures = root / "empty-fixtures"
            empty_fixtures.mkdir()
            missing_code, missing = self.run_v2_cli(
                empty_fixtures, "next", "--session-id", str(uuid.uuid4()),
                state_dir=root / "state",
            )
            blocked_store = root / "blocked-state"
            blocked_store.write_text("not a directory", encoding="utf-8")
            store_code, success = self.run_v2_cli(
                FIXTURES, "search", "--query-json",
                json.dumps({"keywords": ["实验室设备"]}, ensure_ascii=False),
                state_dir=blocked_store,
            )

        self.assertEqual((missing_code, missing["error_code"]), (2, "RESULT_SET_ID_REQUIRED"))
        self.assertEqual(missing["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")
        self.assertTrue(missing["needs_clarification"])
        self.assertFalse(missing["requires_user_confirmation"])
        self.assertNotIn("api_responses", missing)
        self.assertEqual(store_code, 0)
        self.assertTrue(success["ok"])
        self.assertEqual(success["api_responses"][0]["path"], "/api/search")
        self.assertEqual(len(success["api_responses"]), 1)
        self.assertEqual(success["api_responses"][0]["response"], json.loads((FIXTURES / "search_page_1.json").read_text()))
        self.assertNotIn("follow_up", success)
        self.assertTrue(success["presentation_notice"])

    def test_v2_search_does_not_create_legacy_cwd_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp) / "cwd"
            state_dir = Path(tmp) / "state"
            cwd.mkdir()
            code, payload = self.run_v2_cli(
                FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
                cwd=cwd,
            )

            legacy_state_exists = (cwd / ".qianlima_skill_state.json").exists()

        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertFalse(legacy_state_exists)

    def test_v2_next_and_refine_create_new_snapshots_without_overwriting_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            _, first = self.run_v2_cli(
                FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
            )
            first_context = first["follow_up"]
            parent_path = state_dir / first_context["session_id"] / f"{first_context['result_set_id']}.json"
            parent_before = json.loads(parent_path.read_text(encoding="utf-8"))
            parent_before["expires_at"] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=1)).isoformat()
            parent_path.write_text(json.dumps(parent_before, ensure_ascii=False), encoding="utf-8")
            short_expiry = dt.datetime.fromisoformat(parent_before["expires_at"])
            _, next_page = self.run_v2_cli(
                FIXTURES,
                "next",
                "--session-id",
                first_context["session_id"],
                "--result-set-id",
                first_context["result_set_id"],
                state_dir=state_dir,
            )
            parent_after_next = json.loads(parent_path.read_text(encoding="utf-8"))
            _, refined = self.run_v2_cli(
                FIXTURES,
                "refine",
                "--session-id",
                first_context["session_id"],
                "--result-set-id",
                first_context["result_set_id"],
                "--query-json",
                json.dumps({"beginAmount": 1000000}, ensure_ascii=False),
                state_dir=state_dir,
            )
            _, original_detail = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--session-id",
                first_context["session_id"],
                "--result-set-id",
                first_context["result_set_id"],
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_dir=state_dir,
            )
            parent_after = json.loads(parent_path.read_text(encoding="utf-8"))
            snapshot_files = list((state_dir / first_context["session_id"]).glob("*.json"))

        self.assertNotEqual(next_page["follow_up"]["result_set_id"], first_context["result_set_id"])
        self.assertNotEqual(refined["follow_up"]["result_set_id"], first_context["result_set_id"])
        self.assertEqual(next_page["follow_up"]["parent_result_set_id"], first_context["result_set_id"])
        self.assertEqual(refined["follow_up"]["parent_result_set_id"], first_context["result_set_id"])
        self.assertEqual(original_detail["full_detail"]["id"], 101)
        self.assertGreater(dt.datetime.fromisoformat(parent_after_next["expires_at"]), short_expiry)
        self.assertGreater(dt.datetime.fromisoformat(parent_after["expires_at"]), short_expiry)
        self.assertEqual(len(snapshot_files), 3)

    def test_v2_explicit_cross_session_context_reads_while_invalid_paths_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            empty_fixtures = root / "empty-fixtures"
            empty_fixtures.mkdir()
            session_a = str(uuid.uuid4())
            _, first = self.run_v2_cli(
                FIXTURES,
                "search",
                "--session-id",
                session_a,
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
            )
            result_set_id = first["follow_up"]["result_set_id"]
            mismatch_code, mismatch = self.run_v2_cli(
                FIXTURES,
                "detail",
                "--session-id",
                str(uuid.uuid4()),
                "--result-set-id",
                result_set_id,
                "--project-ref",
                "第1条",
                state_dir=state_dir,
            )
            invalid_code, invalid = self.run_v2_cli(
                empty_fixtures,
                "detail",
                "--session-id",
                session_a,
                "--result-set-id",
                "../../other-session",
                "--project-ref",
                "第1条",
                state_dir=state_dir,
            )
            missing_code, missing = self.run_v2_cli(
                empty_fixtures,
                "detail",
                "--session-id",
                session_a,
                "--result-set-id",
                str(uuid.uuid4()),
                "--project-ref",
                "第1条",
                state_dir=state_dir,
            )

        self.assertEqual(mismatch_code, 0)
        self.assertTrue(mismatch["ok"])
        self.assertEqual(mismatch["selected_project_id"], "101")
        self.assertEqual(mismatch["full_detail"]["id"], 101)
        self.assertEqual([item["path"] for item in mismatch["api_responses"]], ["/api/detail/101"])
        self.assertEqual((invalid_code, invalid["error_code"]), (2, "INVALID_RESULT_SET_ID"))
        self.assertEqual((missing_code, missing["error_code"]), (2, "RESULT_SET_NOT_FOUND"))
        for payload in (invalid, missing):
            self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")
            self.assertNotEqual(payload["error_code"], "MOCK_FILE_NOT_FOUND")
            self.assertNotIn("api_responses", payload)
            self.assertTrue(payload["needs_clarification"])
            self.assertFalse(payload["requires_user_confirmation"])

    def test_v2_snapshot_permissions_are_private_and_api_key_is_not_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "state"
            secret = "test-secret-must-not-be-stored"
            _, payload = self.run_v2_cli(
                FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
                extra_env={"QIANLIMA_API_KEY": secret},
            )
            follow_up = payload["follow_up"]
            session_dir = state_dir / follow_up["session_id"]
            snapshot = session_dir / f"{follow_up['result_set_id']}.json"
            snapshot_text = snapshot.read_text(encoding="utf-8")
            session_mode = session_dir.stat().st_mode & 0o777
            snapshot_mode = snapshot.stat().st_mode & 0o777

        self.assertEqual(session_mode, 0o700)
        self.assertEqual(snapshot_mode, 0o600)
        self.assertNotIn(secret, snapshot_text)
        self.assertNotIn("api_key", snapshot_text.lower())

    def test_v2_follow_up_detail_keeps_api_success_with_unwritable_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            empty_fixtures = root / "empty-fixtures"
            empty_fixtures.mkdir()
            _, search = self.run_v2_cli(
                FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_dir=state_dir,
            )
            follow_up = search["follow_up"]
            session_dir = state_dir / follow_up["session_id"]
            session_dir.chmod(0o500)
            try:
                code, payload = self.run_v2_cli(
                    FIXTURES,
                    "detail",
                    "--session-id",
                    follow_up["session_id"],
                    "--result-set-id",
                    follow_up["result_set_id"],
                    "--project-ref",
                    "第1条",
                    "--fields",
                    "budgetAmount",
                    state_dir=state_dir,
                )
            finally:
                session_dir.chmod(0o700)

        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["full_detail"]["id"], 101)
        self.assertEqual(payload["selected_project_id"], "101")
        self.assertEqual([item["path"] for item in payload["api_responses"]], ["/api/detail/101"])
        self.assertEqual(payload["api_responses"][0]["response"], json.loads((FIXTURES / "detail_101.json").read_text()))

    def test_package_excludes_legacy_and_v2_state_artifacts(self) -> None:
        spec = importlib.util.spec_from_file_location("package_skill", PACKAGE_SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "qianlima-bidding-search"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("# Test", encoding="utf-8")
            (skill_dir / ".qianlima_skill_state.json").write_text("{}", encoding="utf-8")
            state_dir = skill_dir / ".qianlima-skill-state"
            state_dir.mkdir()
            (state_dir / "snapshot.json").write_text("{}", encoding="utf-8")
            process_docs = skill_dir / "docs" / "superpowers" / "plans"
            process_docs.mkdir(parents=True)
            (process_docs / "implementation.md").write_text("internal process", encoding="utf-8")
            nested_dist = skill_dir / "dist"
            nested_dist.mkdir()
            (nested_dist / "old.zip").write_bytes(b"old")
            archive_path = root / "skill.zip"

            module.package(skill_dir, archive_path)

            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()

        self.assertIn("qianlima-bidding-search/SKILL.md", names)
        self.assertNotIn("qianlima-bidding-search/.qianlima_skill_state.json", names)
        self.assertFalse(any(".qianlima-skill-state" in name for name in names))
        self.assertFalse(any("docs/superpowers" in name for name in names))
        self.assertFalse(any("/dist/" in name for name in names))

    def test_empty_or_corrupt_state_file_fails_without_traceback(self) -> None:
        for content in ("", "{not-json"):
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp) / "state.json"
                self.run_skill(
                    "search",
                    "--query-json",
                    json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                    state_path=state,
                )
                self.current_snapshot_path(state).write_text(content, encoding="utf-8")
                code, payload = self.run_skill_raw(FIXTURES, "next", state_path=state)

            self.assertEqual(code, 2)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error_code"], "RESULT_SET_CORRUPT")
            self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")
            self.assertTrue(payload["needs_clarification"])
            self.assertFalse(payload["requires_user_confirmation"])
            self.assertNotIn("Traceback", json.dumps(payload, ensure_ascii=False))

    def test_malformed_search_state_fields_fail_without_traceback(self) -> None:
        mutations = [
            lambda payload: payload["effective_query"].update({"currentPage": "abc"}),
            lambda payload: payload.update({"cards": "not-a-list"}),
            lambda payload: payload.update({"result_type": "unknown_source"}),
        ]
        for index, mutate in enumerate(mutations):
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp) / "state.json"
                self.run_skill(
                    "search",
                    "--query-json",
                    json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                    state_path=state,
                )
                snapshot_path = self.current_snapshot_path(state)
                payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
                mutate(payload)
                snapshot_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                if index in {0, 2}:
                    code, result = self.run_skill_raw(FIXTURES, "next", state_path=state)
                else:
                    code, result = self.run_skill_raw(
                        FIXTURES,
                        "detail",
                        "--project-ref",
                        "第1条",
                        "--fields",
                        "budgetAmount",
                        state_path=state,
                    )

            self.assertEqual(code, 2)
            self.assertFalse(result["ok"])
            self.assertEqual(result["error_code"], "RESULT_SET_CORRUPT")
            self.assertTrue(result["needs_clarification"])
            self.assertFalse(result["requires_user_confirmation"])
            self.assertNotIn("Traceback", json.dumps(result, ensure_ascii=False))

    def test_expired_current_search_does_not_continue_old_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            snapshot_path = self.current_snapshot_path(state)
            payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
            payload["expires_at"] = "2000-01-01T00:00:00+00:00"
            snapshot_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            code, payload = self.run_skill_raw(
                FIXTURES,
                "next",
                state_path=state,
            )

        self.assertEqual(code, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "RESULT_SET_EXPIRED")
        self.assertTrue(payload["needs_clarification"])
        self.assertFalse(payload["requires_user_confirmation"])

    def test_next_page_after_failed_search_does_not_continue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, failed = self.run_skill_with_fixtures(
                ERROR_FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            self.assertEqual(code, 0)
            self.assertFalse(failed["ok"])
            code, payload = self.run_skill_with_fixtures(FIXTURES, "next", state_path=state)

        self.assertEqual(code, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "RESULT_SET_ID_REQUIRED")
        self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")

    def test_failed_new_search_preserves_previous_result_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            first = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            code, failed = self.run_skill_with_fixtures(
                ERROR_FIXTURES,
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            self.assertTrue(first["ok"])
            self.assertEqual(code, 0)
            self.assertFalse(failed["ok"])
            code, payload = self.run_skill_with_fixtures(FIXTURES, "next", state_path=state)

        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["effective_query"]["currentPage"], 2)

    def test_detail_out_of_range_does_not_call_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            code, payload = self.run_skill_with_fixtures(
                FIXTURES,
                "detail",
                "--project-ref",
                "第99条",
                "--fields",
                "purchasingUnitLinkName,purchasingUnitLinkPhone",
                state_path=state,
            )

        self.assertEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["resolution"]["method"], "ordinal")
        self.assertEqual(payload["resolution"]["status"], "not_found")
        self.assertIn("未调用详情接口", payload["warnings"][0])
        self.assertIn("当前这批结果只有 2 条，没有第 99 条", payload["user_message"])
        self.assertNotIn("提醒：", payload["user_message"])

    def test_detail_without_current_search_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            code, payload = self.run_skill_with_fixtures(
                FIXTURES,
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_path=state,
            )

        self.assertEqual(code, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_code"], "RESULT_SET_ID_REQUIRED")
        self.assertEqual(payload["retry_policy"], "restore_explicit_context_or_clarify_missing_fields")

    def test_detail_can_reuse_focus_project_for_this_item_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            first = self.run_skill(
                "detail",
                "--project-ref",
                "第2条",
                "--fields",
                "purchasingUnitLinkName,purchasingUnitLinkPhone",
                state_path=state,
            )
            second = self.run_skill(
                "detail",
                "--project-ref",
                "这个项目",
                "--fields",
                "budgetAmount",
                state_path=state,
            )
            state_payload = json.loads(self.current_snapshot_path(state).read_text(encoding="utf-8"))

        self.assertTrue(first["ok"])
        self.assertTrue(second["ok"])
        self.assertEqual(second["resolution"]["method"], "focus_project")
        self.assertEqual(second["full_detail"]["id"], 102)
        self.assertEqual(second["detail"]["budgetAmount"], "900000.00")
        self.assertEqual(state_payload["focus_project"]["id"], 102)

    def test_failed_source_url_request_does_not_keep_previous_focus_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            first = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "budgetAmount",
                state_path=state,
            )
            failed_second = self.run_skill(
                "detail",
                "--project-ref",
                "第2条",
                "--fields",
                "sourceUrl",
                "--source-url",
                state_path=state,
            )
            followup = self.run_skill(
                "detail",
                "--project-ref",
                "这个项目",
                "--fields",
                "budgetAmount",
                state_path=state,
            )

        self.assertTrue(first["ok"])
        self.assertFalse(failed_second["ok"])
        self.assertEqual(followup["resolution"]["method"], "focus_project")
        self.assertEqual(followup["full_detail"]["id"], 101)
        self.assertEqual(followup["detail"]["budgetAmount"], "1200000.00")

    def test_source_url_repeated_request_does_not_create_local_quota_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "areaIds": [2], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            first = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "sourceUrl",
                "--source-url",
                state_path=state,
            )
            after_first = json.loads(self.current_snapshot_path(state).read_text(encoding="utf-8"))
            second = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "sourceUrl",
                "--source-url",
                state_path=state,
            )
            after_second = json.loads(self.current_snapshot_path(state).read_text(encoding="utf-8"))

        self.assertTrue(first["ok"])
        self.assertTrue(second["ok"])
        self.assertIn("## 您关心的信息", first["user_message"])
        self.assertIn("- 原文链接：[查看原文](https://example.gov.cn/source/101)（https://example.gov.cn/source/101）", first["user_message"])
        self.assertIn("您可以直接[查看项目详情](https://www.qianlima.com/bid-101.html)", first["user_message"])
        self.assert_markdown_link(first["user_message"], "查看项目详情", first["full_detail"]["url"])
        self.assert_markdown_link(first["user_message"], "查看原文", first["detail"]["sourceUrl"])
        self.assert_url_only_appears_as_link_target(first["user_message"], first["full_detail"]["url"])
        self.assertNotIn("原文链接：https://example.gov.cn/source/101", first["user_message"])
        self.assertNotIn("详情页链接：https://www.qianlima.com/bid-101.html", first["user_message"])
        self.assertEqual(first["full_detail"]["purchasingUnit"], "北京市第一医院")
        self.assertNotIn("quotas", after_first)
        self.assertNotIn("quotas", after_second)

    def test_live_validation_fails_when_sent_area_is_broader_than_expected(self) -> None:
        spec = importlib.util.spec_from_file_location("live_validate", LIVE_VALIDATE)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        case = {
            "expected_query": {
                "areaIds": [2791],
                "keywords": ["物业"],
                "numPerPage": 10,
            }
        }
        payload = {
            "request_query": {
                "areaIds": [305],
                "keywords": ["物业"],
                "currentPage": 1,
                "numPerPage": 10,
            }
        }

        case["expected_query"] = project_query(case["expected_query"])
        payload["request_query"] = project_query(payload["request_query"])
        ok, note = module.request_matches_expected(case, payload)

        self.assertFalse(ok)
        self.assertIn("地区", note)
        self.assertIn("广东省-广州市", note)

    def test_live_validation_accepts_clear_table_output(self) -> None:
        spec = importlib.util.spec_from_file_location("live_validate", LIVE_VALIDATE)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        card = {
            "id": 101,
            "title": "北京市第一医院实验室设备采购招标公告",
            "purchasingUnit": "北京市第一医院",
            "areaName": "北京市-北京市-东城区",
            "infoType": "公告-招标公告",
            "budgetAmount": "1200000.00",
            "biddingAmount": "",
            "publishTime": "2026-04-10",
            "url": "https://www.qianlima.com/bid-101.html",
        }
        payload = {
            "ok": True,
            "total_count": 1,
            "returned_count": 1,
            "effective_query": {"keywords": ["实验室设备"], "areaIds": [2]},
            "warnings": [],
            "cards": [card],
            "user_message": (
                "| 项目名称 | 招标单位 | 金额 |\n"
                "| --- | --- | --- |\n"
                "| 北京市第一医院实验室设备采购招标公告 | 北京市第一医院 | 120.00 |"
            ),
        }

        self.assertTrue(module.search_passed(payload))


    def test_live_validation_cases_are_plain_language(self) -> None:
        payload = json.loads(LIVE_CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["current_date"], "2026-04-15")
        self.assertGreaterEqual(len(payload["cases"]), 23)
        for case in payload["cases"]:
            self.assertIn("natural_language", case)
            self.assertIn("understanding", case)
            if case["type"] == "search":
                self.assertIn("expected_query", case)
                self.assertIn("numPerPage", case["expected_query"])

    def test_live_validation_writes_markdown_report(self) -> None:
        cases_payload = {
            "current_date": "2026-04-15",
            "cases": [
                {
                    "id": "search_report_mock",
                    "type": "search",
                    "expected_command": "search",
                    "expected_capability": "search-projects",
                    "expected_api_path": "/api/search",
                    "expected_result_type": "project",
                    "natural_language": "帮我看看北京实验室设备项目",
                    "understanding": "北京；关键词“实验室设备”。",
                    "expected_query": {
                        "keywords": ["实验室设备"],
                        "areaIds": [2],
                        "numPerPage": 2,
                    },
                },
                {
                    "id": "area_report_mock",
                    "type": "ambiguous_area",
                    "natural_language": "新区最近的物业招标看看",
                    "understanding": "地区“新区”有歧义，不直接搜索。",
                    "area_phrase": "新区",
                },
                {
                    "id": "next_report_mock",
                    "type": "next_success",
                    "natural_language": "继续看下一批",
                    "understanding": "沿用上一条成功搜索条件，只把页码加 1。",
                },
            ],
        }
        for case in cases_payload["cases"]:
            if case.get("expected_command") == "search":
                case["expected_query"] = project_query(case["expected_query"])
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cases = tmp_path / "cases.json"
            state = tmp_path / "state.json"
            report = tmp_path / "report.md"
            cases.write_text(json.dumps(cases_payload, ensure_ascii=False), encoding="utf-8")
            env = os.environ.copy()
            env["QIANLIMA_MOCK_DIR"] = str(FIXTURES)
            env["QIANLIMA_API_KEY"] = "dummy-test-key"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(LIVE_VALIDATE),
                    "--cases",
                    str(cases),
                    "--state",
                    str(state),
                    "--report-md",
                    str(report),
                ],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            content = report.read_text(encoding="utf-8")

        self.assertIn("# 千里马 Skill 真实验收报告", content)
        self.assertIn("正常业务场景", content)
        self.assertIn("异常场景", content)
        self.assertIn("用户实际看到的数据", content)
        self.assertNotIn("本次生效条件", content)
        self.assertIn("当前查询条件未变，继续展示下一批。", content)
        self.assertIn("北京学校实验室设备采购中标通知", content)
        self.assertIn("138.00", content)
        for internal_word in ("total_count", "returned_count", "effective_query", "warnings", "areaIds", "infoTypes"):
            self.assertNotIn(internal_word, content)

    def test_endpoint_contract_rejects_unsupported_fields_before_request(self) -> None:
        cases = [
            (
                "search-expiring",
                ("--query-json", json.dumps({"keywords": ["物业"], "beginTime": "2026-07-01"}, ensure_ascii=False)),
            ),
            (
                "enterprise",
                (
                    "--kind",
                    "co-bidder-competitors",
                    "--query-json",
                    json.dumps({"companyName": "深圳市城市服务有限公司", "sortType": 2}, ensure_ascii=False),
                ),
            ),
            (
                "enterprise",
                (
                    "--kind",
                    "potential-competitors",
                    "--query-json",
                    json.dumps({"companyName": "深圳市城市服务有限公司", "sortType": 2}, ensure_ascii=False),
                ),
            ),
            (
                "enterprise",
                (
                    "--kind",
                    "business-info",
                    "--query-json",
                    json.dumps({"companyName": "深圳市城市服务有限公司", "beginTime": "2026-01-01"}, ensure_ascii=False),
                ),
            ),
            (
                "enterprise",
                (
                    "--kind",
                    "contacts",
                    "--query-json",
                    json.dumps({"companyName": "深圳市城市服务有限公司", "endTime": "2026-07-01"}, ensure_ascii=False),
                ),
            ),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            for index, (command, extra_args) in enumerate(cases):
                with self.subTest(command=command, extra_args=extra_args):
                    payload = self.run_skill(command, *extra_args, state_path=Path(tmp) / f"state-{index}.json")
                    self.assertFalse(payload["ok"])
                    self.assertEqual(payload["error_code"], "AGENT_QUERY_CORRECTION_REQUIRED")
                    self.assertTrue(payload["requires_agent_correction"])
                    self.assertFalse(payload["requires_user_confirmation"])
                    self.assertIsNone(payload.get("request_query"))
                    self.assertIn("agent_instruction", payload)

    def test_endpoint_specific_constraints_and_amount_self_check(self) -> None:
        invalid_cases = [
            (
                "search-expiring",
                {"keywords": ["物业"], "beginServiceExpireTime": "2026-08-01"},
            ),
            (
                "search-purchase",
                {"keywords": ["设备"], "matchScopes": [11]},
            ),
            (
                "search-expiring",
                {"keywords": ["物业"], "contractPeriodType": 7},
            ),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for index, (command, query) in enumerate(invalid_cases):
                with self.subTest(command=command, query=query):
                    payload = self.run_skill(
                        command,
                        "--query-json",
                        json.dumps(query, ensure_ascii=False),
                        state_path=Path(tmp) / f"invalid-{index}.json",
                    )
                    self.assertFalse(payload["ok"])
                    self.assertIsNone(payload.get("request_query"))

            phone_payload = self.run_skill(
                "enterprise",
                "--kind",
                "contacts",
                "--query-json",
                json.dumps({"companyName": "深圳市城市服务有限公司", "phoneType": 3}, ensure_ascii=False),
                state_path=Path(tmp) / "invalid-phone.json",
            )
            self.assertFalse(phone_payload["ok"])
            self.assertIsNone(phone_payload.get("request_query"))

            amount_payload = self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["物业"], "beginAmount": 500}, ensure_ascii=False),
                state_path=Path(tmp) / "amount-check.json",
            )
            self.assertFalse(amount_payload["ok"])
            self.assertEqual(amount_payload["error_code"], "AMOUNT_UNIT_SELF_CHECK_REQUIRED")
            self.assertTrue(amount_payload["requires_agent_correction"])
            self.assertFalse(amount_payload["requires_user_confirmation"])
            self.assertIn("接口金额单位是元", amount_payload["agent_instruction"])
            self.assertIn("5000000", amount_payload["agent_instruction"])
            self.assertNotIn("请您确认", amount_payload["user_message"])

            confirmed = self.run_skill(
                "search",
                "--query-json",
                json.dumps(
                    {"keywords": ["物业"], "beginAmount": 500, "amount_unit_confirmed": True},
                    ensure_ascii=False,
                ),
                state_path=Path(tmp) / "amount-confirmed.json",
            )
            self.assertTrue(confirmed["ok"])
            self.assertEqual(confirmed["request_query"]["beginAmount"], 500)
            self.assertNotIn("amount_unit_confirmed", confirmed["request_query"])
            self.assertNotIn("amount_unit_confirmed", confirmed["effective_query"])

    def test_detail_fields_and_source_url_are_scoped_by_result_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            purchase_state = tmp_path / "purchase-state.json"
            self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_path=purchase_state,
            )
            unsupported = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--fields",
                "purchasingUnitLinkName,targetKeywords,biddingEndTime",
                state_path=purchase_state,
            )
            self.assertFalse(unsupported["ok"])
            self.assertEqual(unsupported["error_code"], "AGENT_DETAIL_CORRECTION_REQUIRED")
            self.assertTrue(unsupported["requires_agent_correction"])
            self.assertFalse(unsupported["requires_user_confirmation"])
            self.assertNotIn("未公示", unsupported["user_message"])

            unsupported_source = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--source-url",
                state_path=purchase_state,
            )
            self.assertFalse(unsupported_source["ok"])
            self.assertEqual(unsupported_source["error_code"], "AGENT_DETAIL_CORRECTION_REQUIRED")
            self.assertIsNone(unsupported_source.get("request_query"))

            project_state = tmp_path / "project-state.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_path=project_state,
            )
            project_source = self.run_skill(
                "detail",
                "--project-ref",
                "第1条",
                "--source-url",
                state_path=project_state,
            )
            self.assertTrue(project_source["ok"])
            self.assertIn("sourceUrl", project_source["detail"])

            fixtures = self.copy_fixtures(tmp_path)
            (fixtures / "sourceUrl_301.json").write_text(
                json.dumps(
                    {"code": 200, "msg": "", "data": {"sourceUrl": "https://example.gov.cn/source/301"}},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            expiring_state = tmp_path / "expiring-state.json"
            first_code, first = self.run_skill_with_fixtures(
                fixtures,
                "search-expiring",
                "--query-json",
                json.dumps({"keywords": ["物业"], "numPerPage": 2}, ensure_ascii=False),
                state_path=expiring_state,
            )
            self.assertEqual(first_code, 0, first)
            source_code, expiring_source = self.run_skill_with_fixtures(
                fixtures,
                "detail",
                "--project-ref",
                "第1条",
                "--source-url",
                state_path=expiring_state,
            )
            self.assertEqual(source_code, 0, expiring_source)
            self.assertTrue(expiring_source["ok"])
            self.assertEqual(expiring_source["detail"]["sourceUrl"], "https://example.gov.cn/source/301")

    def test_source_url_only_does_not_depend_on_detail_endpoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixtures = self.copy_fixtures(tmp_path)
            self.write_api_error_fixture(fixtures / "detail_101.json", "10025", "详情额度已用完")
            state = tmp_path / "source-only.json"
            self.run_skill_with_fixtures(
                fixtures,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )

            code, payload = self.run_skill_with_fixtures(
                fixtures,
                "detail",
                "--project-ref",
                "第1条",
                "--source-url",
                state_path=state,
            )

        self.assertEqual(code, 0, payload)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["detail"]["sourceUrl"], "https://example.gov.cn/source/101")
        self.assertNotIn("详情额度已用完", payload["user_message"])

    def test_api_return_fields_are_preserved_and_labeled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixtures = self.copy_fixtures(tmp_path)
            search_fixture = json.loads((fixtures / "search_page_1.json").read_text(encoding="utf-8"))
            search_fixture["data"]["list"][0]["winningBidderUnit"] = "北京中标服务有限公司"
            (fixtures / "search_page_1.json").write_text(
                json.dumps(search_fixture, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            code, project = self.run_skill_with_fixtures(
                fixtures,
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "numPerPage": 2}, ensure_ascii=False),
                state_path=tmp_path / "project.json",
            )
            self.assertEqual(code, 0, project)
            self.assertEqual(project["cards"][0]["winningBidderUnit"], "北京中标服务有限公司")
            self.assertIn("中标单位：北京中标服务有限公司", project["user_message"])

            business = self.run_skill(
                "enterprise",
                "--kind",
                "business-info",
                "--query-json",
                json.dumps({"companyName": "深圳市城市服务有限公司"}, ensure_ascii=False),
                state_path=tmp_path / "business.json",
            )
            self.assertTrue(business["ok"])
            for label in ("企业名称", "经营状态", "企业类型", "法定代表人", "注册资本", "成立日期", "统一社会信用代码"):
                self.assertIn(label, business["user_message"])
            self.assertNotIn("companyName：", business["user_message"])

            for kind in ("co-bidder-competitors", "potential-competitors"):
                payload = self.run_skill(
                    "enterprise",
                    "--kind",
                    kind,
                    "--query-json",
                    json.dumps({"companyName": "深圳市城市服务有限公司"}, ensure_ascii=False),
                    state_path=tmp_path / f"{kind}.json",
                )
                self.assertTrue(payload["ok"])
                levels = {row["competitivenessLevel"] for row in payload["rows"]}
                self.assertTrue(levels <= {"高级", "中级", "低级"})


    def test_pagination_verify_and_purchase_default_time_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = tmp_path / "last-page.json"
            self.run_skill(
                "search",
                "--query-json",
                json.dumps({"keywords": ["实验室设备"], "currentPage": 2, "numPerPage": 2}, ensure_ascii=False),
                state_path=state,
            )
            no_more = self.run_skill("next", state_path=state)
            self.assertFalse(no_more["ok"])
            self.assertEqual(no_more["error_code"], "NO_MORE_PAGES")
            self.assertIsNone(no_more.get("request_query"))

            fixtures = self.copy_fixtures(tmp_path)
            invalid_verify = json.loads((fixtures / "verify.json").read_text(encoding="utf-8"))
            invalid_verify["data"] = {"username": ""}
            (fixtures / "verify.json").write_text(
                json.dumps(invalid_verify, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            invalid_code, invalid_payload = self.run_skill_raw(
                fixtures,
                "verify",
                state_path=tmp_path / "invalid-verify.json",
            )
            self.assertEqual(invalid_code, 0)
            self.assertTrue(invalid_payload["ok"])
            self.assertEqual(invalid_payload["user"], {"username": ""})
            self.assertEqual(invalid_payload["api_responses"][0]["response"], invalid_verify)

            valid = self.run_skill("verify", state_path=tmp_path / "valid-verify.json")
            self.assertTrue(valid["ok"])
            self.assertEqual(valid["user"]["username"], "mock-user")

            purchase = self.run_skill(
                "search-purchase",
                "--query-json",
                json.dumps(
                    {
                        "keywords": ["设备"],
                        "beginTime": "2026-06-01",
                        "endTime": "2026-06-30",
                    },
                    ensure_ascii=False,
                ),
                state_path=tmp_path / "purchase-time.json",
            )
            self.assertTrue(purchase["ok"])
            self.assertTrue(any("预计采购时间" in warning and "未来 1 到 3 个月" in warning for warning in purchase["warnings"]))

    def test_mock_enforces_endpoint_contract(self) -> None:
        module = self.load_runtime_module("qianlima_skill_mock_contract")
        client = module.ApiClient("https://skills.qianlima.com", None, str(FIXTURES))
        valid_query = project_query({"keywords": ["实验室设备"], "currentPage": 1, "numPerPage": 2})

        with self.assertRaises(module.SkillError) as wrong_method:
            client._mock_response("GET", "/api/search", valid_query)
        self.assertEqual(wrong_method.exception.code, "MOCK_METHOD_MISMATCH")

        with self.assertRaises(module.SkillError) as extra_field:
            client._mock_response("POST", "/api/search", {**valid_query, "beginServiceExpireTime": "2026-08-01"})
        self.assertEqual(extra_field.exception.code, "AGENT_QUERY_CORRECTION_REQUIRED")

        with self.assertRaises(module.SkillError):
            client._mock_response(
                "POST",
                "/api/search/purchase",
                {"keywords": ["设备"], "matchScopes": [11], "currentPage": 1, "numPerPage": 2},
            )

        with self.assertRaises(module.SkillError):
            client._mock_response(
                "POST",
                "/api/search/expiring",
                {
                    "keywords": ["物业"],
                    "beginServiceExpireTime": "2026-08-01",
                    "currentPage": 1,
                    "numPerPage": 2,
                },
            )

        with self.assertRaises(module.SkillError):
            client._mock_response("POST", "/api/search", {"currentPage": 1, "numPerPage": 2})

        data = client._mock_response("POST", "/api/search", valid_query)
        self.assertIn("rowCount", data)
        self.assertIn("pageCount", data)
        self.assertIsInstance(data["list"], list)



if __name__ == "__main__":
    unittest.main()
