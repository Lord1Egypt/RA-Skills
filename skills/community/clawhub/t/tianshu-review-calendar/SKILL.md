---
name: tianshu-review-calendar
description: >
  根据考试日期与科目列表，把复习主题均摊到考前每一天，生成 Markdown 日程表（可打印勾选）。
  Use when: 期末周、多门课冲刺；用户说「复习排期」「考前两周计划」。
  NOT for: 精确到小时的闹钟；代替个人学习习惯诊断。
metadata:
  openclaw:
    primaryEnv: ""
---

# 考前复习排期

## Workflow

```bash
node ~/.openclaw/skills/tianshu-review-calendar/scripts/review_cal.js \
  --exam 2026-07-01 \
  --topics "高数第三章,线代特征值,英语作文,数据结构树"
```

`--topics` 可用逗号或中文逗号分隔；也可用 `--file topics.txt`（每行一课/一章）。

## 参数

- `--exam` / `-e`：考试日期 `YYYY-MM-DD`（必填）
- `--days` / `-d`：从考试日往前推多少天开始排，默认 `14`
- `--topics` / `-t`：逗号分隔
- `--file` / `-f`：每行一个主题

## Output

从「第一天」到「考前一天」的表格：日期、建议复习主题、轻量任务提示。
