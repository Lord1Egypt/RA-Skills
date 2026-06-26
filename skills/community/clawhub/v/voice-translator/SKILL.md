---
name: senseaudio-voice-translator
description: 说中文出外语语音——按住说中文，2-3秒内播放英/日/韩语音。支持场景模式、双向对话、常用句收藏。
metadata:
  openclaw:
    emoji: "🌏"
    homepage: https://senseaudio.cn/docs
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - python3
    primaryEnv: SENSEAUDIO_API_KEY
---

# Voice Translator / 语音翻译器

按住说中文，松手后 2-3 秒内播放目标语言语音。出国旅行、跨国沟通即开即用。

## 工作流程

```
[按住录音] → ASR识别中文 → LLM场景化翻译 → TTS合成外语语音 → [播放]
双向模式：[录入外语] → ASR识别 → 翻译成中文 → TTS播放中文
```

## 核心 API

### 第一步：语音识别（ASR）

```bash
# 录制音频后上传识别（中文）
curl https://api.senseaudio.cn/v1/audio/transcriptions \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F file="@recording.wav" \
  -F model="sense-asr" \
  -F language="zh" \
  -F response_format="text"
# 返回：买单
```

双向模式识别外语（自动检测语言）：
```bash
curl https://api.senseaudio.cn/v1/audio/transcriptions \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F file="@foreign.wav" \
  -F model="sense-asr" \
  -F response_format="text"
# 返回：Can I get the check please
```

### 第二步：场景化翻译（LLM）

翻译不是直译，而是目标语言的自然表达。通过系统提示注入场景上下文：

| 场景 | system prompt 关键词 |
|------|---------------------|
| 餐厅 | restaurant, ordering food, dining |
| 机场 | airport, check-in, boarding, customs |
| 酒店 | hotel, check-in, room service, concierge |
| 出租车 | taxi, directions, destination |
| 购物 | shopping, price, discount, payment |
| 就医 | medical, symptoms, pharmacy, emergency |

翻译示例（餐厅场景）：
- 中文"买单" → `"Can I get the check, please?"` ✓（非 "buy the bill" ✗）
- 中文"这个怎么做的" → `"How is this dish prepared?"` ✓
- 中文"不要辣" → `"Could you make it not spicy, please?"` ✓

### 第三步：语音合成（TTS）

```bash
# 英语播报
curl -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.0",
    "text": "Can I get the check, please?",
    "stream": false,
    "voice_setting": {
      "voice_id": "female_0001_a",
      "speed": 0.9
    },
    "audio_setting": {
      "format": "mp3",
      "sample_rate": 32000
    }
  }' | python3 -c "
import sys, json, subprocess
r = json.load(sys.stdin)
audio = bytes.fromhex(r['data']['audio'])
open('/tmp/translated.mp3','wb').write(audio)
subprocess.run(['play','/tmp/translated.mp3'])
"
```

## 完整 Python 实现

```python
import os
import json
import requests
import subprocess
import tempfile

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
ASR_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"

# 场景配置
SCENES = {
    "restaurant": {
        "name": "餐厅",
        "prompt": "You are translating for a customer in a restaurant. Use natural, polite expressions a native speaker would use when ordering food, asking about dishes, or requesting service.",
    },
    "airport": {
        "name": "机场",
        "prompt": "You are translating at an airport. Use standard travel expressions for check-in, boarding, customs, and baggage.",
    },
    "hotel": {
        "name": "酒店",
        "prompt": "You are translating at a hotel. Use polite hospitality expressions for check-in, room requests, and concierge services.",
    },
    "taxi": {
        "name": "出租车",
        "prompt": "You are translating in a taxi. Use clear, direct expressions for giving directions and destinations.",
    },
    "shopping": {
        "name": "购物",
        "prompt": "You are translating while shopping. Use natural expressions for asking prices, sizes, discounts, and payment.",
    },
    "medical": {
        "name": "就医",
        "prompt": "You are translating at a medical facility. Use clear, precise expressions for describing symptoms and seeking help.",
    },
}

# 目标语言配置
LANGUAGES = {
    "en": {"name": "英语", "voice_id": "female_0001_a"},
    "ja": {"name": "日语", "voice_id": "female_0001_a"},
    "ko": {"name": "韩语", "voice_id": "female_0001_a"},
    "fr": {"name": "法语", "voice_id": "female_0001_a"},
    "de": {"name": "德语", "voice_id": "female_0001_a"},
    "es": {"name": "西班牙语", "voice_id": "female_0001_a"},
}

LANG_NAMES = {
    "en": "English", "ja": "Japanese", "ko": "Korean",
    "fr": "French", "de": "German", "es": "Spanish",
}


def asr(audio_path: str, language: str = None) -> str:
    """语音识别"""
    with open(audio_path, "rb") as f:
        data = {"model": "sense-asr", "response_format": "text"}
        if language:
            data["language"] = language
        resp = requests.post(
            ASR_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": f},
            data=data,
            timeout=15,
        )
    resp.raise_for_status()
    return resp.text.strip()


def translate(text: str, target_lang: str, scene: str = None) -> str:
    """场景化翻译（调用 LLM）"""
    scene_prompt = SCENES.get(scene, {}).get("prompt", "Translate naturally.")
    lang_name = LANG_NAMES.get(target_lang, target_lang)

    # 此处接入你的 LLM（如 Claude API）
    # 示例 prompt：
    system = f"{scene_prompt} Translate the Chinese text to {lang_name}. Return ONLY the translated text, no explanations."
    # user = text
    # ... call LLM API ...
    # 返回翻译结果
    raise NotImplementedError("请接入 LLM 翻译接口")


def tts(text: str, target_lang: str) -> bytes:
    """文字转语音"""
    voice_id = LANGUAGES.get(target_lang, {}).get("voice_id", "female_0001_a")
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id, "speed": 0.9},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    resp = requests.post(
        TTS_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    return bytes.fromhex(resp.json()["data"]["audio"])


def play_audio(audio_bytes: bytes):
    """播放音频"""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    # macOS: afplay, Linux: play (sox), Windows: start
    for cmd in [["afplay", tmp_path], ["play", tmp_path], ["mpg123", tmp_path]]:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue


class VoiceTranslator:
    def __init__(self, target_lang: str = "en", scene: str = None, bidirectional: bool = False):
        self.target_lang = target_lang
        self.scene = scene
        self.bidirectional = bidirectional
        self.favorites: list[dict] = []  # 收藏的句子

    def translate_voice(self, audio_path: str) -> dict:
        """主流程：录音 → 识别 → 翻译 → 合成 → 播放"""
        # 1. ASR
        src_lang = None if self.bidirectional else "zh"
        recognized = asr(audio_path, language=src_lang)
        print(f"识别: {recognized}")

        # 2. 翻译
        tgt_lang = "zh" if self.bidirectional else self.target_lang
        translated = translate(recognized, tgt_lang, self.scene)
        print(f"翻译: {translated}")

        # 3. TTS + 播放
        audio = tts(translated, tgt_lang)
        play_audio(audio)

        result = {"original": recognized, "translated": translated, "lang": tgt_lang}
        return result

    def add_favorite(self, result: dict):
        """收藏句子"""
        entry = {**result, "scene": self.scene}
        if entry not in self.favorites:
            self.favorites.append(entry)
            print(f"已收藏: {result['original']} → {result['translated']}")

    def play_favorite(self, index: int):
        """直接播放收藏句子"""
        entry = self.favorites[index]
        audio = tts(entry["translated"], entry["lang"])
        play_audio(audio)

    def save_favorites(self, path: str = "favorites.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def load_favorites(self, path: str = "favorites.json"):
        try:
            with open(path, encoding="utf-8") as f:
                self.favorites = json.load(f)
        except FileNotFoundError:
            pass


# 使用示例
if __name__ == "__main__":
    # 餐厅场景，翻译成英语
    translator = VoiceTranslator(target_lang="en", scene="restaurant")
    translator.load_favorites()

    # 翻译一句话
    result = translator.translate_voice("recording.wav")

    # 收藏
    translator.add_favorite(result)
    translator.save_favorites()

    # 双向模式：对方说英语，翻译成中文
    reverse = VoiceTranslator(target_lang="zh", bidirectional=True)
    reverse.translate_voice("foreign_speech.wav")
```

## 场景模式速查

| 场景 | 常见中文输入 | 自然外语输出（英语示例） |
|------|------------|------------------------|
| 餐厅 | 买单 | Can I get the check, please? |
| 餐厅 | 这个怎么做的 | How is this dish prepared? |
| 餐厅 | 不要辣 | Could you make it not spicy? |
| 机场 | 我的行李丢了 | I'd like to report lost luggage. |
| 机场 | 登机口在哪 | Where is the boarding gate? |
| 酒店 | 我要退房 | I'd like to check out, please. |
| 出租车 | 去这个地址 | Please take me to this address. |
| 购物 | 能便宜点吗 | Is there any discount available? |
| 就医 | 我头很痛 | I have a severe headache. |

## 支持语言

| 代码 | 语言 | ASR 支持 | TTS 支持 |
|------|------|---------|---------|
| en | 英语 | ✅ | ✅ |
| ja | 日语 | ✅ | ✅ |
| ko | 韩语 | ✅ | ✅ |
| fr | 法语 | ✅ | ✅ |
| de | 德语 | ✅ | ✅ |
| es | 西班牙语 | ✅ | ✅ |
| th | 泰语 | ✅ | ✅ |
| vi | 越南语 | ✅ | ✅ |

## 收藏功能

翻译过的句子可一键收藏，自动积累个人旅行用语库：

```python
# 收藏
translator.add_favorite(result)
translator.save_favorites("my_phrases.json")

# 下次直接播放，无需重新录音
translator.load_favorites("my_phrases.json")
translator.play_favorite(0)  # 播放第一条收藏
```

收藏文件格式（`favorites.json`）：
```json
[
  {
    "original": "买单",
    "translated": "Can I get the check, please?",
    "lang": "en",
    "scene": "restaurant"
  }
]
```

## TTS 参数说明

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| speed | 0.9 | 略慢，外语更清晰易懂 |
| vol | 1.0 | 标准音量 |
| format | mp3 | 通用格式 |
| sample_rate | 32000 | 平衡音质与速度 |

## 相关资源

- [SenseAudio ASR API](https://senseaudio.cn/docs/asr_api)
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [支持语言列表](https://senseaudio.cn/docs/asr_api#language-support)
