---
name: wan-video
slug: wan-video
displayName: 三剪客 · Wan 视频生成
description: "Wan 模型族视频生成应用。版本通过 model 参数选择，支持文生视频、角色参考生视频与视频编辑。支持 查询视频任务、创建视频任务。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.6
summary: "「Wan 视频生成」的完整调用封装：2 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 视频生成
  - 文生视频
---

# Wan 视频生成

`api.a7w.cn` 插件 **`wan`**，共 **2 个接口**。按平台 task_id 查询 Wan 任务状态与结果。

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema wan

# 3. 调用（示例）
python3 scripts/client.py call wan query --json '{"task_id": "task_xxxxxxxxxxxx"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `query` | 查询视频任务 | 同步 | 免费 |
| `create` | 创建视频任务 | 异步 | 免费 |

## 接口详情

### `query` · 查询视频任务query### `create` · 创建视频任务createquery