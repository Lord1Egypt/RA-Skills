# Voice Bridge Light

轻量级语音桥接服务，提供 OpenAI 兼容的 STT/TTS HTTP API。

## 功能

- **TTS 文本转语音**：支持 Edge TTS（在线）和 Piper（本地）
- **STT 语音识别**：基于 Whisper 本地识别
- **OpenAI 兼容接口**：与 OpenAI Audio API 兼容
- **轻量部署**：依赖少，易于安装

## 使用方法

### 安装

```bash
pip install -r requirements.txt
```

### 启动服务

默认使用 Edge TTS：
```bash
python api_server.py
```

使用 Piper（需下载模型）：
```bash
TTS_ENGINE=piper PIPER_MODEL=models/piper/zh_CN-huayan-medium.onnx python api_server.py
```

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `GET /health` | GET | 健康检查 |
| `POST /audio/speech` | POST | TTS 语音合成 |
| `POST /audio/transcriptions` | POST | STT 语音识别 |

### 配置环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `VOICE_BRIDGE_HOST` | `0.0.0.0` | 监听地址 |
| `VOICE_BRIDGE_PORT` | `18790` | 监听端口 |
| `TTS_ENGINE` | `edge` | TTS 引擎：`edge` 或 `piper` |
| `EDGE_VOICE` | `zh-CN-XiaoxiaoNeural` | Edge TTS 音色 |
| `PIPER_MODEL` | `models/piper/zh_CN-huayan-medium.onnx` | Piper 模型路径 |
| `STT_MODEL` | `base` | Whisper 模型大小 |

### TTS 请求示例

```bash
curl -X POST http://localhost:18790/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "你好，世界！",
    "voice": "zh-CN-XiaoxiaoNeural",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

### STT 请求示例

```bash
curl -X POST http://localhost:18790/audio/transcriptions \
  -F "file=@speech.mp3" \
  -H "Content-Type: multipart/form-data"
```

## OpenClaw 集成

在 `openclaw.json` 中配置：

```json
{
  "tts": {
    "enabled": true,
    "provider": "local-piper",
    "baseUrl": "http://127.0.0.1:18790",
    "apiKey": "local",
    "voice": "zh-CN-XiaoxiaoNeural"
  }
}
```

## 依赖

- Python 3.8+
- edge-tts（Edge TTS）
- faster-whisper（Whisper STT）
- soundfile（音频处理）
- Flask + Flask-CORS（Web 服务）

## 服务管理

### systemd 服务（推荐）

```ini
[Unit]
Description=Voice Bridge Light - STT/TTS HTTP API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/skills/voice-bridge-light
ExecStart=/usr/bin/python3 api_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用并启动：
```bash
systemctl daemon-reload
systemctl enable voice-bridge-light.service
systemctl start voice-bridge-light.service
```

## 性能

- TTS 延迟：< 1s（Edge TTS 需要网络）
- STT 延迟：依赖音频长度，CPU 实时
- 内存占用：约 300-500MB（主要来自 Whisper 模型）

## 注意事项

- Edge TTS 需要外网访问微软服务
- Piper 需要下载模型文件（首次使用）
- Whisper 模型首次加载较慢，建议预热
- 生产环境建议使用 systemd 管理

## License

MIT
