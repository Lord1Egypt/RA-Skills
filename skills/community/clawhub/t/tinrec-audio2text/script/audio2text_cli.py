#!/usr/bin/env python3
"""
Tinrec OpenClaw CLI：本地音频 → 上传 TOS → 提交转写 → 轮询完成 → 输出转写与 AI 总结。

核心能力：音频转文字、AI 总结、录音要点、发言人区分。便于 AI/脚本调用。
仅使用标准库（urllib + json），无外部依赖。

用法:
  # 从 api-keys 文件读取 Key（推荐）：在技能目录创建 api-keys 并写入 mt-xxx，然后执行
  python audio2text_cli.py /path/to/audio.mp3 --api-keys-file /path/to/api-keys
  # 或环境变量 / 命令行传 Key
  export TINREC_API_KEY="mt-xxx"
  python audio2text_cli.py /path/to/audio.mp3
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://api.tinrec.com/api"
EXT_TO_FORMAT = {
    ".mp3": "mp3",
    ".wav": "wav",
    ".m4a": "m4a",
    ".aac": "aac",
    ".ogg": "ogg",
    ".flac": "flac",
    ".opus": "opus",
}


def get_format_from_path(path: str) -> str:
    ext = Path(path).suffix.lower()
    return EXT_TO_FORMAT.get(ext, "mp3")


def _status(resp) -> int:
    return getattr(resp, "status", resp.getcode())


def _http_get(url: str, headers: dict, timeout: float = 30) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _status(resp), resp.read()


def _http_put(url: str, data: bytes, timeout: float = 120) -> int:
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/octet-stream"}, method="PUT")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _status(resp)


def _http_post_json(url: str, body: dict, headers: dict, timeout: float = 30) -> tuple[int, bytes]:
    headers = {**headers, "Content-Type": "application/json"}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _status(resp), resp.read()


def _parse_json_response(status: int, raw: bytes, err_prefix: str) -> dict:
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        data = {}
    if status != 200:
        msg = data.get("message", raw.decode("utf-8", errors="replace"))
        print(f"{err_prefix}: {msg}", file=sys.stderr)
        sys.exit(1)
    if data.get("code") != 200:
        print(f"{err_prefix}: {data.get('message', data)}", file=sys.stderr)
        sys.exit(1)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Tinrec OpenClaw：本地音频上传并转写，输出文字、AI 总结、要点与发言人信息。"
    )
    parser.add_argument(
        "audio_path",
        type=str,
        help="本地音频文件路径（如 .mp3 / .wav / .m4a）",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API Key（mt- 开头），优先于环境变量和 api-keys 文件",
    )
    parser.add_argument(
        "--api-keys-file",
        type=str,
        default="api-keys",
        help="存放 API Key 的文件路径（默认当前目录下的 api-keys），每行一个 key，取第一行非空",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=DEFAULT_BASE_URL,
        help=f"API 基础地址，默认 {DEFAULT_BASE_URL}",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=3.0,
        help="轮询间隔（秒），默认 3",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0,
        help="轮询总超时（秒），默认 600",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="仅输出最终详情的 JSON，便于 AI 解析",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="提交转写后立即返回任务 id，不轮询",
    )
    args = parser.parse_args()

    api_key = (args.api_key or os.environ.get("TINREC_API_KEY") or "").strip()
    if not api_key and args.api_keys_file:
        api_keys_path = Path(args.api_keys_file)
        if api_keys_path.is_file():
            with open(api_keys_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        api_key = line
                        break
    api_key = (api_key or "").strip()
    if not api_key:
        print("错误: 未提供 API Key。请使用 --api-key、环境变量 TINREC_API_KEY 或 --api-keys-file 指向的 api-keys 文件。", file=sys.stderr)
        print("获取方式: https://tinrec.com/api-keys", file=sys.stderr)
        sys.exit(1)

    path = Path(args.audio_path)
    if not path.is_file():
        print(f"错误: 文件不存在: {args.audio_path}", file=sys.stderr)
        sys.exit(1)

    base = args.base_url.rstrip("/")
    headers = {"Authorization": f"Bearer {api_key}"}
    filename = path.name
    audio_format = get_format_from_path(args.audio_path)

    # 1) 获取 OpenClaw 上传凭证
    token_url = f"{base}/tos/openclaw/upload-token?{urllib.parse.urlencode({'filename': filename})}"
    try:
        status, raw = _http_get(token_url, headers, timeout=30)
    except urllib.error.HTTPError as e:
        try:
            raw_err = e.read()
            body = json.loads(raw_err.decode("utf-8"))
            msg = body.get("message", raw_err.decode("utf-8", errors="replace"))
        except Exception:
            msg = str(e)
        print(f"获取上传凭证失败: {msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"获取上传凭证失败: {e}", file=sys.stderr)
        sys.exit(1)

    data = _parse_json_response(status, raw, "获取上传凭证失败")
    payload = data.get("data", {})
    signed_url = payload.get("signed_url")
    key = payload.get("key")
    if not signed_url or not key:
        print("响应缺少 signed_url 或 key", file=sys.stderr)
        sys.exit(1)

    # 2) 上传到 TOS
    try:
        with open(path, "rb") as f:
            body_bytes = f.read()
        put_status = _http_put(signed_url, body_bytes, timeout=120)
    except urllib.error.HTTPError as e:
        print(f"上传 TOS 失败: HTTP {e.code}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"上传 TOS 失败: {e}", file=sys.stderr)
        sys.exit(1)
    if put_status not in (200, 201):
        print(f"上传 TOS 失败: HTTP {put_status}", file=sys.stderr)
        sys.exit(1)

    # 3) 提交转写
    body = {
        "oss_key": key,
        "format": audio_format,
        "filename": filename,
        "source": "upload",
        "duration": 0,
    }
    try:
        status2, raw2 = _http_post_json(f"{base}/upload-v2", body, headers, timeout=30)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8")).get("message", str(e))
        except Exception:
            msg = str(e)
        print(f"提交转写失败: {msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"提交转写失败: {e}", file=sys.stderr)
        sys.exit(1)

    data2 = _parse_json_response(status2, raw2, "提交转写失败")
    task_data = data2.get("data", {})
    audio_id = task_data.get("id")
    if audio_id is None:
        print("响应缺少任务 id (data.id)", file=sys.stderr)
        sys.exit(1)

    if args.no_wait:
        print(json.dumps({"audio_id": audio_id, "message": "已提交，请自行轮询 GET /api/audio-detail/{id}"}))
        return

    # 4) 轮询详情直至终态（两个状态：转写状态 + 任务状态）
    # 转写状态(transcript_status)完成后才有正文；任务状态(task_status)==success 后才有总结、要点、发言人等
    start = time.time()
    while True:
        if time.time() - start > args.timeout:
            print("轮询超时", file=sys.stderr)
            sys.exit(1)
        try:
            status3, raw3 = _http_get(f"{base}/audio-detail/{audio_id}", headers, timeout=30)
        except Exception:
            time.sleep(args.poll_interval)
            continue
        if status3 != 200:
            time.sleep(args.poll_interval)
            continue
        try:
            data3 = json.loads(raw3.decode("utf-8"))
        except Exception:
            time.sleep(args.poll_interval)
            continue
        if data3.get("code") != 200:
            time.sleep(args.poll_interval)
            continue
        detail = data3.get("data", {})
        transcript_status = detail.get("transcript_status", "")
        task_status = detail.get("task_status", "")
        # 先等转写终态
        if transcript_status not in ("success", "limit", "failed"):
            time.sleep(args.poll_interval)
            continue
        # 转写成功后，再等任务状态完成（总结/要点/发言人需 task_status == "success"）
        if transcript_status == "success" and task_status != "success":
            time.sleep(args.poll_interval)
            continue
        transcript_data = None
        if transcript_status == "success":
            try:
                status4, raw4 = _http_get(f"{base}/transcript/{audio_id}", headers, timeout=30)
                if status4 == 200:
                    data4 = json.loads(raw4.decode("utf-8"))
                    if data4.get("code") == 200:
                        transcript_data = data4.get("data")
            except Exception:
                pass
        out = _build_result(detail, transcript_data)
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            _print_detail(out)
        return


def _build_result(detail: dict, transcript_data: dict | None) -> dict:
    """合并详情与转写。转写状态(transcript_status)决定是否有正文；任务状态(task_status)完成后才有 summary/要点/发言人。"""
    out = {
        "id": detail.get("id"),
        "file_name": detail.get("file_name"),
        "duration": detail.get("duration"),
        "transcript_status": detail.get("transcript_status"),  # 转写状态
        "task_status": detail.get("task_status"),              # 任务状态，完成后才有总结/要点/发言人
        "summary": detail.get("summary"),
        "chapters": detail.get("chapters"),
        "todos": detail.get("todos"),
        "recommend": detail.get("recommend"),
    }
    if transcript_data:
        out["transcripts"] = transcript_data.get("transcripts")
        out["speaker_data"] = transcript_data.get("speaker_data")
        out["enable_speaker"] = transcript_data.get("enable_speaker")
    return out


def _print_detail(out: dict) -> None:
    """输出转写与 AI 总结、要点、发言人等，便于人类阅读。总结/要点/发言人仅在任务状态完成后有值。"""
    print("--- 任务信息 ---")
    print(f"ID: {out.get('id')}  转写状态: {out.get('transcript_status')}  任务状态: {out.get('task_status')}")
    print(f"文件名: {out.get('file_name')}  时长: {out.get('duration')}s")
    print()
    summary = out.get("summary")
    if summary:
        print("--- AI 总结 / 录音要点 ---")
        if isinstance(summary, dict):
            text = summary.get("summary") or summary.get("content") or json.dumps(summary, ensure_ascii=False)
        else:
            text = str(summary)
        print(text)
        print()
    chapters = out.get("chapters")
    if chapters:
        print("--- 章节/要点 ---")
        print(json.dumps(chapters, ensure_ascii=False, indent=2))
        print()
    speaker_data = out.get("speaker_data")
    if speaker_data:
        print("--- 发言人 ---")
        print(json.dumps(speaker_data, ensure_ascii=False, indent=2))
        print()
    transcripts = out.get("transcripts")
    if transcripts:
        print("--- 转写正文（发言人区分） ---")
        print(json.dumps(transcripts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
