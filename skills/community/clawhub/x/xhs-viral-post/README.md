# XiaoHongShu Viral Post Generator

AI 一键生成小红书爆款笔记（标题、正文、标签、封面提示词、发帖策略），并通过 SkillPay 按次计费。

## Requirements

必须配置以下环境变量：

- `OPENAI_API_KEY`
- `SKILLPAY_KEY`

用途说明：

- `OPENAI_API_KEY`：用于调用 OpenAI API 进行文案生成。
- `SKILLPAY_KEY`：用于调用 SkillPay API 完成每次执行扣费。

## Features

- 趋势关键词发现（公开关键词 API + 本地模拟兜底）
- GPT-4o 真实小红书风标题与正文生成
- 标签热度排序（Top 5）
- 封面图 AI 提示词（Midjourney / DALL-E 友好）
- 发帖策略（最佳时间 / 目标人群 / 互动钩子）

## Security / Compliance

本 Skill 的外部访问：

- OpenAI API（内容生成）
- Public Keyword API（趋势词）
- SkillPay API（计费）

本 Skill 不读取本地文件，不扫描本地目录，不访问本地 secrets 文件。

## Billing

- Billing provider: `SkillPay`
- SkillPay ID: `66d32381-4e78-4593-9309-63576e85a8b7`
- Price: `0.05 USDT / execution`

说明：每次调用会先请求 SkillPay 扣费，扣费成功后才执行生成逻辑。

## Usage

Input:

```json
{
  "topic": "夏日通勤穿搭"
}
```

Output:

```json
{
  "title": "...",
  "content": "...",
  "hashtags": ["#...", "#...", "#...", "#...", "#..."],
  "coverPrompt": "...",
  "strategy": {
    "bestTime": "20:10",
    "audience": "22-30 一二线通勤女生",
    "hook": "正文最后加一句“要不要我出对比版？”提高评论率。"
  }
}
```
