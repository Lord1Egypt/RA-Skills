---
name: reading-notes
description: Use when organizing reading notes from books, articles, or papers into structured summaries and knowledge maps. Helps extract key insights, connect ideas across sources, and build a personal knowledge base using proven note-taking frameworks like Zettelkasten and Cornell method.
---

# Reading Notes Organizer & Knowledge Graph Builder

Turn scattered reading notes into a connected, searchable knowledge base.

## When to Use
- After finishing a book/article/paper
- Building a second brain or knowledge repository
- Preparing for writing, research, or presentations
- Connecting ideas across multiple sources

## Core Workflow

### Step 1: Capture (边读边记)

Use the **3-Layer Capture** method:
1. **Highlight** — verbatim quotes worth keeping
2. **Summary** — your own words for each chapter/section
3. **Reaction** — your thoughts, questions, disagreements

### Step 2: Processing Template

```markdown
# 📚 读书笔记 | Reading Note

## 基本信息
- **书名/文章:** [标题]
- **作者:** [作者名]
- **类型:** 书籍 / 文章 / 论文 / 视频
- **阅读日期:** YYYY-MM-DD
- **评分:** ⭐⭐⭐⭐⭐ (1-5)
- **推荐给:** [适合什么类型的读者]

---

## 一句话总结
> [用一句话概括核心观点，< 50字]

## 核心主张 (3-5条)
1. [主张1]: [简要解释]
2. [主张2]: [简要解释]
3. [主张3]: [简要解释]

---

## 章节摘要

### [章节名]
- **关键观点:** [1-2句]
- **重要引用:** "[原文摘录]" (p.XX)
- **我的理解:** [自己的解读]

---

## 金句收藏 | Highlights
> "[精彩句子]" — 作者名, p.XX

> "[另一句]"

---

## 知识连接 | Connections
- 与《[其他书名]》的关联: [如何呼应或对比]
- 印证了 [某个理论/概念]: [说明]
- 挑战了 [某个观念]: [说明]

---

## 行动清单 | Action Items
- [ ] [受书启发想做的事1]
- [ ] [想深入研究的方向]
- [ ] [想分享给谁]

---

## 标签 | Tags
#[主题1] #[主题2] #[领域]
```

### Step 3: 知识图谱构建

为每本书创建节点，连接相关概念：

```
[书名] → 核心概念A → 相关书籍X
              ↓
         核心概念B → 相关书籍Y
              ↓
         核心概念C → 实践项目Z
```

**连接类型:**
- `支持` — 两本书观点互相印证
- `反驳` — 观点相互对立，值得深思
- `延伸` — 一本书是另一本的深化
- `应用` — 理论书 → 实践案例

### Step 4: Zettelkasten 原子笔记法

每个概念/想法独立成卡片：

```markdown
## 卡片 ID: YYYYMMDD-001

**概念:** [一个明确的想法或观点]

**内容:** 
[2-5句话解释这个概念，用自己的话]

**来源:** 《书名》p.XX / [作者]

**链接:**
- [[相关卡片ID-1]] — [关联说明]
- [[相关卡片ID-2]] — [关联说明]

**标签:** #概念类别 #领域
```

### Step 5: 定期复习系统

| 复习周期 | 内容 |
|----------|------|
| 读完当天 | 写完整笔记，填行动清单 |
| 1周后 | 回顾核心主张，补充连接 |
| 1个月后 | 检查行动项完成情况 |
| 季度末 | 整理同主题书籍，生成主题综述 |

## 输出示例：主题综述

当积累同主题3本以上读书笔记后，生成综述：

```markdown
# 主题综述：[主题名称]

## 共识观点（多书印证）
1. [所有书都认同的核心观点]

## 争议观点（观点分歧）
- 甲方（书A, 书B）: [观点]
- 乙方（书C）: [观点]
- 我的判断: [综合结论]

## 推荐阅读顺序
1. 入门: 《书名》— 理由
2. 进阶: 《书名》— 理由
3. 深度: 《书名》— 理由
```

## 工具推荐

| 工具 | 用途 | 适合人群 |
|------|------|----------|
| Obsidian | 双链笔记+知识图谱 | 重度笔记用户 |
| Notion | 数据库+模板 | 偏好结构化 |
| 飞书文档 | 团队共享 | 职场协作 |
| 微信读书 | 电子书+划线 | 移动端阅读 |
