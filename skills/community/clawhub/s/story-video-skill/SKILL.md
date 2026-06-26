---
name: story-video
version: 1.5.1
description: >
  当用户提到以下内容时触发此技能：
  把故事做成视频、生成视频、故事视频、AI视频制作、文生视频、图生视频、剧本转视频、分镜生成、分镜头、导演分镜、编剧分析、故事分镜、需要分镜、给视频分镜、拍成视频、拍成分镜、generate video、story to video、video generation、video script、screenplay analysis、shot breakdown、scene breakdown、film directing、编剧、导演、分镜、分镜头、给个分镜

  这是一个AI视频制作流水线，覆盖从故事文本到分镜再到视频生成的全流程：
  从分析故事结构、提炼主题，到设计人物对白、构建叙事节奏；
  从编写分镜脚本、设计镜头语言，到生成视觉描述词；
  从文本到图片、图片到视频的生成，再到ffmpeg合并输出最终成片。

trigger: 故事视频|分镜|剧本|编剧分析|故事分镜|导演分镜|AI视频制作|文生视频|图生视频|generate video|story to video|video generation|shot breakdown|scene breakdown|screenplay|film directing|分镜脚本|镜头语言|视觉描述|视频成片
tags:
  - video-generation
  - storytelling
  - screenplay
  - filmmaking
  - minimax
  - story-structure
  - shot-breakdown
  - film-production
required_environment_variables:
  - MINIMAX_API_KEY
optional_environment_variables:
  - MINIMAX_BASE_URL
  - MINIMAX_IMAGE_URL
---

# story-video-skill

## 技能概述

这是一个**分镜脚本**到**完整视频**的 AI 制作流水线。

**分镜脚本：** 分析故事结构，设计人物对白，构建叙事节奏；建立人物串联线索，设计对应场景板；设计对比板式、建立人物关系图；设计对峙场面、构建起承转合。

**视频流水线：** 故事文本 → MiniMax T2I（图片生成）→ MiniMax I2V（图片转视频）→ ffmpeg 合并输出成片。

## 核心流程

```
故事文本 → 分镜JSON → T2I图片 → I2V视频 → ffmpeg合并 → 视频成片
```

### 第一步：生成shots.json

用户提供故事文本后，用 `scripts/pipeline.py` 生成 `shots.json`：

```
python3 scripts/pipeline.py "你的故事大纲或剧本"
```

输出 `output/screenplay/shots.json`，包含每个分镜的：
- `shot_number`：镜头编号
- `description`：分镜描述（画面+动作+台词）
- `visual_prompt`：视觉生成词（送入T2I）

### 第二步：生成并合并视频

用 `scripts/full_pipeline.py` 或 `scripts/full_pipeline_v2.py` 执行完整流水线：

```
export MINIMAX_API_KEY="你的key"
python3 scripts/full_pipeline.py output/screenplay/shots.json
```

流水线自动：
1. 读取 shots.json
2. 对每个分镜调用 MiniMax T2I 生成图片
3. 对每张图片调用 MiniMax I2V 生成视频
4. 用 ffmpeg 合并所有视频为单个成片

输出目录：`output/videos/`

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/pipeline.py` | 故事文本 → shots.json 分镜脚本 |
| `scripts/full_pipeline.py` | shots.json → T2I图片 → I2V视频 → ffmpeg合并 |
| `scripts/full_pipeline_v2.py` | 同上，模型版本不同 |
| `scripts/generate_shot_images.py` | 独立运行T2I图片生成 |
| `scripts/generate_shot_videos.py` | 独立运行I2V视频生成 |

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `MINIMAX_API_KEY` | ✅ | — | MiniMax API密钥 |
| `MINIMAX_BASE_URL` | ❌ | `https://api.minimaxi.com/v1` | MiniMax API地址 |
| `MINIMAX_IMAGE_URL` | ❌ | `https://api.minimaxi.com/v1/image_generation` | 图片生成端点 |

## 目录结构

```
story-video-skill/
├── SKILL.md                          # 本技能说明
├── README.md                         # 详细文档
├── output/
│   ├── frames/                      # T2I生成的图片
│   ├── videos/                      # I2V生成的视频 + 最终成片
│   └── screenplay/
│       └── shots.json               # 分镜脚本
└── scripts/
    ├── pipeline.py                  # 生成shots.json
    ├── full_pipeline.py             # 完整流水线 v1
    ├── full_pipeline_v2.py          # 完整流水线 v2
    ├── generate_shot_images.py      # T2I图片生成
    └── generate_shot_videos.py      # I2V视频生成
```

## 分镜设计原则

### 视觉叙事优先

- 每个分镜有明确的主角视线和注意力焦点
- 用「镜头角度 + 运动方式」代替「人物动作罗列」
- 优先通过场景/道具/表情暗示情绪，少用直接台词

### 分镜描述格式

```
镜头编号 | 镜头类型 | 画面描述 | 台词/声音
```

### 情绪节奏把控

- 开场30秒：建立世界规则，展示日常状态
- 中段：矛盾积累，节奏加快
- 高潮：情感爆发，动作密集
- 收束：留白，克制

## 专业知识：编剧体系

### 故事结构模板

| 三幕 | 占比 | 核心 |
|------|------|------|
| 第一幕：建置 | 25% | 开场钩子、日常世界、催化事件 |
| 第二幕：对抗 | 50% | 进展升级、中点转折、灵魂黑夜 |
| 第三幕：解决 | 25% | 高潮决战、结局收束 |

### 起承转合

| 阶段 | 功能 | 情绪 |
|------|------|------|
| 起 | 引入 | 好奇 |
| 承 | 发展 | 期待 |
| 转 | 转折 | 紧张 |
| 合 | 解决 | 满足 |

### 人物塑造

- **性格三角**：内在欲望 × 外在行为 × 他人评价
- **关系对位**：主角与对手形成镜像对照
- **成长弧线**：每个重要人物都有从A点到B点的变化

## 视觉风格指南

### 色调与光影

| 类型 | 适合场景 | 推荐色调 |
|------|----------|----------|
| 温暖怀旧 | 回忆、亲情 | 暖黄、褪色 |
| 冷峻现实 | 困境、独立 | 低饱和、冷蓝 |
| 奇幻冒险 | 超现实、梦境 | 高饱和、撞色 |
| 悬疑紧张 | 秘密、危机 | 暗调、阴影 |

### 镜头语言

| 镜头 | 适合场景 | 情绪效果 |
|------|----------|----------|
| 远景 | 建立场景 | 渺小感/史诗感 |
| 中景 | 人物互动 | 亲近感 |
| 特写 | 情绪高潮 | 冲击力 |
| 俯拍 | 命运转折 | 宿命感 |
| 仰拍 | 英雄登场 | 力量感 |

## 故障排除

### T2I 生成失败

- 检查 `MINIMAX_API_KEY` 是否有效
- 缩短 visual_prompt（过长会被截断）
- 避免敏感词（血腥/暴力内容会被拦截）

### I2V 生成卡住

- 确认 model 为 `MiniMax-Hailuo-2.3`
- 检查图片URL是否可访问（需要公网可访问的HTTP链接）

### ffmpeg 合并失败

- 确保所有视频文件完整（非0字节）
- 确认 ffmpeg 已安装：`ffmpeg -version`
- 检查视频格式是否兼容（推荐MP4/H.264）

### 速率限制

- MiniMax API 有速率限制，高并发时会429
- `full_pipeline.py` 内置 exponential backoff 重试
- 大量分镜建议分批处理
