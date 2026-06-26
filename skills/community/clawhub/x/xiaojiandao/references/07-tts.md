# 字幕TTS生成

将解说旁白文本批量合成为语音音频，并生成对应的 word.json 时间轴文件，最终输出 SRT 字幕。

## 接口

### 提交TTS合成

```
POST /api/aipkg/submit/azure.tts.texts
```

### 查询TTS结果

```
POST /api/aipkg/query/azure.tts.texts.result
```

## 请求参数（提交）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `texts` | array | ✅ | 旁白文本列表（每项对应一段音频） |
| `voice` | string | ✅ | **必须使用音色推荐接口返回的 voice 值**（如 `zh-CN-XiaochenNeural`），不可使用任意Azure TTS音色名 |
| `style` | string | ❌ | 风格，如 `cheerful` / `sad` |
| `rate` | string | ❌ | 语速，如 `+10%`（范围 -50%～+50%） |
| `volume` | string | ❌ | 音量，如 `+50`（范围 -100～+100） |
| `pitch` | string | ❌ | 音调，如 `+5%`（范围 -50%～+50%） |

**示例**：
```json
{
  "task_id": 123456,
  "texts": ["第一段旁白内容", "第二段旁白内容"],
  "voice": "zh-CN-XiaoxiaoNeural",
  "style": "cheerful",
  "rate": "+10%"
}
```

## 异步轮询

1. 提交后从 `data.client_id` 获取轮询 ID
2. **轮询接口**：POST `/api/aipkg/query/azure.tts.texts.result`，body `{"client_id": "xxx"}`
3. **指数退避**：首次 3s，每次翻倍，上限 30s
4. **建议超时**：300秒
5. **state=2 成功** → 返回 `audio_url`（zip 包下载地址）

## 查询响应（state=2 成功）

```json
{
  "err_code": -1,
  "data": {
    "state": 2,
    "audio_url": "https://cdn.example.com/tts/batch_001.zip"
  }
}
```

## 音频包处理

下载 zip 包并解压，得到文件：

```
batch_001/
├── 0001.mp3          # 第1段音频
├── 0001.word.json    # 第1段时间轴
├── 0002.mp3          # 第2段音频
└── 0002.word.json    # 第2段时间轴
```

**word.json 格式**：
```json
[
  {"Text": "你好", "AudioOffset": 0, "Duration": 350},
  {"Text": "世界", "AudioOffset": 350, "Duration": 400}
]
```

## word.json → SRT 字幕

### 规则

| 条件 | 动作 |
|------|------|
| 遇到句末标点（。！？…!?） | 立即断行 |
| 字数 ≥ max_chars 且以分句标点（，、：；）结尾 | 断行 |
| 字数 ≥ max_chars + 3 仍未遇标点 | 强制回溯断行 |

### 时间轴对齐策略

- **云端合成 (推荐)**：直接将下载得到的 `audio_url` (ZIP包) 传给 `final_compose` 接口，后端将自动解析 ZIP 包内的 `word.json` 并校准时长，无需本地处理。
- **本地处理 (备选)**：若需在本地预览，建议通过读取 `word.json` 中最后一个元素的 `Offset + Duration` 来推算音频片段时长，以减少静音漂移。

### SRT 输出格式

```srt
1
00:00:00,000 --> 00:00:01,500
第一行字幕

2
00:00:01,500 --> 00:00:03,200
第二行字幕
```

## Python 实现

```python
import glob, json, subprocess, zipfile
from pathlib import Path

def ms_to_srt(ms):
    h, m, s, mil = ms//3600000, (ms%3600000)//60000, (ms%60000)//1000, ms%1000
    return f"{h:02d}:{m:02d}:{s:02d},{mil:03d}"

def word_json_to_srt(word_json_dir, output_path, max_chars=15):
    word_files = sorted(glob.glob(f"{word_json_dir}/*.word.json"))
    global_items = []
    time_offset = 0

    for wf in word_files:
        with open(wf, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            text = item.get("Text") or item.get("text") or ""
            offset = int(item.get("AudioOffset") or 0)
            dur = int(item.get("Duration") or 0)
            if text:
                global_items.append((text, time_offset+offset, time_offset+offset+dur))
        
        # 估算该段音频结束时间（最后一个词的结束点）
        file_end = max((i.get("AudioOffset", 0) + i.get("Duration", 0) for i in items), default=0)
        time_offset += file_end

    # 合并字幕行...
    # 输出 SRT 文件...
```

## 注意事项

- **批量限制**：每批最多 20 条文本，超出自动分批
- **音频包下载**：返回的 `audio_url` 需要下载并解压才能获取音频文件
- **时长漂移**：word.json 的 Duration 不含静音尾部。在云端流程中，直接将 ZIP 包透传给合成接口即可由后端自动处理漂移；若在本地预览，请注意累积误差。
- **多批次**：文本超过 20 条时，服务端自动分批，每批独立下载后再合并
- **voice 参数**：建议使用 `zh-CN-XiaoxiaoNeural`（女声），可根据音色推荐结果选择
