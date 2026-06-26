# TTS — 文字转语音生成技能

## 描述

通过免费TTS接口将文字转换为语音文件（MP3格式），支持90+种语音选择。生成后以文件形式发送给用户。

## 触发场景

- 用户要求"语音"、"读出来"、"转语音"
- 需要将文字内容转为语音文件发送
- 需要批量生成语音

## TTS接口

**接口地址：**
```
https://tts.wangwangit.com/v1/audio/speech
```

**请求方式：** POST，Content-Type: application/json

**请求体：**
```json
{
    "input": "要说的话",
    "voice": "zh-CN-YunjianNeural",
    "speed": 0.9,
    "pitch": "0",
    "style": "general"
}
```

**参数说明：**
- `input`（必填）：要转换的文本
- `voice`（必填）：语音ID，见下方语音列表
- `speed`：速度，范围 0.25-3.0，默认 1.0
- `pitch`：音调，范围 -50 到 +50，默认 0
- `style`：语音风格，默认 `general`

**可选风格：**
- `general`（通用）
- `assistant`（助手）
- `chat`（聊天）
- `customerservice`（客服）
- `newscast`（新闻播报）
- `affectionate`（亲切）
- `calm`（平静）
- `cheerful`（欢快）
- `gentle`（温柔）
- `lyrical`（抒情）
- `serious`（严肃）

## 常用语音ID

**中文（推荐）：**

| 语音ID | 名称 | 性别/风格 |
|--------|------|----------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女声·温柔 |
| zh-CN-YunxiNeural | 云希 | 男声·清朗 |
| zh-CN-YunyangNeural | 云扬 | 男声·阳光 |
| zh-CN-XiaoyiNeural | 晓伊 | 女声·甜美 |
| zh-CN-YunjianNeural | 云健 | 男声·稳重 |
| zh-CN-XiaochenNeural | 晓辰 | 女声·知性 |
| zh-CN-XiaohanNeural | 晓涵 | 女声·优雅 |
| zh-CN-XiaomoNeural | 晓墨 | 女声·文艺 |
| zh-CN-XiaoruiNeural | 晓睿 | 女声·智慧 |
| zh-CN-XiaoshuangNeural | 晓双 | 女声·活泼 |
| zh-CN-XiaoxuanNeural | 晓萱 | 女声·清新 |
| zh-CN-YunfengNeural | 云枫 | 男声·磁性 |
| zh-CN-YunhaoNeural | 云皓 | 男声·豪迈 |
| zh-CN-YunzeNeural | 云泽 | 男声·深沉 |

## 使用方法

**单条生成：**
```bash
curl -s -X POST 'https://tts.wangwangit.com/v1/audio/speech' \
  -H 'content-type: application/json' \
  -d '{"input":"你好","voice":"zh-CN-YunyangNeural","speed":0.9,"pitch":"0","style":"general"}' \
  -o /tmp/tts_output.mp3
```

**用Python脚本生成：**
```python
import requests

def text_to_speech(text, output_file, voice="zh-CN-YunyangNeural", speed=0.9, pitch="0", style="general"):
    ttsurl = 'https://tts.wangwangit.com/v1/audio/speech'
    jd = {
        "input": text,
        "voice": voice,
        "speed": speed,
        "pitch": pitch,
        "style": style
    }
    res = requests.post(ttsurl, json=jd, timeout=300)
    res.raise_for_status()
    with open(output_file, "wb") as f:
        f.write(res.content)
    return True
```

## 生成音频文件

生成语音文件后，使用 message 工具发送：

```
message action=send media=/tmp/tts_output.mp3
```

文件保存到 `/tmp/` 目录下，使用绝对路径。

## 注意事项

- 接口免费，无API密钥
- 单次转换字符数上限 10,000 字，超出需分段生成
- 支持任意音频文件格式（MP3/WAV/OGG/AMR等）
- 需要设置合理的headers保证调用成功
