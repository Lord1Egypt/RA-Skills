---
catalog_version: 0.1.0-draft
theme: finance-accounting
title: 财务管理 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  财务 / 记账 / 报销 / 开票主题积木。当前以连接器（MCP）为主，skill 较少，待社区补充。
  评分二维：usability=实际好用 / composable=可组合 workflow。
---

# 财务管理 · 主题积木

> 使用指引：本主题当前以财务类连接器为主（记账/开票/报销/对账），skill 积木待补充。

- name: 云帐房（记账）
  slug: yzf-general-mcp-server
  type: mcp
  source: connector
  version: ""
  purpose: 云帐房 AI 记账/财务处理
  install_cmd: "（连接器管理页启用云帐房）"
  risk: 中
  usability: 3
  composable: 3
  workflow_set: []

- name: 云帐房 AI 开票
  slug: yzf-invoice-mcp-server
  type: mcp
  source: connector
  version: ""
  purpose: 云帐房 AI 开票
  install_cmd: "（连接器管理页启用云帐房AI开票）"
  risk: 中
  usability: 3
  composable: 3
  workflow_set: []

- name: 分贝通（报销）
  slug: fenbeitong
  type: mcp
  source: connector
  version: ""
  purpose: 企业报销/费用管理
  install_cmd: "（连接器管理页启用分贝通）"
  risk: 中
  usability: 3
  composable: 3
  workflow_set: []

- name: 九数云 BI（财务分析）
  slug: jiushuyun
  type: mcp
  source: connector
  version: ""
  purpose: 财务/经营数据 BI 分析与看板
  install_cmd: "（连接器管理页启用九数云BI）"
  risk: 中
  usability: 3
  composable: 4
  workflow_set: []

- name: 畅捷通 T+
  slug: tplus-api
  type: mcp
  source: connector
  version: ""
  purpose: 财务进销存一体化管理
  install_cmd: "（连接器管理页启用畅捷通T+）"
  risk: 中
  usability: 3
  composable: 3
  workflow_set: []

> 待补充：财务 skill 积木较少，社区如有「对账/发票识别/财务报表生成」类 skill 可补入。
