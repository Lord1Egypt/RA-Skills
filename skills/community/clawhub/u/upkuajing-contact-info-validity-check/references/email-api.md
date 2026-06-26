# 邮件有效性检测 API

## 请求参数

### Header
- `Authorization`: Bearer Token (必填)

### Body
- `emails` (array): 邮箱地址列表

## 响应字段

### code
- 类型: integer
- 说明: 状态码

### msg
- 类型: string
- 说明: 消息

### data.list
- 类型: array
- 说明: 检测结果列表

### data.list[].email
- 类型: string
- 说明: 被检测的邮箱地址

### data.list[].status
- 类型: integer
- 说明: '状态: 0-未检测, 1-有效, 2-无效, 3-未知'

### data.list[].reason
- 类型: string
- 说明: 无效原因

### data.total
- 类型: integer
- 说明: 总数量

### fee.apiCost
- 类型: integer
- 说明: API消耗费用(分钱)

### fee.accountBalance
- 类型: integer
- 说明: 账户余额(分钱)
