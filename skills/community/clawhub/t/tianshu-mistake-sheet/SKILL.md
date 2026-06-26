---
name: tianshu-mistake-sheet
description: >
  生成 Markdown 错题表：支持 `--template` 输出空表；或 `--file`/`--text` 中每行 `题干片段|错因|知识点`（竖线分隔）。
  Use when: 学生整理错题、考前复盘；用户说「错题本格式」「错题表」。
  NOT for: 拍照自动 OCR 识别题目。
metadata:
  openclaw:
    primaryEnv: ""
---

# 错题本表格

## Workflow

空模板：

```bash
node ~/.openclaw/skills/tianshu-mistake-sheet/scripts/mistake_sheet.js --template --rows 15
```

从文本导入（每行：`简写题干|错因|章节/知识点`）：

```bash
node scripts/mistake_sheet.js --file mistakes.txt
```

## Output

三列表：`题目/来源` | `错因` | `知识点/章节` | `复习日期（自填）`
