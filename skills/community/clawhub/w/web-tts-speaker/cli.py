#!/usr/bin/env python3
"""
Web TTS Speaker v3.0
=====================
网页→文字→生成语音 → 多渠道自动匹配推送

核心思路：CLI 生成所有渠道格式，Agent 根据请求来源自动取用。
不调飞书/微信 API，不复杂。Agent 负责发送，脚本只做三件事：
提取文字 → 生成语音 → 输出标准化标记

用法：
  # 自动模式（推荐）：生成全部格式，Agent 按来源渠道自动发
  python cli.py --url https://example.com/article
  python cli.py --text "你好世界"

  # 指定渠道（单发）
  python cli.py --channel feishu --text "你好"
  python cli.py --channel wechat --text "你好"

输出标记：Agent 读取标记 → 根据消息来源渠道选择对应文件发送

支持渠道：
  feishu      → .opus 语音气泡
  wechat      → .mp3  文件消息
  telegram    → .mp3  文件消息  (保留)
  whatsapp    → .mp3  文件消息  (保留)
  default     → .mp3  文件消息
"""

import asyncio, re, sys, os, subprocess, tempfile, shutil
from datetime import datetime
from pathlib import Path

# FFmpeg 路径
FFMPEG = r"D:\Programs\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

# Edge TTS 单块安全上限（中文约3000字符，留余量）
CHUNK_SIZE = 2800
# 句子分割正则（中文标点 + 英文句号）
RE_SENTENCE = re.compile(r"(?<=[。！？；\n])|(?<=[.])(?=\s|$)")


# ── 渠道配置 ──────────────────────────────────────────────────────────────
# 格式： {格式名: (扩展名, ffmpeg编解码器, 编码参数列表, 备注)}
CHANNEL_CONFIG = {
    "feishu": {
        "ext": ".opus",
        "codec": "libopus",
        "params": ["-ac", "1", "-ar", "16000", "-b:a", "12k"],
        "tag": "FEISHU_VOICE",
        "note": "飞书语音气泡",
    },
    "wechat": {
        "ext": ".mp3",
        "codec": "libmp3lame",
        "params": ["-ac", "1", "-ar", "24000", "-b:a", "48k"],
        "tag": "WECHAT_VOICE",
        "note": "微信文件消息",
    },
    "telegram": {
        "ext": ".mp3",
        "codec": "libmp3lame",
        "params": ["-ac", "1", "-ar", "24000", "-b:a", "48k"],
        "tag": "TELEGRAM_VOICE",
        "note": "Telegram 文件消息",
    },
    "discord": {
        "ext": ".mp3",
        "codec": "libmp3lame",
        "params": ["-ac", "1", "-ar", "24000", "-b:a", "48k"],
        "tag": "DISCORD_VOICE",
        "note": "Discord 文件消息",
    },
}


AVAILABLE_CHANNELS = list(CHANNEL_CONFIG.keys())


def extract_web_text(url):
    """提取网页正文"""
    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=15, headers=headers)
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 15]
    return "\n".join(lines)


def split_text(text, max_chars=CHUNK_SIZE):
    """按句子分块，每块 ≤ max_chars 字符"""
    raw_sentences = RE_SENTENCE.split(text)
    sentences = [s.strip() for s in raw_sentences if s.strip()]

    chunks = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) + 1 > max_chars:
            if current:
                chunks.append(current.strip())
            current = sent
        else:
            current += ("。" if current and not current.endswith("。") else "") + sent

    if current:
        chunks.append(current.strip())

    return chunks


def generate_chunk(text, temp_wav, voice):
    """Edge TTS 生成单块语音"""
    import edge_tts

    async def _gen():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_wav)

    asyncio.run(_gen())


def get_duration(audio_path):
    """用 ffprobe 获取音频时长（秒）"""
    try:
        result = subprocess.run(
            [
                FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"),
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path,
            ],
            capture_output=True, text=True, timeout=10,
        )
        return round(float(result.stdout.strip()))
    except Exception:
        return 0


def generate_voice_auto(text, out_dir, base_name, voice):
    """
    生成所有渠道格式，返回 {渠道名: {file, dur, tag, size}} 字典
    """
    # 1. 分块后合成一份合并 WAV
    chunks = split_text(text)
    merged_wav = _synthesize_wav(chunks, out_dir, voice)
    print(f"   ✅ 合成完成")

    # 2. 转码为各渠道格式
    results = {}
    for ch, cfg in CHANNEL_CONFIG.items():
        out_path = os.path.join(out_dir, f"{base_name}{cfg['ext']}")
        cmd = [
            FFMPEG, "-y", "-i", merged_wav,
            "-acodec", cfg["codec"],
            *cfg["params"],
            out_path,
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        dur = get_duration(out_path)
        size = os.path.getsize(out_path)
        results[ch] = {
            "file": out_path,
            "tag": cfg["tag"],
            "dur": dur,
            "size": size,
            "full": cfg["note"],
        }
        print(f"   📁 {ch}: {os.path.basename(out_path)} ({size/1024:.0f}KB, {fmt_duration(dur)})")

    # 清理合并 WAV
    os.remove(merged_wav)
    return results


def generate_voice_single(text, out_path, voice, channel):
    """
    生成单渠道格式
    """
    chunks = split_text(text)
    merged_wav = _synthesize_wav(chunks, os.path.dirname(out_path) or ".", voice)
    cfg = CHANNEL_CONFIG[channel]
    cmd = [
        FFMPEG, "-y", "-i", merged_wav,
        "-acodec", cfg["codec"],
        *cfg["params"],
        out_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    os.remove(merged_wav)
    return get_duration(out_path)


def _synthesize_wav(chunks, out_dir, voice):
    """分块合成并拼接为一份临时 WAV"""
    temp_dir = tempfile.mkdtemp(prefix="tts_")
    temp_files = []
    chunk_count = len(chunks)
    print(f"   分块生成：{chunk_count} 块")

    try:
        for i, chunk in enumerate(chunks, 1):
            wav_path = os.path.join(temp_dir, f"chunk_{i:04d}.wav")
            print(f"   [{i}/{chunk_count}] 生成语音 ({len(chunk)} 字符)...", end="")
            generate_chunk(chunk, wav_path, voice)
            dur = get_duration(wav_path)
            print(f" {fmt_duration(dur)}")
            temp_files.append(wav_path)

        # 拼接
        concat_list = os.path.join(temp_dir, "concat.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for wav_path in temp_files:
                f.write(f"file '{wav_path}'\n")

        merged_wav = os.path.join(out_dir, f"_merged_{os.getpid()}.wav")
        subprocess.run(
            [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", merged_wav],
            capture_output=True, text=True, check=True,
        )
        return merged_wav

    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def fmt_duration(seconds):
    if seconds >= 60:
        return f"{seconds//60}分{seconds%60}秒"
    return f"{seconds}秒"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Web TTS Speaker - 网页转语音，自动匹配来源渠道"
    )
    parser.add_argument(
        "--channel", "-c",
        default="auto",
        choices=["auto"] + AVAILABLE_CHANNELS,
        help="渠道：auto（全部生成）/ feishu / wechat / telegram / discord（默认 auto）",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="网页 URL")
    group.add_argument("--text", help="直接文本")
    parser.add_argument("--output", "-o", help="输出文件（单渠道模式）")
    parser.add_argument(
        "--voice",
        default="zh-CN-XiaoxiaoNeural",
        help="Edge TTS 语音（默认 zh-CN-XiaoxiaoNeural）",
    )
    parser.add_argument(
        "--outdir", "-d",
        default=os.getcwd(),
        help="输出目录（默认当前目录）",
    )
    args = parser.parse_args()

    # ── 1. 获取文本 ──
    if args.url:
        print(f"\U0001f4d6 读取网页：{args.url}")
        text = extract_web_text(args.url)
        print(f"   提取 {len(text)} 字符")
    else:
        text = args.text

    if not text:
        print("❌ 无内容")
        sys.exit(1)

    print(f"   \U0001f3a4 语音：{args.voice}")
    print(f"   文本长度：{len(text)} 字符")

    # ── 2. 生成语音 ──
    out_dir = os.path.abspath(args.outdir)
    os.makedirs(out_dir, exist_ok=True)
    base_name = datetime.now().strftime("voice_%H%M%S")

    if args.channel == "auto":
        # ── 自动模式：生成全部渠道 ──
        print(f"\U0001f3b5 自动模式：生成所有格式 ↓")
        results = generate_voice_auto(text, out_dir, base_name, args.voice)

        # 输出全部标记，Agent 根据来源渠道自行选择
        print(f"\n--- 以下标记供 Agent/Cron 读取 ---")
        for ch, info in results.items():
            snippet = text[:50].replace("\n", " ").strip()
            print(f"[{info['tag']}]")
            print(f"channel={ch}")
            print(f"file={info['file']}")
            print(f"text={snippet}...")
            print(f"dur={info['dur']}")
            print(f"size={info['size']}")
            print(f"full={info['full']}")
            print(f"[/{info['tag']}]")
            print()

    else:
        # ── 单渠道模式 ──
        ext = CHANNEL_CONFIG[args.channel]["ext"]
        output = args.output or f"{base_name}{ext}"
        if not os.path.isabs(output):
            output = os.path.join(out_dir, output)

        print(f"\U0001f3a4 生成语音（{args.channel}）：{os.path.basename(output)}")
        dur = generate_voice_single(text, output, args.voice, args.channel)

        size = os.path.getsize(output)
        print(f"✅ 完成！({size/1024:.0f}KB, {fmt_duration(dur)})")

        # 输出标记
        tag = CHANNEL_CONFIG[args.channel]["tag"]
        abs_path = os.path.abspath(output)
        snippet = text[:60].replace("\n", " ").strip()
        print(f"\n--- 以下标记供 Agent/Cron 读取 ---")
        print(f"[{tag}]")
        print(f"channel={args.channel}")
        print(f"file={abs_path}")
        print(f"text={snippet}...")
        print(f"dur={dur}")
        print(f"size={size}")
        print(f"[/{tag}]")


if __name__ == "__main__":
    main()
