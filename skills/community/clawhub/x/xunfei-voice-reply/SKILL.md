---
name: xunfei-voice-reply
description: 语音回复技能 - 使用讯飞 TTS 生成语音并发送到飞书。当需要用语音回复用户消息时使用。触发词：用语音、语音回复、切换语音模式、语音模式。
---

# 语音回复技能

## 模式切换

用户可以通过以下命令切换回复模式：
- **"用语音"** → 切换到语音模式
- **"用文字"** → 切换到文字模式

切换时更新 `USER.md` 的 `回复模式` 字段。

## 语音回复流程

当 `USER.md` 中 `回复模式: voice` 时：

```
1. 生成文本回复内容
2. 调用 scripts/voice-reply.js 生成语音
3. 使用 message 工具发送 opus 文件到飞书
4. 返回 NO_REPLY（语音已发送）
```

### 脚本调用

```bash
node scripts/voice-reply.js "要说的文本"
```

成功输出：
```
VOICE_READY:/tmp/openclaw/voice-reply.opus
```

### 发送语音

```javascript
message({
  action: 'send',
  channel: 'feishu',
  target: 'user:<open_id>',
  media: '/tmp/openclaw/voice-reply.opus'
})
```

## 配置

### 音色配置

编辑 `config.json` 修改发音人：

```json
{
  "voice": "x4_xiaoyan",
  "availableVoices": {
    "x4_xiaoyan": "晓燕 - 女声，温柔",
    "x4_lingyouyou": "凌悠 - 童声",
    "x4_yezi": "叶子 - 女声，活泼"
  }
}
```

### 环境变量

```bash
export XUNFEI_APP_ID="你的应用ID"
export XUNFEI_API_KEY="你的API Key"
export XUNFEI_API_SECRET="你的API Secret"
export XUNFEI_VOICE="x4_lingyouyou"  # 可选，覆盖 config.json
```

## 技术实现

### 文件结构

```
xunfei-voice-reply/
├── SKILL.md           # 本文件
├── config.json        # 用户配置（音色、参数）
├── scripts/
│   └── voice-reply.js # 语音生成脚本
├── lib/
│   ├── tts-core.js    # 讯飞 TTS 核心模块
│   └── tts-config.js  # 配置读取
└── references/
    └── setup.md       # 环境配置说明
```

### TTS 引擎

使用讯飞 WebSocket TTS API：
- **格式**: PCM → ffmpeg → Opus
- **音色**: 从 config.json 读取
- **码率**: 24kbps, 24kHz

### 输出路径

音频文件输出到 `/tmp/openclaw/`（OpenClaw 标准临时目录），确保在 message 工具允许的路径内。

## 错误处理

1. **TTS 超时** → 降级到文字回复
2. **ffmpeg 不可用** → 提示用户安装
3. **发送失败** → 重试或降级

## 配置持久化

回复模式存储在 `USER.md`:
```markdown
- **Notes:**
  - **回复模式**: text  # text 或 voice
```

每次 session 启动时读取，切换时更新。

## ⚠️ 必须在 AGENTS.md 中添加

使用此技能前，必须在 AGENTS.md 中添加语音回复流程：

```markdown
## 🎤 Voice Reply (讯飞语音)

Check `USER.md` Notes for `回复模式`:
- If `回复模式: voice` → use voice for replies
- If `回复模式: text` (or not set) → use text

### Voice Reply Flow
1. Generate text response
2. Run: `node ~/.agents/skills/xunfei-voice-reply/scripts/voice-reply.js "text"`
3. Send the Opus file via `message` tool
4. Reply with `NO_REPLY`

### Trigger Words
- "用语音" / "语音回复" / "切换语音模式"
```

