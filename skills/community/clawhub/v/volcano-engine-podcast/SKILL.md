---
name: volcano-engine-podcast
description: 生成火山引擎豆包语音播客（PodcastTTS）。输入主题文本，自动生成双人对话式播客音频。
version: 1.1.0
author: xiaohe
license: MIT
metadata:
  hermes:
    tags: [audio, podcast, tts, volcengine, doubao, 语音播客]
---

# 火山引擎豆包语音播客生成

基于火山引擎 PodcastTTS API，输入主题文本，AI 自动生成双人对话播客音频（含片头音乐、多轮对话、片尾结束）。

## 前提条件

1. Python >= 3.9
2. 安装 `websockets>=14.0`
3. 火山引擎账号已开通 PodcastTTS 服务

## 快速开始

### 1. 环境变量配置（推荐）

```bash
export VOLC_APPID="your_appid"
export VOLC_ACCESS_TOKEN="your_access_token"
export VOLC_APP_KEY="your_app_key"  # 可选，默认 aGjiRDfUWi
```

### 2. 命令行调用

```bash
python scripts/generate_podcast.py "Hermes和OpenClaw怎么选"
```

### 3. Python 代码调用

```python
import asyncio
from scripts.generate_podcast import PodcastGenerator

async def main():
    gen = PodcastGenerator(
        appid="3398567544",
        access_token="your_token",
    )
    result = await gen.generate(
        text="今天来聊聊AI编程助手",
        output_dir="./output",
        encoding="mp3",
        use_head_music=True,
    )
    print(result["final_files"])  # 输出音频路径列表

asyncio.run(main())
```

## 参数说明

### PodcastGenerator 初始化参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appid | str | 是 | - | 应用 ID |
| access_token | str | 是 | - | Access Token |
| app_key | str | 否 | aGjiRDfUWi | App Key |
| resource_id | str | 否 | volc.service_type.10050 | 资源 ID |
| endpoint | str | 否 | wss://openspeech... | WebSocket 端点 |

### generate() 方法参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| text | str | 必填 | 输入主题文本 |
| output_dir | str | output | 输出目录 |
| encoding | str | mp3 | 音频格式: mp3/wav/pcm |
| use_head_music | bool | True | 是否加片头音乐 |
| use_tail_music | bool | False | 是否加片尾音乐 |
| only_nlp_text | bool | False | 只生成文本不生成音频 |
| return_audio_url | bool | False | 返回音频URL而非流式 |
| speaker_info | dict | {"random_order":False} | 说话人配置 |
| speech_rate | int | 0 | 语速 |
| skip_round_audio_save | bool | False | 跳过分段保存 |
| voice_type | str | None | 音色类型: `zh_male` / `zh_female` / `multi` |
| normalize_audio | bool | False | 是否对音频进行音量归一化 |
| fade_in_out | bool | False | 是否添加淡入淡出效果 |

### 音色选择 (voice_type)

| 值 | 说明 |
|------|------|
| None | 默认，AI 自动分配 |
| zh_male | 中文男声 |
| zh_female | 中文女声 |
| multi | 多人对话模式 |

## 返回结果

```python
{
    "success": True,
    "output_dir": "/abs/path/to/output",
    "segment_files": ["output/head_music_-1.mp3", "output/zh_female_0.mp3", ...],
    "final_files": ["output/podcast_final_1234567890.mp3"],
    "duration": 164.51,
    "texts": [
        {"text": "今天这期...", "speaker": "zh_female_mizaitongxue_v2_saturn_bigtts"},
        ...
    ],
    "usage": {"input_text_tokens": 0, "output_audio_tokens": 2800, "total_tokens": 2800}
}
```

## CLI 参数

```bash
python scripts/generate_podcast.py "主题文本" \
    -o ./output \
    -f mp3 \
    --no-head-music \
    --tail-music \
    --only-text \
    --voice-type zh_female \
    --normalize \
    --fade \
    --appid YOUR_APPID \
    --token YOUR_TOKEN \
    -v
```

## 技术说明

- **协议**: 自定义二进制 WebSocket 协议（封装在 protocols.py 中）
- **流式下发**: 音频以 4~10KB 分片实时流式下发
- **断点续传**: 支持从中断轮次自动重试
- **音频合并**: 自动合并所有分段为完整音频
- **音频后处理**: 支持音量归一化（peak -1dB）和淡入淡出（0.5s）

## 注意事项

1. Access Token 需从火山引擎控制台获取
2. 每次调用消耗相应的 audio token
3. 音频采样率固定为 24kHz
4. 对话角色由 AI 自动分配（通常为一男一女双人对话）
5. 音色选择 `voice_type` 为提示性参数，最终音色由服务端根据内容智能匹配
