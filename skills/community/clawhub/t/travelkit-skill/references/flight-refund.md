# flight-refund ref

## flight_refund_quote / flight_refund_money_search / flight_refund_request / flight_refund_confirm

对已出票订单发起退票申请，**必须先估算退款金额，经用户明确确认后**再提交。

### 退票流程

1. 需要时先通过 `flight_order_detail` 查询订单
2. 确认需要退票的乘客和航段
3. 询问退票原因
4. 调用 `flight_refund_money_search` 或 `flight_refund_quote` 估算可退金额和手续费
5. 用普通语言展示：估算退款金额、手续费、乘客、航段、退票原因
6. 询问用户明确确认
7. 确认后调用 `flight_refund_request`

### 工具选择

| 工具 | 用途 |
|------|------|
| `flight_refund_money_search` | 查询退款金额估算（主要入口） |
| `flight_refund_quote` | 退款报价（部分场景使用） |
| `flight_refund_request` | 提交退票申请 |
| `flight_refund_confirm` | 独立退款确认步骤（流程需要且用户确认后才调用） |

**不得跳过估算步骤**直接提交退票申请。

### 特殊退票原因

因病、死亡、航班时刻变更或其他特殊原因退票时，工具或政策要求时需询问支持材料文件 URL。

### 未返回信息处理

手续费、退款金额、政策详情或行程文件工具未返回时，说明"未返回相关信息"，不得自行编造。退票规则若以 `*`、`>n`、`<n`、`-1`、`0` 等编码返回，先按 `output-rules` 的 Refund/Change Rule Codes 转成普通中文；不要根据起飞前/起飞后经验规则判断"不可退"，以工具返回的可退金额、手续费和规则摘要为准。

如果工具返回退票规则时伴随票号或订座记录字段，不展示订座记录字段；只展示退票费用、可退权限、订单状态和下一步。

### 错误处理

- 退款估算失败时，不提交退票申请，询问用户重试或核对订单信息
- 退票失败时，简短说明原因，展示最安全的下一步建议
