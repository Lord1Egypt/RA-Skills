#!/usr/bin/env python3
"""Tencent Cloud ASR credential self-check."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


DEFAULT_POLL_INTERVAL = 2
DEFAULT_MAX_POLL_TIME = 120


def fail(message, exit_code=1):
    print(json.dumps({"error": "SELF_CHECK_FAILED", "message": message}, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def skill_dir():
    return Path(__file__).resolve().parents[1]


def script_path(name):
    path = skill_dir() / "scripts" / name
    if not path.exists():
        fail(f"Missing script: {path}")
    return path


def default_sample_candidates():
    base = skill_dir()
    return [
        base / "assets" / "16k.wav",
        base / "assets" / "self-check" / "16k.wav",
        base / "16k.wav",
    ]


def resolve_sample_path(explicit_path):
    if explicit_path:
        path = Path(explicit_path).expanduser()
        if path.exists():
            return path.resolve()
        fail(f"Self-check sample does not exist: {path}")

    for candidate in default_sample_candidates():
        if candidate.exists():
            return candidate.resolve()

    fail(
        "No self-check sample audio found. Put 16k.wav under the skill assets directory "
        "or pass --sample /absolute/path/to/16k.wav."
    )


def parse_json_documents(stdout):
    documents = []
    decoder = json.JSONDecoder()
    index = 0
    length = len(stdout)

    while index < length:
        while index < length and stdout[index].isspace():
            index += 1
        if index >= length:
            break
        try:
            payload, end = decoder.raw_decode(stdout, index)
        except json.JSONDecodeError:
            return []
        documents.append(payload)
        index = end

    return documents


def run_command(command, allow_nonzero=False):
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode != 0 and not allow_nonzero:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Command failed")
    return result


def run_json_command(command):
    result = run_command(command, allow_nonzero=True)
    payloads = parse_json_documents(result.stdout)
    payload = payloads[-1] if payloads else None
    return result, payload


def ensure_ffmpeg():
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return {"status": "already_available"}

    result, payload = run_json_command([sys.executable, str(script_path("ensure_ffmpeg.py")), "--execute"])
    if result.returncode != 0:
        message = "Failed to prepare ffmpeg/ffprobe."
        if isinstance(payload, dict):
            message = payload.get("message") or payload.get("error") or message
        fail(message)
    return payload or {"status": "installed"}


def prepare_sample_audio(sample_path, output_dir):
    prepared_path = output_dir / "self_check.wav"
    normalize_command = [
        "ffmpeg",
        "-y",
        "-i",
        str(sample_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(prepared_path),
    ]
    run_command(normalize_command)
    return prepared_path


def transcript_preview(text, limit=60):
    if text is None:
        return None
    normalized = " ".join(str(text).split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1] + "…"


def build_check(mode, label, status, engine, audio_path, payload=None, stderr="", returncode=0):
    payload = payload or {}
    error = payload.get("error")
    message = payload.get("message") or payload.get("error_msg") or stderr.strip()
    code = payload.get("code")
    transcript = payload.get("result")

    emoji = {"passed": "✅", "failed": "❌", "skipped": "⚠️"}.get(status, "⚠️")
    check = {
        "mode": mode,
        "label": label,
        "status": status,
        "emoji": emoji,
        "engine": engine,
        "audio_path": str(audio_path),
        "returncode": returncode,
    }

    if transcript is not None:
        check["transcript_preview"] = transcript_preview(transcript)
    if payload.get("request_id"):
        check["request_id"] = payload["request_id"]
    if payload.get("task_id"):
        check["task_id"] = payload["task_id"]
    if payload.get("audio_duration") is not None:
        check["audio_duration"] = payload["audio_duration"]
    if error:
        check["error"] = error
    if code is not None:
        check["code"] = code
    if message:
        check["message"] = message
    return check


def run_asr_check(mode, label, command, engine, audio_path):
    result, payload = run_json_command(command)
    if result.returncode == 0 and isinstance(payload, dict) and payload.get("result") is not None:
        return build_check(mode, label, "passed", engine, audio_path, payload=payload, returncode=0)

    payload = payload or {}
    if payload.get("error") == "CREDENTIALS_NOT_CONFIGURED" and mode == "flash":
        return build_check(mode, label, "skipped", engine, audio_path, payload=payload, stderr=result.stderr, returncode=result.returncode)

    return build_check(mode, label, "failed", engine, audio_path, payload=payload, stderr=result.stderr, returncode=result.returncode)


def classify_result(checks):
    passed = {check["mode"] for check in checks if check["status"] == "passed"}
    failed = {check["mode"] for check in checks if check["status"] == "failed"}
    skipped = {check["mode"] for check in checks if check["status"] == "skipped"}

    if passed == {"sentence", "flash", "file"}:
        return "success"
    if failed == {"sentence", "flash", "file"}:
        return "all_failed"
    if failed == {"sentence", "file"} and skipped == {"flash"}:
        return "all_failed"
    if passed == {"sentence", "file"} and failed == {"flash"}:
        return "flash_only_failed"
    if passed == {"sentence", "file"} and skipped == {"flash"}:
        return "flash_not_checked"
    return "partial"


def build_guidance(classification, checks):
    lines = []
    flash_check = next((check for check in checks if check["mode"] == "flash"), None)

    if classification == "success":
        lines.append("✅ 三个模式都通过了自检，可以继续正常使用。")
        return lines

    if classification == "all_failed":
        lines.append("❌ 三个模式都没有通过自检。")
        lines.append("请优先检查你提供的密钥是否有效、ASR 服务是否已开通、资源包或计费状态是否正常。")
        lines.append("如果确认配置无误，建议把报错信息整理后直接咨询腾讯云官网客服。")
        return lines

    if classification == "flash_only_failed":
        lines.append("⚠️ 一句话识别和录音文件识别通过了，只有极速版没有通过。")
        lines.append("这通常不是基础密钥整体失效，更像是极速版单独受限。")
        lines.append("常见于国际站账号，或国内站账号在海外访问时极速版受限。")
        lines.append("也请顺手确认 AppId 是否正确、极速版资源是否已开通。")
        return lines

    if classification == "flash_not_checked":
        lines.append("⚠️ 基础模式已经通过，但极速版还没有完成验证。")
        lines.append("当前最常见原因是缺少 AppId；补充后再跑一次自检即可。")
        return lines

    failed_labels = [check["label"] for check in checks if check["status"] == "failed"]
    if failed_labels:
        lines.append(f"⚠️ 部分模式没有通过：{'、'.join(failed_labels)}。")
    else:
        lines.append("⚠️ 本次自检未得到完整结果。")

    if flash_check and flash_check.get("status") == "failed":
        lines.append("如果只有极速版持续报错，请重点检查 AppId、极速版开通状态，以及账号站点/访问环境限制。")
    else:
        lines.append("请根据失败模式对应的错误信息继续排查；若反复失败，建议整理报错信息后联系腾讯云客服。")
    return lines


def build_report(classification, checks, sample_path):
    header = {
        "success": "✅ 自检通过",
        "all_failed": "❌ 自检失败",
        "flash_only_failed": "⚠️ 基础模式可用，极速版失败",
        "flash_not_checked": "⚠️ 基础模式可用，极速版未验证",
        "partial": "⚠️ 自检部分通过",
    }[classification]

    lines = [
        f"{header}",
        f"样例音频：{sample_path}",
        "",
    ]

    for check in checks:
        line = f"{check['emoji']} {check['label']}（engine={check['engine']}）"
        if check.get("transcript_preview"):
            line += f"：{check['transcript_preview']}"
        elif check.get("message"):
            line += f"：{check['message']}"
        lines.append(line)

    guidance = build_guidance(classification, checks)
    if guidance:
        lines.append("")
        lines.extend(guidance)

    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Tencent Cloud ASR self-check with a bundled sample.")
    parser.add_argument("--sample", help="Path to the sample WAV used for self-check.")
    parser.add_argument("--engine-sentence", default="16k_zh")
    parser.add_argument("--engine-flash", default="16k_zh")
    parser.add_argument("--engine-file", default="16k_zh")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--max-poll-time", type=int, default=DEFAULT_MAX_POLL_TIME)
    return parser.parse_args()


def main():
    args = parse_args()
    sample_path = resolve_sample_path(args.sample)
    ffmpeg_status = ensure_ffmpeg()

    with tempfile.TemporaryDirectory(prefix="tencent-asr-self-check-") as temp_dir:
        prepared_path = prepare_sample_audio(sample_path, Path(temp_dir))

        checks = [
            run_asr_check(
                "sentence",
                "一句话识别",
                [
                    sys.executable,
                    str(script_path("sentence_recognize.py")),
                    str(prepared_path),
                    "--engine",
                    args.engine_sentence,
                ],
                args.engine_sentence,
                prepared_path,
            ),
            run_asr_check(
                "flash",
                "录音文件识别极速版",
                [
                    sys.executable,
                    str(script_path("flash_recognize.py")),
                    str(prepared_path),
                    "--engine",
                    args.engine_flash,
                ],
                args.engine_flash,
                prepared_path,
            ),
            run_asr_check(
                "file",
                "录音文件识别",
                [
                    sys.executable,
                    str(script_path("file_recognize.py")),
                    "rec",
                    str(prepared_path),
                    "--engine",
                    args.engine_file,
                    "--poll-interval",
                    str(args.poll_interval),
                    "--max-poll-time",
                    str(args.max_poll_time),
                ],
                args.engine_file,
                prepared_path,
            ),
        ]

    classification = classify_result(checks)
    payload = {
        "status": classification,
        "sample_path": str(sample_path),
        "ffmpeg_status": ffmpeg_status,
        "checks": checks,
        "guidance": build_guidance(classification, checks),
        "report_markdown": build_report(classification, checks, sample_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
