# flight-invoice ref

## flight_get_order_invoice_application / flight_create_order_invoice_application

Use for flight order invoice requests: checking whether an order can apply for an invoice, checking invoice application status, and creating an invoice application.

## Workflow

1. Collect or confirm the TravelKit `orderId`.
2. Always call read-only `flight_get_order_invoice_application` first.
3. If an application exists, show its status and do not create another application.
4. If `canApply` is false, show `canApplyReason` when returned and stop.
5. If `canApply` is true and the user wants to apply, collect invoice information.
6. Before `flight_create_order_invoice_application`, summarize the application details and ask for explicit confirmation.

## Required Invoice Fields

Collect these fields before creation:

- 开票公司名称 (`companyName`)
- 纳税人识别号 (`taxNo`)
- 接收邮箱 (`email`)
- 联系手机号 (`phone`)

Optional fields:

- 公司地址 (`companyAddress`)
- 公司电话 (`companyPhone`)
- 开户银行 (`bankName`)
- 银行账号 (`bankAccount`)
- 备注 (`remark`)

Use `invoiceType: normal` by default. Do not ask normal users to choose invoice type unless the tool or product later returns more supported values.

## Status Display

For query results, show in natural Chinese:

- 是否可申请
- 不可申请原因（数据返回时）
- 已有申请 ID、状态、公司名称、创建时间、发送时间（数据返回时）

For creation success, show:

- 订单号
- 发票申请 ID
- 申请状态：`pending` = 待处理 / 待发送，`sent` = 已发送
- 开票公司名称
- 创建时间
- 下一步：待财务处理或已发送，以工具返回状态为准

Do not say the invoice has been issued or emailed unless the tool explicitly returns `sent`.

## Errors

- Email format errors: ask only for the email again; do not re-collect company name, tax number, phone, or optional fields.
- Duplicate application: explain that the order has already submitted an invoice application and show returned status if available.
- Order not found, not original order, unsupported status, flight not departed, or other cannot-apply reasons: show the tool-returned reason and do not create.
- Missing optional fields never block creation unless the tool rejects them.
