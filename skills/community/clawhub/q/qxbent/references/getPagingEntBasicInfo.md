# 查询企业变更记录

## 接口

`getPagingEntBasicInfo`

## 描述

查询企业的工商变更记录，包括变更日期、变更事项、变更前后内容等信息。

## 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ename | string | 是 | 企业名称 |

## 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 变更日期 | string | 变更发生日期 |
| 变更事项 | string | 变更的事项类型 |
| 变更前 | string | 变更前的内容 |
| 变更后 | string | 变更后的内容 |

## 注意事项

- 默认返回最近 10 条变更记录
- 变更内容已格式化为纯文本
- 按时间倒序排列（最新的在前）

## 示例代码

```typescript
import { createClient } from 'qxbent-skills'

const client = createClient()

// 查询企业变更记录
const changes = await client.getChangeRecords('上海合合信息科技发展有限公司')

changes.forEach(change => {
  console.log('变更日期:', change.变更日期)
  console.log('变更事项:', change.变更事项)
  console.log('变更前:', change.变更前)
  console.log('变更后:', change.变更后)
  console.log('---')
})
```

## 返回示例

```json
[
  {
    "变更日期": "2025-07-11",
    "变更事项": "董事备案",
    "变更前": "刘忱\n江翔宇\n王少飞\n镇立新\n陈青山\n黄国强\n龙腾\n刘华 【退出】\n汤松榕 【退出】",
    "变更后": "刘忱\n江翔宇\n王少飞\n镇立新\n陈青山\n黄国强\n龙腾\n刘雅琴 【新增】\n萧志雄 【新增】"
  }
]
```
