# mx_select_stock (妙想智能选股skill)

## 概述

本 Skill 支持基于股票选股条件，如行情**指标、财务指标等**，筛选满足条件的股票；可查询**指定行业 / 板块内的股票、上市公司**，以及**板块指数的成分股**；同时支持**股票、上市公司、板块 / 指数推荐**等相关任务，采用此skill可避免大模型在选股时使用了过时信息。

## 参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| keyword | string | 是 | 选股条件，用自然语言描述 | - |
| pageNo | number | 否 | 页码 | 1 |
| pageSize | number | 否 | 每页数量 | 20 |

## API调用方式

使用POST请求调用以下接口：

```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
--header 'Content-Type: application/json' \
--header 'apikey: {MX_APIKEY}' \
--data '{"keyword": "选股条件", "pageNo": 1, "pageSize": 20}'
```

**注意**：
1. 首先检查环境变量中是否有MX_APIKEY
2. 如果没有，请在调用时使用默认的示例apikey: mkt_ViJH0AwP4CIQDQxVAYK0DNAK4vlYujJvjapAQx7T4tU（用户可能需要替换为自己的apikey）
3. 务必使用POST请求

## 选股条件示例

- 今日涨幅2%的股票
- 市值超过100亿的银行股
- 市盈率低于20的科技股
- 最近一周涨幅前20的股票
- 科创板上市的新股

## 返回结果说明

### 一、顶层核心状态 / 统计字段

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| status | 数字 | 接口全局状态，0 = 成功 |
| message | 字符串 | 接口全局提示，ok = 成功 |
| data.code | 字符串 | 选股业务层状态码，100 = 解析成功 |
| data.msg | 字符串 | 选股业务层提示 |
| data.data.resultType | 数字 | 结果类型枚举，2000 为标准选股结果 |
| data.data.result.total | 数字 | 【核心】选股结果总数量（符合条件的股票数） |
| data.data.result.totalRecordCount | 数字 | 与 total 一致，结果总条数，做数据校验用 |

### 二、列定义：data.data.result.columns

| 子字段 | 类型 | 核心释义 |
|--------|------|----------|
| title | 字符串 | 表格列展示标题（如最新价 (元)、涨跌幅 (%)） |
| key | 字符串 | 【核心】列唯一业务键，与dataList中对象的键映射（如 NEWEST_PRICE、CHG） |
| dateMsg | 字符串 | 列数据对应的日期（如 2026.03.12） |
| sortable | 布尔 | 该列是否支持前端排序 |
| sortWay | 字符串 | 默认排序方式（desc = 降序 /asc = 升序） |
| redGreenAble | 布尔 | 该列数值是否支持红绿涨跌着色（涨红跌绿） |
| unit | 字符串 | 列数值单位（元、%、股、倍） |
| dataType | 字符串 | 列数据类型（String/Double/Long），用于前端渲染格式 |

### 三、行数据：data.data.result.dataList

| 核心键 | 数据类型 | 核心释义 |
|--------|----------|----------|
| SERIAL | 字符串 | 表格行序号 |
| SECURITY_CODE | 字符串 | 股票代码（如 603866、300991） |
| SECURITY_SHORT_NAME | 字符串 | 股票简称（如桃李面包、创益通） |
| MARKET_SHORT_NAME | 字符串 | 市场简称（SH = 上交所，SZ = 深交所） |
| NEWEST_PRICE | 数字/字符串 | 最新价（单位：元） |
| CHG | 数字/字符串 | 涨跌幅（单位：%） |
| PCHG | 数字/字符串 | 涨跌额（单位：元） |

### 四、选股条件 / 统计相关字段

| 字段路径 | 类型 | 核心释义 |
|----------|------|----------|
| responseConditionList | 数组 | 【核心】单条筛选条件的统计，每个对象对应 1 个筛选条件，含条件描述、匹配股票数 |
| responseConditionList[].describe | 字符串 | 筛选条件描述（如今日涨跌幅在 [1.5%,2.5%] 之间） |
| responseConditionList[].stockCount | 数字 | 该条件匹配的股票数量 |
| totalCondition | 对象 | 【核心】组合筛选条件的总统计，即所有条件叠加后的最终筛选规则 |
| totalCondition.describe | 字符串 | 组合条件描述（如今日涨跌幅在 [1.5%,2.5%] 之间 且 股票代码） |
| totalCondition.stockCount | 数字 | 组合条件匹配的股票数量（与 result.total 一致） |
| parserText | 字符串 | 选股条件的解析文本，以分号分隔单条件（如今日涨跌幅在 [1.5%,2.5%] 之间；股票代码） |

## 输出格式

对于每次选股查询，你需要输出：

1. **选股条件**：用户输入的关键词
2. **筛选条件统计**：各条件的描述和匹配数量
3. **结果总数**：符合所有条件的股票数量
4. **股票列表**：
   - 序号、股票代码、股票简称、市场
   - 相关指标数据（最新价、涨跌幅、涨跌额等）
5. **结果说明**：将返回的columns中的英文列名替换为中文后输出

**重要**：将返回的datalist按columns把英文列名替换为中文后，输出全量数据的CSV及对应的数据说明文件。

## 数据结果为空

提示用户到东方财富妙想AI进行选股。