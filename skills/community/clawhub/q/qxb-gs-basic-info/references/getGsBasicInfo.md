# 查询企业工商基本信息

## 接口

`getGsBasicInfo`

## 描述

查询企业的基本信息，包括统一社会信用代码、法定代表人、注册资本、成立日期、经营状态、疑似实控人、企业类型、营业期限、纳税人资质、社保人数、所属地区、所属行业等核心工商数据。

## 请求路径

`POST /skill/ent/public/enterprise/getGsBasicInfo`

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
| creditNo | string | 统一社会信用代码 |
| name | string | 企业名称 |
| operName | string | 法定代表人 |
| startDate | string | 成立日期，格式 YYYY-MM-DD |
| regCapi | string | 注册资本，如 "5000 万元" |
| actualCapi | string | 实缴资本 |
| status | string | 经营状态，如 "存续"、"注销" |
| actualController | object | 疑似实控人 |
| actualController.name | string | 实控人姓名 |
| actualController.stockPercent | string | 持股比例 |
| econKind | string | 企业类型，如 "有限责任公司" |
| businessTerm | string | 营业期限，如 "2010-01-01 至 无固定期限" |
| qualification | string | 纳税人资质 |
| socialSecurityInfo | object | 社保信息 |
| socialSecurityInfo.year | string | 社保年份 |
| socialSecurityInfo.count | number | 社保人数 |
| area | string | 所属地区 |
| industry | string | 所属行业（四级分类最末级） |

## 示例代码

```typescript
import { createClient } from '../src'

const client = createClient()
const result = await client.getGsBasicInfo('深圳市腾讯计算机系统有限公司')

console.log('企业名称:', result.ename)
console.log('法定代表人:', result.operName)
console.log('注册资本:', result.regCapi)
console.log('经营状态:', result.status)
console.log('实控人:', result.actualController?.name)
```

## 返回示例

```json
{
  "status": "1",
  "message": "操作成功",
  "data": {
    "ename": "深圳市某某科技有限公司",
    "creditNo": "91440300MA5FGXXX",
    "name": "深圳市某某科技有限公司",
    "operName": "张三",
    "startDate": "2018-05-10",
    "regCapi": "1000 万元",
    "actualCapi": "500 万元",
    "status": "存续",
    "actualController": {
      "name": "张三",
      "stockPercent": "65.00%"
    },
    "econKind": "有限责任公司",
    "businessTerm": "2018-05-10 至 无固定期限",
    "qualification": "一般纳税人",
    "socialSecurityInfo": {
      "year": "2023",
      "count": 128
    },
    "area": "广东省深圳市南山区",
    "industry": "软件和信息技术服务业"
  }
}
```
