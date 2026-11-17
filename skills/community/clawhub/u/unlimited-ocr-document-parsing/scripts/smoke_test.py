"""Offline smoke tests using httpx MockTransport."""

# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "httpx>=0.27,<1",
#   "pymupdf>=1.24,<2",
#   "pillow>=10,<13",
# ]
# ///

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import httpx
from PIL import Image

from client import SkillError, error_envelope, parse_baidu, parse_local


def test_baidu() -> None:
    os.environ.update({
        "UNLIMITED_OCR_API_KEY": "test-key",
        "UNLIMITED_OCR_SECRET_KEY": "test-secret",
        "UNLIMITED_OCR_OAUTH_URL": "http://127.0.0.1/oauth",
        "UNLIMITED_OCR_SUBMIT_URL": "http://127.0.0.1/task",
        "UNLIMITED_OCR_QUERY_URL": "http://127.0.0.1/query",
    })
    queries = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal queries
        if request.url.path == "/oauth":
            return httpx.Response(200, json={"access_token": "token"})
        if request.url.path == "/task":
            assert "access_token=token" in str(request.url)
            return httpx.Response(200, json={"error_code": 0, "result": {"task_id": "task-1"}})
        if request.url.path == "/query":
            queries += 1
            status = "running" if queries == 1 else "success"
            result = {"task_id": "task-1", "status": status}
            if status == "success":
                result.update({"markdown_url": "http://127.0.0.1/result.md", "parse_result_url": "http://127.0.0.1/result.json"})
            return httpx.Response(200, json={"error_code": 0, "result": result})
        if request.url.path == "/result.md":
            return httpx.Response(200, content="# Parsed\n\nComplete text")
        if request.url.path == "/result.json":
            return httpx.Response(200, json={"pages": 1})
        return httpx.Response(404)

    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "sample.pdf"
        source.write_bytes(b"%PDF smoke")
        result = parse_baidu(file_path=str(source), file_url=None, timeout_seconds=30, poll_interval_seconds=0.01, transport=httpx.MockTransport(handler), sleep=lambda _: None)
    assert result["ok"] is True
    assert result["text"].startswith("# Parsed")
    assert result["result"]["parse_result"] == {"pages": 1}


def test_local() -> None:
    os.environ.update({
        "UNLIMITED_OCR_LOCAL_BASE_URL": "http://127.0.0.1:10000",
        "UNLIMITED_OCR_LOCAL_BACKEND": "sglang",
    })

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        assert payload["model"] == "Unlimited-OCR"
        assert payload["images_config"]["image_mode"] == "gundam"
        body = (
            'data: {"choices":[{"delta":{"content":"Hello "}}]}\n\n'
            'data: {"choices":[{"delta":{"content":"OCR"}}]}\n\n'
            "data: [DONE]\n\n"
        )
        return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=body)

    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "sample.png"
        Image.new("RGB", (8, 8), "white").save(source)
        result = parse_local(file_path=str(source), file_url=None, timeout_seconds=30, transport=httpx.MockTransport(handler))
    assert result["ok"] is True
    assert result["text"] == "Hello OCR"
    assert result["result"]["image_count"] == 1


def test_sanitized_error() -> None:
    value = error_envelope("baidu", SkillError("INPUT_ERROR", "bad input"))
    assert value["ok"] is False
    assert value["error"] == {"code": "INPUT_ERROR", "message": "bad input"}


if __name__ == "__main__":
    test_baidu()
    test_local()
    test_sanitized_error()
    print("Unlimited-OCR smoke tests passed")

