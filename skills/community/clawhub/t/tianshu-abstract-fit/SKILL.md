---
name: tianshu-abstract-fit
description: >
  检查中英文摘要大致字数，并按句子顺序粗略填入「背景—方法—结果—结论」四栏草稿（启发式分段，需人工改写）。
  Use when: 写毕业论文/课程报告摘要；用户说「摘要结构」「摘要超字数」「四段摘要」。
  NOT for: 自动投稿或一键生成终稿摘要。
metadata:
  openclaw:
    primaryEnv: ""
---

# 摘要字数与结构槽位

## Workflow

```bash
node ~/.openclaw/skills/tianshu-abstract-fit/scripts/abstract_fit.js --file abstract.txt
node scripts/abstract_fit.js --text "全文…" --max 300
```

## 参数

- `--max`：建议上限（按字符数粗略统计），默认 `300`
- `--file` / `--text`：二选一

## Output

字数统计 + 四段 Markdown 引用块，便于复制到学校模板中润色。
