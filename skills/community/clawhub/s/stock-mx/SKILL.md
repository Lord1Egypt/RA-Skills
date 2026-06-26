# 妙想金融Skills使用指南

本文档包含三个妙想金融Skills的详细说明和使用方法。

---

## 目录

1. [mx_search (妙想资讯搜索skill)](#mx_search-妙想资讯搜索skill)
2. [mx_select_stock (妙想智能选股skill)](#mx_select_stock-妙想智能选股skill)
3. [mx_data (妙想金融数据skill)](#mx_data-妙想金融数据skill)

---

## mx_search (妙想资讯搜索skill)

### 概述

本 Skill 基于东方财富妙想搜索能力，基于金融场景进行信源智能筛选，用于获取涉及时效性信息或特定事件信息的任务，包括新闻、公告、研报、政策、交易规则、具体事件、各种影响分析、以及需要检索外部数据的非常识信息等。避免AI在搜索金融场景信息时，参考到非权威、及过时的信息。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 用户问句，要搜索的金融资讯关键词 |

### API调用方式

```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
--header 'Content-Type: application/json' \
--header 'apikey: {MX_APIKEY}' \
--data '{"query":"查询内容"}'
```

**注意**：
1. 首先检查环境变量中是否有MX_APIKEY
2. 如果没有，请在调用时使用默认的示例apikey: mkt_ViJH0AwP4CIQDQxVAYK0DNAK4vlYujJvjapAQx7T4tU（用户可能需要替换为自己的apikey）
3. 务必使用POST请求

### 问句示例

| 类型 | 示例问句 |
|------|----------|
| 个股资讯 | 格力电器最新研报、贵州茅台机构观点 |
| 板块/主题 | 商业航天板块近期新闻、新能源政策解读 |
| 宏观/风险 | A股具备自然对冲优势的公司 汇率风险、美联储加息对A股影响 |
| 综合解读 | 今日大盘异动原因、北向资金流向解读 |

### 返回说明

| 字段路径 | 简短释义 |
|----------|----------|
| title | 信息标题，高度概括核心内容 |
| secuList | 关联证券列表，含代码、名称、类型等 |
| secuList[].secuCode | 证券代码（如 002475） |
| secuList[].secuName | 证券名称（如立讯精密） |
| secuList[].secuType | 证券类型（如股票 / 债券） |
| trunk | 信息核心正文 / 结构化数据块，承载具体业务数据 |

---

## mx_select_stock (妙想智能选股skill)

### 概述

本 Skill 支持基于股票选股条件，如行情**指标、财务指标等**，筛选满足条件的股票；可查询**指定行业 / 板块内的股票、上市公司**，以及**板块指数的成分股**；同时支持**股票、上市公司、板块 / 指数推荐**等相关任务，采用此skill可避免大模型在选股时使用了过时信息。

### 参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| keyword | string | 是 | 选股条件，用自然语言描述 | - |
| pageNo | number | 否 | 页码 | 1 |
| pageSize | number | 否 | 每页数量 | 20 |

### API调用方式

```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
--header 'Content-Type: application/json' \
--header 'apikey: {MX_APIKEY}' \
--data '{"keyword": "选股条件", "pageNo": 1, "pageSize": 20}'
```

### 选股条件示例

- 今日涨幅2%的股票
- 市值超过100亿的银行股
- 市盈率低于20的科技股
- 最近一周涨幅前20的股票
- 科创板上市的新股

### 返回结果说明

#### 顶层核心状态/统计字段

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| status | 数字 | 接口全局状态，0 = 成功 |
| message | 字符串 | 接口全局提示，ok = 成功 |
| data.code | 字符串 | 选股业务层状态码，100 = 解析成功 |
| data.data.result.total | 数字 | 【核心】选股结果总数量（符合条件的股票数） |

#### 行数据：data.data.result.dataList

| 核心键 | 数据类型 | 核心释义 |
|--------|----------|----------|
| SERIAL | 字符串 | 表格行序号 |
| SECURITY_CODE | 字符串 | 股票代码 |
| SECURITY_SHORT_NAME | 字符串 | 股票简称 |
| MARKET_SHORT_NAME | 字符串 | 市场简称（SH = 上交所，SZ = 深交所） |
| NEWEST_PRICE | 数字/字符串 | 最新价（单位：元） |
| CHG | 数字/字符串 | 涨跌幅（单位：%） |
| PCHG | 数字/字符串 | 涨跌额（单位：元） |

---

## mx_data (妙想金融数据skill)

### 概述

本 Skill 基于**东方财富权威数据库**及**最新行情底层数据**构建，支持通过**自然语言**查询以下三类数据：

1. **行情类数据**：股票、行业、板块、指数、基金、债券的实时行情、主力资金流向、估值等数据

2. **财务类数据**：上市公司与非上市公司的基本信息、财务指标、高管信息、主营业务、股东结构、融资情况等数据

3. **关系与经营类数据**：股票、非上市公司、股东及高管之间的关联关系数据，以及企业经营相关数据

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| toolQuery | string | 是 | 查询内容，用自然语言描述要查询的金融数据 |

### API调用方式

```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
--header 'Content-Type: application/json' \
--header 'apikey: {MX_APIKEY}' \
--data '{"toolQuery": "查询内容"}'
```

### 查询示例

- 东方财富最新价
- 贵州茅台财务指标
- A股总市值
- 中国平安主营业务

### 数据限制说明

请谨慎查询大数据范围的数据，如某只股票3年的每日最新价，可能会导致返回内容过多，模型上下文爆炸问题。

### 返回结果说明

#### 一级核心路径：data

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| data.questionId | 字符串 | 查数请求唯一标识 ID |
| data.dataTableDTOList | 数组 | 【核心】标准化后的证券指标数据列表 |

#### 二级核心路径：dataTableDTOList[]

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| dataTableDTOList[].code | 字符串 | 证券完整代码（如 300059.SZ） |
| dataTableDTOList[].entityName | 字符串 | 证券全称 |
| dataTableDTOList[].title | 字符串 | 本指标数据的标题 |
| dataTableDTOList[].table | 对象 | 【核心】标准化表格数据 |
| dataTableDTOList[].nameMap | 对象 | 【核心】列名映射关系 |
| dataTableDTOList[].field | 对象 | 【核心】当前指标的详细元信息 |
| dataTableDTOList[].entityTagDTO | 对象 | 本指标关联证券的详细主体属性 |

#### 指标元信息：dataTableDTOList[].field

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| field.returnCode | 字符串 | 指标唯一编码 |
| field.returnName | 字符串 | 指标业务中文名 |
| field.returnSourceCode | 字符串 | 指标原始来源编码 |
| field.startDate/endDate | 字符串 | 本次查询的时间范围 |
| field.dateGranularity | 字符串 | 数据粒度（DAY = 日度，MIN = 分钟等） |

#### 证券主体属性：dataTableDTOList[].entityTagDTO

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| entityTagDTO.secuCode | 字符串 | 证券纯代码 |
| entityTagDTO.marketChar | 字符串 | 市场标识（.SZ = 深交所，.SH = 上交所） |
| entityTagDTO.entityTypeName | 字符串 | 证券类型（如 A 股/港股/债券） |
| entityTagDTO.fullName | 字符串 | 证券完整中文名 |
| entityTagDTO.className | 字符串 | 证券大类 |

---

## 公共说明

### API Key

默认API Key: `mkt_ViJH0AwP4CIQDQxVAYK0DNAK4vlYujJvjapAQx7T4tU`

建议用户在妙想Skills页面获取自己的apikey，并存到环境变量 `MX_APIKEY`

### 注意事项

1. 所有接口必须使用POST请求
2. 请谨慎查询大数据范围的数据
3. 数据结果为空时，提示用户到东方财富妙想AI查询