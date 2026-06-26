---
name: tianshu-paper-card
description: >
  把论文摘要或简介整理成「速读卡片」：题目占位、研究问题、方法要点、主要结论、局限、可引用句草稿。
  Use when: 学生读文献、写综述、组会前速览；用户说「文献卡片」「摘要整理」「论文笔记模板」。
  NOT for: 代替精读全文或学术不端式代写。
metadata:
  openclaw:
    primaryEnv: ""
---

# 文献速读卡片

适合**粘贴摘要（Abstract）或中文简介**，生成分栏 Markdown，便于 Zotero / Notion 侧边笔记。

## Workflow

 node ~/.openclaw/skills/tianshu-paper-card/scripts/paper_card.js --file abstract.txt  
 node scripts/paper_card.js --text "摘要全文…"  
可选：`--title "论文题目"`

## Output

含：**题目**、**研究问题/动机**、**方法**、**主要结果**、**局限**、**引用句草稿（需自己核对原文）**。
