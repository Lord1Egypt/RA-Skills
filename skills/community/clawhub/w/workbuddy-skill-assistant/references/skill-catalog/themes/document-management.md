---
catalog_version: 0.1.0-draft
theme: document-management
title: 文档管理 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  文档生成 / 格式转换 / 报告输出主题积木。评分二维：usability=实际好用 / composable=可组合 workflow。
  注：tencent-docs 与 Work_document_pipeline 已入通用核心，本主题不重复。
---

# 文档管理 · 主题积木

> 使用指引：Markdown→多格式→PDF 定稿的完整文档生产线；与核心的 tencent-docs / 管线协同。

- name: HTML 报告工具包
  slug: Work_html_report_toolkit
  type: skill
  source: installed
  version: "1.0.0"
  purpose: Jinja2 模板 + 金融/出版级主题 + 图表组装器，周报/总结/汇报一键生成
  install_cmd: "skillhub install Work_html_report_toolkit --dir ~/.workbuddy/skills"
  risk: 低
  usability: 5
  composable: 5
  workflow_set: [Work_document_pipeline, Work_pandoc_pdf_generation]

- name: PDF 生成（LaTeX）
  slug: Work_pandoc_pdf_generation
  type: skill
  source: installed
  version: "1.0.0"
  purpose: Pandoc + XeLaTeX 中文 PDF，学术/投资分析/正式文档/合同
  install_cmd: "skillhub install Work_pandoc_pdf_generation --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [Work_document_pipeline, Work_html_report_toolkit]

- name: 文档格式转换（pandoc）
  slug: pandoc
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 文档多格式互转（md/docx/html/pdf/epub）
  install_cmd: "skillhub install pandoc --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [Work_document_pipeline]

- name: DOCX 转换（pandoc）
  slug: pandoc-docx
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 以 DOCX 为核心的通用文档转换
  install_cmd: "skillhub install pandoc-docx --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [pandoc, Work_document_pipeline]

- name: 文档转 Markdown
  slug: markitdown-skill
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 用 Microsoft MarkItDown 把文档转 Markdown
  install_cmd: "skillhub install markitdown-skill --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [pandoc]

- name: Kindle 电子书生成
  slug: Work_kindle_epub_generator
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 文档转 EPUB/Kindle 推送，长文移动阅读
  install_cmd: "skillhub install Work_kindle_epub_generator --dir ~/.workbuddy/skills"
  risk: 低
  usability: 3
  composable: 3
  workflow_set: [Work_document_pipeline]

- name: 本地 Office 路由（内置）
  slug: tencent-docs-routing
  type: skill
  source: builtin
  version: "1.1.0"
  purpose: 本地 doc/docx/xls/ppt 与腾讯文档无缝路由，编辑优先本地
  install_cmd: "（内置插件，启用即生效）"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [tencent-docs, Work_document_pipeline]

> 待补充：WPS 协同、合同模板、电子签等（社区有则补入）。
