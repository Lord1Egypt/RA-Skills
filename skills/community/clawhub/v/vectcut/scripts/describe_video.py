#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys
import time
from urllib.parse import urlparse

import requests

BASE_URL = "https://open.vectcut.com"
ASR_SUBMIT_PATH = "/llm/asr/asr_llm/submit_task/submit_asr_llm_task"
ASR_STATUS_PATH = "/llm/asr/asr_llm/submit_task/task_status"
EXTRACT_SUBMIT_PATH = "/process/extract_audio/submit_task/submit_extract_audio_task"
EXTRACT_STATUS_PATH = "/process/extract_audio/submit_task/task_status"
GET_DURATION_PATH = "/cut_jianying/get_duration"
SPLIT_SUBMIT_PATH = "/process/split_video/submit_task/submit_split_video_task"
SPLIT_STATUS_PATH = "/process/split_video/submit_task/task_status"
VIDEO_DETAIL_PATH = "/llm/video_detail"
DONE_STATUSES = {"success", "failed"}
SPLIT_DONE_STATUSES = {"success", "failed", "not_found", "succeeded"}
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


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _extract_video_detail_and_think_from_obj(obj):
    if not isinstance(obj, dict):
        return {"video_detail": "", "think": ""}
    output = obj.get("output") or {}
    text = output.get("video_detail") or ""
    think = output.get("think") or output.get("reasoning") or ""

    if text or think:
        return {"video_detail": str(text), "think": str(think)}

    # Compatible with chat.completion.chunk style stream:
    # {"choices":[{"delta":{"content":"..."}}]}
    content_pieces = []
    think_pieces = []
    for choice in obj.get("choices") or []:
        delta = (choice or {}).get("delta") or {}
        content = delta.get("content")
        if content:
            content_pieces.append(str(content))
        reasoning = (
            delta.get("reasoning_content")
            or delta.get("reasoning")
            or delta.get("think")
            or ""
        )
        if reasoning:
            think_pieces.append(str(reasoning))
    if content_pieces or think_pieces:
        return {
            "video_detail": "".join(content_pieces),
            "think": "".join(think_pieces),
        }

    # Compatible with some non-stream completion schemas.
    message = obj.get("message") or {}
    msg_content = message.get("content")
    msg_think = message.get("reasoning_content") or message.get("think") or ""
    if msg_content or msg_think:
        return {
            "video_detail": str(msg_content or ""),
            "think": str(msg_think or ""),
        }
    return {"video_detail": "", "think": ""}


def _merge_stream_piece(assembled, piece):
    if not piece:
        return assembled
    # cumulative mode: new piece is full text prefix growth
    if piece.startswith(assembled):
        return piece
    # delta mode: new piece is incremental chunk
    return assembled + piece


def _parse_video_detail_stream_text(text):
    lines = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("data:"):
            line = line[len("data:") :].strip()
        if not line or line == "[DONE]":
            continue
        lines.append(line)

    if not lines:
        raise RuntimeError("Empty streaming response for /llm/video_detail")

    last_obj = None
    assembled_detail = ""
    assembled_think = ""
    for line in lines:
        try:
            obj = json.loads(line)
            last_obj = obj
            extracted = _extract_video_detail_and_think_from_obj(obj)
            assembled_detail = _merge_stream_piece(
                assembled_detail, extracted.get("video_detail", "")
            )
            assembled_think = _merge_stream_piece(
                assembled_think, extracted.get("think", "")
            )
            continue
        except Exception:
            assembled_detail = _merge_stream_piece(assembled_detail, line)

    if last_obj is not None:
        merged = dict(last_obj)
        merged_output = merged.get("output") or {}
        if assembled_detail and not merged_output.get("video_detail"):
            merged["output"] = dict(merged_output)
            merged["output"]["video_detail"] = assembled_detail.strip()
        if assembled_think and not merged_output.get("think"):
            merged.setdefault("output", dict(merged_output))
            merged["output"]["think"] = assembled_think.strip()
        merged.setdefault("success", True)
        merged.setdefault("error", "")
        return merged

    return {
        "success": True,
        "error": "",
        "output": {"video_detail": assembled_detail.strip()},
    }


def _parse_video_detail_stream_lines(lines):
    cleaned = []
    for raw_line in lines:
        line = (raw_line or "").strip()
        if not line:
            continue
        if line.startswith("data:"):
            line = line[len("data:") :].strip()
        if not line or line == "[DONE]":
            continue
        cleaned.append(line)

    if not cleaned:
        raise RuntimeError("Empty streaming response for /llm/video_detail")

    last_obj = None
    assembled_detail = ""
    assembled_think = ""
    for line in cleaned:
        try:
            obj = json.loads(line)
            last_obj = obj
            extracted = _extract_video_detail_and_think_from_obj(obj)
            assembled_detail = _merge_stream_piece(
                assembled_detail, extracted.get("video_detail", "")
            )
            assembled_think = _merge_stream_piece(
                assembled_think, extracted.get("think", "")
            )
            continue
        except Exception:
            assembled_detail = _merge_stream_piece(assembled_detail, line)

    if last_obj is not None:
        merged = dict(last_obj)
        merged_output = merged.get("output") or {}
        if assembled_detail and not merged_output.get("video_detail"):
            merged["output"] = dict(merged_output)
            merged["output"]["video_detail"] = assembled_detail.strip()
        if assembled_think and not merged_output.get("think"):
            merged.setdefault("output", dict(merged_output))
            merged["output"]["think"] = assembled_think.strip()
        merged.setdefault("success", True)
        merged.setdefault("error", "")
        return merged

    return {
        "success": True,
        "error": "",
        "output": {"video_detail": assembled_detail.strip()},
    }


def _validate_url(url):
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        raise RuntimeError(f"Invalid url: {url!r}")


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


def _ms_to_ts(ms):
    if ms is None:
        return ""
    try:
        total_ms = int(float(ms))
    except Exception:
        return ""
    if total_ms < 0:
        total_ms = 0
    total_seconds = total_ms // 1000
    msec = total_ms % 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{msec:03d}"


def _seconds_to_ts(seconds):
    try:
        return _ms_to_ts(int(float(seconds) * 1000))
    except Exception:
        return ""


def _looks_like_filler_heavy(text):
    if not text:
        return False
    markers = ["嗯", "啊", "呃", "额", "然后", "就是"]
    hit = 0
    for marker in markers:
        if marker in text:
            hit += 1
    return hit >= 2


def submit_asr_basic_task(token, url):
    payload = {"url": url, "effect_mode": "basic"}
    resp = requests.post(
        f"{BASE_URL}{ASR_SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"ASR submit response missing task_id: {body}")
    return body


def get_duration(token, url):
    resp = requests.post(
        f"{BASE_URL}{GET_DURATION_PATH}",
        headers=_auth_headers(token),
        json={"url": url},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    return body.get("output") or {}


def _duration_output_to_seconds(duration_output):
    raw = (duration_output or {}).get("duration")
    try:
        value = float(raw)
    except Exception:
        return 0.0
    if value <= 0:
        return 0.0
    # In practice duration may be ms; use a conservative heuristic.
    if value > 10_000:
        return value / 1000.0
    return value


def _extract_task_status(body):
    status = str(body.get("status") or "").strip().lower()
    if status:
        return status
    result = body.get("result")
    if isinstance(result, dict):
        return str(result.get("status") or "").strip().lower()
    return ""


def submit_split_video_task(token, video_url, start_s, end_s):
    resp = requests.post(
        f"{BASE_URL}{SPLIT_SUBMIT_PATH}",
        headers=_auth_headers(token),
        json={"video_url": video_url, "start": start_s, "end": end_s},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"split-video submit response missing task_id: {body}")
    return body


def query_split_video_task_status(token, task_id):
    resp = requests.get(
        f"{BASE_URL}{SPLIT_STATUS_PATH}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def wait_split_video_done(token, task_id, poll_interval, timeout, log_prefix=""):
    started = time.monotonic()
    last_status = None
    last_heartbeat_at = started
    while True:
        status_body = query_split_video_task_status(token, task_id)
        status = _extract_task_status(status_body)
        if status != last_status:
            print(
                f"{log_prefix} split-video status changed: {status or 'unknown'}",
                file=sys.stderr,
                flush=True,
            )
            last_status = status
        now = time.monotonic()
        if now - last_heartbeat_at >= 15:
            print(
                f"{log_prefix} split-video polling... status={status or 'unknown'}",
                file=sys.stderr,
                flush=True,
            )
            last_heartbeat_at = now
        if status in SPLIT_DONE_STATUSES:
            return status_body
        if now - started >= timeout:
            raise RuntimeError(
                f"split-video polling timeout after {timeout}s. "
                f"Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def query_asr_task_status(token, task_id):
    headers = _auth_headers(token)
    get_resp = requests.get(
        f"{BASE_URL}{ASR_STATUS_PATH}",
        headers=headers,
        params={"task_id": task_id},
        timeout=60,
    )
    get_body = _parse_json_response(get_resp)
    if get_resp.status_code == 200 and "status" in get_body:
        return get_body

    post_resp = requests.post(
        f"{BASE_URL}{ASR_STATUS_PATH}",
        headers=headers,
        json={"task_id": task_id},
        timeout=60,
    )
    post_body = _parse_json_response(post_resp)
    if post_resp.status_code != 200:
        raise RuntimeError(post_body.get("error") or str(post_body))
    return post_body


def wait_asr_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_asr_task_status(token, task_id)
        status = status_body.get("status")
        if status in DONE_STATUSES:
            return status_body
        if time.monotonic() - started >= timeout:
            raise RuntimeError(
                f"ASR polling timeout after {timeout}s. "
                f"Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


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
        if time.monotonic() - started >= timeout:
            raise RuntimeError(
                f"Extract-audio polling timeout after {timeout}s. "
                f"Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def maybe_extract_audio_before_asr(token, url, poll_interval, timeout):
    if not _looks_like_video_url(url):
        return {
            "asr_input_url": url,
            "extract_audio_used": False,
            "extract_audio_task_id": "",
            "extract_audio_status": "",
            "extract_audio_error": "",
        }

    try:
        submit_body = submit_extract_audio_task(token, url)
        status_body = wait_extract_audio_done(
            token=token,
            task_id=submit_body["task_id"],
            poll_interval=poll_interval,
            timeout=timeout,
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
            "extract_audio_error": "",
        }
    except Exception as exc:
        return {
            "asr_input_url": url,
            "extract_audio_used": False,
            "extract_audio_task_id": "",
            "extract_audio_status": "failed_fallback_to_video",
            "extract_audio_error": str(exc),
        }


def _build_asr_aligned_ranges(duration_seconds, segments, max_chunk_seconds):
    duration_ms = int(float(duration_seconds) * 1000)
    max_chunk_ms = int(float(max_chunk_seconds) * 1000)
    if duration_ms <= 0 or max_chunk_ms <= 0:
        return []
    if duration_ms <= max_chunk_ms:
        return [(0.0, duration_ms / 1000.0)]

    end_points = []
    for seg in segments or []:
        end_ms = seg.get("end_ms")
        if end_ms is None:
            continue
        try:
            val = int(end_ms)
        except Exception:
            continue
        if 0 < val <= duration_ms:
            end_points.append(val)
    end_points = sorted(set(end_points))

    ranges = []
    cursor_ms = 0
    while cursor_ms < duration_ms:
        hard_end_ms = min(cursor_ms + max_chunk_ms, duration_ms)
        candidate_end_ms = None
        for end_ms in end_points:
            if end_ms <= cursor_ms:
                continue
            if end_ms <= hard_end_ms:
                candidate_end_ms = end_ms
            else:
                break

        if hard_end_ms == duration_ms:
            next_end_ms = duration_ms
        elif candidate_end_ms is not None:
            next_end_ms = candidate_end_ms
        else:
            # No sentence boundary in current window; fallback to hard cut.
            next_end_ms = hard_end_ms

        if next_end_ms <= cursor_ms:
            next_end_ms = min(cursor_ms + max_chunk_ms, duration_ms)
            if next_end_ms <= cursor_ms:
                break
        ranges.append((cursor_ms / 1000.0, next_end_ms / 1000.0))
        cursor_ms = next_end_ms
    return ranges


def maybe_split_long_video(token, url, poll_interval, timeout, chunk_seconds=300):
    print(
        "[progress] get_duration request sent...",
        file=sys.stderr,
        flush=True,
    )
    duration_output = get_duration(token, url)
    duration_seconds = _duration_output_to_seconds(duration_output)
    print(
        (
            "[progress] get_duration done: "
            f"raw_duration={duration_output.get('duration')}, "
            f"normalized_seconds={duration_seconds:.3f}"
        ),
        file=sys.stderr,
        flush=True,
    )
    if duration_seconds <= 0 or duration_seconds <= float(chunk_seconds):
        print(
            "[progress] duration <= chunk threshold, skip split-video",
            file=sys.stderr,
            flush=True,
        )
        return [
            {
                "analysis_url": url,
                "is_split_clip": False,
                "original_url": url,
                "duration_seconds": duration_seconds,
                "duration_output": duration_output,
            }
        ]

    print(
        "[progress] duration > 5min, running ASR basic for sentence-aligned split...",
        file=sys.stderr,
        flush=True,
    )
    asr_segments = []
    try:
        submit_body = submit_asr_basic_task(token, url)
        print(
            f"[progress] split-prep ASR submitted, task_id={submit_body.get('task_id', '')}; polling...",
            file=sys.stderr,
            flush=True,
        )
        asr_status_body = wait_asr_done(
            token=token,
            task_id=submit_body["task_id"],
            poll_interval=poll_interval,
            timeout=timeout,
        )
        if asr_status_body.get("status") == "success":
            parsed_asr = _extract_asr_text_and_segments(asr_status_body)
            asr_segments = parsed_asr.get("segments") or []
            print(
                f"[progress] split-prep ASR done, segment_count={len(asr_segments)}",
                file=sys.stderr,
                flush=True,
            )
        else:
            print(
                "[progress] split-prep ASR failed, fallback to hard-cut split plan",
                file=sys.stderr,
                flush=True,
            )
    except Exception as exc:
        print(
            f"[progress] split-prep ASR exception, fallback to hard-cut split plan: {exc}",
            file=sys.stderr,
            flush=True,
        )

    ranges = _build_asr_aligned_ranges(
        duration_seconds=duration_seconds,
        segments=asr_segments,
        max_chunk_seconds=float(chunk_seconds),
    )
    if not ranges:
        # Safety fallback to one hard-cut plan if range building fails.
        ranges = [(0.0, duration_seconds)]
    clip_count = len(ranges)
    print(
        f"[progress] sentence-aligned split plan generated, clip_count={clip_count}",
        file=sys.stderr,
        flush=True,
    )
    clips = []
    for clip_idx, (start_s, end_s) in enumerate(ranges, start=1):
        log_prefix = (
            f"[progress][split {clip_idx}/{clip_count}]"
            f"[{_seconds_to_ts(start_s)} - {_seconds_to_ts(end_s)}]"
        )
        print(
            f"{log_prefix} submit split-video task...",
            file=sys.stderr,
            flush=True,
        )
        submit_body = submit_split_video_task(token, url, start_s=start_s, end_s=end_s)
        print(
            f"{log_prefix} submitted, task_id={submit_body.get('task_id', '')}",
            file=sys.stderr,
            flush=True,
        )
        status_body = wait_split_video_done(
            token=token,
            task_id=submit_body["task_id"],
            poll_interval=poll_interval,
            timeout=timeout,
            log_prefix=log_prefix,
        )
        final_status = _extract_task_status(status_body)
        if final_status not in {"success", "succeeded"}:
            raise RuntimeError(f"split-video task failed: {status_body}")
        result = status_body.get("result") or {}
        public_url = result.get("public_url") or ""
        if not public_url:
            raise RuntimeError(f"split-video success but missing public_url: {status_body}")
        clips.append(
            {
                "analysis_url": public_url,
                "is_split_clip": True,
                "original_url": url,
                "clip_index": clip_idx,
                "clip_count": clip_count,
                "clip_start_s": start_s,
                "clip_end_s": end_s,
                "clip_start_ts": _seconds_to_ts(start_s),
                "clip_end_ts": _seconds_to_ts(end_s),
                "split_task_id": submit_body.get("task_id", ""),
                "split_status": final_status,
                "duration_seconds": duration_seconds,
                "duration_output": duration_output,
            }
        )
    return clips


def describe_video_detail(token, video_url, prompt=None):
    payload = {"video_url": video_url, "stream": True}
    if isinstance(prompt, str) and prompt.strip():
        payload["prompt"] = prompt.strip()
    resp = requests.post(
        f"{BASE_URL}{VIDEO_DETAIL_PATH}",
        headers=_auth_headers(token),
        json=payload,
        stream=True,
        timeout=(30, 300),
    )
    if resp.status_code != 200:
        # Keep a fallback for non-SSE error bodies.
        try:
            body = _parse_json_response(resp)
        except RuntimeError:
            body = _parse_video_detail_stream_text(resp.text)
        raise RuntimeError(body.get("error") or str(body))

    stream_lines = []
    printed_text = ""
    printed_think = ""
    print("[video_detail] stream started...", file=sys.stderr, flush=True)
    for raw in resp.iter_lines(decode_unicode=True):
        line = (raw or "").strip()
        if not line:
            continue
        stream_lines.append(line)
        # 实时回显流式内容，避免长时等待时看起来“卡住”。
        if line.startswith("data:"):
            payload_text = line[len("data:") :].strip()
        else:
            payload_text = line
        if payload_text and payload_text != "[DONE]":
            try:
                obj = json.loads(payload_text)
                extracted = _extract_video_detail_and_think_from_obj(obj)
                piece = extracted.get("video_detail", "")
                think_piece = extracted.get("think", "")
                if think_piece:
                    if think_piece.startswith(printed_think):
                        think_delta = think_piece[len(printed_think) :]
                        printed_think = think_piece
                    else:
                        think_delta = think_piece
                        printed_think += think_piece
                    if think_delta:
                        print(f"[think]{think_delta}", end="", file=sys.stderr, flush=True)
                if piece:
                    if piece.startswith(printed_text):
                        delta = piece[len(printed_text) :]
                        printed_text = piece
                    else:
                        delta = piece
                        printed_text += piece
                    if delta:
                        print(delta, end="", file=sys.stderr, flush=True)
            except Exception:
                print(payload_text, end="", file=sys.stderr, flush=True)
        if line == "data: [DONE]" or line == "[DONE]":
            break
    if printed_text:
        print("", file=sys.stderr, flush=True)
    print("[video_detail] stream finished.", file=sys.stderr, flush=True)

    body = _parse_video_detail_stream_lines(stream_lines)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    output = body.get("output") or {}
    return {
        "prompt": payload.get("prompt", ""),
        "video_detail": output.get("video_detail", ""),
        "raw": body,
    }


def normalize_segments(segments):
    normalized = []
    for idx, seg in enumerate(segments or [], start=1):
        start_ms = seg.get("start")
        end_ms = seg.get("end")
        normalized.append(
            {
                "id": idx,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "start_ts": _ms_to_ts(start_ms),
                "end_ts": _ms_to_ts(end_ms),
                "text": seg.get("text", ""),
            }
        )
    return normalized


def _extract_asr_text_and_segments(asr_status_body):
    asr_result = asr_status_body.get("result") or {}
    nested_result = asr_result.get("result") or {}
    raw_result = ((nested_result.get("raw") or {}).get("result")) or {}

    full_text = (
        asr_result.get("content")
        or nested_result.get("content")
        or raw_result.get("text")
        or ""
    )

    raw_segments = (
        asr_result.get("segments")
        or nested_result.get("segments")
        or raw_result.get("utterances")
        or []
    )
    normalized_segments = []
    for seg in raw_segments:
        if not isinstance(seg, dict):
            continue
        start_ms = seg.get("start")
        if start_ms is None:
            start_ms = seg.get("start_time")
        end_ms = seg.get("end")
        if end_ms is None:
            end_ms = seg.get("end_time")
        normalized_segments.append(
            {
                "start": start_ms,
                "end": end_ms,
                "text": seg.get("text", ""),
            }
        )

    return {
        "mode": asr_result.get("mode") or nested_result.get("mode") or "",
        "effect_mode": (
            asr_result.get("effect_mode")
            or nested_result.get("effect_mode")
            or "basic"
        ),
        "full_text": full_text,
        "segments": normalize_segments(normalized_segments),
    }


def build_asset_analysis(url, asr_status_body, visual_result, index, preproc):
    parsed_asr = _extract_asr_text_and_segments(asr_status_body)
    full_text = parsed_asr["full_text"]
    segments = parsed_asr["segments"]
    segment_count = len(segments)

    oral_candidate = segment_count >= 3 and len(full_text.strip()) >= 20
    broll_candidate = bool(visual_result.get("video_detail")) and not oral_candidate

    return {
        "asset_index": index,
        "source_url": url,
        "asset_type_guess": (
            "oral_candidate"
            if oral_candidate
            else "broll_candidate" if broll_candidate else "mixed_or_unknown"
        ),
        "asr_basic": {
            "source_input_url": url,
            "asr_input_url": preproc.get("asr_input_url", url),
            "preprocessing": {
                "extract_audio_used": preproc.get("extract_audio_used", False),
                "extract_audio_task_id": preproc.get("extract_audio_task_id", ""),
                "extract_audio_status": preproc.get("extract_audio_status", ""),
                "extract_audio_error": preproc.get("extract_audio_error", ""),
            },
            "task_id": asr_status_body.get("task_id", ""),
            "status": asr_status_body.get("status", ""),
            "error": (
                (asr_status_body.get("result") or {}).get("error")
                or asr_status_body.get("error")
                or ""
            ),
            "mode": parsed_asr["mode"],
            "effect_mode": parsed_asr["effect_mode"],
            "full_text": full_text,
            "segment_count": segment_count,
            "segments": segments,
        },
        "video_detail": {
            "analyzed": bool(visual_result.get("video_detail")),
            "prompt": visual_result.get("prompt", ""),
            "detail_text": visual_result.get("video_detail", ""),
            "error": visual_result.get("error", ""),
        },
        "editing_hints": {
            "suggest_trim_fillers": oral_candidate and _looks_like_filler_heavy(full_text),
            "can_be_broll": broll_candidate,
            "has_talking_head_signal": oral_candidate,
        },
    }


def build_global_summary(assets):
    oral_assets = [a for a in assets if a["asset_type_guess"] == "oral_candidate"]
    broll_assets = [a for a in assets if a["editing_hints"]["can_be_broll"]]
    recs = []

    if len(oral_assets) == 0:
        recs.append("未检测到明确口播素材，建议补充口播主线或改为画面驱动剪辑。")
    elif len(oral_assets) == 1:
        recs.append("检测到 1 条口播，建议先评估是否需要去气口，再定字幕节奏。")
    else:
        recs.append(f"检测到 {len(oral_assets)} 条口播，可按主题拆分多段口播结构。")

    if oral_assets and broll_assets:
        recs.append(
            f"检测到 {len(broll_assets)} 条可用 B-roll，建议按口播分句时间戳穿插补画面。"
        )
    elif oral_assets and not broll_assets:
        recs.append("口播存在但缺少明确 B-roll，建议补拍或用 AI 生成补画面素材。")

    filler_flags = [a for a in oral_assets if a["editing_hints"]["suggest_trim_fillers"]]
    if filler_flags:
        recs.append(
            f"{len(filler_flags)} 条口播疑似有气口/停顿，建议进入 asr-vad 做精剪。"
        )

    return {
        "total_assets": len(assets),
        "oral_candidate_count": len(oral_assets),
        "broll_candidate_count": len(broll_assets),
        "recommended_actions": recs,
    }


def render_markdown(report):
    lines = []
    summary = report["summary"]

    lines.append("# 素材描述报告（describe-video）")
    lines.append("")
    lines.append("## 全局概览")
    lines.append(f"- 素材总数：{summary['total_assets']}")
    lines.append(f"- 口播候选：{summary['oral_candidate_count']}")
    lines.append(f"- B-roll 候选：{summary['broll_candidate_count']}")
    lines.append("- 剪辑建议：")
    for item in summary["recommended_actions"]:
        lines.append(f"  - {item}")
    lines.append("")

    for asset in report["assets"]:
        lines.append(f"## 素材 {asset['asset_index']}")
        lines.append(f"- URL：{asset['source_url']}")
        origin = asset.get("origin") or {}
        if origin.get("is_split_clip"):
            lines.append(f"- 原始视频：{origin.get('original_url', '')}")
            lines.append(
                (
                    f"- 切片：{origin.get('clip_index')}/{origin.get('clip_count')} "
                    f"[{origin.get('clip_start_ts')} - {origin.get('clip_end_ts')}]"
                )
            )
        lines.append(f"- 类型判断：{asset['asset_type_guess']}")
        lines.append(f"- ASR 分句数：{asset['asr_basic']['segment_count']}")
        lines.append(f"- 是否建议去气口：{asset['editing_hints']['suggest_trim_fillers']}")
        lines.append(f"- 是否可作为 B-roll：{asset['editing_hints']['can_be_broll']}")
        lines.append("")
        lines.append("### 字幕全文")
        lines.append("")
        lines.append(asset["asr_basic"]["full_text"] or "(空)")
        lines.append("")
        lines.append("### 分句时间戳")
        for seg in asset["asr_basic"]["segments"]:
            display_start = seg.get("global_start_ts") or seg["start_ts"]
            display_end = seg.get("global_end_ts") or seg["end_ts"]
            seg_line = (
                f"- [{display_start} - {display_end}] "
                f"{re.sub(r'\\s+', ' ', seg['text']).strip()}"
            )
            lines.append(seg_line)
        if not asset["asr_basic"]["segments"]:
            lines.append("- (无)")
        lines.append("")
        lines.append("### 画面理解")
        lines.append("")
        lines.append(asset["video_detail"]["detail_text"] or "(未获取)")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def load_urls_from_file(input_file):
    urls = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            candidate = line.strip()
            if not candidate or candidate.startswith("#"):
                continue
            urls.append(candidate)
    return urls


def run(urls, analysis_prompt="", poll_interval=2.0, timeout=600.0):
    token = _ensure_token()
    assets = []

    total = len(urls)
    for idx, url in enumerate(urls, start=1):
        print(
            f"[progress][{idx}/{total}] start asset: {url}",
            file=sys.stderr,
            flush=True,
        )
        _validate_url(url)
        print(
            f"[progress][{idx}/{total}] checking duration...",
            file=sys.stderr,
            flush=True,
        )
        if _looks_like_video_url(url):
            clips = maybe_split_long_video(
                token=token,
                url=url,
                poll_interval=poll_interval,
                timeout=timeout,
            )
        else:
            clips = [
                {
                    "analysis_url": url,
                    "is_split_clip": False,
                    "original_url": url,
                    "duration_seconds": 0.0,
                    "duration_output": {},
                }
            ]
        if clips and clips[0].get("is_split_clip"):
            print(
                (
                    f"[progress][{idx}/{total}] long video detected, "
                    f"split into {len(clips)} clips (<=10min each)"
                ),
                file=sys.stderr,
                flush=True,
            )

        for clip in clips:
            analysis_url = clip.get("analysis_url") or url
            clip_label = ""
            if clip.get("is_split_clip"):
                clip_label = (
                    f" clip {clip.get('clip_index')}/{clip.get('clip_count')} "
                    f"[{clip.get('clip_start_ts')} - {clip.get('clip_end_ts')}]"
                )
            print(
                f"[progress][{idx}/{total}]{clip_label} extracting audio if needed...",
                file=sys.stderr,
                flush=True,
            )
            preproc = maybe_extract_audio_before_asr(
                token=token,
                url=analysis_url,
                poll_interval=poll_interval,
                timeout=timeout,
            )
            if preproc.get("extract_audio_used"):
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} extract-audio success, "
                        f"task_id={preproc.get('extract_audio_task_id', '')}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )
            elif preproc.get("extract_audio_status") == "failed_fallback_to_video":
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} extract-audio failed, fallback to "
                        f"original url. error={preproc.get('extract_audio_error', '')}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )
            else:
                print(
                    f"[progress][{idx}/{total}]{clip_label} non-video input, skip extract-audio",
                    file=sys.stderr,
                    flush=True,
                )

            print(
                f"[progress][{idx}/{total}]{clip_label} submitting ASR basic task...",
                file=sys.stderr,
                flush=True,
            )
            status_body = {}
            submit_body = {}
            try:
                submit_body = submit_asr_basic_task(token, preproc["asr_input_url"])
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} ASR submitted, "
                        f"task_id={submit_body.get('task_id', '')}; polling..."
                    ),
                    file=sys.stderr,
                    flush=True,
                )
                status_body = wait_asr_done(
                    token=token,
                    task_id=submit_body["task_id"],
                    poll_interval=poll_interval,
                    timeout=timeout,
                )
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} ASR done, "
                        f"status={status_body.get('status')}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )
                status_body["task_id"] = submit_body.get("task_id", "")
            except Exception as exc:
                status_body = {
                    "task_id": submit_body.get("task_id", ""),
                    "status": "failed",
                    "error": str(exc),
                    "result": {"error": str(exc)},
                }
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} ASR failed but continue: "
                        f"{exc}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )
            if status_body.get("status") != "success":
                error = (
                    (status_body.get("result") or {}).get("error")
                    or status_body.get("error")
                    or str(status_body)
                )
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} ASR non-fatal error: "
                        f"{error}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )

            visual_result = {
                "prompt": analysis_prompt.strip(),
                "video_detail": "",
                "raw": {},
                "error": "",
            }
            try:
                print(
                    f"[progress][{idx}/{total}]{clip_label} running video_detail stream...",
                    file=sys.stderr,
                    flush=True,
                )
                visual_result = describe_video_detail(token, analysis_url, prompt=analysis_prompt)
                visual_result["error"] = ""
                print(
                    f"[progress][{idx}/{total}]{clip_label} video_detail done",
                    file=sys.stderr,
                    flush=True,
                )
            except Exception as exc:
                visual_result["error"] = str(exc)
                print(
                    (
                        f"[progress][{idx}/{total}]{clip_label} "
                        f"video_detail failed but continue: {exc}"
                    ),
                    file=sys.stderr,
                    flush=True,
                )

            asset = build_asset_analysis(
                analysis_url,
                status_body,
                visual_result,
                index=len(assets) + 1,
                preproc=preproc,
            )
            asset["origin"] = dict(clip)
            if clip.get("is_split_clip"):
                offset_ms = int(float(clip.get("clip_start_s", 0.0)) * 1000)
                for seg in asset["asr_basic"]["segments"]:
                    start_ms = seg.get("start_ms")
                    end_ms = seg.get("end_ms")
                    if start_ms is not None:
                        seg["global_start_ms"] = int(start_ms) + offset_ms
                        seg["global_start_ts"] = _ms_to_ts(seg["global_start_ms"])
                    if end_ms is not None:
                        seg["global_end_ms"] = int(end_ms) + offset_ms
                        seg["global_end_ts"] = _ms_to_ts(seg["global_end_ms"])
            assets.append(asset)
            print(
                f"[progress][{idx}/{total}]{clip_label} asset analysis completed",
                file=sys.stderr,
                flush=True,
            )

    report = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "asr_effect_mode": "basic",
            "analysis_prompt": analysis_prompt.strip(),
        },
        "summary": build_global_summary(assets),
        "assets": assets,
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--input-file", default="")
    parser.add_argument("--analysis-prompt", default="")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--json-output", default="describe_video_report.json")
    parser.add_argument("--md-output", default="describe_video_report.md")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.input_file:
        urls.extend(load_urls_from_file(args.input_file))
    if not urls:
        print("Error: Please provide urls or --input-file.", file=sys.stderr)
        sys.exit(1)

    try:
        report = run(
            urls=urls,
            analysis_prompt=args.analysis_prompt,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        markdown = render_markdown(report)
        with open(args.md_output, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        print(f"结构化 JSON 已输出到: {args.json_output}", file=sys.stderr)
        print(f"剪辑阅读文档已输出到: {args.md_output}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
