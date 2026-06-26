# 定价规则（统一版）

## 一句话

**¥0.99 一次性买断，之后所有功能永久免费。**

## 免费额度（3次，不分类型）

未付费用户共有 **3 次免费机会**，以下所有操作共享这 3 次：

| 操作 | 消耗免费次数 |
|------|:-----------:|
| 上传自有模板 + 填充内容 | 1 次 |
| 描述需求，让我从零创建模板 | 1 次 |
| 用内置模板库生成文档 | 1 次 |
| 下载内置模板 | 1 次 |

**3 次用完 → 提醒付费 → 交 ¥0.99 → 永久畅用**

不区分"自有模板免费3次"或"内置模板库付费"——**所有操作统一 3 次免费额度**，超了锁住，付了费全开。

## 付费检查流程

调 `key_balance()` 查看：

```json
{
  "ok": true,
  "data": {
    "paid": false,              // 是否已付费
    "free_uses_remaining": 2,   // 剩余免费次数
    "total_free_uses": 3        // 总免费次数
  }
}
```

### 情景判断

| paid | free_uses_remaining | 行为 |
|:----:|:-------------------:|------|
| true | — | 直接干活，不提收费 |
| false | ≥ 1 | 干活，每次消耗 1 次，提醒"还剩余 X 次免费" |
| false | 0 | 告知用户免费额度用完，引导付费 |

## 收费话术

**还剩免费次数时（每次干完活说）：**
> "已生成。你还有 N 次免费机会，用完可以 ¥0.99 买断终身使用。"

**免费次数用完时：**
> "免费次数已用完。¥0.99 买断后所有模板和功能不限次数、不限类型，要付费吗？"

**用户同意付费：**
> 调 `pay_for_download()` → 展示付款方式 → 用户付完再干活

**已付费用户：**
> 全程不提钱，直接干。

## 支付流程（AI收 / alipay-a2a-prod）

用户确认付费后，龙虾通过支付宝 AI 收完成支付。**用户不需要扫码，龙虾代劳**。

### 步骤

1. **创建订单** — 调 `pay_for_download()` 或 `POST /api/v1/pay/create`
   - 返回 `payment_needed` 结构（含 RSA2 签名、金额 ¥0.99、订单号）
   
2. **发起支付** — 龙虾将 `payment_needed` 提交给支付宝 AI 收
   - 用户的支付宝 APP 会收到支付请求
   - 用户在支付宝里点确认即可
   
3. **验证支付** — 支付宝返回 `trade_no` + `payment_proof`
   - 龙虾调 `POST /api/v1/pay/verify` 传入这两个值
   - 服务器向支付宝验证 → 开通 premium → 永久解锁

### 龙虾操作清单

```
用户同意付费后：
1. 调 POST /api/v1/pay/create {api_key, amount:"0.99"}
   → 拿到 payment_needed（含 protocol + scheme）
2. 将 payment_needed 提交给支付宝 AI 收
   → 用户在支付宝确认
3. 拿到 trade_no 和 payment_proof 后：
   POST /api/v1/pay/verify {api_key, trade_no, payment_proof}
   → verified=true → 永久解锁
4. 然后继续干活，不再提收费
```

### 支付 API

| 工具 | 说明 |
|------|------|
| `pay_for_download()` | 创建 ¥0.99 支付订单 → 返回 Payment-Needed |
| `pay_verify(trade_no, payment_proof)` | 验证支付凭证 → 开通 premium |
| `key_balance()` | 查余额 + 剩余免费次数 |
