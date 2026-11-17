---
name: music-generation-kit
slug: music-generation-kit
displayName: 三剪客 · 音乐生成
description: "音乐生成应用，支持歌曲生成、歌词生成、参考音频、声音克隆、音频导出和分轨处理。支持 歌词混合、人声处理、优化音乐风格、导出 MIDI、歌词时间轴、导出 MP4、导出 WAV、声音克隆。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.0.6
summary: "「音乐生成」的完整调用封装：13 个接口的官方文档、参数表与一个零依赖客户端。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 音乐生成
  - 音频
---

# 音乐生成

`api.a7w.cn` 插件 **`music_generation`**，共 **13 个接口**。将两段歌词融合为新的混合版本。

本 Skill 是它的完整调用封装：逐接口参数表、平台官方文档摘录、真实计费口径，以及一个零依赖、可直接跑的 `client.py`。

## 快速开始

```bash
# 1. 配置你自己的 api.a7w.cn API Key（只需一次）
python3 scripts/client.py login --key sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema music_generation

# 3. 调用（示例）
python3 scripts/client.py call music_generation mashup_lyrics --json '{}'
```

> **没有 Key？** 见 `references/getting-started.md`——注册、充值、取 Key 的完整步骤。也可以直接去 [算力集市](https://api.a7w.cn/) 注册。

## 接口一览

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `mashup_lyrics` | 歌词混合 | 同步 | 按次固定价 12 点（租户价） |
| `vox` | 人声处理 | 异步 | 按次固定价 14 点（租户价） |
| `style` | 优化音乐风格 | 同步 | 按次固定价 14 点（租户价） |
| `midi` | 导出 MIDI | 异步 | 按次固定价 14 点（租户价） |
| `timing` | 歌词时间轴 | 同步 | 免费 |
| `mp4` | 导出 MP4 | 同步 | 按次固定价 20 点（租户价） |
| `wav` | 导出 WAV | 异步 | 按次固定价 14 点（租户价） |
| `voice_clone` | 声音克隆 | 同步 | 按次固定价 20 点（租户价） |
| `persona` | 创建歌手风格 | 同步 | 按次固定价 12 点（租户价） |
| `upload_audio` | 上传参考音频 | 同步 | 按次固定价 13 点（租户价） |
| `lyrics` | 生成歌词 | 同步 | 按次固定价 12 点（租户价） |
| `query` | 查询音乐任务 | 同步 | 免费 |
| `create` | 创建音乐任务 | 异步 | 按次固定价 65 点（租户价） |

## 接口详情

### `mashup_lyrics` · 歌词混合mashup_lyrics### `vox` · 人声处理vox### `style` · 优化音乐风格style### `midi` · 导出 MIDImidi### `timing` · 歌词时间轴timing### `mp4` · 导出 MP4mp4### `wav` · 导出 WAVwav### `voice_clone` · 声音克隆voice_clone### `persona` · 创建歌手风格persona### `upload_audio` · 上传参考音频upload_audio### `lyrics` · 生成歌词lyrics### `query` · 查询音乐任务query### `create` · 创建音乐任务createmashup_lyrics