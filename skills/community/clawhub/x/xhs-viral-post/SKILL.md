---
name: xhs-viral-post
description: AI 一键生成小红书爆款笔记（标题、正文、标签、封面提示、发帖策略）。真实种草风，防封号友好。
version: 1.1.0
author: ArthuronAI
triggers:
  - 小红书笔记
  - xhs post
  - 发小红书
  - xiaohongshu viral
user-invocable: true
pricing:
  skillpay: 66d32381-4e78-4593-9309-63576e85a8b7   # SkillPay ID
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY     # Required for content generation
        - SKILLPAY_KEY       # Required for paid billing per call
    primaryEnv: OPENAI_API_KEY
    emoji: "🌸"
---

# XiaoHongShu Viral Post Generator

面向 OpenClaw / ClawHub 的小红书爆款笔记生成 Skill。

## Requirements

必须配置的环境变量：

- `OPENAI_API_KEY`
- `SKILLPAY_KEY`

用途说明：

- `OPENAI_API_KEY`：用于调用 OpenAI API 生成标题与正文。
- `SKILLPAY_KEY`：用于调用 SkillPay 计费接口，按次扣费。

## Security & External APIs

本 Skill 的网络行为如下：

- 调用 OpenAI API（内容生成）。
- 调用公开关键词 API（趋势关键词发现）。
- 调用 SkillPay API（每次执行计费）。

本 Skill 不读取本地文件，不扫描本地目录，不访问除环境变量外的本地敏感信息。

## Pricing

- 价格：`0.05 USDT / 次`
- SkillPay ID：`66d32381-4e78-4593-9309-63576e85a8b7`

## Input

```json
{
  "topic": "夏日通勤穿搭"
}
```

## Output

```json
{
  "title": "...",
  "content": "...",
  "hashtags": ["#...", "#...", "#...", "#...", "#..."],
  "coverPrompt": "...",
  "strategy": {
    "bestTime": "20:30",
    "audience": "...",
    "hook": "..."
  }
}
```

## Runtime Pipeline

1. 获取趋势关键词
2. 调用 GPT-4o 生成标题与正文
3. 生成并排序标签
4. 生成封面图提示词
5. 生成发帖策略
6. 调用 SkillPay 扣费
