# 小安智能健身｜MCP 工具契约 v1

> 状态：MVP 冻结版。后端实现必须遵守本契约；允许新增可选字段，不得无版本升级地改变既有字段含义。

## 共同约定

- 所有日期使用 `YYYY-MM-DD`，时区为 `Asia/Shanghai`。
- MCP 工具输入输出中的金额以人民币“分”为单位，`20000` 表示 ¥200；写入飞书预约排班表时使用“金额（元）”字段，需转换为 `200`。
- 业务工具返回都包含 `ok`。失败时包含稳定的 `code` 和可向用户解释的 `message`。
- 创建操作必须使用 `idempotency_key` 防止超时重试造成重复订单。
- 首版只创建预约，不处理银行卡、在线支付、自动退款、自动取消或自动改期。
- 首版飞书记录使用中文业务字段和中文业务状态；不要把英文状态值写入飞书。

## 飞书写入映射

`create_booking` 成功时，MCP 必须写入飞书“预约订单”表：

| MCP / 固定值 | 飞书字段 | 写入规则 |
|---|---|---|
| 生成的 `booking_id` | 订单ID | 如 `XA-20260718-0001` |
| `idempotency_key` | 幂等键 | 原样写入，用于防重复 |
| 固定值 | 订单状态 | 新订单写“待确认” |
| 固定值 | 教练 | 首版写“安教练” |
| `service_id` | 商品 ID | 首版 `xiaoan-pt-60` |
| 服务名称 | 商品名称 | `1 对 1 健身私教训练` |
| `price_cents / 100` | 金额（元） | 首版写 `200` |
| `duration_minutes` | 服务时长（分钟） | 首版写 `60` |
| `customer_name` | 客户名字 | 原样写入 |
| `customer_phone` | 客户电话 | 原样写入，仅商家可见 |
| 手机号后四位 | 手机号后四位 | 从 `customer_phone` 派生 |
| 当前时间 | 下单时间 | `YYYY-MM-DD HH:mm:ss` |
| `requested_date` | 预定日期 | `YYYY-MM-DD 00:00:00` |
| `requested_time_slot` | 预定时间段 | 一小时一行，如 `14:00-15:00` |
| 空 | 确认时间 | 商家确认后再填 |
| `fitness_goal` | 健身目标 | 原样写入 |
| `health_risk` | 健康风险 | `none`、`reported`、`unsure` |
| `health_note` | 健康风险说明 | 仅保存必要简短说明 |
| 派生值 | 是否需人工评估 | `reported/unsure` 写“是”，否则写“否” |
| 固定值 | 付款方式 | 首版写“到店支付” |
| 固定值 | 支付状态 | 新订单写“待付款” |
| 调用来源 | 下单渠道 | 默认“个人 Agent”；公域接入后写“美团”“千问”等 |
| 当前时间 | 更新时间 | 创建时同下单时间 |
| 空或内部说明 | 商家备注 | 不对用户返回 |
| 默认公开说明 | 对外备注 | 如“预约已提交，等待商家确认具体时间” |

排班冲突判断：同一 `教练 + 预定日期 + 预定时间段` 已存在未作废订单时，不自动创建第二笔有效订单，返回可解释的失败信息或提示换时段。

## 1. `list_services`｜查询可预约服务

在介绍价格、时长、地址、营业时间或开始预约前调用。首版无必填参数。

### 输入

```json
{}
```

### 成功输出

```json
{
  "catalog_version": "v1.0-test",
  "services": [
    {
      "service_id": "xiaoan-pt-60",
      "name": "1 对 1 健身私教训练",
      "merchant_name": "小安智能健身",
      "coach": "安教练",
      "city": "北京",
      "price_cents": 20000,
      "price_yuan": 200,
      "duration_minutes": 60,
      "address": "崇文门地铁站 G 口东 200 米底商 1 层",
      "business_hours": "每天 10:00–20:00",
      "payment_method": "测试阶段到店支付"
    }
  ]
}
```

## 2. `create_booking`｜创建预约

只有 Agent 已展示预约摘要并获得用户明确确认后调用。

### 输入

```json
{
  "idempotency_key": "由客户端为本次提交生成的唯一字符串",
  "service_id": "xiaoan-pt-60",
  "customer_name": "测试用户",
  "customer_phone": "13800138000",
  "requested_date": "2026-07-18",
  "requested_time_slot": "14:00-15:00",
  "fitness_goal": "改善体能并减脂",
  "health_risk": "none",
  "health_note": "",
  "user_confirmed": true
}
```

字段规则：

- `health_risk` 只允许 `none`、`reported`、`unsure`。
- `health_note` 仅保存用户主动提供且预约必要的简短说明。
- `user_confirmed` 必须为 `true`，否则返回 `CONFIRMATION_REQUIRED`。
- 日期、时段不代表商家已有空位；创建后订单状态始终从“待确认”开始。

### 成功输出

```json
{
  "ok": true,
  "duplicated": false,
  "risk_review_required": false,
  "booking": {
    "booking_id": "XA-20260718-0001",
    "order_status": "待确认",
    "service_name": "1 对 1 健身私教训练",
    "requested_date": "2026-07-18 00:00:00",
    "requested_time_slot": "14:00-15:00",
    "confirmed_at": "",
    "payment_status": "待付款",
    "public_note": "预约已提交，等待商家确认具体时间。"
  },
  "message": "预约已创建，并已写入飞书多维表格。"
}
```

当 `health_risk` 为 `reported` 或 `unsure` 时，返回 `risk_review_required: true`，但不要返回诊断结论。

## 3. `get_booking`｜查询预约

用于用户凭订单号查询状态。为避免他人仅凭订单号查看信息，同时校验预留手机号后四位。

### 输入

```json
{
  "booking_id": "XA-20260718-0001",
  "phone_last4": "8000"
}
```

### 成功输出

```json
{
  "ok": true,
  "booking": {
    "booking_id": "XA-20260718-0001",
    "order_status": "待确认",
    "service_name": "1 对 1 健身私教训练",
    "requested_date": "2026-07-18 00:00:00",
    "requested_time_slot": "14:00-15:00",
    "confirmed_at": "",
    "payment_status": "待付款",
    "public_note": "预约已提交，等待商家确认具体时间。"
  }
}
```

不要返回完整手机号、内部备注或详细健康说明。

## 错误码

| 错误码 | 含义 | Agent 应对 |
|---|---|---|
| MCP 参数错误 | 缺少字段、格式错误、商品不存在或用户未确认 | 指出需要修正的字段，不创建订单 |
| `BOOKING_NOT_FOUND` | 未找到订单 | 检查订单号，不猜测状态 |
| `TIME_SLOT_CONFLICT` | 同一教练在该日期和时段已有未作废订单 | 请用户更换时间段，不创建第二笔订单 |
| `duplicated: true` | 相同幂等键已处理 | 使用返回的原订单，不再次创建 |
| MCP / 飞书异常 | 调用超时或后端暂时不可用 | 明确说明结果不确定，先查单或人工核查，禁止盲目重试创建 |
