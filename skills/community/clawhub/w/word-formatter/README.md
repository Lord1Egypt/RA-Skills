# word-formatter v1.0.0「黑灰白」

> 咨询报告 Word 排版引擎 — 配置驱动、5 类交付物、极度克制的黑/白/灰设计语言。

## 快速开始

```bash
# 1. 克隆
git clone <仓库地址> ~/.workbuddy/skills/word-formatter

# 2. 装环境
cd ~/.workbuddy/skills/word-formatter
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. 排版
.venv/bin/python scripts/format_docx.py 输入.docx configs/dd_report_financial.json -o 输出.docx

# 4. 校验
.venv/bin/python scripts/validate_docx.py 输出.docx configs/dd_report_financial.json
```

## 更新到最新版

```bash
cd ~/.workbuddy/skills/word-formatter && git pull
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-07-29 | 首发「黑灰白」：5 ��报告、封面专业布局、页眉双栏、Heading 1-6、三线表规范、校验 26 项通过 |
