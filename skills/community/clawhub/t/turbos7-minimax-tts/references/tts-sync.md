# 同步语音合成 API 参考

## 基础信息

- **API 地址**: `https://api.minimaxi.com/v1/t2a_v1`
- **认证**: Bearer Token
- **适用场景**: 短文本实时合成

## 请求体

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称 |
| `text` | string | 是 | 待合成文本，最长 5 千字符 |
| `voice_setting` | object | 是 | 音色设置 |
| `audio_setting` | object | 否 | 音频设置 |
| `language_boost` | string | 否 | 语言增强 |

### voice_setting

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `voice_id` | string | 必填 | 音色 ID |
| `speed` | float | 1.0 | 语速 [0.5, 2] |
| `vol` | float | 1.0 | 音量 (0, 10] |
| `pitch` | int | 0 | 语调 [-12, 12] |
| `emotion` | string | - | 情绪 |

### audio_setting

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| `audio_sample_rate` | 8000, 16000, 22050, 24000, 32000, 44100 | 32000 |
| `bitrate` | 32000, 64000, 128000, 256000 | 128000 |
| `format` | mp3, pcm, flac | mp3 |
| `channel` | 1, 2 | 1 |

## 系统音色示例

| 语言 | voice_id | 说明 |
|------|----------|------|
| 中文 | `Chinese (Mandarin)_Lyrical_Voice` | 抒情女声 |
| 中文 | `moss_audio_ce44fc67-7ce3-11f0-8de5-96e35d26fb85` | 中文音色 |
| 英文 | `English_Graceful_Lady` | 优雅女声 |
| 英文 | `English_Persuasive_Man` | 说服力男声 |
| 日文 | `Japanese_Whisper_Belle` | 日文低语 |

## 语气词标签（speech-2.8 系列）

`(laughs)`, `(chuckle)`, `(coughs)`, `(clear-throat)`, `(groans)`, `(breath)`, `(pant)`, `(inhale)`, `(exhale)`, `(gasps)`, `(sniffs)`, `(sighs)`, `(snorts)`, `(burps)`, `(lip-smacking)`, `(humming)`, `(hissing)`, `(emm)`, `(whistles)`, `(sneezes)`, `(crying)`, `(applause)`

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 限流 |
| 1004 | 鉴权失败 |
| 2013 | 参数错误 |

## 使用示例

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/t2a_v1",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "speech-02-hd",
        "text": "你好，欢迎使用语音合成服务(sighs)",
        "voice_setting": {
            "voice_id": "Chinese (Mandarin)_Lyrical_Voice",
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0,
            "emotion": "happy"
        },
        "audio_setting": {
            "audio_sample_rate": 32000,
            "format": "mp3",
            "bitrate": 128000
        }
    }
)

result = response.json()
audio_url = result["data"]["audio_url"]
print(f"音频地址: {audio_url}")
```
