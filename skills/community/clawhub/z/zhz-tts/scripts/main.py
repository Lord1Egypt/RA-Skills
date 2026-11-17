#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文AI语音合成工具
支持 Edge-TTS（免费）和 DashScope CosyVoice 接口
"""

import argparse
import asyncio
import base64
import os
import sys
from pathlib import Path
import logging

logger = logging.getLogger("TTS_Interaction")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    fh = logging.FileHandler("tts_interaction.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

try:
    import yaml
except ImportError:
    yaml = None


# ─── Edge-TTS 引擎（免费，无需 API Key）────────────────────────────

async def edge_tts_synthesize(text, voice, rate, volume, output_path):
    """使用 edge-tts 合成语音"""
    try:
        import edge_tts
    except ImportError:
        print("错误：需要安装 edge-tts 库", file=sys.stderr)
        print("安装命令：pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(output_path)
    logger.info(f"Edge-TTS 合成完成: voice={voice}, rate={rate}, output={output_path}")


# ─── DashScope CosyVoice 引擎 ─────────────────────────────────────

def dashscope_tts_synthesize(text, model, voice, output_path, api_key=None, base_url=None):
    """使用 DashScope CosyVoice 合成语音"""
    try:
        import requests
    except ImportError:
        print("错误：需要安装 requests 库", file=sys.stderr)
        print("安装命令：pip install requests", file=sys.stderr)
        sys.exit(1)

    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        for p in [
            Path.cwd() / ".dashscope_key",
            Path.home() / ".zhz-skills" / ".dashscope_key",
            Path(r"C:\Users\zhang\.openclaw\workspace") / ".dashscope_key",
        ]:
            if p.exists():
                api_key = p.read_text(encoding="utf-8").strip()
                if api_key:
                    logger.info(f"从密钥文件加载: {p}")
                    break

    if not api_key:
        raise ValueError(
            "DashScope 需要 API 密钥，任选其一：\n"
            "  1. 环境变量: set DASHSCOPE_API_KEY=xxx\n"
            "  2. 密钥文件: .dashscope_key"
        )

    if not base_url:
        base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com")

    url = f"{base_url}/api/v1/services/aigc/text2audio/generation"

    body = {
        "model": model,
        "input": {
            "text": text,
        },
        "parameters": {
            "voice": voice,
            "format": "mp3",
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    logger.info(f"DashScope TTS: model={model}, voice={voice}")
    print(f"正在合成语音（DashScope {model}，音色：{voice}）...")

    try:
        response = requests.post(url, headers=headers, json=body, timeout=120)
    except Exception as e:
        raise RuntimeError(f"网络请求失败：{e}")

    if response.status_code != 200:
        raise RuntimeError(f"API错误（{response.status_code}）：{response.text}")

    result = response.json()
    output = result.get("output", {})
    audio_url = output.get("audio")

    if not audio_url:
        audio_data = output.get("audio_data")
        if audio_data:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(audio_data))
            return
    
    if audio_url.startswith("http://") or audio_url.startswith("https://"):
        try:
            audio_response = requests.get(audio_url, timeout=60)
        except Exception as e:
            raise RuntimeError(f"下载音频失败：{e}")
        if audio_response.status_code != 200:
            raise RuntimeError(f"下载音频失败：{audio_response.status_code}")
        with open(output_path, "wb") as f:
            f.write(audio_response.content)
        return

    raise RuntimeError(f"响应中没有音频数据：{result}")


# ─── 配置加载 ──────────────────────────────────────────────────────

def load_config():
    """加载配置文件"""
    if not yaml:
        return {}
    candidates = [
        Path.cwd() / ".zhz" / "tts" / "config.yaml",
        Path.home() / ".zhz" / "tts" / "config.yaml",
    ]
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    print(f"已加载配置：{path}")
                    return config or {}
            except Exception as e:
                print(f"警告：无法解析配置文件 {path}: {e}")
    return {}


# ─── 命令行解析 ─────────────────────────────────────────────────────

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="zhz-tts",
        description=(
            "zhz-tts — 中英文AI语音合成工具\n"
            "\n"
            "支持两个引擎：\n"
            "  edge       微软 Edge 神经网络 TTS（免费，无需 API Key，默认）\n"
            "  dashscope  阿里云 CosyVoice（需要 DASHSCOPE_API_KEY）\n"
            "\n"
            "适用场景：\n"
            "  - 英文听力练习：英文文本默认以 0.9 倍速朗读，方便跟读和听写\n"
            "  - 中文有声内容：将文章、笔记转为语音文件\n"
            "  - 多语言朗读：支持中、英、日、韩等多种语言和音色"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 英文听力练习（自动 0.9 倍速）
  python main.py -t "The quick brown fox jumps over the lazy dog." -a fox.mp3

  # 朗读英文文章
  python main.py --textfile article.txt -a article.mp3

  # 中文语音
  python main.py -t "你好世界" -a hello.mp3

  # 自定义语速和音色
  python main.py -t "Hello world" -a hello.mp3 -v en-US-JennyNeural -r "-20%"

  # 使用 DashScope CosyVoice
  python main.py -t "你好" -a hello.mp3 -e dashscope -v longxiaochun

  # 列出可用音色
  python main.py --list-voices
  python main.py --list-voices --lang en

  # 从文件批量生成
  python main.py --textfile english_lesson.txt -a lesson.mp3 -r "-15%"
        """
    )

    parser.add_argument("--text", "-t",
                        help="要合成的文本内容")
    parser.add_argument("--textfile",
                        help="从文件读取文本（支持 UTF-8 编码的 txt/md 等）")
    parser.add_argument("--audio", "-a", default="output.mp3",
                        help="输出音频文件路径（默认: output.mp3）")
    parser.add_argument("--engine", "-e", choices=["edge", "dashscope"], default="edge",
                        help="TTS 引擎: edge（免费，默认）或 dashscope（阿里云）")
    parser.add_argument("--voice", "-v",
                        help="音色名称（不指定则根据语言自动选择）")
    parser.add_argument("--model", "-m",
                        help="DashScope 模型ID（仅 dashscope 引擎，默认: cosyvoice-v1）")
    parser.add_argument("--rate", "-r", default=None,
                        help="语速调整，如 +20%%（加速）、-10%%（减速）。"
                             "英文默认 -10%%（0.9 倍速），中文默认 +0%%")
    parser.add_argument("--volume", default="+0%",
                        help="音量调整，如 +20%%、-10%%（默认 +0%%）")
    parser.add_argument("--list-voices", action="store_true",
                        help="列出可用的音色（配合 --lang 过滤语言）")
    parser.add_argument("--lang", default="zh",
                        help="语言过滤，配合 --list-voices 使用（默认 zh，可选 en/ja/ko 等）")

    return parser.parse_args()


def load_text(args):
    """加载文本"""
    if args.text:
        return args.text

    if args.textfile:
        path = Path(args.textfile)
        if not path.exists():
            print(f"错误：文本文件不存在：{args.textfile}", file=sys.stderr)
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    # 从 stdin 读取
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    print("错误：未提供文本。请使用 --text 或 --textfile", file=sys.stderr)
    sys.exit(1)


async def list_edge_voices(lang_filter="zh"):
    """列出 Edge-TTS 可用音色"""
    try:
        import edge_tts
    except ImportError:
        print("错误：需要安装 edge-tts 库", file=sys.stderr)
        sys.exit(1)

    voices = await edge_tts.list_voices()
    if lang_filter:
        voices = [v for v in voices if v["Locale"].startswith(lang_filter)]

    print(f"\n可用 Edge-TTS 音色（语言: {lang_filter}）:\n")
    print(f"{'音色名称':<40} {'语言':<10} {'性别':<6}")
    print("-" * 60)
    for v in sorted(voices, key=lambda x: x["Locale"]):
        print(f"{v['ShortName']:<40} {v['Locale']:<10} {v['Gender']:<6}")
    print(f"\n共 {len(voices)} 个音色")


# ─── 自动检测语言 ──────────────────────────────────────────────────

def detect_language(text):
    """简单检测文本语言"""
    cjk_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_alpha = sum(1 for c in text if c.isalpha())
    if total_alpha == 0:
        return "zh"
    return "zh" if cjk_count / max(total_alpha, 1) > 0.3 else "en"


# ─── 主函数 ────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # 列出音色
    if args.list_voices:
        if args.engine == "edge":
            asyncio.run(list_edge_voices(args.lang))
        else:
            print("DashScope CosyVoice 可用音色：")
            print("  longxiaochun - 龙小淳（女声）")
            print("  longxiaoxia  - 龙小夏（女声）")
            print("  longxiaochen - 龙小辰（男声）")
            print("  longxiaobai  - 龙小白（男声）")
            print("  longlaotie   - 龙老铁（男声，东北口音）")
            print("  longshu      - 龙书（男声）")
            print("  longjing     - 龙静（女声）")
            print("  longshuo     - 龙硕（男声）")
        return

    text = load_text(args)
    if not text:
        print("错误：文本为空", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    lang = detect_language(text)

    output_path = Path(args.audio)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 确定语速：英文默认 -10%（0.9 倍速），中文默认 +0%
    rate = args.rate
    if rate is None:
        if lang == "en":
            rate = "-10%"
            logger.info("英文文本，使用默认 0.9 倍速（-10%）")
        else:
            rate = "+0%"

    logger.info(f"引擎: {args.engine}, 文本长度: {len(text)}, 检测语言: {lang}, 语速: {rate}")
    print(f"文本长度: {len(text)} 字符")
    print(f"检测语言: {'中文' if lang == 'zh' else '英文'}")
    if lang == "en" and rate == "-10%":
        print(f"语速: 0.9 倍速（适合听力练习）")

    try:
        if args.engine == "edge":
            # Edge-TTS
            if args.voice:
                voice = args.voice
            elif config.get("default_voice"):
                voice = config["default_voice"]
            elif lang == "zh":
                voice = "zh-CN-XiaoxiaoNeural"
            else:
                voice = "en-US-GuyNeural"

            print(f"正在合成语音（Edge-TTS，音色：{voice}，语速：{rate}）...")
            asyncio.run(edge_tts_synthesize(text, voice, rate, args.volume, str(output_path)))

        elif args.engine == "dashscope":
            # DashScope CosyVoice
            model = args.model or config.get("default_model", "cosyvoice-v1")
            if args.voice:
                voice = args.voice
            elif config.get("default_voice"):
                voice = config["default_voice"]
            else:
                voice = "longxiaochun"

            dashscope_tts_synthesize(text, model, voice, str(output_path))

        file_size = output_path.stat().st_size
        print(f"[OK] 语音已保存：{output_path}（{file_size / 1024:.1f} KB）")

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
