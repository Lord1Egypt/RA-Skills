---
name: happy-horse-video
slug: happy-horse-video
displayName: 三剪客 · Happy Horse
description: "Happy Horse（HappyHorse-1.1 系列）面向文生/图生高质量短视频，采用统一多模态建模，可一阶段生成声画、支持多语言对白与多镜头场景衔接。计费按目标分辨率与生成秒数对应的参数档位计点。本能力为内测邀请制，正式调用前需完成内测申请。支持 提交任务、创建任务、查询任务。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.4
summary: "「Happy Horse」的完整调用封装：3 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 文生视频
  - 视频生成
---

# Happy Horse

`api.a7w.cn` 插件 **`happy_horse`**，共 **3 个接口**。提交文生/图生视频任务（矩阵点数/秒 × 目标时长，内测中）

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema happy_horse

# 3. 调用（示例）
python3 scripts/client.py call happy_horse submit --json '{"seed": 42, "media": [{"url": "https://example.com/input.mp4", "type": "video"}, {"url": "https://example.com/ref1.jpg", "type": "image"}], "model": "happyhorse-1.1-t2v", "ratio": "16:9", "prompt": "一只猫在草地上奔跑", "watermark": true}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `submit` | 提交任务 | 异步 | 免费 |
| `create` | 创建任务 | 异步 | 免费 |
| `query` | 查询任务 | 同步 | 免费 |

## 接口详情

### `submit` · 提交任务submit### `create` · 创建任务create### `query` · 查询任务querysubmit