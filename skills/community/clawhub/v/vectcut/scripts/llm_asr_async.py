#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
from urllib.parse import urlparse
import sys
import time

import requests

BASE_URL = "https://open.vectcut.com"
SUBMIT_PATH = "/llm/asr/asr_llm/submit_task/submit_asr_llm_task"
STATUS_PATH = "/llm/asr/asr_llm/submit_task/task_status"
EXTRACT_SUBMIT_PATH = "/process/extract_audio/submit_task/submit_extract_audio_task"
EXTRACT_STATUS_PATH = "/process/extract_audio/submit_task/task_status"
VALID_EFFECT_MODES = {"basic", "nlp"}
DONE_STATUSES = {"success", "failed"}
VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".m4v",
    ".avi",
    ".mkv",
    ".webm",
    ".flv",
    ".wmv",
    ".mpeg",
    ".mpg",
}


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _ensure_token():
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    return token


def _validate_inputs(url, effect_mode):
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        raise RuntimeError("Input url must be a valid http/https link.")
    if effect_mode not in VALID_EFFECT_MODES:
        raise RuntimeError("effect_mode must be one of: basic|nlp")


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _looks_like_video_url(url):
    try:
        path = urlparse(url).path.lower()
    except Exception:
        return False
    return any(path.endswith(ext) for ext in VIDEO_EXTENSIONS)


def _normalize_extracted_audio_url(url):
    if not isinstance(url, str):
        return ""
    fixed = url.strip()
    if fixed.startswith("http://http://"):
        return "http://" + fixed[len("http://http://") :]
    if fixed.startswith("https://https://"):
        return "https://" + fixed[len("https://https://") :]
    return fixed


def submit_extract_audio_task(token, video_url):
    resp = requests.post(
        f"{BASE_URL}{EXTRACT_SUBMIT_PATH}",
        headers=_auth_headers(token),
        json={"video_url": video_url},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"extract-audio submit response missing task_id: {body}")
    return body


def query_extract_audio_task_status(token, task_id):
    resp = requests.get(
        f"{BASE_URL}{EXTRACT_STATUS_PATH}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def wait_extract_audio_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_extract_audio_task_status(token, task_id)
        status = status_body.get("status")
        if status in DONE_STATUSES:
            return status_body
        elapsed = time.monotonic() - started
        if elapsed >= timeout:
            raise RuntimeError(
                f"Extract-audio polling timeout after {timeout}s. "
                f"Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def maybe_extract_audio_before_asr(token, url, poll_interval, timeout, auto_extract_audio):
    if not auto_extract_audio or not _looks_like_video_url(url):
        return {
            "asr_input_url": url,
            "extract_audio_used": False,
            "extract_audio_task_id": "",
            "extract_audio_status": "",
        }

    submit_body = submit_extract_audio_task(token, url)
    status_body = wait_extract_audio_done(
        token, submit_body["task_id"], poll_interval=poll_interval, timeout=timeout
    )
    if status_body.get("status") != "success":
        raise RuntimeError(f"Extract-audio task failed: {status_body}")

    result = status_body.get("result") or {}
    public_url = _normalize_extracted_audio_url(result.get("public_url", ""))
    if not public_url:
        raise RuntimeError(f"Extract-audio success but missing public_url: {status_body}")

    return {
        "asr_input_url": public_url,
        "extract_audio_used": True,
        "extract_audio_task_id": submit_body.get("task_id", ""),
        "extract_audio_status": status_body.get("status", ""),
    }


def submit_task(token, url, effect_mode, content=None):
    payload = {
        "url": url,
        "effect_mode": effect_mode,
    }
    if content:
        payload["content"] = content

    resp = requests.post(
        f"{BASE_URL}{SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)

    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))

    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"submit response missing task_id: {body}")

    return body


def query_task_status(token, task_id):
    headers = _auth_headers(token)

    # Prefer GET (per task_status doc); fallback to POST for compatibility.
    get_resp = requests.get(
        f"{BASE_URL}{STATUS_PATH}",
        headers=headers,
        params={"task_id": task_id},
        timeout=60,
    )
    get_body = _parse_json_response(get_resp)
    if get_resp.status_code == 200 and "status" in get_body:
        return get_body

    post_resp = requests.post(
        f"{BASE_URL}{STATUS_PATH}",
        headers=headers,
        json={"task_id": task_id},
        timeout=60,
    )
    post_body = _parse_json_response(post_resp)
    if post_resp.status_code != 200:
        raise RuntimeError(post_body.get("error") or str(post_body))
    return post_body


def wait_until_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()

    while True:
        status_body = query_task_status(token, task_id)
        status = status_body.get("status")

        if status in DONE_STATUSES:
            return status_body

        elapsed = time.monotonic() - started
        if elapsed >= timeout:
            raise RuntimeError(
                f"Polling timeout after {timeout}s. Last status={status!r}, body={status_body}"
            )

        time.sleep(poll_interval)


def to_editable_json(source_url, asr_input_url, submit_body, status_body, preproc_meta=None):
    result = status_body.get("result") or {}
    segments = result.get("segments") or []

    editable_subtitles = []
    for idx, segment in enumerate(segments, start=1):
        editable_subtitles.append(
            {
                "id": idx,
                "start_ms": segment.get("start"),
                "end_ms": segment.get("end"),
                "text": segment.get("text", ""),
            }
        )

    return {
        "meta": {
            "source_url": source_url,
            "asr_input_url": asr_input_url,
            "task_id": submit_body.get("task_id"),
            "message_id": submit_body.get("message_id"),
            "status": status_body.get("status"),
            "mode": result.get("mode"),
            "effect_mode": submit_body.get("effect_mode") or result.get("effect_mode"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "preprocessing": preproc_meta or {},
        },
        "full_text": result.get("content", ""),
        "editable_subtitles": editable_subtitles,
        "raw_result": result,
    }


def run(
    url,
    effect_mode="nlp",
    content=None,
    poll_interval=2.0,
    timeout=600,
    auto_extract_audio=True,
):
    token = _ensure_token()
    _validate_inputs(url, effect_mode)
    preproc = maybe_extract_audio_before_asr(
        token,
        url,
        poll_interval=poll_interval,
        timeout=timeout,
        auto_extract_audio=auto_extract_audio,
    )
    asr_input_url = preproc["asr_input_url"]
    submit_body = submit_task(token, asr_input_url, effect_mode, content=content)
    status_body = wait_until_done(
        token, submit_body["task_id"], poll_interval=poll_interval, timeout=timeout
    )

    if status_body.get("status") != "success":
        error = (
            (status_body.get("result") or {}).get("error")
            or status_body.get("error")
            or str(status_body)
        )
        raise RuntimeError(f"ASR task failed: {error}")

    return to_editable_json(
        source_url=url,
        asr_input_url=asr_input_url,
        submit_body=submit_body,
        status_body=status_body,
        preproc_meta=preproc,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument(
        "--effect-mode",
        default="nlp",
        choices=sorted(VALID_EFFECT_MODES),
        help="One of basic|nlp",
    )
    parser.add_argument("--content", default=None)
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument(
        "--auto-extract-audio",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="If input looks like video url, try extract-audio first.",
    )
    parser.add_argument("--output", default="subtitle_editable.json")
    args = parser.parse_args()

    try:
        result = run(
            url=args.url,
            effect_mode=args.effect_mode,
            content=args.content,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
            auto_extract_audio=args.auto_extract_audio,
        )
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(
            (
                f"已落盘到 {args.output}。你可以修改 editable_subtitles[].text "
                "（如改错别字/润色）。如果这是口播素材，是否需要继续去气口？"
                "可直接调用 asr-vad 技能：先标记 keep/drop，再重建新字幕与 add_video 分段工作流。"
            ),
            file=sys.stderr,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
