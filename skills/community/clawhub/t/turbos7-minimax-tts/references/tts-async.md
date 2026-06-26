# 异步语音合成 API 参考

## 基础信息

- **创建任务**: `POST https://api.minimaxi.com/v1/t2a_async_v2`
- **查询状态**: `GET https://api.minimaxi.com/v1/query/t2a_async_query_v2`
- **认证**: Bearer Token
- **适用场景**: 长文本（最长 5 万字符）

## 创建任务请求

### 请求体

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 语音模型 |
| `text` | string | 是* | 待合成文本（*与 text_file_id 二选一） |
| `text_file_id` | int | 是* | 文本文件 ID（*与 text  二选一） |
| `voice_setting` | object | 是 | 音色设置 |
| `audio_setting` | object | 否 | 音频设置 |
| `pronunciation_dict` | object | 否 | 发音字典 |
| `language_boost` | string | 否 | 语言增强 |
| `voice_modify` | object | 否 | 声音效果器 |

### voice_setting

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `voice_id` | string | 必填 | 音色 ID |
| `speed` | float | 1.0 | 语速 [0.5, 2] |
| `vol` | float | 1.0 | 音量 (0, 10] |
| `pitch` | int | 0 | 语调 [-12, 12] |
| `emotion` | string | - | 情绪 |
| `english_normalization` | bool | false | 英语数字规范化 |

### voice_modify（声音效果器）

| 参数 | 类型 | 说明 |
|------|------|------|
| `pitch` | int | 音高 [-100, 100] |
| `intensity` | int | 强度 [-100, 100] |
| `timbre` | int | 音色 [-100, 100] |
| `sound_effects` | string | 音效 |

### 音效选项

- `spacious_echo` - 空旷回音
- `auditorium_echo` - 礼堂广播
- `lofi_telephone` - 电话失真
- `robotic` - 电音

## 任务状态查询

### 查询参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | 是 | 任务 ID |

### 状态返回值

| status | 说明 |
|--------|------|
| `Processing` | 处理中 |
| `Success` | 已完成，可用 file_id 下载 |
| `Failed` | 失败 |
| `Expired` | 已过期 |

## 输出文件

任务完成后生成：
- **音频文件**: 格式由 audio_setting 指定
- **字幕文件**: 精确到句的字幕
- **JSON 文件**: 附加信息（title, content, extra）

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 限流 |
| 1004 | 鉴权失败 |
| 1039 | 触发 TPM 限流 |
| 1042 | 非法字符超 10% |
| 2013 | 参数错误 |

## 使用示例

### 创建异步任务

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/t2a_async_v2",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "speech-2.8-hd",
        "text": "这是一段较长的文本内容，用于测试异步语音合成...",
        "voice_setting": {
            "voice_id": "Chinese (Mandarin)_Lyrical_Voice",
            "speed": 1.0
        },
        "audio_setting": {
            "audio_sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 2
        },
        "voice_modify": {
            "pitch": 0,
            "intensity": 0,
            "timbre": 0,
            "sound_effects": "spacious_echo"
        }
    }
)

result = response.json()
task_id = result["task_id"]
file_id = result["file_id"]
print(f"任务 ID: {task_id}, 文件 ID: {file_id}")
```

### 查询任务状态

```python
response = requests.get(
    f"https://api.minimaxi.com/v1/query/t2a_async_query_v2?task_id={task_id}",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

result = response.json()
status = result["status"]  # Processing / Success / Failed / Expired
file_id = result.get("file_id")
```
