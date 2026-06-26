#!/usr/bin/env python3
"""CLI transcription wrapper for hosts like OpenClaw."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


SHORT_MAX_SECONDS = 60
SENTENCE_MAX_BYTES = 3 * 1024 * 1024
FLASH_MAX_SECONDS = 2 * 60 * 60
FLASH_MAX_BYTES = 100 * 1024 * 1024
FILE_ASYNC_MAX_SECONDS = 5 * 60 * 60
FILE_BODY_MAX_BYTES = 5 * 1024 * 1024
SEGMENT_SECONDS = 30 * 60
URL_ASYNC_FALLBACK_ERRORS = {
    "FFPROBE_FAILED",
    "FFPROBE_TIMEOUT",
    "requires_ffprobe_or_ffmpeg",
}


def fail(message, exit_code=1):
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def script_dir():
    return Path(__file__).resolve().parent


def script_path(name):
    path = script_dir() / name
    if not path.exists():
        fail(f"Missing Tencent ASR script: {path}")
    return path


def run_command(command, allow_nonzero=False):
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.returncode != 0 and not allow_nonzero:
        stdout = result.stdout.strip()
        if stdout:
            try:
                payload = json.loads(stdout)
            except json.JSONDecodeError:
                fail(stdout)
            fail(format_payload_error(payload))
        fail(f"Command failed: {' '.join(command)}")
    return result


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


def run_json_command(command, allow_nonzero=False):
    result = run_command(command, allow_nonzero=allow_nonzero)
    stdout = result.stdout.strip()
    payloads = []
    if stdout:
        payloads = parse_json_documents(stdout)
        if not payloads:
            if allow_nonzero and result.returncode != 0:
                payloads = []
            else:
                fail(f"Expected JSON output from {' '.join(command)}")
    return result, payloads


def select_payload(payloads):
    if not payloads:
        return None
    return payloads[-1]


def format_payload_error(payload):
    if not isinstance(payload, dict):
        return "Tencent ASR command failed."
    error = payload.get("error")
    message = payload.get("message")
    if error and message:
        return f"{error}: {message}"
    if message:
        return str(message)
    if error:
        return str(error)
    return json.dumps(payload, ensure_ascii=False)


def ensure_ffmpeg():
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return

    command = [sys.executable, str(script_path("ensure_ffmpeg.py")), "--execute"]
    _, payloads = run_json_command(command, allow_nonzero=True)
    payload = select_payload(payloads)
    if not payload:
        fail("Failed to provision ffmpeg/ffprobe for Tencent ASR.")

    status = payload.get("status")
    if status not in {"already_available", "installed"}:
        fail(format_payload_error(payload))

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        fail("ffmpeg/ffprobe are still unavailable after installation.")


def inspect_audio(input_value, allow_async_url_fallback=False):
    command = [sys.executable, str(script_path("inspect_audio.py")), input_value]
    _, payloads = run_json_command(command, allow_nonzero=True)
    for payload in payloads:
        if isinstance(payload, dict) and not payload.get("error"):
            return payload

    payload = select_payload(payloads)
    error = payload.get("error") if isinstance(payload, dict) else None
    if error == "requires_ffprobe_or_ffmpeg" and not (
        allow_async_url_fallback and should_fallback_to_async_url(input_value, payload)
    ):
        ensure_ffmpeg()
        _, payloads = run_json_command(command, allow_nonzero=True)
        for payload in payloads:
            if isinstance(payload, dict) and not payload.get("error"):
                return payload
        payload = select_payload(payloads)

    if allow_async_url_fallback and should_fallback_to_async_url(input_value, payload):
        return None

    if isinstance(payload, dict):
        fail(format_payload_error(payload))
    fail(f"Unable to inspect audio: {input_value}")


def normalize_audio(input_path, output_path):
    ensure_ffmpeg()
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        output_path,
    ]
    run_command(command)


def segment_audio(input_path, output_dir):
    ensure_ffmpeg()
    pattern = str(output_dir / "part_%03d.wav")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-f",
        "segment",
        "-segment_time",
        str(SEGMENT_SECONDS),
        "-c:a",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        pattern,
    ]
    run_command(command)
    return sorted(output_dir.glob("part_*.wav"))


def is_http_url(value):
    return value.startswith("http://") or value.startswith("https://")


def validate_public_url(value, flag_name):
    if value and not is_http_url(value):
        fail(f"{flag_name} must be an http:// or https:// public URL.")
    return value


def should_fallback_to_async_url(input_value, payload):
    return (
        is_http_url(input_value)
        and isinstance(payload, dict)
        and payload.get("error") in URL_ASYNC_FALLBACK_ERRORS
    )


def is_normalized_wav(metadata):
    container = (metadata.get("container_format") or "").split(",")
    return (
        metadata.get("sample_rate") == 16000
        and metadata.get("channels") == 1
        and "wav" in container
    )


def file_size(path):
    return os.path.getsize(path)


def appid_configured():
    return bool(os.getenv("TENCENTCLOUD_APPID"))


def require_credentials(require_appid=False):
    missing = []
    if not os.getenv("TENCENTCLOUD_SECRET_ID"):
        missing.append("TENCENTCLOUD_SECRET_ID")
    if not os.getenv("TENCENTCLOUD_SECRET_KEY"):
        missing.append("TENCENTCLOUD_SECRET_KEY")
    if require_appid and not os.getenv("TENCENTCLOUD_APPID"):
        missing.append("TENCENTCLOUD_APPID")
    if missing:
        fail("Missing Tencent Cloud credentials: " + ", ".join(missing))


def extract_transcript(payload):
    if not isinstance(payload, dict):
        fail("Tencent ASR returned an invalid payload.")
    transcript = payload.get("result")
    if transcript is None:
        fail(format_payload_error(payload))
    return str(transcript).strip()


def run_asr_script(script_name, args):
    command = [sys.executable, str(script_path(script_name))] + args
    _, payloads = run_json_command(command)
    payload = select_payload(payloads)
    return extract_transcript(payload)


def transcribe_short(input_value, engine):
    require_credentials()
    return run_asr_script("sentence_recognize.py", [input_value, "--engine", engine])


def transcribe_flash(input_value, engine):
    require_credentials(require_appid=True)
    return run_asr_script("flash_recognize.py", [input_value, "--engine", engine])


def transcribe_async(input_value, engine, poll_interval, max_poll_time):
    require_credentials()
    return run_asr_script(
        "file_recognize.py",
        [
            "rec",
            input_value,
            "--engine",
            engine,
            "--poll-interval",
            str(poll_interval),
            "--max-poll-time",
            str(max_poll_time),
        ],
    )


def transcribe_local_file(
    input_path,
    short_engine,
    long_engine,
    poll_interval,
    max_poll_time,
    async_public_url=None,
):
    metadata = inspect_audio(input_path)

    with tempfile.TemporaryDirectory(prefix="tencent-asr-cli-") as temp_dir:
        temp_dir_path = Path(temp_dir)
        working_path = Path(input_path)

        if not is_normalized_wav(metadata):
            normalized_path = temp_dir_path / "normalized.wav"
            normalize_audio(str(working_path), str(normalized_path))
            working_path = normalized_path
            metadata = inspect_audio(str(working_path))

        duration = metadata.get("duration_seconds")
        if duration is None:
            fail("Unable to determine audio duration after normalization.")

        size_bytes = file_size(working_path)

        if duration <= SHORT_MAX_SECONDS and size_bytes <= SENTENCE_MAX_BYTES:
            return transcribe_short(str(working_path), short_engine)

        if duration <= FLASH_MAX_SECONDS and size_bytes <= FLASH_MAX_BYTES:
            if appid_configured():
                return transcribe_flash(str(working_path), long_engine)
            if async_public_url and duration <= FILE_ASYNC_MAX_SECONDS:
                return transcribe_async(
                    async_public_url,
                    long_engine,
                    poll_interval,
                    max_poll_time,
                )
            if size_bytes <= FILE_BODY_MAX_BYTES:
                return transcribe_async(
                    str(working_path),
                    long_engine,
                    poll_interval,
                    max_poll_time,
                )
            fail(
                "Long audio needs Tencent Cloud AppId for Flash ASR. "
                "Without AppId, this local file is too large for CreateRecTask body upload. "
                "If you already uploaded a normalized file to COS, pass its public URL via "
                "--async-public-url."
            )

        if async_public_url and duration <= FILE_ASYNC_MAX_SECONDS:
            return transcribe_async(
                async_public_url,
                long_engine,
                poll_interval,
                max_poll_time,
            )

        if not appid_configured():
            fail(
                "Segmented long-audio transcription needs Tencent Cloud AppId because "
                "the wrapper uses Flash ASR for local segments. "
                "If you already uploaded a normalized <=5h file to COS, pass its public URL via "
                "--async-public-url to avoid local segmentation."
            )

        segments_dir = temp_dir_path / "segments"
        segments_dir.mkdir()
        segment_paths = segment_audio(str(working_path), segments_dir)
        if not segment_paths:
            fail("ffmpeg segmenting produced no audio chunks.")

        transcripts = []
        for segment_path in segment_paths:
            transcripts.append(transcribe_flash(str(segment_path), long_engine))
        return "\n\n".join(part for part in transcripts if part)


def transcribe_url(input_value, short_engine, long_engine, poll_interval, max_poll_time):
    del short_engine  # URL input defaults to async recording-file recognition.
    try:
        return transcribe_async(input_value, long_engine, poll_interval, max_poll_time)
    except SystemExit as exc:
        message = str(exc)
        fail(
            "Async URL recognition failed. For public URLs, the default path is "
            "file_recognize.py rec. Please first check whether the URL is publicly reachable "
            "and whether the audio is within the 5h CreateRecTask limit. "
            f"Original error: {message}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI transcription wrapper for Tencent Cloud ASR."
    )
    parser.add_argument("input", help="Local audio path or public URL.")
    parser.add_argument(
        "--async-public-url",
        help=(
            "Optional public URL for a normalized file already uploaded to COS or similar storage. "
            "Used for local inputs when async URL recognition is preferable to body upload or segmentation."
        ),
    )
    parser.add_argument("--engine-short", default="16k_zh")
    parser.add_argument("--engine-long", default="16k_zh")
    parser.add_argument("--poll-interval", type=int, default=5)
    parser.add_argument("--max-poll-time", type=int, default=1800)
    args = parser.parse_args()
    args.async_public_url = validate_public_url(args.async_public_url, "--async-public-url")
    return args


def main():
    args = parse_args()

    if is_http_url(args.input):
        transcript = transcribe_url(
            args.input,
            args.engine_short,
            args.engine_long,
            args.poll_interval,
            args.max_poll_time,
        )
    else:
        input_path = Path(args.input)
        if not input_path.is_file():
            fail(f"Audio file does not exist: {input_path}")
        transcript = transcribe_local_file(
            str(input_path),
            args.engine_short,
            args.engine_long,
            args.poll_interval,
            args.max_poll_time,
            args.async_public_url,
        )

    print(transcript)


if __name__ == "__main__":
    main()
