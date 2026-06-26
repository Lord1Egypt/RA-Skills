# trade-executor 实现：OKX

> 本文件是 `SKILL.md` 的实现层，描述如何通过 OKX API 执行下单操作。

## 基础信息

| 字段             | 值                                                |
| ---------------- | ------------------------------------------------- |
| exchange id      | `okx`                                             |
| 网络白名单       | `api.okx.com`                                     |
| 认证方式         | HMAC-SHA256 签名 + Passphrase                     |
| API Key 环境变量 | `OKX_API_KEY`, `OKX_API_SECRET`, `OKX_PASSPHRASE` |

## 请求签名方法

```
timestamp  = UTC ISO8601（如 2026-02-22T14:30:00.000Z）
method     = POST
requestPath= /api/v5/trade/order
body       = JSON 字符串

preHash    = timestamp + method + requestPath + body
signature  = Base64(HmacSHA256(preHash, OKX_API_SECRET))
```

## 下单请求

```
POST https://api.okx.com/api/v5/trade/order
Headers:
  OK-ACCESS-KEY:        ${OKX_API_KEY}
  OK-ACCESS-SIGN:       {signature}
  OK-ACCESS-TIMESTAMP:  {timestamp}
  OK-ACCESS-PASSPHRASE: ${OKX_PASSPHRASE}
  Content-Type:         application/json

Body:
{
  "instId":  "{pair}",      // 格式 BTC-USDT
  "tdMode":  "cash",        // 现货
  "side":    "buy | sell",
  "ordType": "limit | market",
  "sz":      "{quantity}",  // 基础资产数量
  "px":      "{price}"      // 限价单必填，市价单省略
}
```

## 交易对格式转换

| 接口层格式 | OKX 格式 |
| ---------- | -------- |
| BTC/USDT   | BTC-USDT |
| ETH/USDT   | ETH-USDT |
| SOL/USDT   | SOL-USDT |

## 响应字段映射

```json
{
  "code": "0",
  "data": [
    {
      "ordId": "000000000000000001",
      "sCode": "0",
      "sMsg": ""
    }
  ]
}
```

成功条件：`code == "0"` 且 `data[0].sCode == "0"`

查询成交状态：

```
GET https://api.okx.com/api/v5/trade/order?instId={pair}&ordId={ordId}
响应 data[0].state: live | partially_filled | filled | cancelled
```

状态映射到接口层：

- `filled` → `filled`
- `partially_filled` → `partial`
- `cancelled` → `cancelled`

## 止损止盈设置

OKX 通过附加算法单实现：

```
POST https://api.okx.com/api/v5/trade/order-algo
Body: {
  "instId": "{pair}", "tdMode": "cash",
  "side": "sell",     "ordType": "oco",
  "sz": "{quantity}",
  "tpTriggerPx": "{takeProfit}",
  "slTriggerPx": "{stopLoss}"
}
```

## 错误码对照

| sCode | 含义           | 处理方式                   |
| ----- | -------------- | -------------------------- |
| 51000 | 参数非法       | 检查 instId 格式和 sz 精度 |
| 51008 | 余额不足       | 告知用户账户余额不足       |
| 51010 | 账户模式不匹配 | 确认 tdMode 设置正确       |
| 50011 | 请求频率超限   | 等待 60s 后重试            |
