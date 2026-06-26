---
name: runbook-skill-kit-template-factory
description: Generate a reusable runbook plus self-contained skill kit from a validated workflow. 从一个已验证流程批量生成可复用的 runbook 与自包含 skill 套件。
homepage: https://docs.openclaw.ai/tools/clawhub
---

# Runbook Skill Kit Template Factory

Use this skill when you want a repeatable template that turns a validated workflow into both knowledge docs and a reusable skill bundle.
当你需要一个可重复使用的模板，把已验证流程同时变成知识文档和可复用 skill 套件时，使用这个 skill。

## Read First | 先读这些

- `{baseDir}/README.md`
- `{baseDir}/WORKFLOW.md`
- `{baseDir}/TEMPLATES.md`
- `{baseDir}/FAQ.md`
- `{baseDir}/CHANGELOG.md`

## Primary Rule | 核心原则

Treat the template as a production kit generator, not as a place to dump raw notes.
把这个模板当成生产套件的生成器，不要把它当成随手堆原始笔记的地方。

## Workflow | 执行流程

1. identify the validated workflow
   确认已经验证过的流程
2. choose a topic slug and display name
   选定 topic slug 和显示名称
3. instantiate the knowledge doc trio
   生成三件套知识文档
4. instantiate the self-contained skill bundle
   生成自包含 skill 包
5. replace placeholders consistently
   一致地替换所有占位符
6. add or update changelog
   增补 changelog
7. sync memory, publish, and verify
   同步 memory、发布并验证

## Strong Heuristics | 强判断规则

- if the process is not stable yet, keep it as draft notes
- if the package references outside docs, inline or bundle them before publish
- if operators are mixed-language, keep the kit bilingual
- if the workflow will be reused often, favor templates over ad hoc copying

中文解释：

- 流程还不稳定，就先留在草稿，不要直接模板化。
- 如果包依赖外部文档，发布前先内联或打包进去。
- 如果使用者语言混合，优先双语。
- 如果流程会反复复用，优先做模板，不要每次手工复制。

## Safe Commands | 安全命令

```bash
make sync
clawhub publish /absolute/path/to/skill-folder --slug your-skill --name "Your Skill" --version 1.0.0
clawhub inspect your-skill --version 1.0.0 --files
```

## Constraints | 约束

- keep `knowledge/` as canonical source
- keep the skill bundle self-contained
- do not ship secrets or raw transcripts
- prefer stable naming and consistent file layout
