---
name: three-sentence-summary
display_name: 三句话摘要
display_name_zh: 三句话摘要
display_name_en: Three-Sentence Summary
description: This skill should be used when the user wants long content compressed into an extremely short summary — including phrases like "三句话总结", "一句话说清", "太长不看", "简单说说", "结论是什么", "TL;DR", "sum it up in three sentences". It compresses any article, meeting, or transcript into exactly three sentences.
description_en: This skill should be used when the user wants long content compressed into an extremely short summary — including phrases like "summarize in three sentences", "give me the bottom line", "too long didn't read", "TL;DR", "what's the conclusion", or any request to condense long content drastically. It compresses any article, meeting, or transcript into exactly three sentences.
description_zh: 当用户要把长内容压缩成极短摘要时使用，包括「三句话总结」「一句话说清」「太长不看」「简单说说」「结论是什么」等表达。本技能把任何长文、长会、长视频压成 3 句，每句不超过 30 字。
version: "1.0.0"
category: 知识与学习
agent_created: true
---

# 三句话摘要

任何长度、任何内容，都压成 **3 句话**。

## 何时使用

- 「三句话总结 / 三句话讲清 / 一句话说说」
- 「太长不看 / 简单说 / 结论是什么」
- 用户贴了一段长文、长会议记录、长视频字幕

## 不适用场景

- 用户要详细分析（「帮我逐条分析」）
- 内容本身很短（少于 200 字），压了没意义

## 核心方法

### 三句话的分工（固定，不可变）

| 句 | 回答 | 字数 |
|---|---|---|
| 第 1 句 | 这是什么 | ≤ 30 字 |
| 第 2 句 | 关键结论是什么 | ≤ 30 字 |
| 第 3 句 | 对你要做什么 | ≤ 30 字 |

### 硬约束

- **每句 ≤ 30 字**，总长 ≤ 100 字
- 不写「本文介绍了……」这种套话
- 保留最关键的数字和名字，其余全部砍掉
- 第 3 句必须落到行动或影响，不能只是复述

### 如果内容真的压不进 3 句

说明素材里有 2 个以上独立主题 → 输出两组「3 句话」，各自标注主题名。

## 输出模板

```
① [这是什么]
② [关键结论]
③ [对你的影响 / 下一步]
```

## Few-shot 范例

### 例 1：一份 5000 字的行业报告（关于 AI 芯片）

```
① AI 芯片需求两年翻了三倍，主要来自大模型训练。
② 但产能卡在先进封装，明年仍然供不应求。
③ 如果你在看相关标的，关注封装环节，不是设计。
```

### 例 2：一场 1 小时的会议记录

```
① 会上讨论三季度目标，最终定为营收增长 15%。
② 分歧在要不要砍掉低毛利老产品线，没定。
③ 你要在周五前补一份老产品线的毛利数据。
```

## 兜底话术

- 如果用户只给了一句话素材（信息量太少），老实说：「这个信息量不足 3 句，我只能给你 1 句：[给出]。要 3 句的话，请把原文发我。」
- 如果素材里有明显矛盾，在 3 句后面加一行「⚠️ 原文第 X 段和第 Y 段说法不一致」，但主体仍保持 3 句。
- 如果用户明确说「只要结论」→ 只给第 2 句，并说明「按你要求只保留结论」。
