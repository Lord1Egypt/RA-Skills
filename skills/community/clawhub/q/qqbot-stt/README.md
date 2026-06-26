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

# 🦞 OpenClaw + Qwen3-ASR-0.6B（CLI 模式）完整配置教程

> **不启动服务**，直接通过命令行脚本调用你的 Qwen3-ASR 本地模型， Telegram 生效，qqbot不生效。

---

## 📋 架构对比

```
❌ 之前的方式（需要启动服务）:
TG 发语音 → channels.*.stt → http://127.0.0.1:8787/v1 → python server.py（常驻）

✅ 现在的方式（CLI 模式，不启动服务）:
TG 发语音 → tools.media.audio → python qwen3_asr_cli.py input.wav → 输出文字（按需启动，用完退出）
```

---

## 第一步：确认 Qwen3-ASR 模型已下载

```bash
# 如果你之前已经通过 server.py 用过，模型应该已经缓存在本地了
# 默认缓存路径
ls ~/.cache/huggingface/hub/models--Qwen--Qwen3-ASR-0.6B/

# 如果没有，手动下载
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir ~/models/Qwen3-ASR-0.6B
```

---

## 第二步：确认 Python 依赖已安装

```bash
pip install transformers torch librosa soundfile
# 如果要用 vLLM 加速（可选）
# pip install qwen-asr[vllm]
```

---

## 第三步：创建 CLI 转写脚本（⭐ 核心）

创建文件 `~/.openclaw/scripts/qwen3_asr_cli.py`：

```bash
mkdir -p ~/.openclaw/scripts
nano ~/.openclaw/scripts/qwen3_asr_cli.py
```

写入以下内容：

```python
#!/usr/bin/env python3
"""
Qwen3-ASR-0.6B CLI 转写脚本
用法: python qwen3_asr_cli.py <音频文件路径>
输出: 纯文本转写结果（stdout）
退出码: 0=成功, 1=失败
"""

import sys
import os
import warnings
warnings.filterwarnings("ignore")

def main():
    if len(sys.argv) < 2:
        print("用法: python qwen3_asr_cli.py <音频文件路径>", file=sys.stderr)
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"错误: 文件不存在 {audio_path}", file=sys.stderr)
        sys.exit(1)
    
    import librosa
    import torch
    from transformers import AutoProcessor, Qwen2AudioForConditionalGeneration
    
    # ========== 模型路径配置 ==========
    # 方式1: 使用 HuggingFace 缓存（如果你之前在线加载过）
    model_id = "Qwen/Qwen3-ASR-0.6B"
    
    # 方式2: 如果你手动下载到了本地目录，改成本地路径
    # model_id = os.path.expanduser("~/models/Qwen3-ASR-0.6B")
    # ===================================
    
    # 加载模型和处理器（首次运行会缓存，后续秒加载）
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    model = Qwen2AudioForConditionalGeneration.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,  # 如果GPU显存小，用 float16
        trust_remote_code=True
    )
    
    # 加载音频文件
    audio, sr = librosa.load(audio_path, sr=processor.feature_extractor.sampling_rate)
    
    # 构造对话格式输入
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": audio_path},
            ]
        }
    ]
    
    # 使用 processor 处理
    text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    inputs = processor(text=text, audios=[audio], return_tensors="pt", padding=True)
    inputs = inputs.to(model.device)
    
    # 推理生成
    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_length=512)
    
    # 解码输出
    generated_ids = generated_ids[:, inputs.input_ids.size(1):]
    result = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    
    # 输出纯文本到 stdout（OpenClaw 会读取这个）
    print(result.strip())

if __name__ == "__main__":
    main()
```

### 设置执行权限

```bash
chmod +x ~/.openclaw/scripts/qwen3_asr_cli.py
```

### 测试脚本

```bash
# 用一个测试音频验证
python ~/.openclaw/scripts/qwen3_asr_cli.py /path/to/test.wav
# 应该直接输出转写的文字，例如：
# 你好，今天天气怎么样？
```

> ⚠️ **关键要求**：脚本必须**退出码 0** + **stdout 输出纯文本**。OpenClaw 只读取 stdout 的内容作为转写结果。

---

## 第四步：配置 OpenClaw（⭐ 关键配置）

编辑 `~/.openclaw/openclaw.json`：

```bash
nano ~/.openclaw/openclaw.json
```

### 完整配置示例

```json

  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "maxBytes": 20971520,
        "models": [
          {
            "type": "cli",
            "command": "python ~/.openclaw/scripts/qwen3_asr_cli.py {{file}}",
            "timeoutSeconds": 120
          }
        ]
      }
    }
  },

```

### 🔑 配置要点解读

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  tools.media.audio          ← 框架级配置，所有渠道共享       │
│    ├── enabled: true        ← 开启音频理解                   │
│    ├── maxBytes: 20MB       ← 最大音频文件大小               │
│    └── models:                                               │
│        └── type: "cli"      ← CLI 模式，不需要 HTTP 服务     │
│            command: "..."   ← 你的 Python 脚本               │
│            {{file}}         ← OpenClaw 自动替换为音频文件路径 │
│            timeoutSeconds   ← 超时时间（模型加载可能需要久）  │
│                                                              │
│  channels.telegram          ← 不需要配 stt！                 │
│                               框架自动使用 tools.media.audio  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 第五步：重启并验证

```bash
# 校验配置
openclaw config validate

# 重启网关
openclaw gateway restart

# 查看日志
openclaw logs --follow | grep -i -E "audio|transcri|cli|media"
```

---

## 第六步：测试

### Telegram 测试
1. 给你的 Telegram Bot 发一条**语音消息**
2. 同样会走 `tools.media.audio` → CLI 脚本 → 转写

---

## ⚡ 性能优化（可选）

### 问题：每次调用都要加载模型，太慢！

CLI 模式每次调用都会重新加载模型（~10-30秒），如果你觉得太慢，有两个优化方案：

### 方案 A：使用 `qwen-asr` 官方 CLI（推荐）

```bash
pip install qwen-asr
```

安装后你会得到一个 `qwen-asr` 命令，模型加载一次后会缓存，速度更快：

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "qwen-asr --model Qwen/Qwen3-ASR-0.6B --input {{file}}",
            "timeoutSeconds": 120
          }
        ]
      }
    }
  }
}
```

### 方案 B：写一个带「模型预加载」的守护脚本

创建 `~/.openclaw/scripts/qwen3_asr_daemon.py`，用 UNIX socket 或管道保持模型常驻内存，但这本质上又变成了"服务"模式。

### 方案 C：继续用你之前的 HTTP 服务方式 + CLI 双保险

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "python ~/.openclaw/scripts/qwen3_asr_cli.py {{file}}",
            "timeoutSeconds": 120
          }
        ]
      }
    }
  }
}
```

---

## 📊 最终对比

| | HTTP 服务方式 | CLI 方式（本教程） |
|---|---|---|
| 需要启动服务 | ✅ `python server.py` | ❌ 不需要 |
| 模型 | Qwen3-ASR-0.6B | **同一个** Qwen3-ASR-0.6B |
| 配置位置 | `channels.qqbot.stt` | `tools.media.audio` |
| 适用渠道 | **QQBot + Telegram + 所有渠道** |仅 Telegram |
| 首次转写速度 | 快（模型已常驻） | 慢（需加载模型~10-30s） |
| 后续速度 | 快 | 取决于系统缓存 |
| 内存占用 | 常驻 ~2GB | 按需使用，用完释放 |

---

## 🔧 常见问题

| 问题 | 解决方案 |
|------|---------|
| `ModuleNotFoundError: No module named 'transformers'` | `pip install transformers torch librosa soundfile` |
| 转写超时 | 增大 `timeoutSeconds` 到 180 或 300 |
| `Exit code 1` | 手动运行脚本查看 stderr 错误信息 |
| 模型每次重新下载 | 设置 `model_id` 为本地路径 |
|  Telegram 不行 | 检查 Telegram botToken 是否正确，`channels.telegram.enabled: true` |
| 想同时保留云端 fallback | 在 `models` 数组中加第二个 provider 条目 |

---

## ✅ 总结

```
你要的效果：
  ✅ 继续用 Qwen3-ASR-0.6B（你的本地模型）
  ✅ 不启动 HTTP 服务
  ✅ Telegram 能接收语音

怎么做到的：
  tools.media.audio.models → type: "cli" → python 脚本直接调用模型
  框架级配置 → 所有渠道自动生效
```

如果首次加载模型太慢是个大问题，建议安装 `pip install qwen-asr` 使用官方 CLI 工具，或者折中方案：**平时保持 server.py 运行 + channels.stt 配置，同时加上 CLI 作为 fallback**。需要我帮你配置哪种方案都可以！ 🎉
