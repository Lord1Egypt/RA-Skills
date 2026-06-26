---
name: minimax-tts
description: MiniMax 语音合成技能（TTS）。使用 MiniMax API 将文本转换为语音。触发场景：(1) 用户请求将文本转换为语音，(2) 用户需要特定音色的语音合成，(3) 用户想要生成不同语言的语音，(4) 用户需要长文本语音合成，(5) 用户想要克隆自己的声音。支持的模型：speech-2.8-hd, speech-2.8-turbo, speech-2.6-hd, speech-2.6-turbo 等。支持情绪控制：happy, sad, angry, fearful, disgusted, surprised, calm, fluent, whisper。
---

# MiniMax 语音合成技能

## 功能概览

| 功能 | API 端点 | 说明 |
|------|----------|------|
| 异步语音合成 | `/v1/t2a_async_v2` | 长文本语音合成（推荐） |
| 查询任务状态 | `/v1/query/t2a_async_query_v2` | 查询异步任务进度 |
| 音色快速复刻 | `/v1/voice_clone` | 克隆自定义音色 |
| 查询可用音色 | `/v1/get_voice` | 获取音色列表 |
| 删除音色 | `/v1/del_voice` | 删除自定义音色 |

## 重要说明

**同步端点 `/v1/t2a_v1` 已停用，返回 404。请使用异步端点 `/v1/t2a_async_v2`。**

## 工作流程

```
文本 → 创建任务 → 轮询状态 → 获取file_id → 下载音频 → 本地保存
```

## 快速开始

### 异步语音合成

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

# 1. 创建任务
response = requests.post(
    "https://api.minimaxi.com/v1/t2a_async_v2",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "speech-2.8-hd",
        "text": "你好，欢迎使用 MiniMax 语音合成服务",
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
            "bitrate": 128000,
            "channel": 1
        }
    }
)

task_id = response.json()["task_id"]

# 2. 查询状态
status_resp = requests.get(
    f"https://api.minimaxi.com/v1/query/t2a_async_query_v2?task_id={task_id}",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
status = status_resp.json()["status"]  # Processing / Success / Failed

# 3. 下载音频
if status == "Success":
    file_id = status_resp.json()["file_id"]
    file_resp = requests.get(
        f"https://api.minimaxi.com/v1/files/retrieve?file_id={file_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    download_url = file_resp.json()["file"]["download_url"]
    
    # 保存到本地
    save_dir = "~/.openclaw/workspace/assets/audios"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "output.mp3")
    
    audio_resp = requests.get(download_url)
    with open(save_path, 'wb') as f:
        f.write(audio_resp.content)
```

## 支持的模型

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| `speech-2.8-hd` | 高清语音（推荐） | 高质量要求 |
| `speech-2.8-turbo` | 快速语音 | 低延迟 |
| `speech-2.6-hd` | 高清语音 | 标准质量 |
| `speech-02-hd` | 标准高清 | 通用场景 |
| `speech-01-hd` | 基础高清 | 简单场景 |

## 音色设置 (voice_setting)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `voice_id` | string | 必填 | 音色 ID |
| `speed` | float | 1.0 | 语速 [0.5, 2] |
| `vol` | float | 1.0 | 音量 (0, 10] |
| `pitch` | int | 0 | 语调 [-12, 12] |
| `emotion` | string | - | 情绪控制 |

### 情绪选项

`happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `calm`, `fluent`, `whisper`

### 常用系统音色

| 语言 | voice_id | 说明 |
|------|----------|------|
| 中文 | `Chinese (Mandarin)_Lyrical_Voice` | 抒情女声 |
| 中文 | `Chinese (Mandarin)_HK_Flight_Attendant` | 空乘女声 |
| 英文 | `English_Graceful_Lady` | 优雅女声 |
| 英文 | `English_Persuasive_Man` | 说服力男声 |
| 日文 | `Japanese_Whisper_Belle` | 日文低语 |

## 音频设置 (audio_setting)

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| `audio_sample_rate` | 8000, 16000, 22050, 24000, 32000, 44100 | 32000 |
| `bitrate` | 32000, 64000, 128000, 256000 | 128000 |
| `format` | mp3, pcm, flac | mp3 |
| `channel` | 1 (单声道), 2 (双声道) | 1 |

## 声音效果器 (voice_modify)

| 参数 | 类型 | 说明 |
|------|------|------|
| `pitch` | int | 音高调整 [-100, 100] |
| `intensity` | int | 强度调整 [-100, 100] |
| `timbre` | int | 音色调整 [-100, 100] |
| `sound_effects` | string | 音效 |

### 音效选项

- `spacious_echo` - 空旷回音
- `auditorium_echo` - 礼堂广播
- `lofi_telephone` - 电话失真
- `robotic` - 电音

## 音色快速复刻

1. 上传音频文件获取 `file_id`
2. 调用 `/v1/voice_clone` 进行复刻
3. 使用复刻的 `voice_id` 进行语音合成

## 输出目录

生成的音频保存在：`~/.openclaw/workspace/assets/audios/`

## 脚本工具

- `scripts/tts_sync.py` - 异步语音合成（自动保存本地）
- `scripts/tts_async.py` - 异步语音合成 + 状态查询
- `scripts/voice_clone.py` - 音色复刻
- `scripts/voice_list.py` - 查询可用音色

### 命令行用法

```bash
# 语音合成
python tts_sync.py "要转换的文本" --voice "Chinese (Mandarin)_Lyrical_Voice"

# 查询音色列表
python voice_list.py --type all

# 音色复刻
python voice_clone.py --file-id 123456789 --voice-id "my_voice"
```

## API 参考

详细文档：
- [references/tts-async.md](references/tts-async.md) - 异步语音合成
- [references/voice-clone.md](references/voice-clone.md) - 音色复刻
- [references/voice-management.md](references/voice-management.md) - 音色管理
