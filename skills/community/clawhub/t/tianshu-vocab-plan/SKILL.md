---
name: tianshu-vocab-plan
description: >
  根据词表（每行一词或短语）生成本地课表式的复习计划：第几天学新词、第几天回顾（简化艾宾浩斯：+1,+2,+4,+7,+15 天）。
  Use when: 背单词、考前词汇突击；用户说「复习计划」「词表排期」「间隔复习」。
  NOT for: 内置背单词 App 联动；精细到分钟的提醒。
metadata:
  openclaw:
    primaryEnv: ""
---

# 词表间隔复习计划

## Workflow

准备 `words.txt`，每行一条（单词或短语，可加 `# 注释` 行忽略）。

```bash
node ~/.openclaw/skills/tianshu-vocab-plan/scripts/vocab_plan.js --file words.txt --start 2026-03-21 --per-day 20
```

## 参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--file` / `-f` | 必填 | 词表路径 |
| `--start` | 今天 | 开始日期 `YYYY-MM-DD` |
| `--per-day` | 20 | 每天新词数量 |

## Output

Markdown 表格：日期 | 新学 | 当日复习（第几次回顾），并附使用说明。
