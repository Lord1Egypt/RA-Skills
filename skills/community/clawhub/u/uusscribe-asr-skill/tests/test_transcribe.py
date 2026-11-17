from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from typing import Any

SCRIPT = Path(__file__).parents[1] / "scripts" / "transcribe.py"
SPEC = importlib.util.spec_from_file_location("uusscribe_asr_transcribe", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RecordingClient(MODULE.UUScribeClient):
    def __init__(self) -> None:
        super().__init__("https://example.test", "secret")
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []
        self.parts: list[bytes] = []

    def request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        retry_transient: bool = False,
    ) -> dict[str, Any]:
        self.calls.append((method, path, payload))
        if path == "/api/uploads/sign":
            return {
                "path": "2026-09-06/1/audio.mp3",
                "upload_id": "upload-1",
                "part_size": 5,
                "part_count": 3,
            }
        if path == "/api/uploads/sign-part":
            assert payload
            return {"url": f"https://upload.test/{payload['part_number']}", "headers": {}}
        if path == "/api/uploads/complete":
            return {"task": {"id": 42}}
        if path == "/api/uploads/abort":
            return {"message": "aborted"}
        if path == "/api/tasks":
            return {"id": 43}
        if path == "/api/user":
            return {"balance": {"remaining_seconds": 3600}}
        raise AssertionError(f"Unexpected request: {method} {path}")

    def put_part(self, url: str, headers: dict[str, str], data: bytes) -> None:
        self.parts.append(data)


class PollingClient(MODULE.UUScribeClient):
    def __init__(self, responses: list[dict[str, Any] | Exception]) -> None:
        super().__init__("https://example.test", "secret")
        self.responses = iter(responses)

    def request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        retry_transient: bool = False,
    ) -> dict[str, Any]:
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


class UUScribeAsrTests(unittest.TestCase):
    def test_accepts_single_youtube_video_urls(self) -> None:
        accepted = [
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/shorts/dQw4w9WgXcQ",
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ",
        ]
        for url in accepted:
            with self.subTest(url=url):
                self.assertTrue(MODULE.youtube_video_url(url))

    def test_rejects_non_youtube_and_playlist_urls(self) -> None:
        rejected = [
            "https://youtube.com.evil.example/watch?v=abc",
            "https://fake.youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/playlist?list=abc",
            "https://www.youtube.com/watch?v=abc&list=PL123",
            "https://youtu.be/abc?list=PL123",
            "https://www.youtube.com/@channel",
            "https://example.com/audio.mp3",
        ]
        for url in rejected:
            with self.subTest(url=url):
                self.assertFalse(MODULE.youtube_video_url(url))

    def test_youtube_task_uses_existing_api_contract(self) -> None:
        client = RecordingClient()
        task_id = client.create_youtube_task(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Demo"
        )
        self.assertEqual(task_id, 43)
        self.assertEqual(
            client.calls,
            [
                (
                    "POST",
                    "/api/tasks",
                    {
                        "disk": "youtube",
                        "name": "Demo",
                        "path": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "file": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    },
                )
            ],
        )

    def test_audio_upload_splits_parts_and_completes_task(self) -> None:
        client = RecordingClient()
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "meeting.mp3"
            audio.write_bytes(b"hello world")
            task_id = client.upload_audio(audio, "Meeting", 12)

        self.assertEqual(task_id, 42)
        self.assertEqual(client.parts, [b"hello", b" worl", b"d"])
        complete = next(call for call in client.calls if call[1] == "/api/uploads/complete")
        assert complete[2]
        self.assertEqual(complete[2]["duration"], 12)
        self.assertEqual(complete[2]["content_type"], "audio/mpeg")

    def test_audio_upload_aborts_after_part_failure(self) -> None:
        client = RecordingClient()

        def fail_part(url: str, headers: dict[str, str], data: bytes) -> None:
            raise MODULE.UUScribeError("upload failed")

        client.put_part = fail_part
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "meeting.mp3"
            audio.write_bytes(b"hello world")
            with self.assertRaisesRegex(MODULE.UUScribeError, "upload failed"):
                client.upload_audio(audio, "Meeting", 12)

        self.assertTrue(any(path == "/api/uploads/abort" for _, path, _ in client.calls))

    def test_completion_disconnect_does_not_abort_uncertain_task(self) -> None:
        client = RecordingClient()
        original_request = client.request_json

        def fail_completion(
            method: str,
            path: str,
            payload: dict[str, Any] | None = None,
            retry_transient: bool = False,
        ) -> dict[str, Any]:
            if path == "/api/uploads/complete":
                client.calls.append((method, path, payload))
                raise MODULE.UUScribeError("response lost")
            return original_request(method, path, payload, retry_transient)

        client.request_json = fail_completion
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "meeting.mp3"
            audio.write_bytes(b"hello world")
            with self.assertRaisesRegex(MODULE.UUScribeError, "response lost"):
                client.upload_audio(audio, "Meeting", 12)

        self.assertFalse(any(path == "/api/uploads/abort" for _, path, _ in client.calls))

    def test_transcript_keeps_nonempty_segment_text(self) -> None:
        transcript = MODULE.transcript_from_segments(
            [{"text": "Hello"}, {"text": ""}, {"other": "ignored"}, {"text": "World"}]
        )
        self.assertEqual(transcript, "Hello\nWorld")

    def test_result_reports_timestamp_unit_and_speaker_coverage(self) -> None:
        result = MODULE.result_payload(
            {
                "status": "finished",
                "segments": [
                    {"start": 0, "end": 1000, "speaker": "Host", "text": "Hi"},
                    {"start": 1000, "end": 2000, "speaker": None, "text": "There"},
                ],
            },
            9,
            "https://example.test",
        )
        self.assertEqual(result["timestamps_unit"], "milliseconds")
        self.assertTrue(result["speaker_labels_present"])
        self.assertEqual(result["speaker_labeled_segments"], 1)
        self.assertEqual(result["text_segments"], 2)

    def test_rejects_non_local_plain_http_api_base(self) -> None:
        with self.assertRaisesRegex(MODULE.UUScribeError, "must use HTTPS"):
            MODULE.UUScribeClient("http://example.test", "secret")

        client = MODULE.UUScribeClient("http://127.0.0.1:8000", "secret")
        self.assertEqual(client.api_base, "http://127.0.0.1:8000")

    def test_api_request_pacing_stays_below_server_limit(self) -> None:
        now = [0.0]

        def sleep(seconds: float) -> None:
            now[0] += seconds

        client = MODULE.UUScribeClient(
            "https://example.test", "secret", sleep=sleep, clock=lambda: now[0]
        )
        client.pace_api_request()
        client.pace_api_request()
        self.assertGreaterEqual(now[0], 60 / MODULE.API_REQUESTS_PER_MINUTE)

    def test_polling_reaches_finished_after_transient_error(self) -> None:
        client = PollingClient(
            [
                MODULE.ApiError(429, "slow down"),
                {"status": "scribing"},
                {"status": "finished", "segments": [{"text": "Done"}]},
            ]
        )
        now = [0.0]

        def sleep(seconds: float) -> None:
            now[0] += seconds

        task = client.wait_for_task(9, 60, 1, sleep=sleep, clock=lambda: now[0])
        self.assertEqual(task["status"], "finished")

    def test_polling_reports_failed_task(self) -> None:
        client = PollingClient([{"status": "failed"}])
        with self.assertRaisesRegex(MODULE.UUScribeError, "task 9 failed"):
            client.wait_for_task(9, 60, 0)

    def test_polling_reports_insufficient_balance_for_pending_task(self) -> None:
        client = PollingClient(
            [
                {"status": "pending", "duration": 120},
                {"balance": {"remaining_seconds": 30}},
            ]
        )
        with self.assertRaisesRegex(MODULE.UUScribeError, "needs 120.*has 30"):
            client.wait_for_task(9, 60, 1)

    def test_polling_rechecks_balance_while_task_stays_pending(self) -> None:
        client = PollingClient(
            [
                {"status": "pending", "duration": 120},
                {"balance": {"remaining_seconds": 200}},
                {"status": "pending", "duration": 120},
                {"status": "pending", "duration": 120},
                {"balance": {"remaining_seconds": 30}},
            ]
        )
        now = [0.0]

        def sleep(seconds: float) -> None:
            now[0] += seconds

        with self.assertRaisesRegex(MODULE.UUScribeError, "needs 120.*has 30"):
            client.wait_for_task(9, 120, 30, sleep=sleep, clock=lambda: now[0])

    def test_balance_shape_must_match_api_contract(self) -> None:
        client = PollingClient([{"balance": {}}])
        with self.assertRaisesRegex(MODULE.UUScribeError, "invalid balance"):
            client.ensure_balance(60)

    def test_submit_receipt_can_be_used_to_resume(self) -> None:
        receipt = MODULE.receipt_payload(42, "https://example.test/")
        self.assertEqual(receipt["task_id"], 42)
        self.assertEqual(receipt["status"], "submitted")
        self.assertEqual(receipt["task_url"], "https://example.test/tasks/42")


if __name__ == "__main__":
    unittest.main()
