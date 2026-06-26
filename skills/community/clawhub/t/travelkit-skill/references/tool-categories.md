# tool-categories ref

## TravelKit MCP 工具分类

### 读取 / 报价工具（可按需调用）

任务需要时可直接调用，无需额外确认：

| 工具 | 说明 |
|------|------|
| `flight_search` | 搜索可订航班 |
| `flight_pricing` | 按航班号查询实时价格 |
| `flight_verify_solution` | 验证选定方案的实时价格 |
| `flight_order_detail` | 查询订单详情（by TravelKit 订单号）|
| `flight_order_detail_by_external_id` | 查询订单详情（by 外部订单号）|
| `flight_order_list` | 查询历史订单列表 |
| `flight_get_order_invoice_application` | 查询订单发票申请状态和是否可申请 |
| `flight_download_itinerary` | 下载行程单 |
| `flight_change_search` | 搜索可用改签选项 |
| `flight_refund_quote` | 退款报价 |
| `flight_refund_money_search` | 查询退款金额估算 |
| `flight_get_airline_alliances` | 查询航司联盟列表 |
| `flight_get_airline_alliance_by_airline` | 按航司查询联盟信息 |
| `flight_get_balance` | 查询账户余额 |

### 写入 / 状态变更工具（每次调用前必须获得用户明确确认）

| 工具 | 说明 |
|------|------|
| `flight_create_order` | 创建订单 |
| `flight_pay_order` | 支付订单 |
| `flight_create_order_invoice_application` | 创建订单发票申请 |
| `flight_cancel_order` | 取消订单 |
| `flight_refund_request` | 提交退票申请 |
| `flight_refund_confirm` | 确认退票 |
| `flight_change_request` | 提交改签申请 |

### 确认原则

**不得**将"帮我订"、"退了吧"等笼统意图视为写入操作的足够确认。

每次调用写入工具前，必须：

1. 重述即将执行的操作（关键字段）
2. 明确询问用户确认

详细确认内容见 `confirmation-rules` ref。
