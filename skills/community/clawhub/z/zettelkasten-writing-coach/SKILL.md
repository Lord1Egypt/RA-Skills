---
name: zettelkasten-writing-coach
description: Turn scattered notes into atomic notes, connections, and writing structure
version: v1.0.0
tags: zettelkasten, note-taking, knowledge-management, writing-coach
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":[],"env":[]}}}
---

# Zettelkasten Writing Coach

把零散摘录、想法和笔记，转成可连接、可写作、可生长的卡片盒结构。


## Usage Scenarios

### Scenario 1: Organize Scattered Notes
**User input:** "我有一堆关于阅读、记忆、元认知的摘录，不知道怎么整理。"

**Expected output:** Atomic notes breaking down each concept into single-idea cards, connection map showing relationships between concepts, cluster themes identified, and 2-3 potential article angles with thesis statements.

### Scenario 2: Find Writing Topics from Notes
**User input:** "帮我从这些笔记中找出可以写成文章的主题。"

**Expected output:** Theme clustering analysis identifying viable article topics from existing notes, each with a working title, core argument, outline of supporting notes, and suggestions for supplementary research.

### Scenario 3: Connect Existing Cards
**User input:** "这些卡片之间有什么联系？帮我建立连接。"

**Expected output:** Connection graph showing relationships between individual atomic notes, shared concepts and contrasting viewpoints highlighted, emergent themes surfaced, and suggestions for new cards that bridge gaps.
### Scenario 4: 用卡片笔记法整理读书笔记
**User input:** "我看完了《认知觉醒》这本书，想用卡片笔记法整理一下，怎么开始？"
**Expected output:** 按照Zettelkasten方法指导：1）阅读时标记3-5个最有感触的观点；2）每个观点写一张独立卡片（标签+来源+自己的理解+联想）；3）在已有卡片之间建立链接（用Obsidian/Notion/flomo实现双向链接）。给出第一张卡片示例：标签#元认知，来源《认知觉醒》P67，内容+个人感悟+联想到的《思考快与慢》。建议每天只写2-3张卡片保持可持续。

## 适用场景

- 笔记很多但写不出来
- 摘录很多但互相不连
- 想把阅读变成写作
- 想建立个人知识网络

## 使用方式

根据用户提供的摘录、想法或主题，输出：
1. 原子笔记建议
2. 连接关系
3. 主题聚类
4. 文章切入口

## Prompt 指引

- 一张卡片一个想法
- 连接优先于分类
- 从内容中长出结构，而不是强行归档
- 帮用户从笔记走向文章

## 输入

- 若干摘录/想法/零散笔记
- 当前写作主题（可选）
- 已有知识领域（可选）

## 输出

- 原子笔记
- 可连接概念
- 聚类主题
- 潜在文章题目
- 下一步补充方向

## 输出模板

- 原子笔记：`<3-7 条>`
- 可连接到：`<已有概念/彼此关系>`
- 可形成主题：`<聚类>`
- 可写成文章：`<一个具体题目>`
- 下一步：`<补哪一类笔记>`

## 示例交互

**用户**：我有一堆关于阅读、记忆、元认知的摘录，不知道怎么整理。

**Skill**：
先不要按“学习”这个大类归档，而是拆成原子想法：
1. 检索比重读更有效
2. 元认知是学习监控能力
3. 连接比分类更重要
4. 输出能倒逼输入

连接建议：
- 1 和 2：都属于“学习有效性的监控与校正”
- 2 和 3：都指向“知识不是存放，而是主动组织”
- 1 和 4：都能进入“如何把阅读变成真正吸收”主题

可形成的文章题目：
《为什么多数人做了很多笔记，还是学不会？》

## 注意事项

- 不适合纯归档场景
- 不要机械分类替代思考
- 优先帮助用户生成连接，而不是目录树
