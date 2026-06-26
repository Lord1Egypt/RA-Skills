---
name: xiaoxia-image-gen
description: "通用文生图技能。使用 MiniMax、OpenAI、DALL-E、Stability 等模型生成图片。用户需要配置自己的 API Key（MINIMAX_API_KEY、OPENAI_API_KEY 等）。当用户需要生成图片、AI绘图时使用此技能。"
---

# 通用文生图技能 (xiaoxia-image-gen)

支持多种文生图模型，用户可根据需要配置不同的 API Key。

## 支持的模型

| 模型 | 环境变量 | 说明 |
|------|----------|------|
| MiniMax image-01 | `MINIMAX_API_KEY` | 推荐，性价比高 |
| OpenAI DALL-E 3 | `OPENAI_API_KEY` | 质量高 |
| Stability AI | `STABILITY_API_KEY` | 写实风格 |

## 使用方法

### 1. 配置 API Key

根据你想使用的模型，设置对应的环境变量：

```bash
# MiniMax (推荐)
set MINIMAX_API_KEY=sk-cp-xxxxx

# OpenAI
set OPENAI_API_KEY=sk-xxxxx

# Stability AI
set STABILITY_API_KEY=sk-xxxxx
```

### 2. 生成图片

在 OpenClaw 中，直接告诉我想生成什么图片，例如：
- "帮我生成一只可爱的小龙虾"
- "画一幅日落风景图"

## 示例提示词

- 可爱小龙虾：cute cartoon lobster mascot, kawaii style, orange color, big eyes
- 风景：beautiful sunset over ocean, golden hour, photorealistic
- 人物：portrait of a young woman, natural lighting, professional photography

## 技术实现

技能会根据用户配置的 API Key 自动选择可用的模型。优先顺序：MiniMax > OpenAI > Stability。

---

_🦞 虾虾团队出品_