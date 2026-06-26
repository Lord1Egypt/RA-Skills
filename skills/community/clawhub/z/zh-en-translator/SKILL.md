---
name: zh-en-translator
description: "中英互译工具。支持中文与英文的双向翻译。Use when: (1) translating Chinese text to English, (2) translating English text to Chinese, (3) user asks to translate between Chinese and English, (4) user mentions 中英互译, 翻译, translate, 中译英, 英译中."
---

# 中英互译工具

提供中文与英文之间的双向翻译。

## 工作流程

1. 检测输入文本语言（中文或英文）
2. 若为中文 → 翻译为英文；若为英文 → 翻译为中文
3. 输出翻译结果，格式：原文 → 译文

## 翻译原则

- 信达雅优先，忠于原文语义
- 保持自然流畅的目标语言表达
- 专有名词、成语、俗语采用通行译法
- 保留原文语气（正式/口语/幽默等）

## 示例

输入：`周末我们一起去图书馆查阅资料吧`
输出：`Let's go to the library together this weekend to look up some materials.`

输入：`The early bird catches the worm.`
输出：`早起的鸟儿有虫吃。`
