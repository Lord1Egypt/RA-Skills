# viral-video-replicator

爆款视频复刻 — 逆向分析参考视频，生成可复刻的 Seedance 2.0 提示词

## 概述

从已有的参考视频（如竞品爆款、热门带货短视频）中逆向提取所有参数，生成可直接使用的 Seedance 2.0 复刻提示词：

1. **帧提取**：FFmpeg 3fps 采样 → 带时间戳的联系表网格图
2. **语音转录**：Seed-ASR-2.0 提取视频中的对话/旁白
3. **视觉分析**：Vision LLM 结构化分析（人物/服装/场景/动作/镜头/音频）
4. **Prompt 生成**：组装 Seedance 2.0 复刻提示词，支持 4 种素材替换模式
5. **操作手册**：即梦平台的逐步操作指引

支持单个和批量模式。每个视频独立选择复刻模式和替换素材。

## 四种替换模式

| 模式 | 上传素材 | 效果 |
|------|---------|------|
| 纯复刻 (clone) | 无 | 100% 文字描述还原，不引用任何图片 |
| 换人脸 (face_swap) | 模特参考图 | 替换人物，保留原服装 |
| 换衣服 (outfit_swap) | 衣服商品图 | 替换服装，保留原人物 |
| 全换 (full_swap) | 商品图 + 模特图 | 同时替换人物和服装 |

## 快速开始

### 安装

```bash
# Claude Code 用户
claude install-skill https://github.com/dingtom336-gif/outfit-video/tree/main/skills/viral-video-replicator
```

### 前置条件

- **本地工具**：FFmpeg + ffprobe（`brew install ffmpeg`）
- **云端 API**：火山方舟 API Key + 视觉模型（doubao-seed-1-6-vision-250815）
- **可选**：Seed-ASR-2.0 访问令牌 + TOS 对象存储密钥（视频有对话时需要）

### 使用

对 Claude 说：
- "帮我复刻这个爆款视频"
- "分析一下这个视频是怎么拍的"
- "把这个视频的衣服换成我的商品图"
- "批量分析这 3 个竞品视频"

## 降级模式

当部分服务不可用时，技能不会直接停止，而是降级运行并明确告知质量损失：

| 故障点 | 降级方式 | 质量影响 |
|--------|---------|---------|
| ASR 失败 | 仅视觉分析 | ~50% — 丢失全部对话内容 |
| Vision 精确模式失败 | 自动切换改写模式 | ~70% — 分析精度降低 |
| Vision 全部失败 | 返回原始帧图+转录 | ~20% — 需手动分析 |
| FFmpeg 不可用 | 用户手动提供截图 | ~40% — 无时间戳和均匀采样 |

## 文件结构

```
viral-video-replicator/
├── README.md                          # 本文件
├── SKILL.md                           # 核心技能逻辑
└── references/
    ├── frame-extraction.md            # FFmpeg 帧提取规范
    ├── asr-pipeline.md                # TOS 上传 + Seed-ASR-2.0 转录协议
    ├── vision-analysis.md             # Vision LLM 分析 schema（精确/改写两种模式）
    ├── reverse-prompt.md              # 4 种替换模式的 Prompt 组装规则
    └── fallbacks.md                   # 8 种故障的恢复流程
```

## 兼容性

Claude Code, Claude.ai（需本地 FFmpeg）, 以及所有兼容 SKILL.md 的 Agent。

## 关联技能

- **[fashion-video-creator](/fashion-video-creator/)** — 没有参考视频？用它从零创建穿搭视频素材

## 许可证

MIT

---

# viral-video-replicator

Viral Video Replicator — Reverse-engineer reference videos into replicable Seedance 2.0 prompts

## Overview

Extract all parameters from existing reference videos (e.g., competitor viral content, trending fashion shorts) and generate ready-to-use Seedance 2.0 replication prompts:

1. **Frame Extraction**: FFmpeg 3fps sampling → timestamped contact sheet grids
2. **Speech Transcription**: Seed-ASR-2.0 extracts dialogue/voiceover
3. **Visual Analysis**: Vision LLM structured analysis (person/clothing/scene/actions/camera/audio)
4. **Prompt Generation**: Assemble Seedance 2.0 replication prompt with 4 material replacement modes
5. **Operator SOP**: Step-by-step guide for the Jimeng (即梦) platform

Supports single and batch modes. Each video can independently choose its replication mode and replacement materials.

## Four Replacement Modes

| Mode | Upload | Effect |
|------|--------|--------|
| Clone | Nothing | 100% text-based replication, no image references |
| Face Swap | Model reference image | Replace person, keep original clothing |
| Outfit Swap | Garment product image | Replace clothing, keep original person |
| Full Swap | Garment + model images | Replace both person and clothing |

## Quick Start

### Install

```bash
# Claude Code users
claude install-skill https://github.com/dingtom336-gif/outfit-video/tree/main/skills/viral-video-replicator
```

### Prerequisites

- **Local tools**: FFmpeg + ffprobe (`brew install ffmpeg`)
- **Cloud APIs**: Volcano Engine API Key + Vision model (doubao-seed-1-6-vision-250815)
- **Optional**: Seed-ASR-2.0 access token + TOS storage credentials (needed when video has dialogue)

### Usage

Say to Claude:
- "Replicate this viral video"
- "Analyze how this video was made"
- "Replace the clothing in this video with my product image"
- "Batch analyze these 3 competitor videos"

## Degraded Modes

When some services are unavailable, the skill degrades gracefully instead of stopping, with clear quality impact warnings:

| Failure Point | Degraded Mode | Quality Impact |
|---------------|---------------|---------------|
| ASR fails | Visual-only analysis | ~50% — all dialogue content lost |
| Vision exact mode fails | Auto-switch to rewrite mode | ~70% — reduced analysis precision |
| Vision fully fails | Return raw frames + transcript | ~20% — manual analysis required |
| FFmpeg unavailable | User provides screenshots manually | ~40% — no timestamps or uniform sampling |

## File Structure

```
viral-video-replicator/
├── README.md                          # This file
├── SKILL.md                           # Core skill logic
└── references/
    ├── frame-extraction.md            # FFmpeg frame extraction specs
    ├── asr-pipeline.md                # TOS upload + Seed-ASR-2.0 transcription protocol
    ├── vision-analysis.md             # Vision LLM analysis schema (exact + rewrite modes)
    ├── reverse-prompt.md              # 4-mode prompt assembly rules
    └── fallbacks.md                   # 8 failure recovery procedures
```

## Compatibility

Claude Code, Claude.ai (with local FFmpeg), and all SKILL.md-compatible agents.

## Related Skills

- **[fashion-video-creator](/fashion-video-creator/)** — No reference video? Use this to create fashion video assets from scratch

## License

MIT
