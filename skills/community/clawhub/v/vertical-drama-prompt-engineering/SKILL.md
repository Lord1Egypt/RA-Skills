---
name: vertical-drama-prompt-engineering
description: "竖屏短剧分镜提示词工程技能，用于在 9:16 竖屏格式下构建具有纵深感和叙事力度的 AI 分镜画面。触发词：竖屏短剧, 9:16, 分镜提示词, 竖屏构图, 竖屏分镜, 纵深构图, Z轴调度, 前后叠放, 高低落差, 透视锚定, 竖屏特写, 竖屏全景, 竖屏航拍。English: vertical short drama, 9:16 vertical format, vertical framing, depth composition, Z-axis staging, over-shoulder vertical, vertical cinematography, short drama storyboard. 适用场景：短剧平台分镜规划, AI 生图提示词编写, 竖屏构图咨询。"
---

# 竖屏短剧分镜提示词工程 / Vertical Drama Prompt Engineering

## Overview / 概述

竖屏短剧的分镜不是"把横屏画面切掉两边"——而是在一条纵深走廊里调度人物与空间。

横屏（16:9）的叙事语言依赖 X 轴横向调度：人物从左走到右，两人对话用正反打覆盖整个画面宽度。竖屏（9:16）丢失了横向宽度，必须用 **Z 轴纵深** 取代 X 轴横向，作为画面的主要叙事维度。

本技能提供：
- Z 轴纵深的分镜构建原则
- 竖屏格式下的人物位置体系
- 针对 9:16 优化的镜头类型指南
- AI 生图提示词质量检查清单

---

## Z 轴纵深规则 / Z-Axis Depth Rules

### 核心原则

| 原则 | 说明 |
|------|------|
| **纵深优先** | 以 Z 轴（前后）而非 X 轴（左右）组织画面层次 |
| **三段式深度** | 前景 / 中景 / 背景，三层必须同时存在 |
| **叠放替代覆盖** | 两人对峙用"一前一后"的 Z 轴站位，代替横屏的正反打 |
| **落差建立权力** | 高位置 = 权力/控制；低位置 = 被动/脆弱 |

### Three-Layer Depth System / 三层纵深系统

```
前景（Foreground, Z=0）    ← 主要叙事主体最近的层
中景（Midground, Z=1）      ← 主体或第二主体的层
背景（Background, Z=2）    ← 环境、群演、空间交代的层
```

竖屏 AI 生图提示词必须明确说明每层的内容和相对位置关系，不能只描述单一主体。

### 透视锚定 / Perspective Anchoring

当核心人物在 Z 轴上移动时，画面中必须包含其他人物或物体作为**空间锚点**（anchor），以维持纵深关系的可读性。

❌ 错误：一个人走在无尽走廊里，没有任何参照
✅ 正确：一个人走在走廊深处，前景有另一个人靠在门框上，形成前后关系

---

## Character Placement in Vertical Frame / 竖屏人物位置体系

### 画面分区

竖屏 9:16 可划分为：

```
┌─────────┐
│  头顶留白  │  ← 通常 10-15% 高度
├─────────┤
│   上区   │  ← 背景层（天空、天花板、远方墙面）
│  (UB/UB) │
├─────────┤
│   中区   │  ← 中景层（对话、情绪）
│  (MB/MB) │
├─────────┤
│   下区   │  ← 前景层（手势、地面、压迫感）
│  (LB/LB) │
├─────────┤
│  脚部留白  │  ← 通常 5-10%，取决于是否需要稳定感
└─────────┘
```

### 两人对峙的 Z 轴站位

不用横屏的正反打，改用纵深叠放：

- **男前女后**：男性在 Z=0 前景，女性在 Z=1 中景 → 男性占据主动/压迫位置
- **女前男后**：反向设置 → 女性主导
- **同 Z 轴平排**：用于平等对话或并肩关系
- **高台/低地落差**：楼梯、台阶、窗台是竖屏里建立权力关系的核心道具

### 高低落差法则 / Vertical Power Hierarchy

| 位置关系 | 权力语义 |
|----------|----------|
| 人物 A 在楼梯上方，人物 B 在下方仰拍 | A 主导 |
| 两人同高度，但前景 A 比背景 B 更大 | A 主动，B 被动 |
| 人物低头俯视下方（高角度） | 压迫、怜悯、冷漠 |
| 人物仰头望向高处（低角度） | 仰慕、恐惧、期待 |

---

## Shot Type Guide for Vertical / 竖屏镜头类型指南

### 1. 竖屏特写 / Vertical Close-Up (VCU)

**用途**：情绪放大、台词重点、内心独白
**构图**：人物面部占据画面 60-80% 高度，眼睛在画面上 1/3 处
**提示词要点**：

- `vertical close-up, 9:16 portrait framing`
- `head and shoulders, face fills frame`
- `eyes in upper third of frame`

### 2. 竖屏中景 / Vertical Medium Shot (VMS)

**用途**：日常对话、两人互动、部分环境
**构图**：膝盖以上取景，头顶留白 10-15%，脚部留白 5%
**提示词要点**：

- `vertical medium shot, waist-up framing`
- `two characters in depth composition, foreground and background`
- `shallow depth of field, subject sharp`

### 3. 竖屏过肩 / Vertical Over-the-Shoulder (VOTS)

**用途**：两人对话的核心镜头，竖屏替代正反打
**构图**：前景人物肩部/后脑勺占画面 30-40%，背景人物完整
**提示词要点**：

- `vertical over-shoulder shot, 9:16`
- `foreigner character's shoulder in foreground, main subject in background`
- `depth layering, shallow focus on background subject`

**重要**：前景人物不能太靠近镜头边缘，否则会显得像"乱入"。保持在画面侧边 1/3 到 1/2 处。

### 4. 竖屏低角度 / Vertical Low-Angle (VLA)

**用途**：确立角色威严、压迫感、崇拜感
**构图**：镜头置于腰部以下高度，仰视主体，背景天空或天花板
**提示词要点**：

- `low angle vertical shot, looking up`
- `dramatic upward perspective, 9:16 portrait`
- `subject against light from above`

### 5. 竖屏高角度 / Vertical High-Angle (VHA)

**用途**：表现脆弱、渺小、被动，或场景 overview
**构图**：镜头在头顶高度向下俯视
**提示词要点**：

- `high angle downward shot, 9:16`
- `bird's eye influence, vulnerable framing`
- `overhead vertical composition`

### 6. 竖屏航拍 / Vertical Aerial (VAE)

**用途**：开场、建立场景、情绪转场
**构图**：高空垂直向下，或 45° 斜向下
**提示词要点**：

- `aerial top-down view, 9:16 vertical`
- `drone shot looking straight down`
- `establishing shot, vertical format`

### 7. 竖屏纵深全景 / Vertical Depth Wide (VDW)

**用途**：交代空间、走廊感、纵深感强的环境
**构图**：前景占画面下方 20-30%，中景在画面中部，背景在画面远方
**提示词要点**：

- `vertical wide shot with deep perspective`
- `corridor depth, foreground midground background layers`
- `9:16 portrait, strong Z-axis depth`

---

## AI 提示词质量检查清单 / Quality Checklist

生成前逐项确认：

### 构图检查

- [ ] 画面有前景、中景、背景三层纵深
- [ ] 没有把横屏构图直接压缩为竖屏
- [ ] 人物头顶留白 10-15%（除非特写）
- [ ] 脚部有适当留白或稳定接地

### 叙事检查

- [ ] 两人对峙使用 Z 轴叠放而非正反打
- [ ] 权力关系通过高/低位置或前/后位置表达
- [ ] 移动镜头包含空间锚点
- [ ] 环境道具参与叙事（楼梯、门框、窗户等）

### 技术检查

- [ ] 明确标注 `9:16` 或 `vertical format` 或 `portrait mode`
- [ ] 景深关系说明（shallow focus / deep focus）
- [ ] 光线方向和质感说明
- [ ] 人物数量和位置关系说明

### 避坑检查

- [ ] 没有"一个人走在无尽走廊"的无效纵深
- [ ] 没有对称构图导致画面呆板
- [ ] 没有把所有人物放在同一 Z 轴平面上（失去纵深）
- [ ] 过肩镜头前景人物没有切到画面边缘

---

## 参考文件 / References

- `references/z-axis-depth.md` — Z 轴纵深系统详解
- `references/vertical-shot-types.md` — 竖屏镜头类型详解

---

## 关联技能 / Related Skills

- `storyboard-creation` — 分镜头设计基础
- `filmmaker` — 电影语法通用原则
- `libtv-skill` / `libtv-advanced` — AI 生图/视频生成工具对接
