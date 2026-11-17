import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import meeting_kb_writer
from gitea_api import GiteaClient
from meeting_kb_writer import MANIFEST_FORMAT, apply_pages, validate_page_manifest
from meeting_reader import (
    DEFAULT_CONTENT_PREVIEW_CHARS,
    DEFAULT_HISTORY_DAYS,
    DEFAULT_MAX_RECORDS,
    compact_record_trace,
    expand_record_file_variants,
    expected_page_output,
    initialize_page_output,
    load_cached_prepare_context,
    max_records,
    merge_records_by_meeting_occurrence,
    safe_context_config,
    save_prepare_context_cache,
)
from tencent_meeting_bridge import unwrap_tencent_response


class FakeGiteaClient:
    files = {}

    def __init__(self, payload=None):
        self.last_commit = "fake-initial"

    def read_text(self, path):
        return self.files.get(path, "")

    def exists(self, path):
        return path in self.files

    def upsert_text(self, path, content, message):
        self.files[path] = content
        self.last_commit = "fake-" + str(len(self.files))
        return {"path": path, "commit": self.last_commit}


class ManifestWorkflowTest(unittest.TestCase):
    def setUp(self):
        FakeGiteaClient.files = {}
        self.context = {
            "inputItems": [
                {
                    "itemKey": "record-1",
                    "sourceId": 9,
                    "title": "项目同步会",
                    "meetingId": "meeting-1",
                    "meetingCode": "123456789",
                    "recordFileId": "record-file-1",
                    "meetingRecordId": "meeting-record-1",
                    "archivedPath": "source_files/tencent_meeting/9/source.md",
                    "sha256": "abc123",
                    "readable": True,
                }
            ],
            "snapshot": {"scanUntil": "2026-07-11T00:00:00Z"},
        }

    def test_manifest_keeps_markdown_out_of_json_and_applies_utf8_draft(self):
        with tempfile.TemporaryDirectory() as temp:
            draft_root = Path(temp)
            draft = draft_root / "meetings" / "2026-07-11-project-sync.md"
            draft.parent.mkdir(parents=True)
            body = (
                "# 项目同步会：JSON 与引号验证\n\n"
                "## 关键讨论\n\n"
                "他说：\"保留原样\"，并引用“中文引号”。\n\n"
                "```json\n{\"name\": \"value\"}\n```\n\n"
                "## 关联页面\n\n"
                "- 关联概念：[[concepts/devops-maturity.md|DevOps 成熟度]]\n"
                "- 关联项目：[[projects/cloud-native.md|云原生项目]]\n"
            )
            draft.write_text(body, encoding="utf-8")
            manifest = {
                "format": MANIFEST_FORMAT,
                "pages": [
                    {
                        "draftFile": "meetings/2026-07-11-project-sync.md",
                        "sourceItemKeys": ["record-1"],
                        "projectIds": "general",
                        "relatedResources": "resources/example-tool.md",
                        "sourceIds": [999],
                        "sourceStatus": "deleted",
                    }
                ],
                "snapshot": {"scanUntil": "model-controlled-value"},
                "errors": [{"message": "model-controlled-error"}],
            }

            validation = validate_page_manifest(manifest, self.context, draft_dir=draft_root)
            self.assertTrue(validation["success"])
            self.assertEqual(1, validation["meetingPageCount"])

            with patch.object(meeting_kb_writer, "GiteaClient", FakeGiteaClient):
                result = apply_pages({}, manifest, self.context, draft_dir=draft_root, require_drafts=True)

            page = FakeGiteaClient.files["meetings/2026-07-11-project-sync.md"]
            self.assertIn('他说："保留原样"', page)
            self.assertIn('{"name": "value"}', page)
            self.assertIn('relatedConcepts: ["concepts/devops-maturity.md"]', page)
            self.assertIn('relatedResources: ["resources/example-tool.md"]', page)
            self.assertIn('relatedPages: ["projects/cloud-native.md"]', page)
            self.assertIn('sourceStatus: "active"', page)
            self.assertEqual([9], json.loads(FakeGiteaClient.files["catalog.json"])["pages"][0]["sourceIds"])
            self.assertEqual(["record-1"], result["processedSources"])
            self.assertEqual("2026-07-11T00:00:00Z", result["snapshot"]["scanUntil"])
            self.assertEqual([], result["errors"])
            self.assertIn("catalog.json", FakeGiteaClient.files)
            self.assertIn("index.md", FakeGiteaClient.files)

    def test_manifest_rejects_embedded_markdown_body(self):
        manifest = {
            "format": MANIFEST_FORMAT,
            "pages": [{"draftFile": "meetings/a.md", "sourceItemKeys": ["record-1"], "content": "# bad"}],
        }
        with self.assertRaisesRegex(ValueError, "must not embed content/body"):
            validate_page_manifest(manifest, self.context, draft_dir=tempfile.gettempdir())

    def test_manifest_rejects_unknown_source_key(self):
        with tempfile.TemporaryDirectory() as temp:
            draft = Path(temp) / "meetings" / "a.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("# A", encoding="utf-8")
            manifest = {
                "format": MANIFEST_FORMAT,
                "pages": [{"draftFile": "meetings/a.md", "sourceItemKeys": ["not-a-record"]}],
            }
            with self.assertRaisesRegex(ValueError, "Unknown or ambiguous"):
                validate_page_manifest(manifest, self.context, draft_dir=temp)

    def test_manifest_rejects_absolute_and_parent_paths(self):
        for invalid in ("/meetings/a.md", "C:/temp/a.md", "../meetings/a.md"):
            manifest = {
                "format": MANIFEST_FORMAT,
                "pages": [{"draftFile": invalid, "sourceItemKeys": ["record-1"]}],
            }
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validate_page_manifest(manifest, self.context, draft_dir=tempfile.gettempdir())

    def test_manifest_rejects_duplicate_destination_path(self):
        with tempfile.TemporaryDirectory() as temp:
            draft = Path(temp) / "meetings" / "a.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("# A", encoding="utf-8")
            manifest = {
                "format": MANIFEST_FORMAT,
                "pages": [
                    {"draftFile": "meetings/a.md", "sourceItemKeys": ["record-1"]},
                    {"draftFile": "meetings/a.md", "sourceItemKeys": ["record-1"]},
                ],
            }
            with self.assertRaisesRegex(ValueError, "Duplicate page path"):
                validate_page_manifest(manifest, self.context, draft_dir=temp)

    def test_legacy_pages_json_remains_supported(self):
        legacy = {
            "pages": [
                {
                    "path": "meetings/legacy.md",
                    "title": "Legacy",
                    "sourceItemKeys": ["record-1"],
                    "content": "# Legacy\n\n旧协议兼容。",
                }
            ]
        }
        validation = validate_page_manifest(legacy, self.context, require_drafts=False)
        self.assertEqual("legacy-pages-json", validation["format"])

        legacy["pages"][0]["path"] = "/meetings/legacy.md"
        with self.assertRaisesRegex(ValueError, "KB-relative"):
            validate_page_manifest(legacy, self.context, require_drafts=False)

    def test_page_output_is_attempt_scoped_and_clears_stale_files(self):
        with tempfile.TemporaryDirectory() as temp:
            payload = {"sharedDir": temp, "taskRunId": "23", "attemptNo": "2"}
            first = initialize_page_output(payload)
            stale = Path(first["draftDir"]) / "meetings" / "stale.md"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale", encoding="utf-8")

            second = initialize_page_output(payload)

            self.assertEqual(first, second)
            self.assertFalse(stale.exists())
            self.assertTrue(Path(second["draftDir"]).is_dir())

    def test_retry_reuses_successful_prepare_context_without_platform_fetch(self):
        with tempfile.TemporaryDirectory() as temp:
            first_payload = {
                "sharedDir": temp,
                "taskId": "23",
                "taskRunId": "23-100",
                "attemptNo": 1,
                "source": {"id": 9, "type": "tencent_meeting", "config": {"windowDays": 31}, "lastSnapshot": {}},
            }
            first_context = dict(self.context)
            first_context.update({
                "mode": "ingest",
                "pageOutput": initialize_page_output(first_payload),
                "archivedFiles": ["source_files/tencent_meeting/9/source.md"],
            })
            save_prepare_context_cache(first_payload, first_context)

            retry_payload = dict(first_payload)
            retry_payload.update({"taskRunId": "23-101", "attemptNo": 2})
            reused = load_cached_prepare_context(retry_payload)

            self.assertIsNotNone(reused)
            self.assertTrue(reused["prepareCache"]["reused"])
            self.assertEqual(first_context["inputItems"], reused["inputItems"])
            self.assertNotEqual(first_context["pageOutput"]["draftDir"], reused["pageOutput"]["draftDir"])

            changed_payload = dict(retry_payload)
            changed_payload["source"] = dict(retry_payload["source"])
            changed_payload["source"]["config"] = {"windowDays": 7}
            self.assertIsNone(load_cached_prepare_context(changed_payload))

    def test_compact_record_trace_drops_large_content(self):
        raw = {
            "meeting_id": "meeting-1",
            "subject": "项目同步会",
            "content": "x" * 100000,
            "transcript": "y" * 100000,
            "records": [{"record_file_id": "file-1", "text": "z" * 100000}],
        }
        compact = compact_record_trace(raw)
        encoded = json.dumps(compact, ensure_ascii=False)
        self.assertIn("meeting-1", encoded)
        self.assertIn("file-1", encoded)
        self.assertNotIn("content", compact)
        self.assertNotIn("transcript", compact)
        self.assertLess(len(encoded), 1000)

    def test_scan_pressure_defaults_remain_bounded(self):
        self.assertEqual(14, DEFAULT_HISTORY_DAYS)
        self.assertEqual(30, DEFAULT_MAX_RECORDS)
        self.assertEqual(12000, DEFAULT_CONTENT_PREVIEW_CHARS)
        self.assertEqual(1, max_records({"maxRecords": 0}))
        self.assertEqual(500, max_records({"maxRecords": 5000}))

    def test_context_config_redacts_nested_credentials(self):
        cleaned = safe_context_config({
            "windowDays": 31,
            "TENCENT_MEETING_TOKEN": "secret-token",
            "nested": {"accessToken": "nested-token", "clientSecret": "nested-secret", "pageSize": 10},
        })
        encoded = json.dumps(cleaned)
        self.assertEqual(31, cleaned["windowDays"])
        self.assertEqual(10, cleaned["nested"]["pageSize"])
        self.assertNotIn("secret-token", encoded)
        self.assertNotIn("nested-token", encoded)
        self.assertNotIn("nested-secret", encoded)

    def test_record_variants_merge_only_within_same_occurrence(self):
        records = [
            {
                "meeting_id": "meeting-1",
                "meeting_code": "123456789",
                "subject": "项目同步会",
                "record_file_id": "file-1",
                "record_start_time": "2026-07-11T10:00:00+08:00",
                "record_end_time": "2026-07-11T10:30:00+08:00",
            },
            {
                "meeting_id": "meeting-1",
                "meeting_code": "123456789",
                "subject": "转写_项目同步会",
                "record_file_id": "file-2",
                "record_start_time": "2026-07-11T10:30:00+08:00",
                "record_end_time": "2026-07-11T10:35:00+08:00",
            },
            {
                "meeting_id": "meeting-1",
                "meeting_code": "123456789",
                "subject": "项目同步会",
                "record_file_id": "file-3",
                "record_start_time": "2026-07-11T15:00:00+08:00",
                "record_end_time": "2026-07-11T15:30:00+08:00",
            },
            {
                "meeting_id": "meeting-1",
                "meeting_code": "123456789",
                "subject": "项目同步会",
                "record_file_id": "file-4",
                "record_start_time": "2026-07-12T10:00:00+08:00",
                "record_end_time": "2026-07-12T10:30:00+08:00",
            },
        ]

        merged = merge_records_by_meeting_occurrence(records)

        self.assertEqual(3, len(merged))
        self.assertEqual(2, len(merged[0]["_mergedRecords"]))

    def test_nested_record_files_expand_then_merge_by_occurrence(self):
        records = [{
            "meeting_id": "meeting-1",
            "meeting_code": "123456789",
            "subject": "项目同步会",
            "record_files": [
                {
                    "record_file_id": "file-1",
                    "record_start_time": "2026-07-11T10:00:00+08:00",
                    "record_end_time": "2026-07-11T10:30:00+08:00",
                },
                {
                    "record_file_id": "file-2",
                    "record_start_time": "2026-07-11T10:30:00+08:00",
                    "record_end_time": "2026-07-11T10:40:00+08:00",
                },
            ],
        }]

        expanded = expand_record_file_variants(records)
        merged = merge_records_by_meeting_occurrence(expanded)

        self.assertEqual(["file-1", "file-2"], [item["record_file_id"] for item in expanded])
        self.assertEqual(1, len(merged))
        self.assertEqual(2, len(merged[0]["_mergedRecords"]))

    def test_tencent_bridge_unwraps_success_and_rejects_quota_error(self):
        success = unwrap_tencent_response({
            "status_code": 200,
            "body": json.dumps({"record_meetings": [{"meeting_id": "meeting-1"}]}),
        })
        self.assertEqual("meeting-1", success["record_meetings"][0]["meeting_id"])

        wrapped_success = unwrap_tencent_response({
            "*meta": {"hints": ["new skill version available"]},
            "data": {
                "status_code": 200,
                "body": json.dumps({"record_meetings": [{"meeting_id": "meeting-2"}]}),
            },
        })
        self.assertEqual("meeting-2", wrapped_success["record_meetings"][0]["meeting_id"])

        with self.assertRaisesRegex(RuntimeError, "500246"):
            unwrap_tencent_response({
                "status_code": 400,
                "body": json.dumps({
                    "error_info": {
                        "error_code": 500246,
                        "message": "quota exhausted",
                    }
                }),
            })

        with self.assertRaisesRegex(RuntimeError, "500246"):
            unwrap_tencent_response({
                "data": {
                    "status_code": 400,
                    "body": json.dumps({
                        "error_info": {
                            "error_code": 500246,
                            "message": "quota exhausted",
                        }
                    }),
                }
            })

    def test_cli_validates_and_applies_manifest_using_context_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result_path = root / "result.json"
            payload = {
                "sharedDir": str(root),
                "taskId": "23",
                "taskRunId": "23-100",
                "attemptNo": 1,
                "resultFile": str(result_path),
            }
            page_output = initialize_page_output(payload)
            draft = Path(page_output["draftDir"]) / "meetings" / "cli.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("# CLI 会议页\n\n## 决议\n\n保留 \"JSON-like\" 原文。", encoding="utf-8")
            manifest_path = Path(page_output["manifestPath"])
            manifest_path.write_text(
                json.dumps({
                    "format": MANIFEST_FORMAT,
                    "pages": [{"draftFile": "meetings/cli.md", "sourceItemKeys": ["record-1"]}],
                }, ensure_ascii=False),
                encoding="utf-8",
            )
            context = dict(self.context)
            context["pageOutput"] = page_output
            context_path = root / "context.json"
            context_path.write_text(json.dumps(context, ensure_ascii=False), encoding="utf-8")
            payload_path = root / "payload.json"
            payload_path.write_text(json.dumps(payload), encoding="utf-8")
            command = [sys.executable, "-B", str(SCRIPTS / "run_task.py")]
            env = dict(os.environ)
            for key in ("GITEA_URL", "GITEA_BOT_TOKEN", "GITEA_BOT_USERNAME", "GITEA_ORG"):
                env.pop(key, None)
            env["RESEARCH_KB_DRY_RUN"] = "true"

            validated = subprocess.run(
                command + ["validate-manifest", "--input", str(payload_path), "--context", str(context_path)],
                check=True,
                capture_output=True,
                env=env,
            )
            self.assertTrue(json.loads(validated.stdout.decode("utf-8"))["validationOnly"])

            applied = subprocess.run(
                command + ["apply", "--input", str(payload_path), "--context", str(context_path)],
                check=True,
                capture_output=True,
                env=env,
            )
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertTrue(result["success"])
            self.assertTrue(json.loads(applied.stdout.decode("utf-8"))["success"])
            self.assertEqual(["record-1"], result["processedSources"])
            self.assertEqual([], list(root.glob(f".{result_path.name}.*.tmp")))

    def test_cli_rejects_tampered_task_scoped_output_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = {
                "sharedDir": str(root),
                "taskId": "23",
                "taskRunId": "23-100",
                "attemptNo": 1,
            }
            expected = expected_page_output(payload)
            context = dict(self.context)
            context["pageOutput"] = {
                "protocol": expected["protocol"],
                "draftDir": str(root / "untrusted-drafts"),
                "manifestPath": str(root / "untrusted-manifest.json"),
            }
            payload_path = root / "payload.json"
            context_path = root / "context.json"
            payload_path.write_text(json.dumps(payload), encoding="utf-8")
            context_path.write_text(json.dumps(context, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPTS / "run_task.py"),
                    "validate-manifest",
                    "--input",
                    str(payload_path),
                    "--context",
                    str(context_path),
                ],
                check=False,
                capture_output=True,
            )
            self.assertNotEqual(0, completed.returncode)
            output = json.loads(completed.stdout.decode("utf-8"))
            self.assertIn("does not match the task-scoped prepare output", output["errors"][0])

    def test_gitea_client_fails_closed_without_write_configuration(self):
        keys = ("GITEA_URL", "GITEA_BOT_TOKEN", "GITEA_BOT_USERNAME", "GITEA_ORG", "TEAM_KB_REPO", "RESEARCH_KB_DRY_RUN")
        with patch.dict(os.environ, {key: "" for key in keys}, clear=False):
            with self.assertRaisesRegex(RuntimeError, "Gitea write configuration is incomplete"):
                GiteaClient({"team": {"kbRepo": ""}})

    def test_invalid_existing_catalog_fails_before_page_write(self):
        with tempfile.TemporaryDirectory() as temp:
            draft = Path(temp) / "meetings" / "a.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("# A", encoding="utf-8")
            manifest = {
                "format": MANIFEST_FORMAT,
                "pages": [{"draftFile": "meetings/a.md", "sourceItemKeys": ["record-1"]}],
            }
            FakeGiteaClient.files = {"catalog.json": "{not-json"}
            with patch.object(meeting_kb_writer, "GiteaClient", FakeGiteaClient):
                with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                    apply_pages({}, manifest, self.context, draft_dir=temp, require_drafts=True)
            self.assertNotIn("meetings/a.md", FakeGiteaClient.files)


if __name__ == "__main__":
    unittest.main()
