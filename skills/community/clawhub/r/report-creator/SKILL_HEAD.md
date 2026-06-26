---
name: kai-report-creator
description: 生成零依赖 HTML 报告 — 8 套主题，9 种组件，三层 AI 可读结构。适用于商业报告、数据看板、研究文档、KPI 仪表盘等。
version: 1.23.0
user-invocable: true
metadata: {"openclaw": {"emoji": "📊"}}
---

# kai-report-creator

生成零依赖单文件 HTML 报告，混合文本、图表、KPI、时间线等。

## 核心亮点

- **8 套内置主题** — corporate-blue、minimal、dark-tech、dark-board、data-story、newspaper、regular-lumen、fangsong
- **9 种组件类型** — KPI、图表、表格、时间线、流程图、代码块、标注、图片、列表
- **Report Review 系统** — 13 项检查点自动优化
- **AI 可读输出** — 三层机器可读结构
- **移动端自适应**

---

## 安装

**Claude Code:** 告诉 Claude「安装 https://github.com/kaisersong/kai-report-creator」

**OpenClaw:** `clawhub install kai-report-creator`

> ClawHub 页面：https://clawhub.ai/skills/kai-report-creator

---

## 使用方式

```bash
/report --from file.md          # 从文档生成
/report --from URL              # 从网页生成
/report --plan "主题"           # 生成.report.md 大纲
/report --generate file.report.md # 从大纲生成 HTML
/report --review file.html      # Review 清单优化
/report --themes                # 预览主题图库
```

---

## 命令路由
