---
name: seedance-video
slug: seedance-video
displayName: 三剪客 · Seedance 2.0
description: "基于火山方舟 Seedance 2.0 的多模态视频生成应用。支持文本/图片/视频/音频任意组合输入，可输出 480p/720p/1080p 分辨率、4~15 秒时长的视频，并可选生成同步音频。按 token 计费，按分辨率和是否含视频输入分档。支持 创建素材资产组合、上传素材、获取素材详情、更新素材、删除素材、查询任务、创建任务。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.4
summary: "「Seedance 2.0」的完整调用封装：7 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 视频生成
  - 图生视频
---

# Seedance 2.0

`api.a7w.cn` 插件 **`seedance`**，共 **7 个接口**。创建 Asset Group（素材资产组合），上传素材前需先创建分组。

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema seedance

# 3. 调用（示例）
python3 scripts/client.py call seedance createGroup --json '{"Name": "demo-group", "GroupType": "AIGC"}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `createGroup` | 创建素材资产组合 | 同步 | 免费 |
| `createAsset` | 上传素材 | 同步 | 免费 |
| `getAsset` | 获取素材详情 | 同步 | 免费 |
| `updateAsset` | 更新素材 | 同步 | 免费 |
| `deleteAsset` | 删除素材 | 同步 | 免费 |
| `query` | 查询任务 | 同步 | 免费 |
| `create` | 创建任务 | 异步 | 免费 |

## 接口详情

### `createGroup` · 创建素材资产组合createGroup### `createAsset` · 上传素材createAsset### `getAsset` · 获取素材详情getAsset### `updateAsset` · 更新素材updateAsset### `deleteAsset` · 删除素材deleteAsset### `query` · 查询任务query### `create` · 创建任务createcreateGroup