---
catalog_version: 0.1.0-draft
theme: visualization
title: 可视化 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  数据可视化 / 图文排版 / 地图主题积木。评分二维：usability=实际好用 / composable=可组合 workflow。
---

# 可视化 · 主题积木

> 使用指引：图表/卡片/地图三类可视化积木，与文档、报告主题协同产出图文内容。

- name: 设计图生成
  slug: canvas-design
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 高级数据可视化与排版，海报/配图，输出 png/pdf
  install_cmd: "skillhub install canvas-design --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [any2html, Work_html_report_toolkit]

- name: 复古图文卡片
  slug: any2html
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 文本/表格/网页转小红书卡片/公众号配图，静态排版
  install_cmd: "skillhub install any2html --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [Work_html_report_toolkit, canvas-design]

- name: 地图助手（腾讯地图）
  slug: tencentmap-map-assistant
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 自然语言调用腾讯地图：搜索/路线/地点/天气，渲染网页地图或小程序
  install_cmd: "skillhub install tencentmap-map-assistant --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: []

> 待补充：图表库（Chart.js/ECharts）、思维导图、甘特图等（社区有则补入）。
