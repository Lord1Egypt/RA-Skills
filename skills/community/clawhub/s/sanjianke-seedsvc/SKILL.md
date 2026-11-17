---
name: seedsvc
slug: sanjianke-seedsvc
displayName: 三剪客 · 音色修改、AI翻唱
description: "音色修改、AI翻唱，任务由平台弹性部署调度。支持 提交任务、查询任务。使用时需要你自己的 api.a7w.cn API Key。遇到问题可加技术微信 9872659。"
version: 1.0.5
summary: "「音色修改、AI翻唱」的完整调用封装：2 个接口的官方文档、参数表与一个零依赖客户端。需要自带 api.a7w.cn 的 API Key，调用按点数计费。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 变声
  - 音色转换
---

# 音色修改、AI翻唱

`api.a7w.cn` 插件 **`seedsvc`**，共 **2 个接口**。创建一条弹性 GPU 任务，返回平台任务 id

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema seedsvc

# 3. 调用（示例）
python3 scripts/client.py call seedsvc submit --json '{"ref_audio": "https://example.com/target_voice.wav", "source_audio": "https://example.com/original_song.wav"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `submit` | 提交任务 | 异步 | 按次固定价 0.1 点（租户价）；标准价 100 点 |
| `query` | 查询任务 | 同步 | 按次固定价 0.1 点（租户价） |

## 接口详情

### `submit` · 提交任务

**请求**：`POST /api/v1/apps/seedsvc/submit`

**模式**：异步（提交后轮询任务） ｜ **计费**：按次固定价 0.1 点（租户价）；标准价 100 点

创建一条弹性 GPU 任务，返回平台任务 id

在平台「弹性部署」对应应用中配置默认策略后，调用本接口创建 `ai_elastic_task`。 返回示例：`{ "task_id": 123, "status": "pending" }`（task_id 为弹性任务主键）

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `mode` | string | 否 | `async_query` | 任务模式，默认 async_query |
| `ref_audio` | string | **是** |  | 目标音色参考音频 URL　例：`https://example.com/target_voice.wav` |
| `source_audio` | string | **是** |  | 原始音频文件 URL，需要转换音色的音频　例：`https://example.com/original_song.wav` |

```bash
python3 scripts/client.py call seedsvc submit --json '{"ref_audio": "https://example.com/target_voice.wav", "source_audio": "https://example.com/original_song.wav"}' --no-wait
```

官方文档全文：[`references/api-submit.md`](references/api-submit.md)

### `query` · 查询任务

**请求**：`POST /api/v1/apps/seedsvc/query`

**模式**：同步（直接返回结果） ｜ **计费**：按次固定价 0.1 点（租户价）

按弹性任务 id 查询状态与结果

根据 `submit` 返回的 `task_id` 查询执行状态与结果。

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `task_id` | integer | 否 |  | 同 elastic_task_id |
| `elastic_task_id` | integer | 否 |  | 弹性任务 id（与 task_id 二选一） |

```bash
python3 scripts/client.py call seedsvc query --json '{}'
```

官方文档全文：[`references/api-query.md`](references/api-query.md)

## 参考文件

| 文件 | 用途 |
|---|---|
| `references/通用说明.md` | 权限表、异步任务机制、常见错误、能力边界、计费口径 |
| `references/getting-started.md` | 注册、充值、获取与配置 API Key |
| `references/api-submit.md` | `submit` 的平台官方文档全文 + schema 原文 |
| `references/api-query.md` | `query` 的平台官方文档全文 + schema 原文 |
| `scripts/client.py` | 通用客户端（零依赖） |

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
