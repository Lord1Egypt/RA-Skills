# Output Format Reference

各输出格式的模板和规则。

## Chapters（章节列表）

```
00:00 Introduction
02:15 Background and motivation
05:30 Main approach
12:45 Results and evaluation
18:20 Limitations and future work
21:00 Q&A
```

## Summary（摘要）

5-10 句话概述，覆盖视频主要观点、关键论据和结论。第三人称、现在时。

## Chapter Summaries（章节摘要）

```
## 00:00 Introduction (2 min)
Speaker introduces topic X and explains why it matters for Y.

## 02:15 Background (3 min)
Review of prior work, covering approaches A, B, and C.
```

## Thread（Twitter/X 推文）

```
1/ Just watched an incredible talk on [topic]. Here are the key takeaways: 🧵

2/ First insight: [point]. This matters because [reason].

3/ The surprising part: [unexpected finding]. Most people assume [common belief], but the data shows otherwise.

4/ Practical takeaway: [actionable advice].

5/ Full video: [URL]
```

每条 <280 字符，编号格式。

## Blog Post（博客文章）

完整文章结构：
- 标题
- 引言段落
- 每个主题的 H2 章节
- 关键引言（带时间戳）
- 结论/要点

## Structured Notes（结构化笔记）⭐ 默认格式

全面重构的 markdown 文档。不是摘要——保留几乎所有信息但重新组织结构。

### 模板

```markdown
# 视频标题
> 📺 Source: [link] ｜ UP主/Channel
> 📅 Upload date ｜ Duration
> 🤖 Transcription method

---

## 一、核心论点 (Core Thesis)
1-3 bullet points capturing the central argument

## 二、Section Title
### Sub-section
**Key point in bold**
- Supporting detail
- 💡 Insight or methodology callout (using emoji for visual scanning)

## N、总结 (Conclusion)
Tie back to the core thesis
```

### 规则

- **忠实保留**所有事实内容（人名、日期、数字、具体数据）
- 章节标题反映逻辑结构，而非简单的时间顺序
- Emoji 约定：💡 洞察/方法、⚠️ 警告/陷阱、🎯 关键结论、📊 数据/表格
- **加粗**重要名称、概念和结论
- 涉及多实体对比时，使用比较表格
- 使用视频内容相同的语言
- 量化/配置类内容（财务规划、资产配置等），末尾附汇总表（类别|比例|收益|产出）

### 交付时的附加要求

发送给用户时，除了文件本身，还附带一段简短内联摘要（3-5行高亮 + 关键信息 markdown 表格），让用户无需打开文件即可获得即时价值。

## Quotes（金句）

```
"The most important thing is not the model size, but the data quality." — 05:32
"We found that scaling past 70B parameters gave diminishing returns." — 12:18
```
