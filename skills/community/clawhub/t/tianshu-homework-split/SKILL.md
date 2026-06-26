---
name: tianshu-homework-split
description: >
  把课程作业说明、大纲要求或长段文字拆成带序号的学习任务清单（Markdown 勾选框）。
  Use when: 学生要整理作业、拆 DDL、把老师发的要求变成待办；用户说「作业拆分」「学习任务清单」「大作业拆步」。
  NOT for: 自动替写作业内容；代替日历 App 的提醒推送。
metadata:
  openclaw:
    primaryEnv: ""
---

# 作业 / 要求拆分清单

将**课程要求、作业说明、复习提纲**转为可逐项打勾的 Markdown 列表，便于复制到 Notion / Obsidian / Todo。

## Workflow

```bash
node ~/.openclaw/skills/tianshu-homework-split/scripts/split_hw.js --file 要求.txt
# 或
node scripts/split_hw.js --text "第一周…第二周…"
```

## 参数

- `--file` / `-f`：UTF-8 文本
- `--text` / `-t`：直接粘贴

## Output

stdout 为 Markdown：**总览** + **任务清单**（`- [ ]`）。若文中出现「截止」「DDL」「第X周」等字样会尽量原样保留在条目中。
