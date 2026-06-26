"""StepFun ASR (stepaudio-2.5-asr) 客户端 — SSE 流式转写。

用法：
    transcript = transcribe_video(Path("xxx.mp4"))

实现：
    1. ffmpeg 抽出 16kHz mono PCM s16le
    2. base64 编码塞进 JSON
    3. POST /v1/audio/asr/sse 拿 SSE 流
    4. 逐事件解析 transcription.text，最终拼回完整字幕

注意：base64 后请求体会膨胀 ≈ 1.33×，长于 5 分钟的视频建议先截段或换 file_id 路径。
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
from pathlib import Path

import httpx

ASR_ENDPOINT = "https://api.stepfun.com/v1/audio/asr/sse"
MODEL = "stepaudio-2.5-asr"
ASR_TIMEOUT_SEC = 600.0


def _api_key() -> str:
    """与 stepfun_client._api_key 同源；不直接 import 避免循环依赖。"""
    key = os.environ.get("STEP_API_KEY")
    if key:
        return key
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "STEP_API_KEY":
                return v.strip().strip('"').strip("'")
    raise RuntimeError("STEP_API_KEY 未设置")


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg 未安装。macOS: brew install ffmpeg")


def extract_pcm(video_path: Path, out_path: Path | None = None) -> Path:
    """抽出 16kHz mono PCM s16le。返回 .pcm 临时文件路径。"""
    _ensure_ffmpeg()
    if out_path is None:
        out_path = video_path.with_suffix(".asr.pcm")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",                  # 去视频
        "-ac", "1",             # 单声道
        "-ar", "16000",         # 16kHz
        "-f", "s16le",          # 16-bit little-endian PCM
        "-acodec", "pcm_s16le",
        str(out_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg 抽音失败 (returncode={proc.returncode}):\n{proc.stderr[-1500:]}"
        )
    return out_path


def transcribe_pcm(pcm_path: Path, language: str = "zh", enable_itn: bool = True) -> str:
    """把 16kHz mono PCM 文件转录为文本。"""
    pcm_bytes = pcm_path.read_bytes()
    audio_b64 = base64.b64encode(pcm_bytes).decode("ascii")
    payload = {
        "audio": {
            "data": audio_b64,
            "input": {
                "transcription": {
                    "model": MODEL,
                    "language": language,
                    "enable_itn": enable_itn,
                },
                "format": {
                    "type": "pcm",
                    "codec": "pcm_s16le",
                    "rate": 16000,
                    "bits": 16,
                    "channel": 1,
                },
            },
        }
    }

    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    pieces: list[str] = []
    last_full = ""

    with httpx.Client(timeout=ASR_TIMEOUT_SEC) as client:
        with client.stream("POST", ASR_ENDPOINT, headers=headers, json=payload) as resp:
            if resp.status_code != 200:
                body = resp.read().decode("utf-8", errors="ignore")
                raise RuntimeError(f"ASR HTTP {resp.status_code}: {body[:500]}")

            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.strip()
                if not line.startswith("data:"):
                    continue
                data_str = line[len("data:"):].strip()
                if data_str in ("", "[DONE]"):
                    continue
                try:
                    evt = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                # StepFun ASR SSE 事件结构（兼容性容错）：
                #   优先字段：text / transcription.text / result.text / delta.text / data.text
                text = (
                    evt.get("text")
                    or evt.get("transcription", {}).get("text") if isinstance(evt.get("transcription"), dict) else None
                ) or _deep_pick_text(evt)

                if not text:
                    continue
                # 有些实现每帧给"已转录全部内容"，有些给增量；都 hold 住，最终
                # 取"出现过的最长文本 OR 拼接增量"。
                if text.startswith(last_full) or last_full == "":
                    last_full = text
                else:
                    pieces.append(text)

    final = last_full if last_full else "".join(pieces)
    return final.strip()


def _deep_pick_text(node) -> str | None:
    """从未知层级的 SSE event JSON 里捞出疑似 transcript 文本字段。"""
    if isinstance(node, dict):
        for key in ("text", "transcription_text", "transcript", "content"):
            v = node.get(key)
            if isinstance(v, str) and v:
                return v
        for v in node.values():
            r = _deep_pick_text(v)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = _deep_pick_text(v)
            if r:
                return r
    return None


def transcribe_video(video_path: Path) -> str:
    """端到端：mp4 → ASR transcript 文本。会清理临时 PCM 文件。"""
    pcm = extract_pcm(video_path)
    try:
        return transcribe_pcm(pcm)
    finally:
        pcm.unlink(missing_ok=True)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python scripts/asr_client.py /path/to/video.mp4")
        sys.exit(1)
    text = transcribe_video(Path(sys.argv[1]).resolve())
    print("=== Transcript ===")
    print(text)
