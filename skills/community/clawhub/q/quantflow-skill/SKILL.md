---
name: quantflow-skill
description: 面向中文自然语言的量化金融数据研究技能。用于把"看看这只股票最近怎么样""帮我查财报趋势""最近哪个板块最强""北向资金在买什么""给我导出一份行情数据"这类请求，转成可执行的数据获取、清洗、对比、筛选、导出与简要分析流程。适用于 A 股、指数、ETF/基金、财务、估值、资金流、公告新闻、板块概念与宏观数据等研究场景。同时集成了 AKQuant 量化投研引擎，支持策略回测和量化分析。
author: yejinlei
version: 1.0.0
requirements:
  python: 3.7+
  packages:
    - name: akshare
    - name: akquant
  network_access: true
---

# quantflow-skill

把自然语言财经数据请求，转成可执行的 Akshare 数据工作流。

这是一个面向自然语言的金融数据研究 skill。


## What this skill is for

使用场景：
- 看股票、指数、ETF 走势
- 查公司资料、估值、财务趋势
- 多标的横向对比
- 看资金流、板块强弱
- 梳理公告、新闻、政策
- 查看宏观经济数据
- 导出数据供分析或回测
- 使用 AKQuant 进行策略回测

***

## What this skill is NOT for

不适合：
- 直接给买卖建议或替代投资顾问
- 自动下单或执行交易
- 毫秒级实时交易决策
- 复杂回测引擎的实现
- 无网络支持时伪造数据

***

## Environment check

前置校验：
1. 检查 Python 3.7+ 可用
2. 检查 akshare 包已安装
3. 必要时检查 akquant 包已安装

缺失包时提示安装命令：
- `pip install akshare`
- `pip install akquant`

***

## Intent taxonomy

任务类型与核心接口：

### 1. 行情 / 趋势
- 核心接口：`stock_zh_a_hist`, `stock_zh_a_spot`, `stock_zh_a_daily`

### 2. 基本资料 / 标的识别
- 核心接口：`stock_info_a_code_name`, `stock_company_info_em`

### 3. 财务 / 公司质量
- 核心接口：`stock_financial_analysis_indicator`, `stock_balance_sheet_by_report_em`

### 4. 估值 / 基本面指标
- 核心接口：`stock_zh_a_spot`, `stock_financial_analysis_indicator`

### 5. 资金流 / 市场行为
- 核心接口：`stock_em_flows`, `stock_hsgt_hold`, `stock_top_inst`

### 6. 板块 / 指数 / 主题
- 核心接口：`stock_board_industry_spot_em`, `stock_board_concept_spot_em`

### 7. 打板 / 情绪 / 活跃度
- 核心接口：`stock_limit_up_board_em`, `stock_market_activity_em`

### 8. 公告 / 新闻 / 研报 / 政策
- 核心接口：`stock_news_em`, `stock_announcement`

### 9. 宏观 / 跨市场
- 核心接口：`macro_china_cpi`, `macro_china_pmi`, `stock_us_spot`, `stock_hk_spot`

### 10. 导出 / 研究准备
- 核心：统一输出规则与命名规范

### 11. 量化策略回测
- 核心接口：`stock_zh_a_daily`, `stock_zh_a_hist`, `akquant` 库

***

## Entity resolution rules

### 标的解析
- 优先识别股票名、代码、指数名、ETF 名、基金名
- 对中文简称先尝试匹配标准对象
- 重名时列出候选并澄清
- 证券代码统一为标准格式

### 市场识别
- 默认按 A 股理解，除非明确提到其他市场
- 指数、ETF、个股分开判断

### 时间默认值
- “最近走势” → 近 20 个交易日
- “最近一段时间” → 近 3 个月
- “财报 / 业绩” → 最近 8 个季度 + 最近年度
- “资金流最近” → 近 5～20 个交易日
- “宏观最近” → 最近 6～12 期

### 板块口径默认值
- 行业优先用申万 / 中信口径
- 概念优先同花顺 / 东方财富口径
- 依赖口径差异时明确说明

***

## Input normalization rules

数据请求前规范化：
- 日期统一为 `YYYY-MM-DD`
- 检查 `start_date <= end_date`
- 未来日期自动裁剪到最近可用日期
- 裸代码如 `000001` 需澄清或说明补全规则
- 冲突参数先裁决后传递

***

## Data retrieval rules

### 文档先行
- 确认接口名、必填参数、可选参数、返回字段

### 字段确认
- 使用已知字段白名单或接口文档确认
- 字段不存在时明确说明

### 默认分段拉取
- 日线/周线/月线：按年或季度切片
- 财报：按年份/报告期切片
- 分钟数据：按月/周切片
- 大批量多标的：按标的分批 + 日期分段

### 重试与限流
- 仅对瞬时错误（网络抖动、超时、429）有限重试
- 批量拉取时加入节流

### 分段合并
- 合并、去重、按主键排序
- 记录失败分段并明确告知用户

***

## Output contract

默认输出结构：
1. 一句话结论
2. 数据范围与口径
3. 关键指标/表格
4. 异常点/风险点/解释限制
5. 本地输出文件路径

### 结果交付形态
- 小结果：Markdown 摘要 + 简短表格
- 中等数据表：CSV
- 大规模分析：Parquet
- 可复用流程：附 Python 脚本
- 可视化：输出图表或说明

### 元信息
生成数据文件时记录：
- 接口名、请求参数、拉取时间
- 数据行数、字段列表
- 失败分段/缺失情况

***



## Data quality rules

数据拉取后检查：
- schema 校验
- 关键字段存在性检查
- 主键去重
- 固定排序
- 日期标准化
- 数值字段类型规范化

### 空结果处理
区分空表原因：
- 非交易日
- 区间无数据
- 股票未上市
- 参数错误

***

## Cache and reuse rules

支持：
- 基础表缓存（股票列表、交易日历、指数基础信息）
- 增量更新，避免全量重拉
- 大任务断点续跑
- 结果文件规范命名

推荐命名格式：
- `daily_600519_2023-01-01_2023-12-31_2026-03-22.csv`
- `financial_300750_2026-03-22.parquet`

缓存命中时说明来源。

***

## Error handling

采用“人话 + 调试细节分层”方式输出错误。

### 用户可见层
- akshare 包未安装
- 当前接口需要网络连接
- 时间范围过大，已自动分段拉取
- 股票名称不唯一，请确认
- 结果为空，可能因为非交易日/标的未上市

### 调试层
必要时提供：
- 接口名、参数
- 失败分段
- 异常原文

### 部分成功原则
明确说明：
- 成功部分
- 失败部分
- 是否生成不完整结果

***

## Recommended minimal interface set

核心接口集：
- `stock_zh_a_hist`：A股历史行情
- `stock_zh_a_spot`：A股实时行情
- `stock_info_a_code_name`：股票代码和名称
- `stock_financial_analysis_indicator`：财务分析指标
- `stock_balance_sheet_by_report_em`：资产负债表
- `stock_income_statement_by_report_em`：利润表
- `stock_em_flows`：资金流向数据
- `stock_hsgt_hold`：沪深港通持股
- `stock_board_industry_spot_em`：行业板块行情
- `stock_board_concept_spot_em`：概念板块行情
- `stock_limit_up_board_em`：涨停板数据
- `stock_news_em`：股票新闻
- `stock_announcement`：股票公告
- `macro_china_cpi`：中国CPI数据
- `macro_china_pmi`：中国PMI数据
- `stock_us_spot`：美股实时行情
- `stock_hk_spot`：港股实时行情

***

## Best practices

- 先理解任务，再选接口
- 先核心数据，再扩展
- 先给结论，再给证据
- 默认说人话，不堆字段名
- 对模糊中文表达有合理默认口径
- 大任务先给执行计划
- 导出任务保留脚本、元信息、文件路径
- 量化回测明确策略逻辑、时间范围和资金管理
- 回测结果结合交易成本和滑点分析
- 策略优化避免过拟合，使用样本外数据验证

***



## Quick rule

当用户提到：
- 看走势
- 查财报
- 比较公司
- 看板块
- 看资金流
- 梳理公告新闻
- 看宏观
- 拉数据导出
- 测试交易策略
- 回测量化模型

先想：
**这是什么任务？默认该走哪条数据工作流？结果应该怎样交付才真正有用？**