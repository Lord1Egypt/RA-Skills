#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_compat

"""
🎙️ 用户分身·语音克隆引擎 (Voice Clone Engine)
输入：文字 + 风格指纹
输出：自然语音朗读（mp3/wav）
理念：不只读出文字，而是用你的语气、节奏、停顿风格"讲"出来。
免费、无需 API Key、中文发音媲美真人。
"""

import os
import json
import re
import asyncio
import tempfile
from pathlib import Path

_EDGE_TTS_AVAILABLE = False
try:
    import edge_tts
    _EDGE_TTS_AVAILABLE = True
except ImportError:
    pass

# 🎙️ 多语种语音库
VOICE_LIBRARY = {
    # 中文 (9种)
    "zh": {
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",     # 女声·温柔清晰（推荐）
        "xiaoyi": "zh-CN-XiaoyiNeural",          # 女声·活泼
        "yunjian": "zh-CN-YunjianNeural",        # 男声·沉稳
        "yunxi": "zh-CN-YunxiNeural",            # 男声·新闻播报
        "yunxia": "zh-CN-YunxiaNeural",          # 男声·青年
        "yunyang": "zh-CN-YunyangNeural",        # 男声·专业播音（推荐）
        "xiaobei": "zh-CN-liaoning-XiaobeiNeural",  # 东北女声
        "xiaoni": "zh-CN-shaanxi-XiaoniNeural",     # 陕西女声
        "xiaohan": "zh-CN-henan-XiaohanNeural",     # 河南男声
    },
    # English (12种)
    "en": {
        "jenny": "en-US-JennyNeural",            # 女声·通用
        "guy": "en-US-GuyNeural",                # 男声·通用
        "aria": "en-US-AriaNeural",              # 女声·新闻
        "davis": "en-US-DavisNeural",            # 男声·新闻
        "jane": "en-US-JaneNeural",              # 女声·对话
        "jason": "en-US-JasonNeural",            # 男声·对话
        "sara": "en-US-SaraNeural",              # 女声·温柔
        "tony": "en-US-TonyNeural",              # 男声·沉稳
        "nancy": "en-US-NancyNeural",            # 女声·专业
        "brandon": "en-US-BrandonNeural",        # 男声·专业
        "libby": "en-GB-LibbyNeural",            # 英式女声
        "ryan": "en-GB-RyanNeural",              # 英式男声
    },
    # 日本語 (5种)
    "ja": {
        "nanami": "ja-JP-NanamiNeural",          # 女声·通用
        "keita": "ja-JP-KeitaNeural",            # 男声·通用
        "aoi": "ja-JP-AoiNeural",                # 女声·温柔
        "daichi": "ja-JP-DaichiNeural",          # 男声·沉稳
        "shiori": "ja-JP-ShioriNeural",          # 女声·活泼
    },
}

# 合并所有语音到一个字典
ALL_VOICES = {}
for lang, voices in VOICE_LIBRARY.items():
    ALL_VOICES.update(voices)

# 中文语音（向后兼容）
CHINESE_VOICES = VOICE_LIBRARY["zh"]

VOICE_BY_PERSONA = {
    "邻家高手": "xiaoxiao",
    "直率实干家": "xiaoyi",
    "温暖絮叨者": "xiaoxiao",
    "深度思考者": "yunyang",
    "冷面专家": "yunjian",
    "学院派学者": "yunyang",
    "幽默大师": "xiaoyi",
    "儒雅风趣者": "yunxi",
    "务实派": "yunyang",
    "娓娓道来者": "yunjian",
    "轻松达人": "xiaoxiao",
    "故事大王": "yunjian",
}


class VoiceClone:
    def __init__(self, voice_id="xiaoxiao"):
        if not _EDGE_TTS_AVAILABLE:
            raise ImportError(
                "edge-tts 未安装。请运行：pip install edge-tts"
            )
        # 支持所有语种语音，默认中文
        self.voice = ALL_VOICES.get(voice_id, ALL_VOICES.get("xiaoxiao", "zh-CN-XiaoxiaoNeural"))
        self.voice_id = voice_id
        self.style_profile = None
        self.rate = "+0%"
        self.pitch = "+0Hz"

    def load_style(self, fingerprint_path):
        with open(fingerprint_path, "r", encoding="utf-8") as f:
            self.style_profile = json.load(f)
        self._apply_style_to_voice()
        return self

    def auto_voice_by_persona(self, fingerprint_path):
        with open(fingerprint_path, "r", encoding="utf-8") as f:
            fp = json.load(f)
        label = fp.get("overall_label", "")
        matched = VOICE_BY_PERSONA.get(label)
        if matched:
            self.voice = ALL_VOICES.get(matched, ALL_VOICES.get("xiaoxiao"))
            self.voice_id = matched
        self.style_profile = fp
        self._apply_style_to_voice()
        return self

    def _apply_style_to_voice(self):
        if not self.style_profile:
            return

        sl = self.style_profile.get("sentence_length", {})
        avg_len = sl.get("avg", 30)
        if avg_len < 25:
            self.rate = "+15%"
        elif avg_len > 50:
            self.rate = "-10%"

        pct = self.style_profile.get("punctuation", {})
        exclaim_ratio = pct.get("exclaim_ratio", 0.1)
        if exclaim_ratio > 0.5:
            self.pitch = "+10Hz"
            self.rate = "+10%"

        formality = self.style_profile.get("formality", {})
        if formality.get("level") == "学术严谨型":
            self.rate = "-5%"
        elif formality.get("level") == "朋友聊天型":
            self.rate = "+10%"

        expr = self.style_profile.get("expressiveness", {})
        if expr.get("style") == "果断直接型":
            self.rate = "+10%"

        sentiment = self.style_profile.get("sentiment_words", {})
        if sentiment.get("tone") == "积极乐观型":
            self.pitch = "+5Hz"

    async def speak(self, text, output_path=None):
        if not output_path:
            output_path = "voice_output.mp3"

        text = self._preprocess_text(text)

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch,
        )
        await communicate.save(output_path)
        return output_path

    async def speak_file(self, file_path, output_path=None):
        path = Path(file_path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not output_path:
            output_path = path.stem + ".mp3"
        return await self.speak(text, output_path)

    async def speak_with_style(self, text, fingerprint_path, output_path=None):
        self.auto_voice_by_persona(fingerprint_path)
        return await self.speak(text, output_path)

    def _preprocess_text(self, text):
        text = re.sub(r'[#*_~`>\[\](){}\|]', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'---+', '。', text)
        text = re.sub(r'!{2,}', '！', text)
        text = re.sub(r'\?{2,}', '？', text)
        return text.strip()

    @staticmethod
    def list_voices():
        """列出所有支持的语音角色"""
        voice_persona_map = {}
        for persona, vid in VOICE_BY_PERSONA.items():
            voice_persona_map.setdefault(vid, []).append(persona)

        # 中文语音
        print("\n🇨🇳 中文语音 (9种)：\n")
        print(f"{'ID':<12} {'说明':<20} {'适用人格'}")
        print("-" * 60)
        zh_desc = {
            "xiaoxiao": "女声·温柔清晰",
            "xiaoyi": "女声·活泼俏皮",
            "yunjian": "男声·沉稳大气",
            "yunxi": "男声·新闻播报",
            "yunxia": "男声·青年活力",
            "yunyang": "男声·专业播音",
            "xiaobei": "东北女声",
            "xiaoni": "陕西女声",
            "xiaohan": "河南男声",
        }
        for vid, full_name in VOICE_LIBRARY["zh"].items():
            desc = zh_desc.get(vid, "")
            personas = voice_persona_map.get(vid, [])
            print(f"{vid:<12} {desc:<20} {', '.join(personas) if personas else '通用'}")

        # 英文语音
        print("\n🇺🇸 English Voices (12种)：\n")
        print(f"{'ID':<12} {'Description':<25} {'Gender/Style'}")
        print("-" * 65)
        en_desc = {
            "jenny": "Female · General",
            "guy": "Male · General",
            "aria": "Female · News",
            "davis": "Male · News",
            "jane": "Female · Conversational",
            "jason": "Male · Conversational",
            "sara": "Female · Gentle",
            "tony": "Male · Calm",
            "nancy": "Female · Professional",
            "brandon": "Male · Professional",
            "libby": "Female · British",
            "ryan": "Male · British",
        }
        for vid, full_name in VOICE_LIBRARY["en"].items():
            desc = en_desc.get(vid, "")
            gender = "Female" if "Female" in desc else "Male"
            print(f"{vid:<12} {desc:<25} {gender}")

        # 日本語
        print("\n🇯🇵 日本語 (5种)：\n")
        print(f"{'ID':<12} {'説明':<20} {'性別/スタイル'}")
        print("-" * 60)
        ja_desc = {
            "nanami": "女声·通用",
            "keita": "男声·通用",
            "aoi": "女声·温柔",
            "daichi": "男声·沉稳",
            "shiori": "女声·活泼",
        }
        for vid, full_name in VOICE_LIBRARY["ja"].items():
            desc = ja_desc.get(vid, "")
            gender = "女声" if "女声" in desc else "男声"
            print(f"{vid:<12} {desc:<20} {gender}")

        print(f"\n💡 使用示例: python voice_clone.py speak 'Hello' --voice jenny")
        print()


def speak_sync(text, voice_id="xiaoxiao", output_path=None):
    vc = VoiceClone(voice_id)
    return asyncio.run(vc.speak(text, output_path))


def speak_with_fingerprint_sync(text, fingerprint_path, output_path=None):
    vc = VoiceClone()
    return asyncio.run(vc.speak_with_style(text, fingerprint_path, output_path))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🎙️ 用户分身·语音克隆引擎")

    sub = parser.add_subparsers(dest="command")

    list_cmd = sub.add_parser("list", help="列出可选语音角色")

    speak = sub.add_parser("speak", help="朗读一段文字")
    speak.add_argument("text", help="要朗读的文字")
    speak.add_argument("--voice", default="xiaoxiao",
                       help="语音角色ID（默认 xiaoxiao，运行 list 查看全部）")
    speak.add_argument("--output", default=None, help="输出音频文件路径")

    speak_file = sub.add_parser("speak-file", help="朗读文件内容")
    speak_file.add_argument("file", help="要朗读的文件（.md/.txt）")
    speak_file.add_argument("--voice", default="xiaoxiao",
                            help="语音角色ID（默认 xiaoxiao）")
    speak_file.add_argument("--output", default=None, help="输出音频文件路径")

    speak_style = sub.add_parser("speak-style", help="用风格指纹朗读文字（自动选角色+语速+音调）")
    speak_style.add_argument("text", help="要朗读的文字")
    speak_style.add_argument("--fingerprint", default="style_fingerprint.json", help="风格指纹 JSON")
    speak_style.add_argument("--output", default=None, help="输出音频文件路径")

    speak_file_style = sub.add_parser("narrate", help="用你的声音讲述一个文件")
    speak_file_style.add_argument("file", help="要讲述的文件")
    speak_file_style.add_argument("--fingerprint", default="style_fingerprint.json", help="风格指纹 JSON")
    speak_file_style.add_argument("--output", default=None, help="输出音频文件路径")

    args = parser.parse_args()

    if args.command == "list":
        VoiceClone.list_voices()

    elif args.command == "speak":
        vc = VoiceClone(args.voice)
        out = asyncio.run(vc.speak(args.text, args.output))
        print(f"🎙️ 语音已生成：{out}")

    elif args.command == "speak-file":
        vc = VoiceClone(args.voice)
        out = asyncio.run(vc.speak_file(args.file, args.output))
        print(f"🎙️ 语音已生成：{out}")

    elif args.command == "speak-style":
        out = speak_with_fingerprint_sync(args.text, args.fingerprint, args.output)
        print(f"🎙️ 风格化语音已生成：{out}")

    elif args.command == "narrate":
        out = speak_with_fingerprint_sync(
            Path(args.file).read_text(encoding="utf-8", errors="ignore"),
            args.fingerprint,
            args.output or Path(args.file).stem + ".mp3",
        )
        print(f"🎙️ 讲述音频已生成：{out}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()