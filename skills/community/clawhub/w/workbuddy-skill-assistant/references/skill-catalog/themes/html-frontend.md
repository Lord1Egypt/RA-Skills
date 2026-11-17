---
catalog_version: 0.1.0-draft
theme: html-frontend
title: HTML / 前端 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  HTML 主题积木，含两类：① 前端开发/网页界面（已装）；② HTML 汇报/演示（第三方 GitHub·待验证，含 wiki）。
  评分二维：usability=实际好用 / composable=可组合 workflow。每个 skill 配一份 wiki（见 wikis/html-frontend/）。
---

# HTML / 前端 · 主题积木

> 使用指引：本主题是「功能领域积木」，由画像倾斜选择进入组合。每个主题 ≤10 个精华 skill。
> 带 `wiki` 字段的条目有独立说明书（功能/优点/输入/输出/搭配/安装/评分），见 `wikis/html-frontend/`。

## 前端开发 / 网页界面（已装）

- name: 生产级前端界面
  slug: impeccable
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 高设计质量的生产级前端界面/组件/页面
  install_cmd: "skillhub install impeccable --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [html-sandbox-preview, Work_html_report_toolkit]

- name: HTML 沙箱预览
  slug: html-sandbox-preview
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 自包含 HTML 报告/可视化在沙箱面板正确渲染并强制默认浏览器打开
  install_cmd: "skillhub install html-sandbox-preview --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [impeccable, Work_html_report_toolkit]

- name: 浏览器操作
  slug: browser-skill
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 对已登录浏览器执行自动化：访问/读取页面、填表、抓取、点击
  install_cmd: "skillhub install browser-skill --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [agent-browser]

## HTML 汇报 / 演示（第三方 GitHub · 待验证 · 各配 wiki）

> 来源文章：ima 神圣凯莎知识宝库《HTML 已经变成了新时代的 PPT，我推荐这五个》（2026-08-26）。
> 安装走 npx skills 生态（Codex/Claude/Cursor），**WorkBuddy 兼容性待实测**；详见各自 wiki。

- name: Frontend Slides
  slug: frontend-slides
  type: skill
  source: github
  version: ""
  purpose: 先出视觉方案再定设计的 HTML 汇报生成，5 风格 + 16:9 单文件
  install_cmd: "npx skills@latest add https://github.com/zarazhangrui/frontend-slides --global --agent codex --yes"
  risk: 中
  usability: 4
  composable: 4
  workflow_set: [frontend-slides-editable]
  wiki: wikis/html-frontend/frontend-slides.md

- name: Huashu Design
  slug: huashu-design
  type: skill
  source: github
  version: ""
  purpose: 中文高级风格化 HTML 排版，品牌气质 + 视觉叙事 + 多维度评审
  install_cmd: "npx skills@latest add https://github.com/alchaincyf/huashu-design --global --agent codex --yes"
  risk: 中
  usability: 4
  composable: 3
  workflow_set: []
  wiki: wikis/html-frontend/huashu-design.md

- name: Visual Explainer
  slug: visual-explainer
  type: skill
  source: github
  version: ""
  purpose: 深色技术风，把终端/代码/架构/数据/风险整理成可读 HTML 报告或 slides
  install_cmd: "npx skills@latest add https://github.com/nicobailon/visual-explainer/tree/main/plugins/visual-explainer --global --agent codex --yes"
  risk: 中
  usability: 4
  composable: 3
  workflow_set: [html-ppt-skill]
  wiki: wikis/html-frontend/visual-explainer.md

- name: HTML PPT Studio
  slug: html-ppt-skill
  type: skill
  source: github
  version: ""
  purpose: 设计系统 + 现成 deck 模板，稳定出稿（周报/商务提案/技术分享）
  install_cmd: "npx skills@latest add https://github.com/lewislulu/html-ppt-skill --global --agent codex --yes"
  risk: 中
  usability: 4
  composable: 4
  workflow_set: [visual-explainer]
  wiki: wikis/html-frontend/html-ppt-studio.md

- name: Frontend Slides – Editable
  slug: frontend-slides-editable
  type: skill
  source: github
  version: ""
  purpose: Frontend Slides 可编辑版，生成后浏览器内拖拽改版 + 导出干净 HTML
  install_cmd: "npx skills@latest add https://github.com/archlizheng/frontend-slides-editable --global --agent codex --yes"
  risk: 中
  usability: 4
  composable: 4
  workflow_set: [frontend-slides]
  wiki: wikis/html-frontend/frontend-slides-editable.md
