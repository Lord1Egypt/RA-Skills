# 查询企业主要人员

## 接口

`getEmployeesListV4`

## 描述

查询企业的主要人员信息，包括高管、董事、监事等关键人员的姓名、职务、持股比例等信息。数据来源于工商公示。

## 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ename | string | 是 | 企业名称 |

## 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 姓名 | string | 人员姓名 |
| 职务 | string | 职务名称（如：董事长、总经理等） |
| 直接持股比例 | string | 直接持股比例 |
| 综合持股比例 | string | 综合持股比例（包括间接持股） |

## 注意事项

- 默认返回前 10 位主要人员
- 持股比例可能为空
- 数据来源于国家信用信息公示系统

## 示例代码

```typescript
import { createClient } from 'qxbent-skills'

const client = createClient()

// 查询企业主要人员
const personnel = await client.getEmployeesList('上海合合信息科技发展有限公司')

personnel.forEach(person => {
  console.log('姓名:', person.姓名)
  console.log('职务:', person.职务)
  if (person.直接持股比例) {
    console.log('直接持股比例:', person.直接持股比例)
  }
  if (person.综合持股比例) {
    console.log('综合持股比例:', person.综合持股比例)
  }
  console.log('---')
})
```

## 返回示例

```json
[
  {
    "姓名": "镇立新",
    "职务": "总经理,董事长",
    "直接持股比例": "24.19%",
    "综合持股比例": "25.35%"
  }
]
```
