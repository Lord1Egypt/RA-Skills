---
name: voice-tts-studio
slug: voice-tts-studio
displayName: 三剪客 · 语音TTS
description: "语音克隆、文字转语音（同步/异步）、语音识别等多端点 AI 语音能力。支持 文字转语音（Live·异步）、克隆音色、文字转语音、文字转语音（异步）、语音转文字、音色列表。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.6
summary: "「语音TTS」的完整调用封装：6 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 语音合成
  - 音色克隆
  - TTS
---

# 语音TTS

`api.a7w.cn` 插件 **`voice_tts`**，共 **6 个接口**。WebSocket 流式上游，长文本异步合成；返回 task_id，由 fish_tts:worker 执行

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema voice_tts

# 3. 调用（示例）
python3 scripts/client.py call voice_tts tts_live --json '{"text": "<text>"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `tts_live` | 文字转语音（Live·异步） | 异步 | 输入 50 点/1k tokens（租户价） |
| `clone_voice` | 克隆音色 | 同步 | 按次固定价 200 点（租户价）；标准价 50 点 |
| `tts` | 文字转语音 | 同步 | 输入 50 点/1k tokens（租户价） |
| `tts_async` | 文字转语音（异步） | 异步 | 输入 50 点/1k tokens（租户价） |
| `stt` | 语音转文字 | 同步 | 按次固定价 30 点（租户价） |
| `list_voices` | 音色列表 | 同步 | 免费 |

## 接口详情

### `tts_live` · 文字转语音（Live·异步）tts_live### `clone_voice` · 克隆音色clone_voice### `tts` · 文字转语音tts### `tts_async` · 文字转语音（异步）tts_async### `stt` · 语音转文字stt### `list_voices` · 音色列表list_voicestts_live