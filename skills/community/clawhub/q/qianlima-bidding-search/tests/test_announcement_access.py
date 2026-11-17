"""Announcement access and explicit query continuation through the real CLI.

Only the external transport is replaced. Request construction, validation,
snapshot handling, response decoding, and command output remain real.
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlparse
import uuid


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "announcement_access_runtime", ROOT / "scripts" / "qianlima_skill.py"
)
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)

ANNOUNCEMENT_ID = "637357877"
OTHER_ID = "637357878"
NODE_ID = "637357879"
QUERY = {
    "keywordGroups": [{"keywords": ["物业"], "matchScopes": [2, 9]}],
    "currentPage": 2,
    "numPerPage": 10,
    "excludeWords": ["电梯"],
    "hasAnnex": 0,
    "beginTime": "2026-09-01 00:00:00",
    "endTime": "2026-09-30 23:59:59",
}
SOURCE_CASES = (
    ("project", "/api/search", QUERY),
    ("purchase_intention", "/api/search/purchase", {
        "keywords": ["物业"], "matchScopes": [2], "currentPage": 2,
        "numPerPage": 10, "startPlanPurchaseDate": "2026-10",
        "endPlanPurchaseDate": "2026-12",
    }),
    ("expiring_project", "/api/search/expiring", {
        "keywords": ["物业"], "matchScopes": [2], "currentPage": 2,
        "numPerPage": 10, "beginServiceExpireTime": "2026-10-01",
        "endServiceExpireTime": "2026-12-31",
    }),
)
SMALL_AMOUNT_FIELDS = {
    "project": ("beginAmount", "endAmount", "search"),
    "purchase_intention": ("startPlanPurchaseAmount", "endPlanPurchaseAmount", "search-purchase"),
    "expiring_project": ("beginContractAmount", "endContractAmount", "search-expiring"),
}
READ_CASES = (
    (["detail", "--id", ANNOUNCEMENT_ID], f"/api/detail/{ANNOUNCEMENT_ID}"),
    (["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "purchase_intention"], f"/api/purchase/detail/{ANNOUNCEMENT_ID}"),
    (["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "expiring_project"], f"/api/expiring/detail/{ANNOUNCEMENT_ID}"),
    (["detail", "--id", ANNOUNCEMENT_ID, "--fields", "sourceUrl"], f"/api/sourceUrl/{ANNOUNCEMENT_ID}"),
    (["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "expiring_project", "--source-url"], f"/api/sourceUrl/{ANNOUNCEMENT_ID}"),
    (["full-text", "--id", ANNOUNCEMENT_ID], f"/api/fullText/{ANNOUNCEMENT_ID}"),
    (["attachments", "--id", ANNOUNCEMENT_ID], f"/api/attachments/{ANNOUNCEMENT_ID}"),
    (["timeline", "--id", ANNOUNCEMENT_ID], f"/api/timeline/{ANNOUNCEMENT_ID}"),
)


def envelope(value, code=200, message="离线响应"):
    return {"code": code, "msg": message, "data": value,
            "success": code == 200, "unknownEnvelopeField": [False, None, 0]}


def card(project_id=ANNOUNCEMENT_ID, title="物业服务公告"):
    return {"id": int(project_id), "title": title, "purchasingUnit": "测试采购单位",
            "url": "https://example.invalid/announcement/" + project_id,
            "unknownCardField": {"empty": None}}


def read_response(path):
    project_id = path.rsplit("/", 1)[-1]
    if "/sourceUrl/" in path:
        value = {"sourceUrl": "https://example.invalid/source/" + project_id, "new": None}
    elif "/fullText/" in path:
        value = {"projectId": int(project_id), "title": "物业服务公告", "content": "合成正文", "new": False}
    elif "/attachments/" in path:
        value = [{"projectId": int(project_id), "fileName": "采购需求.pdf", "fileUrl": "https://example.invalid/file", "fileSize": None, "new": 0}]
    elif "/timeline/" in path:
        value = [card(project_id), card(NODE_ID, "物业服务成交结果")]
    else:
        value = {**card(project_id), "purchaseContent": None, "newDetailField": [0, False, None]}
    return envelope(value)


class AnnouncementAccessTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.state_dir = Path(temp.name) / "state"
        self.state_dir.mkdir()
        self.environment = patch.dict(os.environ, {
            "PYTHONDONTWRITEBYTECODE": "1",
            "QIANLIMA_SKILL_STATE_DIR": str(self.state_dir),
            "QIANLIMA_API_KEY": "offline-test-key-a",
            "QIANLIMA_MOCK_DIR": "",
            "QIANLIMA_SKILL_SESSION_ID": "",
            "QIANLIMA_SKILL_STATE_TTL_SECONDS": "86400",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def call(self, argv, routes=None, observe_request=None):
        calls = []
        responses = routes or {}

        def receive(request, **kwargs):
            path = urlparse(request.full_url).path
            query = json.loads(request.data.decode()) if request.data else None
            calls.append({"path": path, "method": request.method,
                          "query": query, "headers": dict(request.header_items())})
            if observe_request is not None:
                observe_request(calls[-1])
            if path in responses:
                response = responses[path]
            elif path in {"/api/search", "/api/search/purchase", "/api/search/expiring"}:
                response = envelope({"rowCount": 30, "pageCount": 3,
                                     "list": [card()], "new": [None, False]})
            elif path == "/api/searchCompany":
                response = envelope({"total": 30, "currentPage": query["currentPage"],
                                     "pageSize": query["pageSize"],
                                     "list": [{"companyId": 1, "companyName": "测试物业公司", "new": None}]})
            elif path.startswith(("/api/detail/", "/api/purchase/detail/", "/api/expiring/detail/", "/api/sourceUrl/", "/api/fullText/", "/api/attachments/", "/api/timeline/")):
                response = read_response(path)
            else:
                raise AssertionError("Unexpected extra API request: " + path)
            return io.BytesIO(json.dumps(response, ensure_ascii=False).encode())

        output, errors = io.StringIO(), io.StringIO()
        with patch("urllib.request.urlopen", receive), patch("socket.socket", side_effect=AssertionError("Network forbidden")), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            try:
                runtime.main(["--base-url", "https://offline.invalid", *argv])
            except SystemExit as exc:
                return {"ok": False, "error_code": "CLI_ARGUMENT_ERROR", "exit_code": exc.code,
                        "message": errors.getvalue()}, calls
        return json.loads(output.getvalue()), calls

    def seed(self, result_type="project", query=None, cards=None, session_id=None, origin=None):
        if query is None:
            query = next(copy.deepcopy(value) for source, _, value in SOURCE_CASES if source == result_type) if result_type != "company_candidates" else {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}
        snapshot = runtime.save_search_snapshot(
            session_id=session_id or str(uuid.uuid4()), result_type=result_type,
            effective_query=copy.deepcopy(query), viewed_cards=cards if cards is not None else [card()],
            total_count=30, page_count=3,
        )
        if origin:
            snapshot["origin"] = origin
            runtime.save_snapshot(snapshot)
        return snapshot

    def reference(self, snapshot, include_session=True, session_id=None):
        args = ["--result-set-id", snapshot["result_set_id"]]
        if include_session:
            args += ["--session-id", session_id or snapshot["session_id"]]
        return args

    def assert_single_success(self, output, calls, path, response=None):
        self.assertTrue(output.get("ok"), output)
        self.assertEqual([call["path"] for call in calls], [path])
        self.assertEqual(output["api_responses"][0]["path"], path)
        if response is not None:
            self.assertEqual(output["api_responses"][0]["response"], response)

    def assert_rejected_before_request(self, output, calls):
        self.assertFalse(output.get("ok"), output)
        self.assertNotEqual(output.get("error_code"), "CLI_ARGUMENT_ERROR", output)
        self.assertEqual(calls, [])

    def test_all_read_capabilities_accept_known_id_without_context(self):
        for argv, path in READ_CASES:
            with self.subTest(argv=argv):
                response = read_response(path)
                output, calls = self.call(argv, {path: response})
                self.assert_single_success(output, calls, path, response)

    def test_legacy_real_id_forms_are_direct_without_a_result_set(self):
        for ref in (ANNOUNCEMENT_ID, "公告ID " + ANNOUNCEMENT_ID):
            for command, endpoint in (("detail", "detail"), ("full-text", "fullText"), ("attachments", "attachments"), ("timeline", "timeline")):
                with self.subTest(ref=ref, command=command):
                    output, calls = self.call([command, "--project-ref", ref])
                    self.assert_single_success(output, calls, f"/api/{endpoint}/{ANNOUNCEMENT_ID}")

    def test_known_id_is_not_restricted_to_the_supplied_search_list(self):
        snapshot = self.seed(cards=[card(OTHER_ID, "名单 B 中的其他公告")])
        for ref in (ANNOUNCEMENT_ID, "公告ID " + ANNOUNCEMENT_ID):
            with self.subTest(ref=ref):
                output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", ref])
                self.assert_single_success(output, calls, f"/api/detail/{ANNOUNCEMENT_ID}")

    def test_explicit_id_and_source_override_old_context_and_project_ref(self):
        snapshot = self.seed("purchase_intention", cards=[card(OTHER_ID)])
        output, calls = self.call(["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "expiring_project", "--project-ref", "第1条", *self.reference(snapshot)])
        self.assert_single_success(output, calls, f"/api/expiring/detail/{ANNOUNCEMENT_ID}")

    def test_legacy_real_id_preserves_known_context_source(self):
        for source, _, _ in SOURCE_CASES:
            with self.subTest(source=source):
                snapshot = self.seed(source, cards=[card(OTHER_ID)])
                output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", ANNOUNCEMENT_ID])
                prefix = "" if source == "project" else "purchase/" if source == "purchase_intention" else "expiring/"
                self.assert_single_success(output, calls, f"/api/{prefix}detail/{ANNOUNCEMENT_ID}")

    def test_known_id_ignores_missing_expired_and_corrupt_context(self):
        snapshot = self.seed(cards=[card(OTHER_ID)])
        path = runtime.snapshot_path(snapshot["session_id"], snapshot["result_set_id"])
        for state in ("missing", "expired", "corrupt"):
            with self.subTest(state=state):
                if state == "missing":
                    path.unlink(missing_ok=True)
                elif state == "expired":
                    path.parent.mkdir(exist_ok=True)
                    path.write_text(json.dumps({**snapshot, "expires_at": "2000-01-01T00:00:00+00:00"}))
                else:
                    path.parent.mkdir(exist_ok=True)
                    path.write_text("{broken-json")
                for argv, endpoint in READ_CASES:
                    output, calls = self.call([*argv, *self.reference(snapshot)])
                    self.assert_single_success(output, calls, endpoint)

    def test_known_id_does_not_touch_an_unusable_state_directory(self):
        blocked = self.state_dir.parent / "state-is-a-file"
        blocked.write_text("unavailable directory")
        with patch.dict(os.environ, {"QIANLIMA_SKILL_STATE_DIR": str(blocked)}):
            for argv, path in READ_CASES:
                with self.subTest(argv=argv):
                    output, calls = self.call(argv)
                    self.assert_single_success(output, calls, path)

    def test_explicit_result_set_can_be_used_without_or_with_a_new_session(self):
        for session in (None, str(uuid.uuid4())):
            for source, path, query in SOURCE_CASES:
                with self.subTest(session=session, source=source):
                    snapshot = self.seed(source)
                    ref = self.reference(snapshot, include_session=session is not None, session_id=session)
                    output, calls = self.call(["next", *ref])
                    self.assert_single_success(output, calls, path)
                    self.assertEqual(calls[0]["query"], {**query, "currentPage": 3})

    def test_new_session_can_locate_ordinal_in_an_explicit_result_set(self):
        snapshot = self.seed(cards=[card(OTHER_ID), card(ANNOUNCEMENT_ID)])
        output, calls = self.call(["detail", "--project-ref", "第2条", *self.reference(snapshot, session_id=str(uuid.uuid4()))])
        self.assert_single_success(output, calls, f"/api/detail/{ANNOUNCEMENT_ID}")

    def test_snapshot_identity_corruption_is_not_hidden_by_session_lookup(self):
        for field in ("session_id", "result_set_id"):
            with self.subTest(field=field):
                snapshot = self.seed()
                path = runtime.snapshot_path(snapshot["session_id"], snapshot["result_set_id"])
                path.write_text(json.dumps({**snapshot, field: str(uuid.uuid4())}))
                output, calls = self.call(["next", *self.reference(snapshot, session_id=str(uuid.uuid4()))])
                self.assert_rejected_before_request(output, calls)

    def test_current_key_is_used_when_referring_to_an_existing_query(self):
        snapshot = self.seed()
        with patch.dict(os.environ, {"QIANLIMA_API_KEY": "offline-test-key-b"}):
            output, calls = self.call(["next", *self.reference(snapshot)])
        self.assert_single_success(output, calls, "/api/search")
        self.assertEqual(calls[0]["headers"].get("Qianlimaapikey"), "offline-test-key-b")
        for path in self.state_dir.rglob("*.json"):
            text = path.read_text()
            self.assertNotIn("offline-test-key-a", text)
            self.assertNotIn("offline-test-key-b", text)

    def test_same_session_explicit_a_reference_is_not_replaced_by_later_b(self):
        session = str(uuid.uuid4())
        a = self.seed(cards=[card(OTHER_ID), card(ANNOUNCEMENT_ID)], session_id=session)
        self.seed(cards=[card(NODE_ID), card(OTHER_ID)], session_id=session)
        output, calls = self.call(["detail", *self.reference(a), "--project-ref", "第2条"])
        self.assert_single_success(output, calls, f"/api/detail/{ANNOUNCEMENT_ID}")

    def test_empty_explicit_result_does_not_fall_back_to_older_nonempty_list(self):
        session = str(uuid.uuid4())
        self.seed(cards=[card()], session_id=session)
        empty = self.seed(cards=[], session_id=session)
        output, calls = self.call(["detail", *self.reference(empty), "--project-ref", "第1条"])
        self.assert_rejected_before_request(output, calls)

    def test_object_reference_without_query_is_not_guessed_from_recent_state(self):
        self.seed()
        for ref in ("第1条", "物业服务公告", "当前项目"):
            with self.subTest(ref=ref):
                output, calls = self.call(["detail", "--project-ref", ref])
                self.assert_rejected_before_request(output, calls)

    def test_ambiguous_title_is_not_resolved_to_first_matching_announcement(self):
        snapshot = self.seed(cards=[card(), card(OTHER_ID, "物业服务采购公告")])
        output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "物业服务"])
        self.assert_rejected_before_request(output, calls)

    def test_business_or_company_identifiers_cannot_replace_announcement_id(self):
        for value in ("LAB-2026-001", "companyId:1", "第1条", "物业服务公告"):
            with self.subTest(value=value):
                output, calls = self.call(["detail", "--id", value])
                self.assert_rejected_before_request(output, calls)

    def test_timeline_ordinal_uses_timeline_nodes_and_known_node_is_independent(self):
        snapshot = self.seed()
        timeline, calls = self.call(["timeline", *self.reference(snapshot), "--project-ref", "第1条"])
        self.assert_single_success(timeline, calls, f"/api/timeline/{ANNOUNCEMENT_ID}")
        node_ref = ["--result-set-id", timeline["follow_up"]["result_set_id"], "--session-id", str(uuid.uuid4())]
        detail, calls = self.call(["detail", *node_ref, "--project-ref", "第2条"])
        self.assert_single_success(detail, calls, f"/api/detail/{NODE_ID}")
        direct, calls = self.call(["detail", "--id", NODE_ID])
        self.assert_single_success(direct, calls, f"/api/detail/{NODE_ID}")

    def test_timeline_and_company_snapshots_reject_project_next_and_refine(self):
        for snapshot in (self.seed(origin="timeline"), self.seed("company_candidates")):
            for command in ("next", "refine"):
                with self.subTest(source=snapshot["result_type"], origin=snapshot.get("origin"), command=command):
                    args = [command, *self.reference(snapshot)]
                    if command == "refine":
                        args += ["--query-json", '{"hasAnnex":1}']
                    output, calls = self.call(args)
                    self.assert_rejected_before_request(output, calls)

    def test_full_context_recovers_each_source_without_cached_state_or_total_pages(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                context = {"result_type": source, "effective_query": query}
                output, calls = self.call(["next", "--context-json", json.dumps(context)])
                self.assert_single_success(output, calls, path)
                self.assertEqual(calls[0]["query"], {**query, "currentPage": 3})

    def test_full_context_recovers_missing_expired_or_corrupt_explicit_snapshot(self):
        snapshot = self.seed()
        path = runtime.snapshot_path(snapshot["session_id"], snapshot["result_set_id"])
        for state in ("missing", "expired", "corrupt"):
            with self.subTest(state=state):
                if state == "missing":
                    path.unlink(missing_ok=True)
                elif state == "expired":
                    path.parent.mkdir(exist_ok=True)
                    path.write_text(json.dumps({**snapshot, "expires_at": "2000-01-01T00:00:00+00:00"}))
                else:
                    path.parent.mkdir(exist_ok=True)
                    path.write_text("[broken-json")
                context = {"result_type": "project", "effective_query": QUERY, "page_count": 3}
                output, calls = self.call(["next", *self.reference(snapshot), "--context-json", json.dumps(context)])
                self.assert_single_success(output, calls, "/api/search")
                self.assertEqual(calls[0]["query"], {**QUERY, "currentPage": 3})

    def test_refine_context_changes_only_patch_and_starts_at_first_page(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                context = {"result_type": source, "effective_query": query}
                patch_query = {"excludeWords": ["保洁"]}
                output, calls = self.call(["refine", "--context-json", json.dumps(context), "--query-json", json.dumps(patch_query)])
                self.assert_single_success(output, calls, path)
                self.assertEqual(calls[0]["query"], {**query, **patch_query, "currentPage": 1})

    def test_company_next_recovers_explicit_context_and_uses_company_paging(self):
        query = {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}
        context = {"result_type": "company_candidates", "effective_query": query}
        output, calls = self.call(["search-company", "--next", "--context-json", json.dumps(context)])
        self.assert_single_success(output, calls, "/api/searchCompany")
        self.assertEqual(calls[0]["query"], {**query, "currentPage": 3})
        self.assertNotIn("numPerPage", calls[0]["query"])

    def test_company_next_can_reference_existing_result_from_a_new_session(self):
        snapshot = self.seed("company_candidates")
        output, calls = self.call(["search-company", "--next", *self.reference(snapshot, session_id=str(uuid.uuid4()))])
        self.assert_single_success(output, calls, "/api/searchCompany")
        self.assertEqual(calls[0]["query"], {**snapshot["effective_query"], "currentPage": 3})

    def test_context_must_include_source_required_conditions_and_explicit_paging(self):
        bad_contexts = [
            {"effective_query": QUERY},
            {"result_type": "unrecognized", "effective_query": QUERY},
            {"result_type": "project"},
            {"result_type": "project", "effective_query": {k: v for k, v in QUERY.items() if k != "keywordGroups"}},
            {"result_type": "project", "effective_query": {k: v for k, v in QUERY.items() if k != "currentPage"}},
            {"result_type": "project", "effective_query": {k: v for k, v in QUERY.items() if k != "numPerPage"}},
            {"result_type": "purchase_intention", "effective_query": QUERY},
            {"result_type": "project", "effective_query": {**QUERY, "currentPage": 0}},
            {"result_type": "project", "effective_query": {**QUERY, "numPerPage": "unknown"}},
        ]
        self.seed()
        for context in bad_contexts:
            with self.subTest(context=context):
                output, calls = self.call(["next", "--context-json", json.dumps(context)])
                self.assert_rejected_before_request(output, calls)

    def test_company_context_rejects_missing_fields_and_wrong_source(self):
        query = {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}
        bad = [{"result_type": "project", "effective_query": query}, {"result_type": "unknown", "effective_query": query}]
        bad += [{"result_type": "company_candidates", "effective_query": {k: v for k, v in query.items() if k != missing}} for missing in query]
        for context in bad:
            with self.subTest(context=context):
                output, calls = self.call(["search-company", "--next", "--context-json", json.dumps(context)])
                self.assert_rejected_before_request(output, calls)

    def test_context_origin_and_source_cannot_turn_timeline_or_company_into_project_search(self):
        for context in ({"result_type": "project", "origin": "timeline", "effective_query": QUERY}, {"result_type": "company_candidates", "effective_query": {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}}):
            for command in ("next", "refine"):
                with self.subTest(context=context, command=command):
                    args = [command, "--context-json", json.dumps(context)]
                    if command == "refine":
                        args += ["--query-json", '{"hasAnnex":1}']
                    output, calls = self.call(args)
                    self.assert_rejected_before_request(output, calls)

    def test_next_does_not_automatically_take_the_most_recent_query(self):
        self.seed()
        output, calls = self.call(["next"])
        self.assert_rejected_before_request(output, calls)

    def test_expired_query_requests_missing_context_without_research_approval(self):
        snapshot = self.seed()
        path = runtime.snapshot_path(snapshot["session_id"], snapshot["result_set_id"])
        path.write_text(json.dumps({**snapshot, "expires_at": "2000-01-01T00:00:00+00:00"}))
        output, calls = self.call(["next", *self.reference(snapshot)])
        self.assert_rejected_before_request(output, calls)
        self.assertEqual(output["error_code"], "RESULT_SET_EXPIRED")
        self.assertFalse(output.get("requires_user_confirmation"), output)
        self.assertTrue(output.get("needs_clarification"), output)
        self.assertIn("--context-json", output.get("agent_instruction", ""))

    def test_ordinal_object_read_does_not_require_cached_query_paging(self):
        snapshot = self.seed(query={"keywordGroups": QUERY["keywordGroups"]})
        output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "第1条"])
        self.assert_single_success(output, calls, f"/api/detail/{ANNOUNCEMENT_ID}")

    def test_cached_continuation_without_page_or_size_never_guesses(self):
        for missing in ("currentPage", "numPerPage"):
            with self.subTest(missing=missing):
                snapshot = self.seed(query={key: value for key, value in QUERY.items() if key != missing})
                output, calls = self.call(["next", *self.reference(snapshot)])
                self.assert_rejected_before_request(output, calls)

    def test_known_last_page_does_not_make_an_extra_business_request(self):
        context = {"result_type": "project", "effective_query": {**QUERY, "currentPage": 3}, "page_count": 3}
        output, calls = self.call(["next", "--context-json", json.dumps(context)])
        self.assert_rejected_before_request(output, calls)

    def test_known_empty_query_does_not_make_an_extra_next_page_request(self):
        for source, command, query in (("project", ["next"], QUERY), ("company_candidates", ["search-company", "--next"], {"companyName": "测试物业", "currentPage": 1, "pageSize": 10})):
            with self.subTest(source=source):
                context = {"result_type": source, "effective_query": query, "page_count": 0, "total_count": 0}
                output, calls = self.call([*command, "--context-json", json.dumps(context)])
                self.assertNotEqual(output.get("error_code"), "CLI_ARGUMENT_ERROR", output)
                self.assertEqual(calls, [], output)

    def test_business_failure_is_preserved_without_trying_another_source(self):
        path = f"/api/purchase/detail/{ANNOUNCEMENT_ID}"
        response = envelope({"originalReason": None}, code=10005, message="公告不存在")
        output, calls = self.call(["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "purchase_intention"], {path: response})
        self.assertFalse(output.get("ok"), output)
        self.assertEqual(output.get("error_code"), "10005")
        self.assertEqual([call["path"] for call in calls], [path])
        self.assertEqual(output["api_responses"][0]["response"], response)

    def test_purchase_source_url_remains_an_unsupported_capability(self):
        output, calls = self.call(["detail", "--id", ANNOUNCEMENT_ID, "--result-type", "purchase_intention", "--fields", "sourceUrl"])
        self.assert_rejected_before_request(output, calls)

    def test_full_context_business_failure_keeps_original_result_and_does_not_restart(self):
        context = {"result_type": "project", "effective_query": QUERY}
        response = envelope({"unknown": [None]}, code=10005, message="业务查询失败")
        output, calls = self.call(["next", "--context-json", json.dumps(context)], {"/api/search": response})
        self.assertFalse(output.get("ok"), output)
        self.assertEqual(output.get("error_code"), "10005")
        self.assertEqual([call["path"] for call in calls], ["/api/search"])
        self.assertEqual(calls[0]["query"], {**QUERY, "currentPage": 3})
        self.assertEqual(output["api_responses"][0]["response"], response)

    def test_partial_detail_and_source_retains_success_and_each_business_reason(self):
        detail_path, source_path = f"/api/detail/{ANNOUNCEMENT_ID}", f"/api/sourceUrl/{ANNOUNCEMENT_ID}"
        success = read_response(detail_path)
        failure = envelope(None, code=10011, message="原文不存在")
        output, calls = self.call(["detail", "--id", ANNOUNCEMENT_ID, "--fields", "title,sourceUrl"], {detail_path: success, source_path: failure})
        self.assertFalse(output.get("ok"), output)
        self.assertTrue(output.get("partial_success"), output)
        self.assertEqual([call["path"] for call in calls], [detail_path, source_path])
        self.assertEqual([entry["response"] for entry in output["api_responses"]], [success, failure])

    def test_unwritable_state_does_not_prevent_new_search_or_continuation_request(self):
        blocked = self.state_dir.parent / "state-is-a-file"
        blocked.write_text("unavailable directory")
        context = {"result_type": "project", "effective_query": QUERY}
        with patch.dict(os.environ, {"QIANLIMA_SKILL_STATE_DIR": str(blocked)}):
            for argv in (["search", "--query-json", json.dumps(QUERY)], ["next", "--context-json", json.dumps(context)], ["refine", "--context-json", json.dumps(context), "--query-json", '{"hasAnnex":1}']):
                with self.subTest(argv=argv):
                    output, calls = self.call(argv)
                    self.assert_single_success(output, calls, "/api/search")
                    self.assertNotIn("follow_up", output)

    def test_post_response_save_failure_keeps_success_and_never_replays(self):
        snapshot = self.seed()
        for argv, path in ((["detail", *self.reference(snapshot), "--project-ref", "第1条"], f"/api/detail/{ANNOUNCEMENT_ID}"), (["next", *self.reference(snapshot)], "/api/search"), (["timeline", *self.reference(snapshot), "--project-ref", "第1条"], f"/api/timeline/{ANNOUNCEMENT_ID}")):
            with self.subTest(argv=argv), patch.object(runtime, "save_json", side_effect=runtime.SkillError("STATE_STORE_UNAVAILABLE", "离线保存失败")):
                output, calls = self.call(argv)
                self.assert_single_success(output, calls, path)
                self.assertEqual(output["api_responses"][0]["response"]["code"], 200)
                self.assertNotIn("follow_up", output)

    def test_review_cached_confirmed_small_amount_survives_next_and_refine(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, upper, command = SMALL_AMOUNT_FIELDS[source]
                initial_query = {**query, "currentPage": 1, lower: 5000, upper: 9000, "amount_unit_confirmed": True}
                first, calls = self.call([command, "--query-json", json.dumps(initial_query)])
                self.assert_single_success(first, calls, path)
                for action in ("next", "refine"):
                    with self.subTest(action=action):
                        args = [action, *self.reference(first["follow_up"])]
                        if action == "refine":
                            args += ["--query-json", '{"excludeWords":["保洁"]}']
                        output, calls = self.call(args)
                        self.assert_single_success(output, calls, path)
                        self.assertEqual(calls[0]["query"][lower], 5000)
                        self.assertEqual(calls[0]["query"][upper], 9000)
                        self.assertEqual(calls[0]["query"]["currentPage"], 2 if action == "next" else 1)
                        self.assertNotIn("amount_unit_confirmed", calls[0]["query"])

    def test_review_context_restores_original_effective_query_without_unit_ack(self):
        for source, path, query in SOURCE_CASES:
            lower, upper, command = SMALL_AMOUNT_FIELDS[source]
            first, calls = self.call([command, "--query-json", json.dumps({**query, lower: 5000, upper: 9000, "amount_unit_confirmed": True})])
            self.assert_single_success(first, calls, path)
            self.assertNotIn("amount_unit_confirmed", first["effective_query"])
            context = {"result_type": source, "effective_query": first["effective_query"]}
            for action in ("next", "refine"):
                with self.subTest(source=source, action=action):
                    args = [action, "--context-json", json.dumps(context)]
                    if action == "refine":
                        args += ["--query-json", "{}"]
                    output, calls = self.call(args)
                    self.assert_single_success(output, calls, path)
                    self.assertEqual(calls[0]["query"], {**first["effective_query"], "currentPage": 3 if action == "next" else 1})
                    self.assertNotIn("amount_unit_confirmed", calls[0]["query"])

    def test_review_first_unconfirmed_small_amount_is_not_silently_trusted(self):
        for source, _, query in SOURCE_CASES:
            lower, _, command = SMALL_AMOUNT_FIELDS[source]
            unconfirmed = {**query, lower: 5000}
            with self.subTest(source=source):
                output, calls = self.call([command, "--query-json", json.dumps(unconfirmed)])
                self.assert_rejected_before_request(output, calls)
                self.assertEqual(output.get("error_code"), "AMOUNT_UNIT_SELF_CHECK_REQUIRED")

    def test_review_context_unchanged_amount_patch_needs_no_new_ack(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, _, command = SMALL_AMOUNT_FIELDS[source]
                first, calls = self.call([command, "--query-json", json.dumps({**query, lower: 5000, "amount_unit_confirmed": True})])
                self.assert_single_success(first, calls, path)
                context = {"result_type": source, "effective_query": first["effective_query"]}
                output, calls = self.call(["refine", "--context-json", json.dumps(context), "--query-json", json.dumps({lower: 5000})])
                self.assert_single_success(output, calls, path)
                self.assertEqual(calls[0]["query"], {**first["effective_query"], "currentPage": 1})

    def test_review_context_changed_amount_still_requires_new_unit_check(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, upper, command = SMALL_AMOUNT_FIELDS[source]
                first, calls = self.call([command, "--query-json", json.dumps({**query, lower: 5000, upper: 9000, "amount_unit_confirmed": True})])
                self.assert_single_success(first, calls, path)
                context = {"result_type": source, "effective_query": first["effective_query"]}
                args = ["refine", "--context-json", json.dumps(context), "--query-json"]
                rejected, calls = self.call([*args, json.dumps({lower: 7000})])
                self.assert_rejected_before_request(rejected, calls)
                self.assertEqual(rejected.get("error_code"), "AMOUNT_UNIT_SELF_CHECK_REQUIRED")
                self.assertEqual(rejected.get("amount_field"), lower)
                self.assertEqual(rejected.get("amount_value"), 7000)
                confirmed, calls = self.call([*args, json.dumps({lower: 7000, "amount_unit_confirmed": True})])
                self.assert_single_success(confirmed, calls, path)
                self.assertEqual(calls[0]["query"], {**first["effective_query"], lower: 7000, "currentPage": 1})
                self.assertNotIn("amount_unit_confirmed", calls[0]["query"])

    def test_review_new_small_amount_patch_still_requires_its_own_unit_check(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, upper, command = SMALL_AMOUNT_FIELDS[source]
                first, calls = self.call([command, "--query-json", json.dumps({**query, "currentPage": 1, lower: 5000, upper: 9000, "amount_unit_confirmed": True})])
                self.assert_single_success(first, calls, path)
                rejected, calls = self.call(["refine", *self.reference(first["follow_up"]), "--query-json", json.dumps({lower: 7000})])
                self.assert_rejected_before_request(rejected, calls)
                self.assertEqual(rejected.get("error_code"), "AMOUNT_UNIT_SELF_CHECK_REQUIRED")
                confirmed, calls = self.call(["refine", *self.reference(first["follow_up"]), "--query-json", json.dumps({lower: 7000, "amount_unit_confirmed": True})])
                self.assert_single_success(confirmed, calls, path)
                self.assertEqual(calls[0]["query"][lower], 7000)
                self.assertEqual(calls[0]["query"][upper], 9000)
                self.assertNotIn("amount_unit_confirmed", calls[0]["query"])

    def test_review_unchanged_amount_patch_keeps_the_existing_unit_check(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, _, command = SMALL_AMOUNT_FIELDS[source]
                first, calls = self.call([command, "--query-json", json.dumps({**query, "currentPage": 1, lower: 5000, "amount_unit_confirmed": True})])
                self.assert_single_success(first, calls, path)
                output, calls = self.call(["refine", *self.reference(first["follow_up"]), "--query-json", json.dumps({lower: 5000})])
                self.assert_single_success(output, calls, path)
                self.assertEqual(calls[0]["query"][lower], 5000)

    def test_review_bad_paging_does_not_prevent_ordinal_announcement_reads(self):
        for source, _, query in SOURCE_CASES:
            for field in ("currentPage", "numPerPage"):
                for value in (None, "unknown", 0):
                    with self.subTest(source=source, field=field, value=value):
                        snapshot = self.seed(source, query={**query, field: value})
                        output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "第1条"])
                        prefix = "" if source == "project" else "purchase/" if source == "purchase_intention" else "expiring/"
                        self.assert_single_success(output, calls, f"/api/{prefix}detail/{ANNOUNCEMENT_ID}")
                        self.assertNotIn("next", output.get("follow_up", {}).get("allowed_actions", []))
                        self.assertNotIn("refine", output.get("follow_up", {}).get("allowed_actions", []))

    def test_review_ordinal_object_read_does_not_require_search_conditions(self):
        for source, _, _ in SOURCE_CASES:
            with self.subTest(source=source):
                snapshot = self.seed(source, query={})
                output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "第1条"])
                prefix = "" if source == "project" else "purchase/" if source == "purchase_intention" else "expiring/"
                self.assert_single_success(output, calls, f"/api/{prefix}detail/{ANNOUNCEMENT_ID}")
                for action in ("next", "refine"):
                    args = [action, *self.reference(snapshot)]
                    if action == "refine":
                        args += ["--query-json", '{"excludeWords":["保洁"]}']
                    rejected, calls = self.call(args)
                    self.assert_rejected_before_request(rejected, calls)

    def test_review_bad_paging_still_prevents_next_and_refine_guessing(self):
        for source, _, query in SOURCE_CASES:
            for field in ("currentPage", "numPerPage"):
                for value in (None, "unknown", 0):
                    for action in ("next", "refine"):
                        with self.subTest(source=source, field=field, value=value, action=action):
                            snapshot = self.seed(source, query={**query, field: value})
                            args = [action, *self.reference(snapshot)]
                            if action == "refine":
                                args += ["--query-json", '{"excludeWords":["保洁"]}']
                            output, calls = self.call(args)
                            self.assert_rejected_before_request(output, calls)

    def test_review_expired_snapshot_locates_object_without_reviving_query(self):
        for source, _, _ in SOURCE_CASES:
            with self.subTest(source=source):
                snapshot = self.seed(source)
                path = runtime.snapshot_path(snapshot["session_id"], snapshot["result_set_id"])
                expired_at = "2000-01-01T00:00:00+00:00"
                path.write_text(json.dumps({**snapshot, "expires_at": expired_at}))
                output, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "第1条"])
                prefix = "" if source == "project" else "purchase/" if source == "purchase_intention" else "expiring/"
                self.assert_single_success(output, calls, f"/api/{prefix}detail/{ANNOUNCEMENT_ID}")
                self.assertTrue(path.exists())
                self.assertEqual(json.loads(path.read_text())["expires_at"], expired_at)
                self.assertNotIn("next", output.get("follow_up", {}).get("allowed_actions", []))
                rejected, calls = self.call(["next", *self.reference(snapshot)])
                self.assert_rejected_before_request(rejected, calls)
                self.assertEqual(rejected.get("error_code"), "RESULT_SET_EXPIRED")
                cleared, calls = self.call(["detail", *self.reference(snapshot), "--project-ref", "第1条"])
                self.assert_rejected_before_request(cleared, calls)
                self.assertEqual(cleared.get("error_code"), "RESULT_SET_NOT_FOUND")

    def test_review_complex_refine_inherits_checked_amount_without_rechecking(self):
        for source, path, query in SOURCE_CASES:
            lower, _, command = SMALL_AMOUNT_FIELDS[source]
            first, calls = self.call([command, "--query-json", json.dumps({**query, lower: 5000, "amount_unit_confirmed": True})])
            self.assert_single_success(first, calls, path)
            for session_id in (None, str(uuid.uuid4())):
                for condition, expected_patch in (({"id": "e", "type": "exclude_words", "value": ["保洁"]}, {"excludeWords": ["保洁"]}), ({"id": "m", "type": "amount_min", "value": 5000}, {lower: 5000})):
                    with self.subTest(source=source, session_id=session_id, condition=condition):
                        operation = {"id": "op", "action": "refine", "data_source": source, "result_set_id": first["follow_up"]["result_set_id"]}
                        if session_id is not None:
                            operation["session_id"] = session_id
                        plan = {"conditions": [condition], "operations": [operation]}
                        output, calls = self.call(["preflight-complex", "--plan-json", json.dumps(plan)])
                        self.assertTrue(output.get("ok"), output)
                        self.assertEqual(calls, [])
                        self.assertEqual(output["approved_operations"][0]["query"], expected_patch)
                        self.assertNotIn("amount_unit_confirmed", output["approved_operations"][0]["query"])

    def test_review_complex_refine_changed_small_amount_is_not_silently_trusted(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                lower, _, command = SMALL_AMOUNT_FIELDS[source]
                first, calls = self.call([command, "--query-json", json.dumps({**query, lower: 5000, "amount_unit_confirmed": True})])
                self.assert_single_success(first, calls, path)
                operation = {"id": "op", "action": "refine", "data_source": source, "session_id": first["follow_up"]["session_id"], "result_set_id": first["follow_up"]["result_set_id"]}
                plan = {"conditions": [{"id": "m", "type": "amount_min", "value": 7000}], "operations": [operation]}
                output, calls = self.call(["preflight-complex", "--plan-json", json.dumps(plan)])
                self.assert_rejected_before_request(output, calls)
                self.assertEqual(output.get("approved_operations"), [])

    def test_review_complex_refine_cannot_guess_missing_result_or_original_conditions(self):
        for source, _, _ in SOURCE_CASES:
            for missing in ("result_set_id", "effective_query"):
                with self.subTest(source=source, missing=missing):
                    snapshot = self.seed(source, query={} if missing == "effective_query" else None)
                    operation = {"id": "op", "action": "refine", "data_source": source, "session_id": str(uuid.uuid4())}
                    if missing != "result_set_id":
                        operation["result_set_id"] = snapshot["result_set_id"]
                    plan = {"conditions": [{"id": "e", "type": "exclude_words", "value": ["保洁"]}], "operations": [operation]}
                    output, calls = self.call(["preflight-complex", "--plan-json", json.dumps(plan)])
                    self.assert_rejected_before_request(output, calls)
                    self.assertEqual(output.get("approved_operations"), [])

    def test_review_successful_query_cleans_expired_cache_after_business_response(self):
        cases = [(SMALL_AMOUNT_FIELDS[source][2], path, query) for source, path, query in SOURCE_CASES]
        cases.append(("search-company", "/api/searchCompany", {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}))
        for command, path, query in cases:
            with self.subTest(command=command):
                old = self.seed()
                expired_path = runtime.snapshot_path(old["session_id"], old["result_set_id"])
                expired_path.write_text(json.dumps({**old, "expires_at": "2000-01-01T00:00:00+00:00"}))
                output, calls = self.call([command, "--query-json", json.dumps(query)], observe_request=lambda request: self.assertTrue(expired_path.exists(), "cache cleanup must follow the API request"))
                self.assert_single_success(output, calls, path)
                self.assertFalse(expired_path.exists())
                self.assertIn("follow_up", output)

    def test_review_cleanup_failure_keeps_success_raw_response_and_saved_followup(self):
        cases = [(SMALL_AMOUNT_FIELDS[source][2], path, query) for source, path, query in SOURCE_CASES]
        cases.append(("search-company", "/api/searchCompany", {"companyName": "测试物业", "currentPage": 2, "pageSize": 10}))
        for command, path, query in cases:
            with self.subTest(command=command), patch.object(runtime, "cleanup_expired_snapshots", side_effect=OSError("offline cleanup unavailable")) as cleanup:
                data = {"total": 30, "currentPage": 2, "pageSize": 10, "list": [{"companyId": 1, "companyName": "测试物业公司", "new": None}]} if command == "search-company" else {"rowCount": 30, "pageCount": 3, "list": [card()], "new": [None, False]}
                response = envelope(data)
                output, calls = self.call([command, "--query-json", json.dumps(query)], {path: response})
                self.assert_single_success(output, calls, path, response)
                cleanup.assert_called_once()
                self.assertEqual(output["rows" if command == "search-company" else "cards"], data["list"])
                self.assertIn("follow_up", output)

    def test_quality_context_excessive_page_size_is_rejected_without_clamping(self):
        for source, _, query in SOURCE_CASES:
            for action in ("next", "refine"):
                with self.subTest(source=source, action=action):
                    context = {"result_type": source, "effective_query": {**query, "numPerPage": 101}}
                    args = [action, "--context-json", json.dumps(context)]
                    if action == "refine":
                        args += ["--query-json", '{"excludeWords":["保洁"]}']
                    output, calls = self.call(args)
                    self.assert_rejected_before_request(output, calls)

    def test_quality_cached_excessive_page_size_is_rejected_without_clamping(self):
        for source, _, query in SOURCE_CASES:
            for action in ("next", "refine"):
                with self.subTest(source=source, action=action):
                    snapshot = self.seed(source, query={**query, "numPerPage": 101})
                    args = [action, *self.reference(snapshot)]
                    if action == "refine":
                        args += ["--query-json", '{"excludeWords":["保洁"]}']
                    output, calls = self.call(args)
                    self.assert_rejected_before_request(output, calls)

    def test_quality_company_context_and_cache_page_size_boundaries(self):
        for size in (20, 21):
            for storage in ("context", "cache"):
                with self.subTest(size=size, storage=storage):
                    query = {"companyName": "测试物业", "currentPage": 2, "pageSize": size}
                    args = ["search-company", "--next"]
                    if storage == "context":
                        args += ["--context-json", json.dumps({"result_type": "company_candidates", "effective_query": query})]
                    else:
                        args += self.reference(self.seed("company_candidates", query=query))
                    output, calls = self.call(args)
                    if size == 21:
                        self.assert_rejected_before_request(output, calls)
                    else:
                        self.assert_single_success(output, calls, "/api/searchCompany")
                        self.assertEqual(calls[0]["query"], {**query, "currentPage": 3})

    def test_quality_project_page_size_upper_boundary_is_preserved(self):
        for source, path, original in SOURCE_CASES:
            for storage in ("context", "cache"):
                for action in ("next", "refine"):
                    with self.subTest(source=source, storage=storage, action=action):
                        query = {**original, "numPerPage": 100}
                        args = [action]
                        if storage == "context":
                            args += ["--context-json", json.dumps({"result_type": source, "effective_query": query})]
                        else:
                            args += self.reference(self.seed(source, query=query))
                        patch_query = {"excludeWords": ["保洁"]} if action == "refine" else {}
                        if action == "refine":
                            args += ["--query-json", json.dumps(patch_query)]
                        output, calls = self.call(args)
                        self.assert_single_success(output, calls, path)
                        self.assertEqual(calls[0]["query"], {**query, **patch_query, "currentPage": 3 if action == "next" else 1})

    def test_quality_excessive_page_size_does_not_block_announcement_reads(self):
        for source, _, query in SOURCE_CASES:
            with self.subTest(source=source):
                snapshot = self.seed(source, query={**query, "numPerPage": 101})
                prefix = "" if source == "project" else "purchase/" if source == "purchase_intention" else "expiring/"
                for ref_args in (["--project-ref", "第1条"], ["--id", ANNOUNCEMENT_ID, "--result-type", source]):
                    output, calls = self.call(["detail", *self.reference(snapshot), *ref_args])
                    self.assert_single_success(output, calls, f"/api/{prefix}detail/{ANNOUNCEMENT_ID}")
                    self.assertNotIn("next", output.get("follow_up", {}).get("allowed_actions", []))

    def test_quality_first_search_keeps_existing_page_size_clamp_strategy(self):
        for source, path, query in SOURCE_CASES:
            with self.subTest(source=source):
                command = SMALL_AMOUNT_FIELDS[source][2]
                output, calls = self.call([command, "--query-json", json.dumps({**query, "numPerPage": 101})])
                self.assert_single_success(output, calls, path)
                self.assertEqual(calls[0]["query"]["numPerPage"], 100)
                self.assertTrue(output.get("warnings"), output)

    def test_quality_refine_excessive_page_size_patch_is_rejected_without_clamping(self):
        for source, _, query in SOURCE_CASES:
            for storage in ("context", "cache"):
                with self.subTest(source=source, storage=storage):
                    args = ["refine", "--query-json", '{"numPerPage":101}']
                    if storage == "context":
                        args += ["--context-json", json.dumps({"result_type": source, "effective_query": query})]
                    else:
                        args += self.reference(self.seed(source, query=query))
                    output, calls = self.call(args)
                    self.assert_rejected_before_request(output, calls)


if __name__ == "__main__":
    unittest.main()
