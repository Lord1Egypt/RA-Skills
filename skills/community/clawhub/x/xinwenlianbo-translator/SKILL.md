---
name: xinwenlianbo-translator
description: "This skill translates CCTV XinWenLianBo (新闻联播) official language into plain Chinese that educated general audiences can understand. It fetches daily XinWenLianBo transcripts from tv.cctv.com, decodes bureaucratic rhetoric, identifies policy signals, and produces structured summaries. Use this skill when the user asks to read, translate, explain, or summarize XinWenLianBo content, or when the user references 新闻联播/新闻联播翻译/联播解读."
---


# XinWenLianBo-Translator

## Overview

《新闻联播》是央视每日 19:00 播出的旗舰新闻节目，使用自成体系的官方话语体系传递国家政策信号。此 skill 将其内容转换为受过高等教育但对政务不甚了解的普通公众可读的内容。

## When to Use

- 用户要求翻译、解读、总结《新闻联播》内容
- 用户提及"新闻联播""联播""xwlb""xinwenlianbo"
- 用户想了解某日国家重大政策动向
- 用户提供了《新闻联播》文字稿要求解读

## Workflow

### 1. 获取新闻稿

**主页地址**: `https://tv.cctv.com/lm/xwlb/index.shtml`

获取方式：
- 使用 `web_fetch` 抓取主页，提取当天的新闻链接列表
- 页面结构：每条新闻以 `<a>` 链接呈现，URL 格式为 `https://tv.cctv.com/YYYY/MM/DD/VIDExxxxxx.shtml`
- 每条链接同时包含视频和完整文字稿
- 逐条访问链接，提取正文文字内容（以"央视网消息（新闻联播）"开头）
- 如需历史内容，可修改 URL 中的日期路径或使用页面的日历选择器

**获取策略**：
- 先抓取主页获取当天所有新闻条目的标题和链接
- 根据用户需求决定翻译全部新闻还是特定条目
- 对每条新闻，使用 `web_fetch` 访问其详情页，提取文字稿正文

### 2. 识别新闻类型

每条新闻稿需首先归类，不同类型的翻译策略不同：

| 类型 | 特征 | 翻译重点 |
|------|------|----------|
| **领导人活动** | 包含"XX强调""XX指出""XX会见" | 提取核心政策信号，解释措辞等级 |
| **政策发布** | 包含"意见""方案""规划""通知" | 解释政策内容和影响范围 |
| **经济数据** | 包含具体数字、百分比、增长/下降 | 数据可视化，趋势解读 |
| **外交活动** | 包含"会见""会谈""访问" | 分析外交关系走向 |
| **突发事件** | 包含"灾害""事故""救援" | 事件经过和官方应对 |
| **典型报道** | "新思想引领新征程"等系列 | 背后的政策导向 |
| **国际新闻** | 不含中国元素的海外事件 | 简要背景说明 |

### 3. 翻译与解读

这是核心步骤。对每条新闻执行以下处理：

#### 3.1 话术解码

读取 `references/xinwenlianbo-jargon-dictionary.md` 获取术语对照表。对新闻稿中出现的官方表述进行解码，将"说的是什么"转化为"实际意味着什么"。

#### 3.2 结构解析

读取 `references/xinwenlianbo-structure-guide.md` 了解《新闻联播》的叙事结构和信号体系。识别：
- 该条新闻在节目中的编排位置（头条 vs 中段 vs 尾段）意味着什么
- 用词选择传达了什么信号强度
- 与近期其他新闻的关联

#### 3.3 翻译输出

对每条新闻生成结构化输出：

```markdown
## [简明标题]

**原文标题**: [原标题]

### 一句话解读
[用一句大白话解释这条新闻的核心意思]

### 关键信息
- **是什么**: [事实陈述]
- **意味着什么**: [政策/趋势解读]
- **对你有什么影响**: [对普通人的实际影响]

### 话术对照
| 官方表述 | 通俗翻译 |
|----------|----------|
| ... | ... |

### 背景（可选）
[帮助理解所需的背景知识，仅在必要时提供]
```

### 4. 输出日度总结

在所有条目翻译完成后，生成日度总结：

```markdown
# 《新闻联播》XX年XX月XX日 通俗解读

## 今日要点（3-5条）
[按重要性排序的核心信息]

## 分条解读
[各条新闻的翻译内容]

## 信号雷达
[基于新闻编排和用词，分析当前政策风向]

---
*解读基于《新闻联播》文字稿，仅供参考。*
```

## Key Principles

1. **忠实原文，不增不减**：翻译基于文字稿原文，不添加个人观点，不遗漏重要信息
2. **通俗但不降智**：目标读者受过高等教育，只是不熟悉政务话语体系，不要过度简化
3. **区分事实与解读**：明确标注哪些是新闻事实，哪些是翻译者的分析
4. **注重信号而非琐碎**：重点解读政策信号和大趋势，不过度解读日常报道
5. **保持中立**：不做价值判断，只做语言翻译和背景解读
6. **标注不确定性**：当解读存在多种可能性时，如实标注

## Resources

### references/
- `xinwenlianbo-jargon-dictionary.md` — 官方话术与通俗表达对照词典
- `xinwenlianbo-structure-guide.md` — 《新闻联播》节目结构与信号体系指南
