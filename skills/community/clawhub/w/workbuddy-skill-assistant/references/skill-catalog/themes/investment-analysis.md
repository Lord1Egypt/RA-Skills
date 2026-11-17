---
catalog_version: 0.1.0-draft
theme: investment-analysis
title: 投资分析 · 主题积木（≤10 个精华 skill）
last_synced: 2026-08-27
note: >
  投资 / 金融数据分析主题积木。评分二维：usability=实际好用 / composable=可组合 workflow。
  金融数据查询优先级：westock-data → neodata → tdx-connector（见相关连接器）。
---

# 投资分析 · 主题积木

> 使用指引：数据入口 → 分析 → 归档 → 风控的完整投研链。A股/港股/美股 + 研报 + 尽调 + 组合风控。

- name: 金融场景总入口
  slug: wb-finance-skill
  type: skill
  source: builtin
  version: "0.1.0"
  purpose: A股/港股/美股/ETF/宏观/财报/估值/持仓/交易等金融场景总入口，优先级最高
  install_cmd: "（内置插件，启用即生效）"
  risk: 低
  usability: 5
  composable: 5
  workflow_set: [a-stock-data, westockdata]

- name: A股全栈数据工具包
  slug: A股全栈数据
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 行情(mootdx+腾讯+百度K线)、研报、信号、资金面、新闻、基础数据全覆盖
  install_cmd: "skillhub install a-stock-data --dir ~/.workbuddy/skills"
  risk: 低
  usability: 5
  composable: 5
  workflow_set: [wb-finance-skill, "@org-gv4zgi7j/stock-volume-12step-analysis"]

- name: 腾讯自选股结构化数据
  slug: westockdata
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 股票/ETF/指数/板块/期货/外汇/可转债K线、财报、研报、公告、龙虎榜等权威数据
  install_cmd: "skillhub install westockdata --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 5
  workflow_set: [wb-finance-skill, A股全栈数据]

- name: 量能 12 步深度分析
  slug: "@org-gv4zgi7j/stock-volume-12step-analysis"
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 五维量能评分+四层决策架构12步SOP，个股/两股/组合深度量能分析
  install_cmd: "skillhub install stock-volume-12step-analysis --namespace @org-gv4zgi7j --dir ~/.workbuddy/skills"
  risk: 低
  usability: 5
  composable: 4
  workflow_set: [A股全栈数据, wb-finance-skill]

- name: Yahoo Finance 跨市场分析
  slug: stock-analysis
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 股票/加密货币 Yahoo Finance 数据，含美股/港股补充视角
  install_cmd: "skillhub install stock-analysis --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [wb-finance-skill, A股全栈数据]

- name: 投资决策归档（Obsidian）
  slug: Work_investment_archiver
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 投资分析/决策完成后自动生成结构化 OB 笔记，归档到 Stock 子仓库
  install_cmd: "skillhub install Work_investment_archiver --dir ~/.workbuddy/skills"
  risk: 低
  usability: 5
  composable: 4
  workflow_set: [Work_html_report_toolkit, Work_document_pipeline]

- name: 组合风险仪表板
  slug: Work_build_dashboard
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 维持担保比例/行业集中度/因子暴露/回撤 KPI+图表+持仓明细（暗色）
  install_cmd: "skillhub install Work_build_dashboard --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 4
  workflow_set: [westockdata, Work_html_report_toolkit]

- name: 尽职调查清单生成器
  slug: dd-checklist-generator
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 按项目类型自动生成结构化尽调资料清单（股权/并购/债权/地产/不良/REITs等）
  install_cmd: "skillhub install dd-checklist-generator --dir ~/.workbuddy/skills"
  risk: 低
  usability: 4
  composable: 3
  workflow_set: [Work_html_report_toolkit]

> 待补充：量化因子、组合引擎、研报生成等（社区有则补入）。
