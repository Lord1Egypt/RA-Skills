# 🦞 OpenClaw + QQBot 本地 STT（语音转文字）完整配置教程-HTTP 服务方式

> 使用 **Qwen3-ASR** 模型，在本地运行语音识别服务，让你的 QQ 机器人能够听懂语音消息。

---

## 📋 架构概览

```
QQ 发语音 → QQBot 插件收到音频 → 调用本地 STT 服务转文字 → 文字交给 AI 处理 → 回复
                                         ↓
                            http://127.0.0.1:8787/v1/audio/transcriptions
                                         ↓
                              Qwen3-ASR 模型（本地运行）
```

---

## 第一步：安装 local-stt 技能

```bash
# 进入 OpenClaw 技能目录
cd ~/.openclaw/skills/

# 克隆 local-stt 技能（如果还没有的话）
# 或通过 ClawHub 安装
npx clawhub@latest install local-stt
```

确认技能目录存在：

```bash
ls ~/.openclaw/skills/local-stt/
```

---

## 第二步：启动本地 STT 服务

local-stt 技能内含一个 `server.py`，它会加载 Qwen3-ASR 模型并启动一个 OpenAI 兼容的 HTTP 服务。

```bash
cd ~/.openclaw/skills/local-stt

# 安装 Python 依赖（首次运行）
pip install -r requirements.txt

# 启动服务
python server.py
```

> 模型首次运行会自动从 HuggingFace 下载 `Qwen/Qwen3-ASR-0.6B`（约 1.2GB）。

### 验证服务是否正常

```bash
# 检查健康状态
curl http://127.0.0.1:8787/
# 期望输出: {"status":"ok","model":"Qwen/Qwen3-ASR-0.6B"}

# 测试转写接口（准备一个 wav 测试文件）
curl -X POST http://127.0.0.1:8787/v1/audio/transcriptions \
  -F "file=@test.wav" \
  -F "model=Qwen/Qwen3-ASR-0.6B"
```

---

## 第三步：配置 OpenClaw（⭐ 关键步骤）

编辑配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

### ✅ 正确配置方式：在 `channels.qqbot.stt` 中直接写 `baseUrl`

```json
{
  "models": {
    "providers": {
      // ✅ 这里不需要添加 local-stt provider
      // 保留你原有的 LLM provider 即可，例如：
      "qwen-portal": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [...]
      }
    }
  },
  "channels": {
    "qqbot": {
      "enabled": true,
      "appId": "你的AppID",
      "clientSecret": "你的AppSecret",
      "stt": {
        "baseUrl": "http://127.0.0.1:8787/v1",
        "apiKey": "not-needed",
        "model": "Qwen/Qwen3-ASR-0.6B"
      }
    }
  }
}
```

### ❌ 不要这样做

```json
// 错误示范：不要把 STT 服务放在 models.providers 里
"models": {
  "providers": {
    "local-stt": {                          // ← 删掉这个！
      "baseUrl": "http://localhost:8787/v1",
      "apiKey": "not-needed",
      "api": "openai-competions"            // ← 拼写错误 + schema 不兼容
    }
  }
}
```

**原因**：`models.providers` 的 schema 要求 `api` 必须是枚举值（如 `openai-completions`），且必须包含 `models` 数组。ASR 服务不是 LLM，放在这里会导致配置校验失败或 URL 拼接异常（变成 `cli/audio/transcriptions`）。

---

## 第四步：校验配置并重启

```bash
# 校验配置文件
openclaw config validate

# 重启网关
openclaw gateway restart
```

---

## 第五步：测试

1. 打开 QQ，给你的机器人**发一条语音消息**
2. 观察日志，确认语音被成功转写：

```bash
# 查看实时日志
grep -i -E "(stt|transcri|audio|error)" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -10
```

### ✅ 成功时日志类似

```
[qqbot:xxx] deliver called, kind: block, payload keys: text, replyToId, audioAsVoice
```

### ❌ 失败时日志类似（已修复）

```
[qqbot:xxx] STT failed: TypeError: Failed to parse URL from cli/audio/transcriptions
```

---

## 🔧 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `Failed to parse URL from cli/audio/transcriptions` | STT 的 `baseUrl` 未正确配置 | 在 `channels.qqbot.stt` 中直接写 `baseUrl` |
| `Config invalid: models.providers.local-stt.api` | 把 STT 放在了 `models.providers` 里 | 删除 `models.providers.local-stt`，改用直接配置 |
| `openai-competions` 报错 | 拼写错误，少了个 `l` | 正确值是 `openai-completions`（但建议不用 provider 方式） |
| `Connection refused 127.0.0.1:8787` | STT 服务未启动 | 先 `python server.py` 启动服务 |
| 语音发了但没反应 | STT 未配置时会 fallback 到 QQ 平台内置 ASR | 检查日志确认是否走了 local-stt |

---

## 📝 配置要点总结

```
┌─────────────────────────────────────────────────────────┐
│  models.providers   →  只放 LLM 模型（Qwen、GPT 等）     │
│                        ❌ 不要放 STT 服务                │
│                                                         │
│  channels.qqbot.stt →  ✅ 直接写 baseUrl + model        │
│                        框架自动拼接为：                   │
│                        {baseUrl}/audio/transcriptions    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔗 参考资料

- [腾讯 QQ 机器人接入 OpenClaw 官方指南](https://new.qq.com/rain/a/20260316A06XBW00)
- [OpenClaw 语音功能配置详解（CSDN）](https://blog.csdn.net/yangyin007/article/details/158649849)
- [Qwen3-ASR 本地部署教程](https://blog.csdn.net/weixin_42509513/article/details/158311971)
- [QQBot 插件官方仓库](https://github.com/tencent-connect/openclaw-qqbot)

---

恭喜你成功配置！🎉 现在你的 QQ 机器人可以听懂语音消息了。 
---
name: local-stt
description: 使用 mlx-qwen3-asr 在 Apple Silicon 上进行本地语音转文字
version: 1.0.0
author: reks
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["python3", "ffmpeg"]
---

# Local STT - mlx-qwen3-asr

基于 mlx-qwen3-asr 的本地语音转文字技能，Apple Silicon 原生 MLX 加速。

## 调用方式

```bash
python3 {baseDir}/scripts/transcribe.py -f <音频文件路径>

