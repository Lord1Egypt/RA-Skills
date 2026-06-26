---
name: senseaudio-tts
description: SenseAudio Text-to-Speech (TTS) API for converting text to natural speech. Supports synchronous and SSE streaming modes, multiple voices, emotion control, speed/pitch/volume adjustment, and multi-language (Chinese/English).
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn/docs/text_to_speech_introduction
---

# SenseAudio Text-to-Speech (TTS)

SenseAudio TTS converts text to natural, emotionally rich speech using a large language model. Supports 10+ emotions, streaming output (SSE), and fine-grained voice control.

**Endpoint:** `POST https://api.senseaudio.cn/v1/t2a_v2`
**Auth:** `Authorization: Bearer $SENSEAUDIO_API_KEY`
**Max text length:** 10,000 characters

---

## Request Parameters

### Headers

| Header | Required | Value |
|--------|----------|-------|
| Authorization | yes | `Bearer YOUR_API_KEY` |
| Content-Type | yes | `application/json` |

### Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | yes | `SenseAudio-TTS-1.0` |
| text | string | yes | Text to synthesize. Supports `<break time=500>` pause tags |
| stream | boolean | yes | `false` = sync response; `true` = SSE streaming |
| voice_setting | object | yes | Voice configuration (see below) |
| audio_setting | object | no | Audio format configuration (see below) |
| dictionary | array | no | Polyphonic character corrections (cloned voices + TTS-1.5 only) |

### voice_setting

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| voice_id | string | - | - | Voice ID (system or cloned) |
| speed | float | 1.0 | [0.5, 2.0] | Speech speed |
| vol | float | 1.0 | [0, 10] | Volume |
| pitch | int | 0 | [-12, 12] | Pitch adjustment |
| latex_read | boolean | false | - | Read LaTeX/MathML formulas aloud |

### audio_setting

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| format | string | mp3 | mp3, wav, pcm, flac |
| sample_rate | int | 32000 | 8000, 16000, 22050, 24000, 32000, 44100 |
| bitrate | int | 128000 | 32000, 64000, 128000, 256000 (MP3 only) |
| channel | int | 2 | 1 (mono), 2 (stereo) |

### `<break>` Pause Tag

Insert pauses in text:
```
你好<break time=500>欢迎使用我们的服务
```
- `time` unit: milliseconds, min 100ms

---

## Non-Streaming Response

```json
{
  "data": {
    "audio": "hex-encoded audio data...",
    "status": 2
  },
  "extra_info": {
    "audio_length": 3500,
    "audio_sample_rate": 32000,
    "audio_size": 56000,
    "bitrate": 128000,
    "audio_format": "mp3",
    "audio_channel": 1,
    "word_count": 24,
    "usage_characters": 30
  },
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

`data.audio` is hex-encoded. Decode: `bytes.fromhex(audio_hex)`

---

## SSE Streaming Response

Each chunk: `data: {"data":{"audio":"hex...","status":1},...}`

Final chunk has `status: 2` and includes `extra_info`.

---

## Code Examples

### curl (non-streaming)

```bash
curl -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.0",
    "text": "道可道，非常道。名可名，非常名。",
    "stream": false,
    "voice_setting": {"voice_id": "male_0004_a"}
  }' -o response.json

jq -r '.data.audio' response.json | xxd -r -p > output.mp3
```

### Python (non-streaming)

```python
import requests

resp = requests.post(
    "https://api.senseaudio.cn/v1/t2a_v2",
    headers={"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "model": "SenseAudio-TTS-1.0",
        "text": "道可道，非常道。",
        "stream": False,
        "voice_setting": {"voice_id": "male_0004_a"}
    }
)
result = resp.json()
audio_bytes = bytes.fromhex(result["data"]["audio"])
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)
```

### Python (SSE streaming)

```python
import requests, json

with requests.post(
    "https://api.senseaudio.cn/v1/t2a_v2",
    headers={"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"},
    json={"model": "SenseAudio-TTS-1.0", "text": "这是流式输出示例。", "stream": True,
          "voice_setting": {"voice_id": "male_0004_a"}},
    stream=True
) as r:
    with open("output.mp3", "wb") as f:
        for line in r.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    chunk = json.loads(line_str[6:])
                    if chunk.get("data", {}).get("audio"):
                        f.write(bytes.fromhex(chunk["data"]["audio"]))
```

---

---

# SenseAudio 文本转语音（TTS）

SenseAudio TTS 基于千亿参数大模型，将文字转化为自然流畅、情感丰富的语音。支持 10+ 种情感、流式输出（SSE）及精细化语音控制。

**接口地址：** `POST https://api.senseaudio.cn/v1/t2a_v2`
**鉴权：** `Authorization: Bearer $SENSEAUDIO_API_KEY`
**最大文本长度：** 10,000 字符

---

## 请求参数

### 请求头

| 参数名 | 必填 | 说明 |
|--------|------|------|
| Authorization | 是 | `Bearer YOUR_API_KEY` |
| Content-Type | 是 | `application/json` |

### 请求体

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model | string | 是 | `SenseAudio-TTS-1.0` |
| text | string | 是 | 待合成文本，支持 `<break time=500>` 停顿符 |
| stream | boolean | 是 | `false` 同步；`true` SSE 流式 |
| voice_setting | object | 是 | 音色设置（见下表） |
| audio_setting | object | 否 | 音频格式设置（见下表） |
| dictionary | array | 否 | 多音字纠正（仅克隆音色 + TTS-1.5） |

### voice_setting（音色设置）

| 参数名 | 类型 | 默认值 | 范围 | 说明 |
|--------|------|--------|------|------|
| voice_id | string | - | - | 音色 ID（系统音色或克隆音色） |
| speed | float | 1.0 | [0.5, 2.0] | 语速 |
| vol | float | 1.0 | [0, 10] | 音量 |
| pitch | int | 0 | [-12, 12] | 音调 |
| latex_read | boolean | false | - | 数学公式朗读 |

### audio_setting（音频设置）

| 参数名 | 类型 | 默认值 | 选项 |
|--------|------|--------|------|
| format | string | mp3 | mp3, wav, pcm, flac |
| sample_rate | int | 32000 | 8000/16000/22050/24000/32000/44100 |
| bitrate | int | 128000 | 32000/64000/128000/256000（仅 MP3） |
| channel | int | 2 | 1（单声道）, 2（双声道） |

### `<break>` 停顿符

在文本中插入停顿：
```
你好<break time=500>欢迎使用我们的服务
```
- `time` 单位为毫秒，最小值 100ms

---

## 非流式响应

```json
{
  "data": {"audio": "hex编码音频...", "status": 2},
  "extra_info": {
    "audio_length": 3500,
    "audio_sample_rate": 32000,
    "audio_size": 56000,
    "audio_format": "mp3",
    "word_count": 24,
    "usage_characters": 30
  },
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

`data.audio` 为 hex 编码，解码：`bytes.fromhex(audio_hex)`

---

## SSE 流式响应

每个数据块：`data: {"data":{"audio":"hex...","status":1},...}`

最后一个 chunk `status: 2`，包含完整 `extra_info`。

---

## 代码示例

### curl（非流式）

```bash
curl -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.0",
    "text": "道可道，非常道。名可名，非常名。",
    "stream": false,
    "voice_setting": {"voice_id": "male_0004_a"}
  }' -o response.json

jq -r '.data.audio' response.json | xxd -r -p > output.mp3
```

### Python（非流式）

```python
import requests

resp = requests.post(
    "https://api.senseaudio.cn/v1/t2a_v2",
    headers={"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "model": "SenseAudio-TTS-1.0",
        "text": "道可道，非常道。",
        "stream": False,
        "voice_setting": {"voice_id": "male_0004_a"}
    }
)
audio_bytes = bytes.fromhex(resp.json()["data"]["audio"])
open("output.mp3", "wb").write(audio_bytes)
```
