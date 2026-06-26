# 查询企业股东信息

## 接口

`getPartnerListV3`

## 描述

查询企业的股东信息，包括股东名称、持股比例、认缴出资额等数据。数据来源于工商公示。

## 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ename | string | 是 | 企业名称 |

## 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 股东名称 | string | 股东姓名或企业名称 |
| 股东类型 | string | 股东类型（个人/企业法人等） |
| 持股比例 | string | 持股比例 |
| 认缴出资额 | string | 认缴出资金额 |
| 认缴出资日期 | string | 认缴出资日期 |
| 实缴出资额 | string | 实际缴纳出资金额 |
| 实缴出资日期 | string | 实际缴纳出资日期 |

## 注意事项

- 默认返回前 10 个股东
- 股东信息来源于国家信用信息公示系统
- 部分字段可能为空

## 示例代码

```typescript
import { createClient } from 'qxbent-skills'

const client = createClient()

// 查询企业股东信息
const shareholders = await client.getPartnerList('上海合合信息科技发展有限公司')

shareholders.forEach(sh => {
  console.log('股东名称:', sh.股东名称)
  console.log('持股比例:', sh.持股比例)
  console.log('认缴出资额:', sh.认缴出资额)
  console.log('---')
})
```

## 返回示例

```json
[
  {
    "股东名称": "江苏长电科技股份有限公司",
    "股东类型": "企业法人",
    "持股比例": "99.0939%",
    "认缴出资额": "19587.888万美元",
    "认缴出资日期": "2021-10-31"
  }
]
```
