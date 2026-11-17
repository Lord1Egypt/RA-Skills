---
catalog_version: 0.1.0-draft
theme: ppt-presentation
title: PPT / 演示 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  演示文稿 / 幻灯片主题积木。评分二维：usability=实际好用 / composable=可组合 workflow。
---

# PPT / 演示 · 主题积木

> 使用指引：正式 PPT、HTML 幻灯、SVG 母版三类互补，覆盖咨询级到轻量演示场景。

- name: 咨询级 PPT 设计
  slug: Work_mck_ppt_design
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 专业咨询级 PowerPoint 演示文稿生成
  install_cmd: "skillhub install Work_mck_ppt_design --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 5
  workflow_set: [Work_frontend_slides, Work_html_report_toolkit]

- name: HTML 演示文稿
  slug: Work_frontend_slides
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 零依赖单文件 HTML 幻灯片，预览-选择-生成三步曲
  install_cmd: "skillhub install Work_frontend_slides --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 5
  workflow_set: [Work_mck_ppt_design, Work_html_report_toolkit]

- name: SVG 演示母版
  slug: Work_ppt_master
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 源文档转高质量 SVG 页并导出 PPT
  install_cmd: "skillhub install Work_ppt_master --dir ~/.workbuddy/skills"
  risk: 低
  usability: 3
  composable: 3
  workflow_set: [Work_mck_ppt_design, Work_frontend_slides]

- name: 腾讯 PPT（内置）
  slug: tencent-pptx
  type: skill
  source: builtin
  version: "1.0.0"
  purpose: 从零生成专业 PowerPoint 演示文稿，可参考已有 PPTX 视觉风格
  install_cmd: "（内置插件，启用即生效）"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [Work_mck_ppt_design]

> 待补充：动态图表 PPT、AI 演讲脚本等（社区有则补入）。
