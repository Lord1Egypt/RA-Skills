#!/usr/bin/env python3
"""
edge-tts 语音生成脚本（中文 + 英文）

用法:
  python tts_generate.py story.txt
  python tts_generate.py story.txt --voice xiaoyi --rate -10
  python tts_generate.py story.txt --output my_story.mp3
  python tts_generate.py --batch batch_config.json

中文语音别名:
  xiaoxiao  - 温暖女声（默认，推荐朗读）
  xiaoyi    - 活泼女声
  yunxi     - 阳光男声
  yunjian   - 激情男声
  yunyang   - 专业男声

英文语音别名:
  jenny       - 温暖女声（默认英文，推荐朗读）
  guy         - 激情男声
  aria        - 自信女声
  christopher - 权威男声
  emma        - 活泼女声
  michelle    - 亲切女声

也可直接传入完整语音 ID，如 en-US-JennyNeural
"""
import argparse
import asyncio
import json
import os
import re
import sys

try:
    import edge_tts
except ImportError:
    print("ERROR: edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)


# ========== 语言检测 ==========
ENGLISH_VOICE_ALIASES = {"jenny", "guy", "aria", "christopher", "emma", "michelle"}


def detect_language(text: str) -> str:
    """检测文本语言：英文字母占比 >60% 判定为英文，否则为中文"""
    alpha_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(re.findall(r'[a-zA-Z\u4e00-\u9fff]', text))
    if total_chars == 0:
        return "zh"
    ratio = alpha_chars / total_chars
    return "en" if ratio > 0.6 else "zh"


def suggest_default_voice(text: str) -> str:
    """根据文本语言建议默认语音"""
    return "jenny" if detect_language(text) == "en" else "xiaoxiao"


# ========== 语音别名映射 ==========
VOICE_ALIASES = {
    # 中文语音
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi":   "zh-CN-XiaoyiNeural",
    "yunxi":    "zh-CN-YunxiNeural",
    "yunjian":  "zh-CN-YunjianNeural",
    "yunyang":  "zh-CN-YunyangNeural",
    "yunxia":   "zh-CN-YunxiaNeural",
    "xiaobei":  "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni":   "zh-CN-shaanxi-XiaoniNeural",
    # 英文语音
    "jenny":    "en-US-JennyNeural",
    "guy":      "en-US-GuyNeural",
    "aria":     "en-US-AriaNeural",
    "christopher": "en-US-ChristopherNeural",
    "emma":     "en-US-EmmaNeural",
    "michelle": "en-US-MichelleNeural",
}

# 默认语音
DEFAULT_VOICE = "xiaoxiao"


def resolve_voice(voice_arg: str) -> str:
    """将语音别名解析为完整语音 ID"""
    return VOICE_ALIASES.get(voice_arg.lower(), voice_arg)


async def generate(text_file: str, output_file: str, voice: str, rate: str) -> bool:
    """生成单个 MP3 文件"""
    # 读取文本
    if not os.path.exists(text_file):
        print(f"ERROR: {text_file} not found")
        return False

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"ERROR: {text_file} is empty")
        return False

    # 语言检测
    lang = detect_language(text)
    voice_id = resolve_voice(voice)
    voice_lang = "en" if voice.lower() in ENGLISH_VOICE_ALIASES else "zh"
    lang_label = "English" if lang == "en" else "Chinese"
    if lang != voice_lang:
        print(f"WARN: Text is {lang_label} but voice is {voice_id} ({voice_lang.upper()}), accent may occur")

    # 解析语音
    voice_id = resolve_voice(voice)

    # 构建 rate 参数（edge-tts 格式: "+0%", "-20%", "+50%"）
    # 支持用户传 "10"、"10%"、"+10%"、"-10%" 等各种格式
    rate = rate.strip()
    if not rate.startswith(("+", "-")):
        rate = f"+{rate}"
    if not rate.endswith("%"):
        rate = f"{rate}%"

    # 生成音频
    communicate = edge_tts.Communicate(text, voice_id, rate=rate)
    await communicate.save(output_file)

    size_kb = os.path.getsize(output_file) // 1024
    print(f"OK: {output_file} ({size_kb}KB) voice={voice_id} rate={rate}")
    return True


async def batch_generate(config_file: str) -> None:
    """批量生成 MP3 文件

    配置文件格式 (JSON):
    {
      "defaults": { "voice": "xiaoxiao", "rate": "+0%" },
      "files": [
        { "input": "story.txt", "output": "story.mp3" },
        { "input": "essay.txt", "output": "essay.mp3", "voice": "xiaoyi", "rate": "-10%" }
      ]
    }
    """
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    defaults = config.get("defaults", {})
    default_voice = defaults.get("voice", DEFAULT_VOICE)
    default_rate = defaults.get("rate", "+0%")

    for item in config.get("files", []):
        text_file = item["input"]
        output_file = item.get("output", text_file.replace(".txt", ".mp3"))
        voice = item.get("voice", default_voice)
        rate = item.get("rate", default_rate)

        if not os.path.isabs(text_file):
            text_file = os.path.join(os.path.dirname(config_file), text_file)
        if not os.path.isabs(output_file):
            output_file = os.path.join(os.path.dirname(config_file), output_file)

        await generate(text_file, output_file, voice, rate)


def main():
    parser = argparse.ArgumentParser(
        description="edge-tts 语音生成（中文 + 英文）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""中文语音别名:
  xiaoxiao  温暖女声（默认）  xiaoyi    活泼女声
  yunxi     阳光男声          yunjian   激情男声
  yunyang   专业男声          yunxia    可爱男声

英文语音别名:
  jenny       温暖女声（默认英文）  guy         激情男声
  aria        自信女声              christopher 权威男声
  emma        活泼女声              michelle    亲切女声

示例:
  python tts_generate.py story.txt
  python tts_generate.py story.txt --voice xiaoyi --rate -10
  python tts_generate.py story.txt --voice jenny --rate -10
  python tts_generate.py story.txt --output my_story.mp3
  python tts_generate.py --batch batch.json"""
    )

    parser.add_argument("input", nargs="?", help="输入文本文件路径")
    parser.add_argument("--output", "-o", help="输出 MP3 文件路径（默认: <输入名>_<语音别名>.mp3）")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE,
                        help=f"语音别名或完整 ID（默认: {DEFAULT_VOICE}）")
    parser.add_argument("--rate", "-r", default="+0%",
                        help="语速调整，如 +20%%、-10%%（默认: +0%%）")
    parser.add_argument("--batch", "-b", help="批量模式，传入 JSON 配置文件路径")

    args = parser.parse_args()

    # 批量模式
    if args.batch:
        asyncio.run(batch_generate(args.batch))
        return

    # 单文件模式
    if not args.input:
        parser.error("请提供输入文本文件，或使用 --batch 批量模式")

    text_file = args.input
    if not os.path.exists(text_file):
        print(f"ERROR: {text_file} not found")
        sys.exit(1)

    # 自动生成输出文件名
    output_file = args.output
    if not output_file:
        base, _ = os.path.splitext(text_file)
        output_file = f"{base}_{args.voice}.mp3"

    success = asyncio.run(generate(text_file, output_file, args.voice, args.rate))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
