# 第五步：下单

> **触发**：`select-sku` 返回 `status: ok` + `fresh: true`（即 `next_action: book_order`）

## 命令

```bash
python3 ./scripts/tms_delivery.py book-order
```

`book-order` 自动完成：
1. 从 session 读取 `estimatePriceRecordId` + `selectedSkuId`
2. 内联 TTL 预检（过期则报错 + 提示 `re-estimate`）
3. 调用 `runerrand_book_order` MCP
4. 成功后落盘 `orderCode`
5. 返回 `orderCode`、`scanUrl`、`senderAddr`、`receiverAddr`、`totalFee`

**LLM 无需手动 `state get` 或拼接 mcp-call 参数。**

## 分支表：`book-order` 返回

| 返回 | 动作 |
|---|---|
| `orderCode` 非空 | 按 [第六步](./step-6-payment.md) 模板回复用户 |
| `status: expired` | 询价过期，调 `re-estimate` → 展示新报价 → 等用户按新序号重选 |
| `code == 40205`（询价过期） | 同上 |
| `code == 40202`（有未完成订单） | 展示 `message`，提示用户完成/取消旧单 |
| `code == 40201`（需支付分授权） | 引导用户去腾讯出行服务小程序授权 |
| 其他错误 | 展示 `message` 原文 |

## 硬约束

- 防泄露：`orderCode` 字段名不得出现在用户端回复，仅作为业务文案"订单号：XXX"展示（见 [第六步](./step-6-payment.md)）
- 完整规则见 [SKILL.md §4](../../SKILL.md#output-leak-firewall)
