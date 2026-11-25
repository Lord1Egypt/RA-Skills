#!/usr/bin/env python3
"""Unit and mock-server integration tests for storyboard_runner.py (zero credits spent)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import storyboard_runner as sr  # noqa: E402

SAMPLE_PATH = SCRIPT_DIR.parent / "examples" / "sample-storyboard.json"

PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc``\x00\x00"
    b"\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82"
)
FAKE_MP4 = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"


class MockHotAPIState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.posts: list[dict[str, Any]] = []
        self.uploads: list[dict[str, Any]] = []
        self.tasks: dict[str, dict[str, Any]] = {}
        self.idempotency_map: dict[tuple[str, str], str] = {}
        self.counter = 0
        self.base_url = ""

    def next_task_id(self) -> str:
        self.counter += 1
        return f"task_mock_{self.counter}"


class MockHotAPIHandler(BaseHTTPRequestHandler):
    server_version = "MockHotAPI/1.0"

    @property
    def state(self) -> MockHotAPIState:
        return self.server.mock_state  # type: ignore[attr-defined]

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _send_json(self, code: int, body: Any) -> None:
        raw = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _check_auth(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if auth != "Bearer hk_test_mock_key":
            self._send_json(401, {"error": {"type": "auth_error", "code": "unauthorized", "message": "Missing bearer token"}})
            return False
        return True

    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/cdn/"):
            is_png = self.path.endswith(".png")
            data = PNG_1X1 if is_png else FAKE_MP4
            ctype = "image/png" if is_png else "video/mp4"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if not self._check_auth():
            return

        if self.path.startswith("/v1/tasks/"):
            task_id = self.path.split("/v1/tasks/", 1)[1].split("?", 1)[0]
            with self.state.lock:
                task = self.state.tasks.get(task_id)
                if not task:
                    self._send_json(404, {"error": {"type": "not_found", "code": "task_not_found", "message": "Not found"}})
                    return
                task["polls"] += 1
                if task["polls"] >= 1:
                    task["record"]["status"] = "succeeded"
                resp = dict(task["record"])
            self._send_json(200, resp)
            return

        self._send_json(404, {"error": {"type": "not_found", "code": "not_found", "message": self.path}})

    def do_POST(self) -> None:  # noqa: N802
        if not self._check_auth():
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)

        if self.path == "/v1/uploads":
            text_body = raw_body.decode("latin1")
            with self.state.lock:
                idx = len(self.state.uploads) + 1
                url = f"{self.state.base_url}/cdn/upload_{idx}.png"
                self.state.uploads.append({"path": self.path, "has_file_field": 'name="file"' in text_body, "size": len(raw_body)})
            self._send_json(
                200,
                {
                    "url": url,
                    "expires_at": int(time.time()) + 3600,
                    "content_type": "image/png",
                    "size": len(raw_body),
                },
            )
            return

        payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        idem_key = self.headers.get("Idempotency-Key", "")

        with self.state.lock:
            self.state.posts.append({"path": self.path, "idempotency_key": idem_key, "payload": payload})
            if idem_key and (self.path, idem_key) in self.state.idempotency_map:
                existing_id = self.state.idempotency_map[(self.path, idem_key)]
                self._send_json(202, dict(self.state.tasks[existing_id]["record"]))
                return

            tid = self.state.next_task_id()
            is_image = "seedream" in self.path
            ext = ".png" if is_image else (".mov" if payload.get("output_format") == "mov" else ".mp4")
            credits = 120 if is_image else (1030 if payload.get("draft") else 5685)
            record = {
                "id": tid,
                "object": "task",
                "status": "queued",
                "model": self.path.strip("/").split("/")[1],
                "task_kind": "image.generate" if is_image else "video.generate",
                "input": payload,
                "output": {"assets": [{"type": "image" if is_image else "video", "url": f"{self.state.base_url}/cdn/{tid}{ext}"}]},
                "estimated_credits_cost": credits,
                "actual_credits_cost": credits,
                "created_at": int(time.time()),
                "expires_at": int(time.time()) + 86400,
            }
            self.state.tasks[tid] = {"record": record, "polls": 0}
            if idem_key:
                self.state.idempotency_map[(self.path, idem_key)] = tid

        self._send_json(202, record)


class StoryboardRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_state = MockHotAPIState()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MockHotAPIHandler)
        self.server.mock_state = self.mock_state  # type: ignore[attr-defined]
        port = self.server.server_address[1]
        self.mock_state.base_url = f"http://127.0.0.1:{port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

        self.prev_key = os.environ.get("HOTAPI_KEY")
        self.prev_base = os.environ.get("HOTAPI_BASE_URL")
        os.environ["HOTAPI_KEY"] = "hk_test_mock_key"
        os.environ["HOTAPI_BASE_URL"] = self.mock_state.base_url

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        if self.prev_key is None:
            os.environ.pop("HOTAPI_KEY", None)
        else:
            os.environ["HOTAPI_KEY"] = self.prev_key
        if self.prev_base is None:
            os.environ.pop("HOTAPI_BASE_URL", None)
        else:
            os.environ["HOTAPI_BASE_URL"] = self.prev_base

    def test_validate_valid_sample(self) -> None:
        data = sr.load_json(SAMPLE_PATH)
        report = sr.validate_storyboard(data)
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["warnings"], [])
        self.assertEqual(report["estimate"]["generated_assets"], 3)
        self.assertEqual(report["estimate"]["total_duration_seconds"], 10)
        self.assertEqual(report["estimate"]["asset_credits"], 360)

    def test_validate_catches_duplicate_id_dangling_ref_and_image_cap(self) -> None:
        too_many_assets = [{"id": f"A{i}", "type": "prop", "prompt": f"prop {i}"} for i in range(11)]
        bad_doc = {
            "project": {
                "title": "Bad",
                "video_model": "seedance-2.0-spicy",
                "image_model": "seedream-5.0-pro-spicy",
                "video_aspect": "16:9",
                "asset_aspect": "16:9",
            },
            "assets": too_many_assets + [{"id": "A0", "type": "prop", "prompt": "dup"}],
            "segments": [
                {
                    "id": "SEG_BAD",
                    "duration_seconds": 5,
                    "asset_refs": [f"A{i}" for i in range(11)] + ["MISSING_ASSET"],
                    "prompt": "test",
                }
            ],
        }
        report = sr.validate_storyboard(bad_doc)
        codes = {e["code"] for e in report["errors"]}
        self.assertFalse(report["valid"])
        self.assertIn("DUPLICATE_ID", codes)
        self.assertIn("DANGLING_REF", codes)
        self.assertIn("REF_IMAGE_CAP", codes)

    def test_import_bundle_roundtrip_passes_validate(self) -> None:
        bundle = {
            "project": {
                "model": "Seedance 2.5",
                "video_aspect": "9:16",
                "asset_aspect": "16:9",
                "total_duration": 5,
            },
            "characters": [
                {"id": "CHR_LIN", "visual_age": 24, "description": "courier in black windbreaker"}
            ],
            "assets": [
                {
                    "id": "AST_LIN",
                    "type": "character",
                    "aspect": "16:9",
                    "prompt": "Three-view character turnaround",
                    "refs": ["CHR_LIN"],
                }
            ],
            "segments": [
                {
                    "id": "SEG_1",
                    "duration": 5,
                    "entry_state": "standing under bridge",
                    "exit_state": "running east",
                    "shots": [
                        {
                            "id": "SH_1",
                            "start": 0,
                            "end": 5,
                            "action": "CHR_LIN checks watch and sprints down stairs",
                            "camera": "tracking medium shot",
                            "dialogues": [{"character_id": "CHR_LIN", "text": "Go now."}],
                            "asset_refs": ["AST_LIN"],
                        }
                    ],
                }
            ],
        }
        sb = sr.import_project_bundle(bundle)
        report = sr.validate_storyboard(sb)
        self.assertTrue(report["valid"], report)
        self.assertEqual(sb["project"]["video_model"], "seedance-2.5-spicy")
        self.assertEqual(sb["project"]["video_aspect"], "9:16")
        self.assertIn("courier in black windbreaker", sb["assets"][0]["prompt"])
        self.assertEqual(sb["segments"][0]["asset_refs"], ["AST_LIN"])

    def test_full_pipeline_assets_render_draft_finalize_board_and_idempotency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "out"
            rc = sr.main(["assets", str(SAMPLE_PATH), "--out-dir", str(out_dir), "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.posts), 3)

            # Rerun assets without --force: must skip all 3 without additional POST calls
            rc = sr.main(["assets", str(SAMPLE_PATH), "--out-dir", str(out_dir), "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.posts), 3)

            # Render 480p drafts
            rc = sr.main(["render", str(SAMPLE_PATH), "--out-dir", str(out_dir), "--draft", "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.posts), 5)

            draft_posts = [p for p in self.mock_state.posts if "/reference-to-video" in p["path"]]
            self.assertEqual(len(draft_posts), 2)
            for post in draft_posts:
                self.assertEqual(post["payload"]["resolution"], "480p")
                self.assertTrue(post["payload"]["draft"])
                self.assertTrue(post["idempotency_key"].startswith("render-draft-"))
                self.assertGreaterEqual(len(post["payload"]["reference_image_urls"]), 2)

            # Finalize drafts to 1080p
            rc = sr.main(["finalize", str(SAMPLE_PATH), "--out-dir", str(out_dir), "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.posts), 7)

            fin_posts = [p for p in self.mock_state.posts if p["path"] == "/v1/seedance-2.5-spicy/draft-to-video"]
            self.assertEqual(len(fin_posts), 2)

            # Rerun finalize without --force: skips cleanly
            rc = sr.main(["finalize", str(SAMPLE_PATH), "--out-dir", str(out_dir), "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.posts), 7)

            # Build offline board
            rc = sr.main(["board", str(SAMPLE_PATH), "--out-dir", str(out_dir)])
            self.assertEqual(rc, 0)

            state = sr.load_state(out_dir)
            self.assertTrue((out_dir / "assets" / "AST_CHR_REN.png").is_file())
            self.assertTrue((out_dir / "segments" / "SEG_01.draft.mp4").is_file())
            self.assertTrue((out_dir / "finals" / "SEG_01.mp4").is_file())
            self.assertEqual(state["segments"]["SEG_02"]["final"]["status"], "succeeded")

            board_html = (out_dir / "board.html").read_text(encoding="utf-8")
            self.assertIn("Neon Ledger", board_html)
            self.assertIn("./assets/AST_CHR_REN.png", board_html)
            self.assertIn("./segments/SEG_01.draft.mp4", board_html)
            self.assertIn("./finals/SEG_01.mp4", board_html)
            self.assertIn("Credits Spent:", board_html)

    def test_upload_local_asset_multipart_and_expiry_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            local_img = tmp_dir / "hero.png"
            local_img.write_bytes(PNG_1X1)
            sb_path = tmp_dir / "sb.json"
            out_dir = tmp_dir / "out"
            sb = {
                "project": {
                    "title": "Local Ref Test",
                    "video_model": "seedance-2.5-flash-spicy",
                    "image_model": "seedream-5.0-lite-spicy",
                    "video_aspect": "16:9",
                    "asset_aspect": "16:9",
                },
                "assets": [
                    {"id": "HERO", "type": "character", "local_file": "hero.png"}
                ],
                "segments": [
                    {"id": "S1", "duration_seconds": 4, "asset_refs": ["HERO"], "prompt": "Hero enters room."}
                ],
            }
            sr.write_json_atomic(sb_path, sb)

            rc = sr.main(["assets", str(sb_path), "--out-dir", str(out_dir), "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.uploads), 1)
            self.assertTrue(self.mock_state.uploads[0]["has_file_field"])

            # Force expiry in state.json to verify render automatically re-uploads local file
            state = sr.load_state(out_dir)
            state["assets"]["HERO"]["upload_expires_at"] = int(time.time()) + 10
            sr.save_state(out_dir, state)

            rc = sr.main(["render", str(sb_path), "--out-dir", str(out_dir), "--resolution", "720p", "--poll-interval", "0.01"])
            self.assertEqual(rc, 0)
            self.assertEqual(len(self.mock_state.uploads), 2)
            r2v_posts = [p for p in self.mock_state.posts if p["path"] == "/v1/seedance-2.5-flash-spicy/reference-to-video"]
            self.assertEqual(len(r2v_posts), 1)
            self.assertEqual(r2v_posts[0]["payload"]["reference_image_urls"][0], f"{self.mock_state.base_url}/cdn/upload_2.png")


if __name__ == "__main__":
    unittest.main()
