---
name: voice-tts
description: 语音输入（Whisper ASR）+ 语音输出（Edge TTS）技能，支持 agent 专属音色，可调用 send_voice_reply.mjs 发送 Telegram 语音消息。
metadata: {"openclaw": {"emoji": "🎙️", "requires": {"bins": ["node>=18", "python3", "ffmpeg"], "pip": ["edge-tts", "whisper", "click"]}}}
---

# voice-tts

语音输入（ASR）+ 语音输出（TTS）技能，完整替代 OpenClaw 内置 tts 工具处理中文内容。

## 技术概览

| 方向 | 技术 | 说明 |
|------|------|------|
| 语音 → 文字 | Whisper（本地） | 接收语音，自动转文字 |
| 文字 → 语音 | Edge TTS（云端） | 生成 MP3，发送 Telegram 语音消息 |

---

## 工作方式

### ASR（语音 → 文字）

用户发来语音消息 → `voice-asr.mjs` 转写为文字 → 触发 agent 处理。

语音识别在 OpenClaw 工具层自动完成，agent 收到的是文字。

### TTS（文字 → 语音）

agent 回复文字后，如需以语音发送，调用 `send_voice_reply.mjs` 手动发送 Telegram 语音消息：

```bash
node /path/to/voice-tts/scripts/send_voice_reply.mjs \
  --text "你的回复内容" \
  --chat-id 8317347201 \
  --agent main
```

---

## 快速安装

### 方式一：一键安装（推荐）

```bash
# 默认安装 turbo 模型
bash /path/to/voice-tts/install.sh

# 国内加代理
bash /path/to/voice-tts/install.sh --proxy http://127.0.0.1:7897
```

### 方式二：手动安装

```bash
pip install edge-tts whisper click
brew install ffmpeg   # macOS
sudo apt install -y ffmpeg  # Ubuntu
```

安装完成后运行冒烟测试：

```bash
bash tests/smoke.sh
```

---

## 配置（可选）

`config.default.json` 已包含所有默认值，**不填配置可直接使用**。

如需自定义 agent 音色映射或 ASR 参数，在 `openclaw.json` 的 `skills.entries.voice-tts.config` 中覆盖：

```json
{
  "skills": {
    "entries": {
      "voice-tts": {
        "enabled": true,
        "config": {
          "tts": {
            "defaultVoice": "zh-CN-XiaoxiaoNeural",
            "agentVoices": {
              "main":       "zh-CN-XiaoxiaoNeural",
              "researcher": "zh-CN-YunxiNeural",
              "product":    "zh-CN-XiaoyiNeural",
              "coder":      "zh-CN-YunyangNeural",
              "devops":     "zh-CN-YunjianNeural"
            }
          },
          "asr": {
            "defaultInitialPrompt": "以下是中文语音转文字。常见词包括：管家、研究员、邮差、码农、产品、运维、OpenClaw、小爱、Telegram。",
            "defaultTemperature": 0,
            "conditionOnPreviousText": true
          }
        }
      }
    }
  }
}
```

修改后执行 `openclaw gateway restart`。

---

## 核心脚本

### 语音合成 — `bin/voice-tts.mjs`

将文字转为语音文件：

```bash
# 基本用法
node bin/voice-tts.mjs "你好" -f /tmp/demo.mp3

# 指定 agent 音色
node bin/voice-tts.mjs "你好" -f /tmp/demo.mp3 --agent main

# 指定声音 / 语速
node bin/voice-tts.mjs "你好" -f /tmp/demo.mp3 -v zh-CN-YunxiNeural -r +10%
```

可用中文音色：`zh-CN-XiaoxiaoNeural`（女声，推荐）、`zh-CN-YunxiNeural`、`zh-CN-XiaoyiNeural`、`zh-CN-YunyangNeural`、`zh-CN-YunjianNeural`、`zh-CN-XiaomoNeural`

### 语音识别 — `bin/voice-asr.mjs`

将音频文件转文字：

```bash
# 基本用法
node bin/voice-asr.mjs audio.ogg

# 指定模型 / 语言
node bin/voice-asr.mjs audio.ogg --model turbo --language zh

# 输出 JSON（含语言检测）
node bin/voice-asr.mjs audio.ogg --json
```

可用模型：`tiny` `base` `small` `turbo` `large-v3`

### 发送 Telegram 语音 — `scripts/send_voice_reply.mjs`

一键完成"文字 → TTS 合成 → Telegram 语音消息发送"：

```bash
node scripts/send_voice_reply.mjs \
  --text "已收到！" \
  --chat-id 8317347201 \
  --agent main
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--text` | ✅ | 要语音播报的文字内容 |
| `--chat-id` | ✅ | Telegram 目标用户 ID |
| `--agent` | 否 | agent id，自动选对应音色 |
| `--voice` | 否 | 覆盖默认音色，如 `zh-CN-YunxiNeural` |
| `--rate` | 否 | 语速，如 `+10%`、`-5%` |
| `--token` | 否 | 直接指定 Telegram Bot Token |

**Token 自动查找优先级：**
1. `--token` 参数
2. `openclaw.json → channels.telegram.accounts.<当前agent>.botToken`
3. `openclaw.json → channels.telegram.accounts.default.botToken`
4. 环境变量 `TELEGRAM_BOT_TOKEN`

---

## 文件结构

```
voice-tts/
├── SKILL.md                      # 本文档
├── config.default.json           # 默认配置（直接可用，不需修改）
├── install.sh                    # 一键安装脚本
│
├── bin/
│   ├── voice-tts.mjs             # TTS 入口
│   └── voice-asr.mjs             # ASR 入口
│
├── lib/
│   ├── config.mjs                # 配置读取（支持 openclaw.json 覆盖）
│   ├── errors.mjs                 # 统一错误码 + 用户兜底消息
│   └── audio.mjs                 # 音频校验
│
├── scripts/
│   ├── send_voice_reply.mjs      # Telegram 语音发送（核心）
│   └── auto_voice_check          # 批量处理未处理语音
│
└── tests/
    └── smoke.sh                   # 冒烟测试
```

> **注意：** `scripts/edge_tts` 和 `scripts/whisper` 是内部 Python 封装，非直接入口；直接使用上表中的 `bin/` 入口即可。

---

## 错误码

| 错误码 | 含义 | 用户兜底消息 |
|--------|------|-------------|
| `no_file_path` | 未提供音频文件 | 抱歉，没有收到音频文件，请重试。 |
| `file_not_found` | 文件不存在 | 抱歉，音频文件没找到，请重试。 |
| `file_empty` | 文件为空 | 抱歉，音频文件是空的，请重试。 |
| `file_too_small` | 文件过小 | 抱歉，音频文件不完整，请重试。 |
| `file_stale` | 文件过期 | 抱歉，音频文件已过期，请重试。 |
| `transcription_failed` | Whisper 转写失败 | 抱歉，语音识别失败了，请重试。 |
| `synthesis_failed` | Edge TTS 生成失败 | 抱歉，语音生成失败了，请重试。 |
| `timeout` | 执行超时 | 抱歉，处理超时了，请稍后重试。 |

---

## 语音文件自动归档

`voice-asr.mjs` 成功转写后，自动将原文件从 `~/.openclaw/media/inbound/` 复制到 **agent workspace** `media/inbound/`，然后删除原文件。

- ✅ 成功时：复制归档，删除原文件
- ❌ 失败时：保留原文件，可重试

---

## 故障排查

```bash
# 检查依赖
ffmpeg -version
python3 -c "import edge_tts; print('edge-tts ok')"
python3 -c "import whisper; print('whisper ok')"

# 检查未处理语音文件
ls -la ~/.openclaw/media/inbound/

# 直接测试 ASR
node bin/voice-asr.mjs ~/.openclaw/media/inbound/your-file.ogg

# 直接测试 TTS
node bin/voice-tts.mjs "测试" -f /tmp/test.mp3

# 运行冒烟测试
bash tests/smoke.sh
```

常见问题：
- **TTS 生成失败**：检查 `python3 -c "import edge_tts; print('ok')"`
- **Telegram 发送失败**：确认 botToken 正确、chat-id 是数字 ID、语音文件 < 20MB
- **语音发错对象**：检查 `conversationId` 是否与预期 chat-id 一致

---

## 可选：批量处理未处理语音

```bash
node scripts/auto_voice_check
```

检查 `~/.openclaw/media/inbound/` 下未处理的 `.ogg` 文件，自动转写并归档。
