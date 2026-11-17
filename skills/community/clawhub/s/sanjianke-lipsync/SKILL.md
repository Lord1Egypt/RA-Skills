---
name: lipsync
slug: lipsync
displayName: 三剪客 · 数字人对口型
description: "数字人对口型（Lipsync），任务由平台弹性部署调度。支持 提交任务、查询任务。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.4
summary: "「数字人对口型」的完整调用封装：2 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 口型同步
  - 数字人
---

# 数字人对口型

`api.a7w.cn` 插件 **`lipsync`**，共 **2 个接口**。创建一条数字人对口型任务，返回平台任务 ID

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema lipsync

# 3. 调用（示例）
python3 scripts/client.py call lipsync submit --json '{"audio_url": "https://example.com/speech.wav", "video_url": "https://example.com/avatar_video.mp4"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `submit` | 提交任务 | 异步 | 以站内计费为准 |
| `query` | 查询任务 | 同步 | 免费 |

## 接口详情

### `submit` · 提交任务submit### `query` · 查询任务querysubmit