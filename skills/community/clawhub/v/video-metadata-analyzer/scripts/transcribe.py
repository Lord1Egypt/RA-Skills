#!/usr/bin/env python3
"""
transcribe.py — 视频音频转写（四种模式）

用法：
  # 本地 Whisper
  python3 transcribe.py --video input.mp4 --output obs_audio.json --mode local [--whisper-model base]

  # 云端 Whisper API（OpenAI 兼容）
  python3 transcribe.py --video input.mp4 --output obs_audio.json --mode cloud \
    --whisper-api-key KEY --whisper-api-base URL [--whisper-api-model whisper-1]

  # audio-llm：通过 chat completions API 发送音频给支持 audio 的多模态 LLM
  python3 transcribe.py --video input.mp4 --output obs_audio.json --mode audio-llm \
    --audio-llm-key KEY --audio-llm-base URL --audio-llm-model MODEL

  # agent-direct：仅提取音频，由 Agent 自己 read
  python3 transcribe.py --video input.mp4 --output obs_audio.json --mode agent-direct
"""

import sys
import os
import json
import base64
import re
import argparse
import subprocess
import tempfile
import shutil
import urllib.request
import mimetypes

# 公共工具
from common import http_request_with_retry, get_media_duration, parse_json_from_llm, extract_llm_content


# ── 音频工具 ──

def extract_audio(video_path: str, audio_path: str) -> bool:
    """从视频中提取音频，根据扩展名自动选择格式。
    .wav → 16kHz mono PCM (agent-direct 模式用)
    .mp3 → 64kbps mono (API 模式用，体积更小)
    """
    print(f"Extracting audio from {video_path}...")
    ext = os.path.splitext(audio_path)[1].lstrip(".").lower()
    if ext == "mp3":
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn",
               "-acodec", "libmp3lame", "-b:a", "64k",
               "-ar", "16000", "-ac", "1", audio_path]
    else:
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn",
               "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Audio extraction failed: {result.stderr}", file=sys.stderr)
        return False
    print(f"Audio extracted: {audio_path} ({os.path.getsize(audio_path)/1024:.0f}KB)")
    return True


def compress_audio(audio_path: str, output_path: str, bitrate: str = "128k") -> bool:
    """将音频压缩为 MP3"""
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", audio_path, "-vn", "-acodec", "libmp3lame", "-b:a", bitrate, output_path],
        capture_output=True, text=True
    )
    return result.returncode == 0 and os.path.exists(output_path)


def split_audio(audio_path: str, output_dir: str, chunk_seconds: int = 60, overlap_seconds: int = 2) -> list:
    """将音频按 chunk_seconds 分片，每片之间 overlap_seconds 秒重叠，返回分片文件路径列表"""
    duration = get_media_duration(audio_path)

    chunks = []
    start = 0.0
    idx = 0
    while start < duration:
        chunk_path = os.path.join(output_dir, f"chunk_{idx:03d}.mp3")
        # 每片长度 = chunk_seconds，但最后一片自然截断
        cmd = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ss", str(start), "-t", str(chunk_seconds),
            "-vn", "-acodec", "libmp3lame", "-b:a", "128k", chunk_path
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)
        idx += 1
        start += chunk_seconds - overlap_seconds
        if start >= duration:
            break

    print(f"Split audio into {len(chunks)} chunks ({chunk_seconds}s each, {overlap_seconds}s overlap)")
    return chunks


def get_audio_duration(audio_path: str) -> float:
    return get_media_duration(audio_path)


def merge_transcripts(transcripts: list, overlap_seconds: int = 2) -> str:
    """合并多个分片转写结果，去除重叠部分的重复文字"""
    if len(transcripts) <= 1:
        return transcripts[0] if transcripts else ""

    merged = transcripts[0]
    for i in range(1, len(transcripts)):
        prev_tail = merged[-200:] if len(merged) > 200 else merged
        curr = transcripts[i]
        # 尝试找到重叠：在当前片段开头寻找上一片段尾部的一些文字
        best_overlap = 0
        for window in range(min(50, len(curr)), 5, -1):
            needle = prev_tail[-window:]
            pos = curr.find(needle)
            if pos >= 0:
                best_overlap = pos + window
                break
        if best_overlap > 0:
            merged += curr[best_overlap:]
        else:
            merged += " " + curr
    return merged.strip()


# ── 转写模式 ──

def transcribe_local(audio_path: str, model_name: str = "base") -> str:
    """本地 Whisper 转写"""
    try:
        import whisper
    except ImportError:
        print("ERROR: openai-whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)
    print("Transcribing...")
    result = model.transcribe(audio_path)
    text = result["text"].strip()
    print(f"Transcription complete ({len(text)} chars)")
    return text


def transcribe_cloud(audio_path: str, api_key: str, api_base: str, model: str = "whisper-1") -> str:
    """云端 Whisper API 转写（/audio/transcriptions，带重试）。大文件自动压缩+分片。"""

    MAX_FILE_BYTES = 25 * 1024 * 1024  # Whisper API 文件限制 25MB

    audio_send_path = audio_path
    audio_size = os.path.getsize(audio_path)
    ext = os.path.splitext(audio_path)[1].lstrip(".").lower()

    # Step 1: WAV 超过阈值才压缩（已经是 MP3 就跳过）
    if ext != "mp3" and audio_size > MAX_FILE_BYTES:
        mp3_path = audio_path.replace(".wav", "_compressed.mp3")
        if compress_audio(audio_path, mp3_path, bitrate="128k"):
            audio_send_path = mp3_path
            print(f"Compressed for Whisper: {audio_size/1024/1024:.1f}MB → {os.path.getsize(mp3_path)/1024/1024:.1f}MB MP3")
        else:
            print(f"WARNING: Compression failed, attempting original file")

    # Step 2: 压缩后仍超限则分片
    send_size = os.path.getsize(audio_send_path)
    if send_size > MAX_FILE_BYTES:
        print(f"Still too large ({send_size/1024/1024:.1f}MB), splitting...")
        chunk_dir = tempfile.mkdtemp(prefix="va-whisper-chunks-")
        duration = get_audio_duration(audio_send_path)
        chunk_duration = max(30, int(duration / (send_size / MAX_FILE_BYTES) + 1))
        chunks = split_audio(audio_send_path, chunk_dir, chunk_seconds=chunk_duration, overlap_seconds=2)

        chunk_transcripts = []
        for i, chunk_path in enumerate(chunks):
            print(f"  Whisper chunk {i+1}/{len(chunks)} ({os.path.getsize(chunk_path)/1024:.0f}KB)...")
            chunk_transcripts.append(_call_whisper_single(chunk_path, api_key, api_base, model))

        text = merge_transcripts(chunk_transcripts, overlap_seconds=2)
        print(f"Merged {len(chunks)} Whisper chunks → {len(text)} chars")

        shutil.rmtree(chunk_dir, ignore_errors=True)
        return text

    # 直接发送
    return _call_whisper_single(audio_send_path, api_key, api_base, model)


def _call_whisper_single(audio_path: str, api_key: str, api_base: str, model: str) -> str:
    """发送单个文件给 Whisper API（带重试）"""

    url = f"{api_base.rstrip('/')}/audio/transcriptions"
    filename = os.path.basename(audio_path)

    boundary = "----PythonBoundary123456"
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {mimetypes.guess_type(audio_path)[0] or 'audio/wav'}\r\n\r\n"
    ).encode() + audio_data + (
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="model"\r\n\r\n{model}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="response_format"\r\n\r\njson\r\n'
        f"--{boundary}--\r\n"
    ).encode()

    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Authorization": f"Bearer {api_key}"}
    )
    print(f"Calling cloud Whisper API ({os.path.getsize(audio_path)/1024:.0f}KB)...")
    resp_data = http_request_with_retry(req, timeout=300, label="Cloud Whisper")
    result = json.loads(resp_data.decode())
    text = result.get("text", "").strip()
    print(f"Chunk complete ({len(text)} chars)")
    return text


def transcribe_audio_llm(audio_path: str, api_key: str, api_base: str, model: str) -> dict:
    """通过 chat completions API 发送音频给支持 audio input 的多模态 LLM，返回结构化观测 dict。
    策略：先压缩 → 判断大小 → 超限则分片 → 并行/串行转写 → 拼接去重"""

    MAX_PAYLOAD_KB = 10 * 1024  # 10MB base64 安全线

    # Step 1: 如果已经是 MP3 就跳过压缩
    ext = os.path.splitext(audio_path)[1].lstrip(".").lower()
    audio_send_path = audio_path
    audio_size = os.path.getsize(audio_path)

    if ext != "mp3" and audio_size > 512 * 1024:  # WAV 且 > 512KB 才压缩
        mp3_path = audio_path.replace(f".{ext}", "_compressed.mp3")
        if compress_audio(audio_path, mp3_path):
            audio_send_path = mp3_path
            ext = "mp3"
            print(f"Compressed: {audio_size/1024:.0f}KB → {os.path.getsize(mp3_path)/1024:.0f}KB MP3")
        else:
            print(f"WARNING: Compression failed, using original ({audio_size/1024:.0f}KB)")

    # Step 2: 检查是否需要分片
    send_size = os.path.getsize(audio_send_path)
    b64_estimate = send_size * 4 / 3  # base64 膨胀约 33%

    if b64_estimate > MAX_PAYLOAD_KB * 1024:  # KB → bytes
        # 需要分片
        print(f"Audio too large ({send_size/1024:.0f}KB, base64 ≈ {b64_estimate/1024:.0f}KB), splitting...")
        chunk_dir = tempfile.mkdtemp(prefix="va-chunks-")
        duration = get_audio_duration(audio_send_path)
        # 估算每片多大才能控制在安全线内
        chunk_duration = max(30, int(duration / (b64_estimate / (MAX_PAYLOAD_KB * 1024)) + 1))
        chunks = split_audio(audio_send_path, chunk_dir, chunk_seconds=chunk_duration, overlap_seconds=2)

        # 逐片转写
        chunk_transcripts = []
        for i, chunk_path in enumerate(chunks):
            print(f"  Transcribing chunk {i+1}/{len(chunks)} ({os.path.getsize(chunk_path)/1024:.0f}KB)...")
            chunk_obs = _call_audio_llm_single(chunk_path, api_key, api_base, model, "mp3")
            chunk_transcripts.append(chunk_obs.get("transcript", ""))

        # 合并转写
        merged_transcript = merge_transcripts(chunk_transcripts, overlap_seconds=2)
        print(f"Merged {len(chunks)} chunks → {len(merged_transcript)} chars")

        # 清理分片
        shutil.rmtree(chunk_dir, ignore_errors=True)

        # 从合并后的文本提取结构化信息（用同模型再做一次提取）
        obs = _extract_structured_from_text(merged_transcript, api_key, api_base, model)
        return obs
    else:
        # 直接发送
        return _call_audio_llm_single(audio_send_path, api_key, api_base, model, ext)


def _call_audio_llm_single(audio_path: str, api_key: str, api_base: str, model: str, fmt: str) -> dict:
    """发送单个音频文件给 LLM，返回结构化观测 dict（带重试）"""

    with open(audio_path, "rb") as f:
        audio_data = f.read()
    b64_audio = base64.b64encode(audio_data).decode()
    print(f"Audio payload: {len(audio_data)/1024:.1f}KB, base64: {len(b64_audio)/1024:.1f}KB")

    audio_prompt = """## 任务
将这段音频完整转写为文字，并提取结构化信息。

注意：如果音频中没有可辨识的人声（例如只有背景音乐或音效），你仍然必须：
1) 在 transcript 字段中写出简短说明（例如："（无语音内容，仅包含背景音乐和游戏音效）"）；
2) 在 key_points 中提供至少 3 条针对音频特征的关键信息点（例如：背景音乐、点击音、胜利提示音等）。

## 输出格式
严格输出一个 JSON 对象，不要包含任何其他文字或解释。字段说明：

| 字段 | 类型 | 说明 |
|------|------|------|
| transcript | string | 完整的语音转写文本（使用音频的实际语言，保留原始断句，不要省略任何内容）。若无语音则写简短说明。 |
| speakers | string[] | 说话人识别（如能辨别多说话人则列出，否则为 ["旁白"] 或 ["主讲"]）。若无语音可写空数组。 |
| key_points | string[] | 从语音中提取的关键信息点（至少 3 条，最多 8 条，每条一个完整短句）。若无语音则描述音频特征（背景音乐/音效/点击/提示声等）。 |
| tone | string | 语气风格（平稳/激动/正式/随意/幽默等）。若无语音可写 "无语音（纯音效/音乐）" 或空字符串。 |

## 示例
{"transcript":"大家好，这是一个测试。","speakers":["旁白"],"key_points":["这是一个测试视频","用于验证转写功能"],"tone":"平稳"}"""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": audio_prompt},
            {"type": "input_audio", "input_audio": {"data": b64_audio, "format": fmt}}
        ]}],
        "max_tokens": 4000
    }

    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    )
    print(f"Calling audio LLM ({model})...")
    resp_data = http_request_with_retry(req, timeout=300, label=f"Audio LLM ({model})")
    content = extract_llm_content(resp_data, label=f"Audio LLM ({model})").strip()

    # ── 多轮 JSON 解析：严格重试 + 宽松重试 + 退化 ──
    obs = None
    max_parse_attempts = 3
    for attempt in range(max_parse_attempts):
        obs = parse_json_from_llm(content, expect_array=False)
        if isinstance(obs, dict) and 'transcript' in obs and 'key_points' in obs:
            print(f"Audio-LLM JSON parsed OK on attempt {attempt+1}")
            break
        # parse_json_from_llm 没拿到，尝试裸解析
        if obs is None:
            try:
                obs = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                pass
        if not isinstance(obs, dict) or 'transcript' not in obs:
            print(f"WARNING: Parse attempt {attempt+1}/{max_parse_attempts} failed")
            if attempt < max_parse_attempts - 1:
                # 重试：告诉模型上次输出哪里错了
                retry_prompt = f"你的上一次输出不是合法 JSON，解析失败。\n错误: output was not a valid JSON object with 'transcript' and 'key_points' fields\n上一次输出（前500字）: {content[:500]}\n\n请重新输出，严格要求：只输出一个 JSON 对象，不要包含任何 markdown 标记、解释或额外文字。"
                retry_payload = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": [
                            {"type": "text", "text": audio_prompt},
                            {"type": "input_audio", "input_audio": {"data": b64_audio, "format": fmt}}
                        ]},
                        {"role": "assistant", "content": content},
                        {"role": "user", "content": retry_prompt}
                    ],
                    "max_tokens": 4000
                }
                retry_req = urllib.request.Request(
                    f"{api_base.rstrip('/')}/chat/completions",
                    data=json.dumps(retry_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
                )
                print(f"  Retrying with error feedback (attempt {attempt+2})...")
                try:
                    retry_resp = http_request_with_retry(retry_req, timeout=300, label=f"Audio LLM retry {attempt+2}")
                    content = extract_llm_content(retry_resp, label=f"Audio LLM retry {attempt+2}").strip()
                except Exception as retry_err:
                    print(f"  Retry request failed: {retry_err}")
                    continue
            else:
                # 最后一次仍失败，退化到纯文本
                print(f"WARNING: All {max_parse_attempts} parse attempts failed. Falling back to raw text.")
                obs = {"transcript": content, "speakers": [], "key_points": [], "tone": ""}

    if obs is None:
        obs = {"transcript": content, "speakers": [], "key_points": [], "tone": ""}

    print(f"Audio-LLM complete (transcript {len(obs.get('transcript',''))} chars, {len(obs.get('key_points',[]))} key points)")
    return obs


def _extract_structured_from_text(text: str, api_key: str, api_base: str, model: str) -> dict:
    """从已合并的纯文本中提取结构化信息（分片转写后调用）"""

    if not text.strip():
        return {"transcript": "", "speakers": [], "key_points": [], "tone": ""}

    extract_prompt = f"""## 任务\n下面是一段完整的音频转写文本（由多个片段合并而来）。请从中提取结构化信息。\n\n## 转写文本\n{text[:8000]}\n\n## 输出格式\n严格输出一个 JSON 对象，字段：\n- transcript: 完整转写文本（直接复制上面的文本）\n- speakers: string[] 说话人识别\n- key_points: string[] 关键信息点（3-8条）\n- tone: string 语气风格\n\n只输出 JSON，不要其他文字。"""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": extract_prompt}],
        "max_tokens": 4000
    }

    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    )
    print(f"Extracting structured info from merged transcript...")
    resp_data = http_request_with_retry(req, timeout=120, label="Audio structure extraction")
    content = extract_llm_content(resp_data, label="Audio structure extraction").strip()

    # 多轮解析重试
    for attempt in range(3):
        obs = parse_json_from_llm(content, expect_array=False)
        if isinstance(obs, dict):
            obs["transcript"] = text  # 确保使用原始完整文本
            return obs
        if obs is None:
            try:
                obs = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                pass
        if not isinstance(obs, dict):
            if attempt < 2:
                print(f"  Extract parse attempt {attempt+1} failed, retrying...")
                retry_msg = f"上一次输出不是合法 JSON。请重新输出，只输出 JSON 对象，不要其他文字。"
                retry_payload = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": extract_prompt},
                        {"role": "assistant", "content": content},
                        {"role": "user", "content": retry_msg}
                    ],
                    "max_tokens": 4000
                }
                retry_req = urllib.request.Request(
                    f"{api_base.rstrip('/')}/chat/completions",
                    data=json.dumps(retry_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
                )
                try:
                    retry_resp = http_request_with_retry(retry_req, timeout=120, label=f"Extract retry {attempt+2}")
                    content = extract_llm_content(retry_resp, label=f"Extract retry {attempt+2}").strip()
                except Exception:
                    continue
            else:
                print(f"WARNING: All extract parse attempts failed. Falling back to raw text.")
    return {"transcript": text, "speakers": [], "key_points": [], "tone": ""}


# ── 主流程 ──

def main():
    parser = argparse.ArgumentParser(description="Video audio transcription")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", required=True, help="Output file path (observations_audio.json)")
    parser.add_argument("--mode",
                        choices=["local", "cloud", "agent-direct", "audio-llm"],
                        required=True,
                        help="Transcription mode (required)")
    # Local whisper
    parser.add_argument("--whisper-model", default="base",
                        help="Local Whisper model: tiny/base/small/medium/large (default: base)")
    # Cloud whisper
    parser.add_argument("--whisper-api-key", default=None, help="API key for cloud Whisper")
    parser.add_argument("--whisper-api-base", default=None, help="API base URL for cloud Whisper")
    parser.add_argument("--whisper-api-model", default="whisper-1", help="Cloud Whisper model name (default: whisper-1)")
    # Audio LLM
    parser.add_argument("--audio-llm-key", default=None, help="API key for audio LLM")
    parser.add_argument("--audio-llm-base", default=None, help="API base URL for audio LLM")
    parser.add_argument("--audio-llm-model", default=None, help="Audio LLM model (must support audio input)")
    args = parser.parse_args()

    # --- agent-direct: extract only ---
    if args.mode == "agent-direct":
        print("Agent-direct mode: extracting audio only (agent will read the file)")
        audio_output = os.path.join(os.path.dirname(args.output) or ".", "transcript.wav")
        if extract_audio(args.video, audio_output):
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump({"transcript": "", "audio_file": audio_output, "speakers": [], "key_points": [], "tone": ""}, f, ensure_ascii=False, indent=2)
            print(f"Audio extracted to: {audio_output}")
        else:
            print("Audio extraction failed")
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump({"transcript": "", "speakers": [], "key_points": [], "tone": ""}, f, ensure_ascii=False, indent=2)
        return

    # --- all other modes need the video file ---
    if not os.path.exists(args.video):
        print(f"ERROR: Video not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    tmp_dir = tempfile.mkdtemp(prefix="va-transcribe-")

    # API 模式直接提取 MP3（省掉 WAV→压缩 二次转码），local/agent-direct 用 WAV
    if args.mode in ("cloud", "audio-llm"):
        print(f"⚠️  PRIVACY: Audio will be sent to external endpoint ({args.mode} mode)")
        audio_path = os.path.join(tmp_dir, "audio.mp3")
    else:
        audio_path = os.path.join(tmp_dir, "audio.wav")

    if not extract_audio(args.video, audio_path):
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"transcript": "", "speakers": [], "key_points": [], "tone": ""}, f, ensure_ascii=False, indent=2)
        return

    # --- local Whisper ---
    if args.mode == "local":
        text = transcribe_local(audio_path, args.whisper_model)
        obs_audio = {"transcript": text, "speakers": [], "key_points": [], "tone": ""}

    # --- cloud Whisper API ---
    elif args.mode == "cloud":
        if not args.whisper_api_key or not args.whisper_api_base:
            print("ERROR: --whisper-api-key and --whisper-api-base required for cloud mode", file=sys.stderr)
            sys.exit(1)
        text = transcribe_cloud(audio_path, args.whisper_api_key, args.whisper_api_base, args.whisper_api_model)
        obs_audio = {"transcript": text, "speakers": [], "key_points": [], "tone": ""}

    # --- audio-llm ---
    elif args.mode == "audio-llm":
        if not args.audio_llm_key or not args.audio_llm_base or not args.audio_llm_model:
            print("ERROR: --audio-llm-key, --audio-llm-base, and --audio-llm-model required for audio-llm mode", file=sys.stderr)
            sys.exit(1)
        obs_audio = transcribe_audio_llm(audio_path, args.audio_llm_key, args.audio_llm_base, args.audio_llm_model)

    else:
        obs_audio = {"transcript": "", "speakers": [], "key_points": [], "tone": ""}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(obs_audio, f, ensure_ascii=False, indent=2)
    print(f"Observations (audio) saved to {args.output}")

    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
