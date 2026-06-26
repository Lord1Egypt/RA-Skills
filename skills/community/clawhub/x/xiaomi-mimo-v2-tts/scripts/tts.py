#!/usr/bin/env python3
"""
小米 MiMo V2 TTS 语音合成脚本
用法: python3 tts.py --text "要合成的文字" --output audio.wav
"""

import argparse
import base64
import json
import os
import sys
import wave
import tempfile
import subprocess
import time

import requests

# ============ 配置 ============
SAMPLE_RATE = 24000
BASE_URL = "https://api.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2-tts"
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

# 风格标签支持的类别（用于验证）
# 风格列表（支持中文和英文，API 两种都认）
VALID_STYLES = [
    # 情绪变化
    "Happy", "Sad", "Angry", "Surprised", "Fearful", "Disgusted", "Calm",
    "开心", "悲伤", "生气", "惊讶", "恐惧", "厌恶", "平静",
    # 语速控制
    "Speed up", "Slow down", "变快", "变慢",
    # 角色扮演
    "Sun Wukong", "Lin Daiyu", "Zhang Fei", "Guan Yu", "Zhuge Liang",
    "孙悟空", "林黛玉", "张飞", "关羽", "诸葛亮",
    # 风格变化
    "Whisper", "Clamped voice", "Taiwanese accent", "Narration", "Storytelling",
    "悄悄话", "夹子音", "台湾腔", "叙事", "讲故事",
    # 方言
    "Northeastern dialect", "Sichuan dialect", "Cantonese", "Henan dialect",
    "东北话", "四川话", "粤语", "河南话",
    # 其他
    "唱歌",
]

# 音色列表
VOICES = {
    "default": "mimo_default",
    "zh": "default_zh",
    "en": "default_en",
}


def _load_api_key() -> str:
    """从环境变量或 openclaw.json 读取 API Key"""
    # 优先环境变量
    key = os.environ.get("MIMO_API_KEY", "")
    if key:
        return key
    # 从 openclaw.json 读取
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        # 尝试从 skills.entries 中读取
        entries = config.get("skills", {}).get("entries", {})
        # 兼容旧配置名称
        for key in ["Xiaomi-MiMo-V2-TTS"]:
            if key in entries:
                env = entries[key].get("env", {})
                if "MIMO_API_KEY" in env:
                    return env["MIMO_API_KEY"]
        # 兼容旧配置
        return config.get("tools", {}).get("mimoTts", {}).get("apiKey", "")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ""


API_KEY = _load_api_key()


def check_prerequisites():
    """检查前置条件：API Key、ffmpeg"""
    if not API_KEY:
        print("❌ 未设置 MIMO_API_KEY", file=sys.stderr)
        print("   设置方法: export MIMO_API_KEY='your-api-key'", file=sys.stderr)
        print("   或在 openclaw.json 中配置 skills.entries.Xiaomi-MiMo-V2-TTS.env.MIMO_API_KEY", file=sys.stderr)
        sys.exit(1)

    # 检查 ffmpeg 是否可用
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  ffmpeg 未安装，opus 格式将不可用", file=sys.stderr)
        print("   安装方法: apt install ffmpeg / brew install ffmpeg", file=sys.stderr)
        return False
    return True


def synthesize(text: str, voice: str = "mimo_default", style: str = None,
               audio_format: str = "wav", user_text: str = None) -> bytes:
    """调用 MiMo TTS API 合成语音（带重试）"""

    # 构建 assistant 消息（合成文本）
    assistant_content = text
    if style:
        assistant_content = f"<style>{style}</style>{text}"

    messages = []

    # 可选的 user 消息（提供上下文）
    if user_text:
        messages.append({"role": "user", "content": user_text})

    # assistant 消息包含要合成的文字
    messages.append({"role": "assistant", "content": assistant_content})

    payload = {
        "model": MODEL,
        "messages": messages,
        "audio": {
            "format": audio_format,
            "voice": voice,
        }
    }

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json",
    }

    # 重试机制
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()

            data = resp.json()

            # 提取音频数据
            if "choices" not in data or not data["choices"]:
                raise ValueError(f"API 返回异常: {json.dumps(data, ensure_ascii=False)}")

            message = data["choices"][0].get("message", {})
            audio_data = message.get("audio", {})

            if not audio_data or "data" not in audio_data:
                raise ValueError(f"未获取到音频数据: {json.dumps(data, ensure_ascii=False)}")

            audio_bytes = base64.b64decode(audio_data["data"])
            return audio_bytes

        except (requests.exceptions.RequestException, ValueError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                print(f"⚠️  第 {attempt} 次合成失败，{RETRY_DELAY} 秒后重试... ({e})", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                print(f"❌ 合成失败（已重试 {MAX_RETRIES} 次）: {e}", file=sys.stderr)
                sys.exit(1)


def save_wav(audio_bytes: bytes, output_path: str):
    """保存为 WAV 文件（24kHz, 16bit, mono）"""
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16bit = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_bytes)


def convert_to_opus(wav_path: str, opus_path: str):
    """用 ffmpeg 将 WAV 转为 OPUS 格式（飞书语音消息格式）"""
    result = subprocess.run(
        ["ffmpeg", "-i", wav_path, "-acodec", "libopus", "-ac", "1", "-ar", "16000", opus_path, "-y"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"❌ ffmpeg 转换失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def process_single(text: str, output: str, voice: str, style: str,
                   audio_format: str, user_text: str = None) -> dict:
    """合成单条语音，返回结果信息"""
    tmp_wav = None
    try:
        # opus 格式需要先请求 wav 再本地转换
        api_format = "wav" if audio_format == "opus" else audio_format

        print(f"🎙️ 正在合成: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
        if style:
            print(f"   风格: {style}")
        print(f"   音色: {voice}")

        audio_bytes = synthesize(
            text=text,
            voice=voice,
            style=style,
            audio_format=api_format,
            user_text=user_text,
        )

        # 保存文件
        if audio_format == "opus":
            tmp_wav = tempfile.mktemp(suffix=".wav")
            save_wav(audio_bytes, tmp_wav)
            convert_to_opus(tmp_wav, output)
        elif audio_format == "wav":
            save_wav(audio_bytes, output)
        else:
            # PCM16 直接写入
            with open(output, "wb") as f:
                f.write(audio_bytes)

        size_kb = os.path.getsize(output) / 1024
        duration = len(audio_bytes) / (SAMPLE_RATE * 2)

        return {
            "status": "success",
            "file": output,
            "size_kb": round(size_kb, 1),
            "duration_sec": round(duration, 1),
            "voice": voice,
            "style": style,
            "text": text,
        }

    finally:
        # 确保清理临时文件
        if tmp_wav and os.path.exists(tmp_wav):
            os.unlink(tmp_wav)


def process_batch(input_file: str, output_dir: str, voice: str, style: str,
                  audio_format: str, user_text: str = None):
    """批量合成语音"""
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not lines:
        print("❌ 输入文件为空", file=sys.stderr)
        sys.exit(1)

    ext = "opus" if audio_format == "opus" else ("wav" if audio_format == "wav" else audio_format)
    results = []

    print(f"📦 批量合成: {len(lines)} 条语音\n")

    for i, text in enumerate(lines, 1):
        output_path = os.path.join(output_dir, f"{i:03d}.{ext}")
        print(f"[{i}/{len(lines)}]", end=" ")
        result = process_single(text, output_path, voice, style, audio_format, user_text)
        results.append(result)
        print(f"   ✅ → {output_path} ({result['size_kb']} KB, {result['duration_sec']}s)\n")

    # 输出批量结果汇总
    total_size = sum(r["size_kb"] for r in results)
    total_duration = sum(r["duration_sec"] for r in results)
    print(f"📊 批量合成完成:")
    print(f"   文件数: {len(results)}")
    print(f"   总大小: {total_size:.1f} KB")
    print(f"   总时长: {total_duration:.1f} 秒")
    print(f"   输出目录: {output_dir}")

    return results


def main():
    check_prerequisites()

    parser = argparse.ArgumentParser(
        description="MiMo V2 TTS 语音合成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础合成
  python3 tts.py --text "你好，世界！" --output hello.wav

  # 飞书语音消息
  python3 tts.py --text "你好呀" --format opus --output hello.opus

  # 多风格组合
  python3 tts.py --text "好开心呀" --style "Happy" --style "Sichuan dialect"

  # 批量合成
  python3 tts.py --batch texts.txt --output-dir ./voices --format opus
        """
    )
    parser.add_argument("--text", help="要合成的文字（单条模式）")
    parser.add_argument("--output", default="output.wav", help="输出文件路径（单条模式）")
    parser.add_argument("--batch", help="批量模式：文本文件路径（每行一条）")
    parser.add_argument("--output-dir", default="./voices", help="批量模式：输出目录")
    parser.add_argument("--voice", default="mimo_default",
                        choices=["mimo_default", "default_zh", "default_en"],
                        help="音色")
    parser.add_argument("--style", action="append", default=None,
                        help="语音风格（中文或英文，如：开心、东北话、孙悟空、唱歌等，可多次指定以组合）")
    parser.add_argument("--format", default="wav", choices=["wav", "pcm16", "opus", "mp3"],
                        help="音频格式（mp3 直接可发微信/飞书，opus 专为飞书语音消息设计）")
    parser.add_argument("--user-text", default=None, help="用户侧消息（可选上下文）")

    args = parser.parse_args()

    # 映射音色简写
    voice = VOICES.get(args.voice, args.voice)

    # 处理风格（支持多个）
    style = None
    if args.style:
        if len(args.style) == 1:
            style = args.style[0]
        else:
            # 组合多个风格标签
            style_tags = "".join(f"<style>{s}</style>" for s in args.style)
            style = style_tags

    # 批量模式
    if args.batch:
        results = process_batch(args.batch, args.output_dir, voice, style, args.format, args.user_text)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    # 单条模式
    if not args.text:
        parser.error("请指定 --text（单条模式）或 --batch（批量模式）")

    result = process_single(args.text, args.output, voice, style, args.format, args.user_text)

    print(f"\n✅ 音频已保存: {args.output}")
    print(f"   大小: {result['size_kb']} KB, 时长: {result['duration_sec']} 秒")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
