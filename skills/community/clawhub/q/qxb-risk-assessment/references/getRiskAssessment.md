# 查询企业风险排查（综合）

## 接口

`getRiskAssessment`

## 描述

查询企业的空壳特征、合同违约情况、日常经营风险（高中低）、企业存续状态（破产/解散/经营异常），一次调用覆盖四大风险维度。

## 请求路径

`POST /skill/ent/public/enterprise/getRiskAssessment`

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

返回 data 中包含 4 个维度：

### shellCompanyCheck - 空壳企业排查

| 字段 | 类型 | 说明                                  |
|------|------|-------------------------------------|
| shellProbability | string | 空壳概率：`低` / `中` / `高`，空字符串表示企业不是空壳公司 |
| abnormalFeatures | array | 异常特征列表，最多3条                         |
| abnormalFeatures[].feature | string | 异常特征名称，如 "经营异常"、"严重违法失信"            |
| abnormalFeatures[].description | string | 异常特征描述                              |

### contractBreach - 合同违约情况

| 字段 | 类型 | 说明                               |
|------|------|----------------------------------|
| breachLevel | string | 违约等级，如 `L4（中等风险）`，空字符串表示企业没有违约情况 |
| breachCount | string | 5年内违约次数，如 `703次`                 |
| breachScale | string | 5年内违约规模，格式化金额，如 `76.48亿元`        |

### qixinRisk - 日常经营风险

| 字段 | 类型 | 说明 |
|------|------|------|
| selfRiskCount | number | 自身风险总数量 |
| highRiskCount | number | 高风险数量 |
| highRiskItems | array | 高风险信息列表，最新10条 |
| mediumRiskCount | number | 中风险数量 |
| mediumRiskItems | array | 中风险信息列表，最新10条 |
| lowRiskCount | number | 低风险数量 |
| lowRiskItems | array | 低风险信息列表，最新10条 |
| tipCount | number | 提示信息数量 |
| relatedRiskCount | number | 关联风险总数量 |
| relatedHighRiskCount | number | 关联风险-高风险数量 |
| relatedMediumRiskCount | number | 关联风险-中风险数量 |
| relatedLowRiskCount | number | 关联风险-低风险数量 |

**riskItems 子项结构（highRiskItems / mediumRiskItems / lowRiskItems 通用）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 风险标题，如 "限制高消费"、"被执行人"、"终本案件" |
| date | string | 日期，格式 YYYY-MM-DD |
| details | string[] | 详情数组，每项格式为 `字段名：字段值` |

### entSurvival - 企业存续情况

| 字段 | 类型 | 说明 |
|------|------|------|
| bankruptcyRisk | string | 破产风险描述 |
| abnormalDissolution | string | 非正常解散描述 |
| operatingStatus | string | 经营状态描述 |

## 示例代码

```typescript
import { createClient } from '../src'

const client = createClient()
const result = await client.getRiskAssessment('恒大地产集团有限公司')

console.log('企业名称:', result.ename)
console.log('空壳概率:', result.shellCompanyCheck.shellProbability)
console.log('违约等级:', result.contractBreach.breachLevel)
console.log('自身风险总数:', result.qixinRisk.selfRiskCount)
console.log('高风险数量:', result.qixinRisk.highRiskCount)
console.log('经营状态:', result.entSurvival.operatingStatus)
```

## 返回示例

```json
{
  "status": "1",
  "message": "操作成功",
  "data": {
    "ename": "恒大地产集团有限公司",
    "shellCompanyCheck": {
      "shellProbability": "高",
      "abnormalFeatures": [
        {
          "feature": "经营异常",
          "description": "有 6 条经营异常（无法联系/年报未申报），疑似无真实经营场所或无实际经营"
        },
        {
          "feature": "严重违法失信",
          "description": "被列入严重违法失信名单，且尚未移出"
        }
      ]
    },
    "contractBreach": {
      "breachLevel": "L4（中等风险）",
      "breachCount": "703次",
      "breachScale": "76.48亿元"
    },
    "qixinRisk": {
      "selfRiskCount": 28124,
      "highRiskCount": 12405,
      "highRiskItems": [
        {
          "title": "限制高消费",
          "date": "2026-04-30",
          "details": [
            "案号：（2026）粤0112执4875号",
            "限消法人或组织：恒大地产集团有限公司",
            "关联对象：赵长龙",
            "案由：票据追索权纠纷"
          ]
        }
      ],
      "mediumRiskCount": 615,
      "mediumRiskItems": [],
      "lowRiskCount": 15104,
      "lowRiskItems": [],
      "tipCount": 1878,
      "relatedRiskCount": 888245,
      "relatedHighRiskCount": 397219,
      "relatedMediumRiskCount": 107411,
      "relatedLowRiskCount": 312914
    },
    "entSurvival": {
      "bankruptcyRisk": "经营不善，（可能）被申请破产",
      "abnormalDissolution": "未发现非正常解散的风险",
      "operatingStatus": "企业经营状态正常"
    }
  }
}
```
