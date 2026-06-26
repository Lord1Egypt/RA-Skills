# AGENT.md - 播客生成器 Agent 调用指南

> 本文档面向 AI Agent，描述如何通过 API 调用播客生成器功能。
> 人类用户请访问 Web 界面：http://localhost:5000

---

## 项目概述

**播客生成器** 是一个将话题文本转换为双主播播客音频的工具。

- **技术栈**: Python Flask + SenseAudio TTS + FFmpeg
- **位置**: `/home/wang/桌面/龙虾工作区/podcast-generator/`
- **默认端口**: 5000
- **默认输出**: `/home/wang/桌面/龙虾工作区/podcast-generator/output/`

---

## 快速启动

```bash
# 启动服务
python3 /home/wang/桌面/龙虾工作区/podcast-generator/backend/app.py

# 检查服务状态
curl http://localhost:5000/api/config
```

---

## API 接口

### 1. 获取配置信息

**GET** `/api/config`

返回音色列表、默认设置、示例话题等。

```json
{
  "success": true,
  "voice_config": {
    "male": { "voice_id": "male_0004_a", "default_speed": 1.0, "default_pitch": 0 },
    "female": { "voice_id": "female_0001_a", "default_speed": 1.0, "default_pitch": 2 }
  },
  "available_voices": { ... },
  "example_topic": "...",
  "ffmpeg_available": true,
  "llm_available": false
}
```

### 2. 生成播客

**POST** `/api/generate`

**Headers**:
- `Content-Type: application/json`
- `X-API-Key: <用户的SenseAudio API Key>`

**Body**:
```json
{
  "topic": "话题内容（建议50-200字）",
  "speed": 1.0,              // 语速 0.5-2.0，默认1.0
  "pitch_male": 0,           // 男声语调 -12~12，默认0
  "pitch_female": 2,         // 女声语调 -12~12，默认2
  "male_voice": "male_0004_a",    // 可选，自定义男声音色
  "female_voice": "female_0001_a" // 可选，自定义女声音色
}
```

**Response**:
```json
{
  "success": true,
  "output_file": "podcast_xxx.mp3",
  "download_url": "/api/download/podcast_xxx.mp3",
  "duration_seconds": 70.88,
  "segments": [
    { "speaker": "A", "speaker_name": "主播小明", "text": "..." },
    { "speaker": "B", "speaker_name": "主播小红", "text": "..." }
  ]
}
```

### 3. 下载播客文件

**GET** `/api/download/<filename>`

返回 MP3 音频文件。

### 4. 检查系统状态

**GET** `/api/status`

返回 FFmpeg、TTS、LLM 可用性。

---

## Agent 调用示例

### Python 示例

```python
import requests

API_BASE = "http://localhost:5000"
API_KEY = "sk-xxx"  # 用户提供的 SenseAudio API Key

# 生成播客
response = requests.post(
    f"{API_BASE}/api/generate",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    },
    json={
        "topic": "人工智能正在改变我们的生活方式...",
        "speed": 1.0,
        "pitch_male": 0,
        "pitch_female": 2,
    }
)

data = response.json()
if data["success"]:
    # 下载音频
    download_url = f"{API_BASE}{data['download_url']}"
    audio_data = requests.get(download_url).content
    
    # 保存到本地
    with open("podcast.mp3", "wb") as f:
        f.write(audio_data)
    
    print(f"播客已生成: {data['duration_seconds']}秒")
else:
    print(f"生成失败: {data.get('error')}")
```

### cURL 示例

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-xxx" \
  -d '{"topic": "人工智能正在改变我们的生活方式...", "speed": 1.0}'
```

---

## 可用音色列表

| 音色 ID | 类型 | 描述 |
|---------|------|------|
| `male_0001_a` | 男声 | 男声1 |
| `male_0002_a` | 男声 | 男声2 |
| `male_0004_a` | 男声 | 男声4（默认） |
| `female_0001_a` | 女声 | 女声1（默认） |
| `female_0002_a` | 女声 | 女声2 |
| `female_0003_a` | 女声 | 女声3 |

---

## 参数说明

| 参数 | 类型 | 范围 | 默认值 | 说明 |
|------|------|------|--------|------|
| `topic` | string | - | - | 必填，话题内容 |
| `speed` | float | 0.5-2.0 | 1.0 | 语速，1.0=正常 |
| `pitch_male` | int | -12~12 | 0 | 男声语调，正数更高 |
| `pitch_female` | int | -12~12 | 2 | 女声语调，正数更高 |
| `male_voice` | string | - | male_0004_a | 男声音色ID |
| `female_voice` | string | - | female_0001_a | 女声音色ID |

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `请先输入 API Key` | 未提供 X-API-Key | 在请求头添加 API Key |
| `请输入话题内容` | topic 为空 | 提供 topic 参数 |
| `TTS failed` | SenseAudio API 调用失败 | 检查 API Key 是否有效 |
| `Audio merge failed` | FFmpeg 合并失败 | 确保 FFmpeg 已安装 |

---

## 文件结构

```
podcast-generator/
├── backend/
│   ├── app.py              # Flask 主应用（API 路由）
│   ├── config.py           # 配置（音色、路径、API）
│   ├── tts_client.py       # SenseAudio TTS 客户端
│   ├── audio_merger.py     # FFmpeg 音频合并
│   ├── script_generator.py # 播客脚本生成
│   └── tests/              # 单元测试
├── frontend/
│   ├── index.html          # Web 界面
│   ├── app.js              # 前端逻辑
│   ├── style.css           # 样式
│   └── guide.html          # API Key 获取指南
├── output/                 # 生成的播客文件
├── AGENT.md                # 本文档
└── README.md               # 用户文档
```

---

## 依赖项

1. **SenseAudio API Key**: 用户需自行获取（注册送10万积分）
   - 注册链接: https://senseaudio.cn/login?inviteCode=KN7TA2FP

2. **FFmpeg**: 音频合并依赖
   - 安装路径: `~/bin/ffmpeg`（静态版本）
   - 检查: `ffmpeg -version`

3. **Python 包**:
   - `flask`, `flask-cors`
   - `requests`
   - `openai`（可选，用于 LLM 脚本生成）

---

## 开发与维护

### 运行测试

```bash
cd /home/wang/桌面/龙虾工作区/podcast-generator/backend
python3 -m pytest tests/
```

### 修改默认音色

编辑 `backend/config.py`:

```python
VOICE_CONFIG = {
    "male_host": {
        "voice_id": "male_0004_a",  # 修改此处
        "speed": 1.0,
        "pitch": 0,
        "name": "主播小明",
    },
    "female_host": {
        "voice_id": "female_0001_a",  # 修改此处
        "speed": 1.0,
        "pitch": 2,
        "name": "主播小红",
    }
}
```

### 修改对话脚本模板

编辑 `backend/script_generator.py` 的 `generate_simple_script()` 函数。

---

## 注意事项

1. **API Key 安全**: 不要在代码中硬编码 API Key，由用户提供
2. **文件清理**: output 目录定期清理（保留最近50个）
3. **超时处理**: 生成请求可能需要30-60秒，Agent 应设置足够 timeout
4. **并发限制**: 建议串行处理生成请求，避免 API 限流

---

*最后更新: 2026-04-13*