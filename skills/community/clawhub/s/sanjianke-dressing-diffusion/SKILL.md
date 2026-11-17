---
name: dressing-diffusion
slug: dressing-diffusion
displayName: 三剪客 · AI换装
description: "智能图片换装，上传模特图和服装图，AI 自动完成试穿效果生成。支持上衣、下装、全身换装。模型可在后台 extra_config 中切换。支持 提交换装任务、查询换装结果。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.6
summary: "「AI换装」的完整调用封装：2 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 换装
  - 图像生成
---

# AI换装

`api.a7w.cn` 插件 **`dressing_diffusion`**，共 **2 个接口**。提交图片换装任务，返回 task_id 用于查询结果

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema dressing_diffusion

# 3. 调用（示例）
python3 scripts/client.py call dressing_diffusion submit --json '{"garment": {}, "model_url": "https://example.com/model.jpg"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `submit` | 提交换装任务 | 异步 | 按次固定价 0.1 点（租户价） |
| `query` | 查询换装结果 | 同步 | 免费 |

## 接口详情

### `submit` · 提交换装任务submit### `query` · 查询换装结果querysubmit