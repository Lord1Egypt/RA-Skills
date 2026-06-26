# 输出文档模板

## 输出文件路径

`{BASE_DIR}/{YYYYMMDD}/{subreddit_name}/{subreddit_name}-{YYYYMMDD}.md`

## 文档结构

```markdown
---
title: "r/{subreddit_name} 每日精选 - {YYYY-MM-DD}"
date: {ISO 8601}
description: "r/{subreddit_name} 最近 24 小时热门 Post 摘要与深度解读"
tags:
  - Reddit
  - {subreddit_name}
  - Daily Digest
categories:
  - 技术
---

# r/{subreddit_name} 每日精选 - {YYYY-MM-DD}

> 本文精选 r/{subreddit_name} 最近 24 小时热门 Post，为每篇提供摘要、核心要点、可实践建议、灵感启发及社交媒体分享文案。

---

### 1. [Post 标题]

> 链接：[url]
> 👍 [upvotes] | 💬 [comments] | 作者：[author]

#### 摘要
3-5 句话总结 Post 内容及评论区核心讨论，准确、信息密度高。

#### 核心要点
- （3-5 个关键要点，综合 Post 原文和高质量评论）

#### 可实践建议
2-3 条可立即付诸行动的具体建议。

#### 灵感启发
思维模型、跨领域启发、值得深入探索的方向。1-2 段。

#### 社交媒体分享文案

**即刻：** 口语化、有观点、适度 emoji、200 字以内，含 #Reddit热门 #{subreddit_name}

**小红书：** 标题党风格标题 + 正文，善用 emoji，300 字以内，带话题标签

**Twitter/X：** 简洁有力，280 字符以内，带 hashtag

### 2. ...（依此类推）

---

## 小结

（今日整体观察：社区热议话题、共同趋势、值得关注的讨论方向。3-5 句话。）
```

## 低价值 Post 筛选规则

剔除以下类型，仅在临时文件中记录标题和原因：
- 纯 meme / 表情包 / 无实质讨论
- 重复搬运、无原创观点
- 评论区全为 bot 回复或无有效互动
- 内容琐碎（如"大家好我是新人"）
