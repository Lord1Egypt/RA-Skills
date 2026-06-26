# 第六步：引导支付

> **触发**：`next_state == step6-payment`（`orderCode` 已写入，支付未确认）

## 回复方式

`book-order` 返回值已包含 `reply_template` 字段，**原样贴给用户即可**。

`reply_template` 内部已：
- 使用 `payInfo.codeUrl`（首选，weixin:// 协议）通过 `https://api.qrserver.com/v1/create-qr-code/` 编码为二维码图片
- `codeUrl` 为空时兜底使用 `payInfo.scanUrl`
- 图片下方附带 `scanUrl` 纯文本兜底链接
- 已包含订单号 / 寄收地址 / 费用 / 支付完成提示

## 硬约束

- **禁止退化成纯链接**：必须保留 `![支付二维码](...)` 的 markdown 图片语法，不得只贴一行"点击支付"
- **禁止丢弃模板**：不得用自然语言改写 `reply_template`，原样输出
- `reply_template` 缺失（codeUrl + scanUrl 双空） → 上报异常，不凭空生成支付入口

## `totalFee` 来源

由脚本从 session 中取出（`skuDetails[selectedSkuId].totalFee`，已是**元**字符串），无需 LLM 自行查找。
