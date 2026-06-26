# 查询上市信息（综合）

## 接口

`getListedInfo`

## 描述

查询上市企业的基本信息、股东信息、财务报表数据。一个企业可能同时有多种上市类型（A股、新三板、H股），符合条件的都会返回。

## 请求路径

`POST /skill/ent/public/enterprise/getListedInfo`

## 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ename | string | 否 | 企业名称（与eid二选一） |
| eid | string | 否 | 企业ID（与ename二选一） |

传 ename 时会自动解析为 eid，如果无法精确匹配会自动取搜索结果第一个。

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| ename | string | 企业名称（实际查询的企业） |
| listings | array | 上市信息列表，一个企业可能有多种上市类型 |

### listings[] 通用结构

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | 上市类型：`A股` / `新三板` / `H股` |
| basicInfo | object | 基础行情信息 |
| shareholders | object | 股东信息 |
| financialReport | object | 财务报表（主要指标） |

### basicInfo 字段（A股/新三板/H股通用）

| 字段 | 类型 | 说明 |
|------|------|------|
| stockName | string | 证券简称 |
| stockCode | string | 证券代码 |
| listDate | string | 上市日期 |
| exchange | string | 交易所/板块类型 |
| totalMarketValue | string | 总市值 |
| circulatingMarketValue | string | 流通市值 |
| totalShares | string | 总股本 |
| circulatingShares | string | 流通股本 |
| pe | string | 市盈率 |
| pb | string | 市净率 |

### shareholders 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| top10 | object | 十大股东（A股/新三板）或主要股东（H股） |
| top10.reportDate | string | 报告期，如 `2024-06-30` |
| top10.items | array | 股东列表 |
| top10.items[].name | string | 股东名称 |
| top10.items[].shares | string | 持股数量 |
| top10.items[].ratio | string | 持股比例 |
| top10Tradable | object | 十大流通股东（仅A股有） |
| top10Tradable.reportDate | string | 报告期 |
| top10Tradable.items | array | 流通股东列表（结构同 top10.items） |

### financialReport 字段（A股/新三板）

无数据时为空字符串。

| 字段 | 说明 |
|------|------|
| reportDate | 报告期 |
| operatereve | 营业总收入 |
| sumprofit | 利润总额 |
| netprofit | 净利润 |
| sumasset | 资产合计 |
| sumliab | 负债合计 |
| netoperatecashflow | 经营活动产生的现金流量净额 |
| mlr | 毛利润 |
| kcfjcxsyjlr | 扣非净利润 |
| zzcjll | 总资产净利率 |
| xsmll | 销售毛利率 |
| xsjll | 销售净利率 |
| ld | 流动比率 |
| sd | 速动比率 |
| zcfzl | 资产负债率 |
| toazzl | 总资产周转率 |
| yszkzzts | 应收账款周转天数 |
| chzzl | 存货周转率 |
| jcsxjecys | 经营现金流/营业收入 |
| xtlxjcys | 销售现金流/营业收入 |

### financialReport 字段（H股）

| 字段 | 说明 |
|------|------|
| reportDate | 报告期 |
| yysr | 营业收入 |
| yylr | 营业利润 |
| zczj | 资产总计 |
| fzzj | 负债总计 |
| jyxjl | 经营活动产生的现金流量净额 |
| oprevettm | TTM营业收入 |
| mlrttm | TTM毛利润 |
| yyzsrtbzz | TTM营业总收入同比增长 |
| mlrtbzz | 毛利润同比增长 |
| zzcjllnh | 总资产净利率 |
| zzcjllttm | TTM总资产净利率 |
| zcfzl | 资产负债率 |

## 示例代码

```typescript
import { createClient } from '../src'

const client = createClient()
const result = await client.getListedInfo('贵州茅台酒股份有限公司')

console.log('企业名称:', result.ename)
for (const listing of result.listings) {
  console.log(`\n--- ${listing.type} ---`)
  console.log('证券简称:', listing.basicInfo.stockName)
  console.log('证券代码:', listing.basicInfo.stockCode)
  console.log('总市值:', listing.basicInfo.totalMarketValue)
  console.log('市盈率:', listing.basicInfo.pe)

  if (listing.shareholders.top10.items.length > 0) {
    console.log('第一大股东:', listing.shareholders.top10.items[0].name)
  }

  if (listing.financialReport.reportDate) {
    console.log('报告期:', listing.financialReport.reportDate)
    console.log('营业收入:', listing.financialReport.operatereve || listing.financialReport.yysr)
  }
}
```

## 返回示例

```json
{
  "status": "1",
  "message": "操作成功",
  "data": {
    "ename": "贵州茅台酒股份有限公司",
    "listings": [
      {
        "type": "A股",
        "basicInfo": {
          "stockName": "贵州茅台",
          "stockCode": "600519",
          "listDate": "2001-08-27",
          "exchange": "上海证券交易所",
          "totalMarketValue": "21234.56亿",
          "circulatingMarketValue": "21234.56亿",
          "totalShares": "12.56亿",
          "circulatingShares": "12.56亿",
          "pe": "33.21",
          "pb": "9.85"
        },
        "shareholders": {
          "top10": {
            "reportDate": "2024-06-30",
            "items": [
              { "name": "中国贵州茅台酒厂(集团)有限责任公司", "shares": "7.58亿", "ratio": "54.00%" }
            ]
          },
          "top10Tradable": {
            "reportDate": "2024-06-30",
            "items": [
              { "name": "中国贵州茅台酒厂(集团)有限责任公司", "shares": "7.58亿", "ratio": "54.00%" }
            ]
          }
        },
        "financialReport": {
          "reportDate": "2024-06-30",
          "operatereve": "819.47亿",
          "sumprofit": "580.12亿",
          "netprofit": "416.96亿",
          "sumasset": "2938.86亿",
          "sumliab": "812.34亿",
          "netoperatecashflow": "245.67亿",
          "mlr": "755.82亿",
          "kcfjcxsyjlr": "412.35亿",
          "zzcjll": "14.83%",
          "xsmll": "92.23%",
          "xsjll": "50.88%",
          "ld": "3.85",
          "sd": "3.41",
          "zcfzl": "27.66%",
          "toazzl": "0.29",
          "yszkzzts": "15.32",
          "chzzl": "0.18",
          "jcsxjecys": "29.98%",
          "xtlxjcys": "98.12%"
        }
      }
    ]
  }
}
```
