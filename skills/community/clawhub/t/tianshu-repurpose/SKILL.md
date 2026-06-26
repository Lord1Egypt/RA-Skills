---
name: tianshu-repurpose
description: >
  一文多发：把长文裁剪成小红书/抖音文案/微博/公众号摘要等多平台长度与格式建议。
  Use when: 用户要「同步多平台」「精简成抖音配文」「微博短讯」「公众号标题摘要」。
  NOT for: 各平台 API 自动发布（本 skill 只产出文案结构，发布需人工或别的自动化）。
metadata:
  openclaw:
    primaryEnv: ""
---

# 一文多发 / 多平台裁剪 (tianshu-repurpose)

读取**一篇长文案**（或纯文本），按常见限制生成多段**可直接粘贴**的平台版本：字数提示、段落断句、标题/摘要占位。规则在本地执行，不调用外网 API。

## When to Run

- 「这篇转成小红书 + 抖音简介」「微博发什么」「公众号标题帮我起几个」
- 有一篇 PR 稿/博客/讲稿要拆成社交矩阵文案

## Workflow

1. 让用户提供 `.txt` / `.md` 路径，或先把正文落到文件
2. 执行：
   ```bash
   node ~/.openclaw/skills/tianshu-repurpose/scripts/repurpose.js --file /path/to/article.md
   ```
   或 `--text "..."`（短文测试）
3. 将输出中各平台区块分别复制到对应后台；需要话题标签可再接 `tianshu-xhs-note` 只做标签部分

## 参数说明

| 参数 | 说明 |
|------|------|
| `--file` / `-f` | 源文件 UTF-8 |
| `--text` / `-t` | 直接传入全文 |

## 默认裁剪规则（可在脚本内改常量）

- **小红书：** 正文约 900 字内 + 提醒首图
- **抖音配文：** 约 280 字 + 第一行「黄金一行」
- **微博：** 约 200 字（偏短传播）
- **公众号：** 标题备选 3 条 + 摘要约 120 字

## Output

stdout 为多段 Markdown，按平台分节，便于复制。
