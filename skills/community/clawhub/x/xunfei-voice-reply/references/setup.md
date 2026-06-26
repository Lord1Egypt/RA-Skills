# 环境配置说明

## 前置要求

### 1. 讯飞 TTS 账号

访问 [讯飞开放平台](https://www.xfyun.cn/) 注册并创建语音合成应用。

### 2. 环境变量

```bash
export XUNFEI_APP_ID="你的应用ID"
export XUNFEI_API_KEY="你的API Key"
export XUNFEI_API_SECRET="你的API Secret"
```

建议在启动脚本中设置。

### 3. ffmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 4. Node.js 依赖

```bash
npm install ws
```

## 音色配置

编辑技能包内的 `config.json`：

```json
{
  "voice": "x4_lingyouyou",
  "availableVoices": {
    "x4_xiaoyan": "讯飞晓燕",
    "x4_yezi": "讯飞小露",
    "aisjiuxu": "讯飞许久",
    "aisjinger": "讯飞小婧",
    "aisbabyxu": "讯飞许小宝"
  },
  "audio": {
    "outputBitrate": "24k",
    "outputSampleRate": 24000
  }
}
```

### 可用音色(免费角色)

| 音色ID | 名称 | 特点 |
|--------|------|------|
| x4_xiaoyan | 晓燕 | 成熟女声 |
| x4_yezi | 小露 | 亲切女声 |
| aisjiuxu | 许久 | 成熟男声 |
| aisjinger | 小婧 | 成熟女声 |
| aisbabyxu | 许小宝 | 童声 |

更多音色见 [讯飞语音合成文档](https://www.xfyun.cn/doc/tts/online_tts/API.html)。

## 集成到 AGENTS.md

```markdown
## Voice Reply

Check `USER.md` Notes for `回复模式`:
- If `回复模式: voice` → use voice for replies
- If `回复模式: text` (or not set) → use text

### Voice Reply Flow
1. Generate text response
2. Run: `node skills/xunfei-voice-reply/scripts/voice-reply.js "text"`
3. Send the Opus file via `message` tool
4. Reply with `NO_REPLY`
```

## 配置 USER.md

```markdown
- **Notes:**
  - **回复模式**: text  # text 或 voice
```

## 配置优先级

1. 环境变量 `XUNFEI_VOICE` - 最高优先级
2. 技能包内 `config.json`
3. 默认值 `x4_xiaoyan`

## 输出路径

音频文件统一输出到 `/tmp/openclaw/voice-reply.opus`。

这是 OpenClaw 的标准临时目录，在 message 工具的 `mediaLocalRoots` 允许路径内。

## 故障排除

### TTS 超时

检查网络连接和讯飞 API 状态。可在 `config.json` 中调整 `timeout`（默认 60 秒）。

### 音频格式错误

确保 ffmpeg 支持 libopus：

```bash
ffmpeg -codecs | grep opus
```

### 权限错误

```bash
chmod +x scripts/voice-reply.js
```

### 查看可用音色

```bash
node -e "console.log(JSON.stringify(require('./config.json').availableVoices, null, 2))"
```
