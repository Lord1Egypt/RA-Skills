---
name: shangan-gongkao
description: Work with Chinese civil-service exam preparation materials. Use when learners ask to organize 公考资料, build 国考/省考/事业编/行政执法 study plans, extract 行测/申论 methods, arrange mock exams, search local notes, or generate daily checklists, formula sheets, essay templates, and review tables.
---

# 上岸公考

## What This Skill Does

This skill turns a learner's public-exam materials into practical study actions. It is designed for 国考、省考、事业编、行政执法 and similar Chinese public-sector exam preparation.

Use it when the user needs:

- 整理资料: 按行测、申论、常识、真题、备考攻略等模块盘点资料，判断哪些先看、哪些刷题、哪些留到后期查漏补缺。
- 制定计划: 生成 7 天、15 天、30 天、60 天冲刺计划，细化到每日任务、复盘节奏和错题回炉安排。
- 行测提分: 提炼资料分析公式、数量关系题型、判断推理规律、言语理解关键词和常识高频主题。
- 申论辅助: 生成分论点模板、大作文开头结尾、金句分类、答题结构，并帮助修改提纲或作文框架。
- 真题刷题: 根据历年真题设计模考安排、错题分类、高频陷阱总结和训练路径。
- 关键词检索: 用户问“增长率怎么速算”“申论分论点怎么写”等问题时，优先从资料中找对应内容，再总结成能直接用的答案。
- 生成产物: 输出每日学习清单、模块知识树、公式速查表、申论模板库、错题复盘表、考前 3 天冲刺清单。

## Source Priority

Use the learner's own material folder as the primary source whenever available:

`E:\公考\公考-上岸资料整理`

Before answering from general knowledge, inspect relevant Markdown files. Prefer grounded summaries with source filenames, especially for formulas, templates, question-type methods, and study plans.

Read `references/material-map.md` when you need to understand the folder structure, file inventory, or which files to inspect first.

## Workflow

1. Classify the request by module: 资料分析, 判断推理, 言语理解与表达, 数量关系, 常识, 申论, 历年真题, or 备考攻略.
2. Read `references/material-map.md` to choose likely source files.
3. Search the materials before deep reading when the request names a topic, formula, question type, teacher, year, or keyword. Use `scripts/search-materials.ps1` or a text search tool if available.
4. Read the smallest useful set of source files or sections.
5. Convert source material into practical outputs: prioritized outlines, concise notes, drills, checklists, memorization cards, wrong-question diagnostics, or time-boxed plans.
6. Cite local filenames in plain language so the learner can trace where the advice came from.

## Output Style

Keep answers practical, short, and exam-oriented.

For learners, prefer:

- “今天先做什么”
- “下一步怎么刷”
- “这份资料该怎么用”
- “错题怎么复盘”
- “考前怎么冲刺”

Use tables for schedules, formulas, module comparisons, and review plans. If source coverage is thin or a file appears to contain only a stub, say so and choose the next best source.
