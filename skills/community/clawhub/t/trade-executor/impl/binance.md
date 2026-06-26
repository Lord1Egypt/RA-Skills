# trade-executor 实现：Binance

> 本文件是 `SKILL.md` 的实现层，描述如何通过 Binance API 执行下单操作。

## 基础信息

| 字段             | 值                                      |
| ---------------- | --------------------------------------- |
| exchange id      | `binance`                               |
| 网络白名单       | `api.binance.com`, `fapi.binance.com`   |
| 认证方式         | HMAC-SHA256 签名                        |
| API Key 环境变量 | `BINANCE_API_KEY`, `BINANCE_API_SECRET` |

## 下单请求

```
POST https://api.binance.com/api/v3/order
Headers:
  X-MBX-APIKEY: ${BINANCE_API_KEY}
  Content-Type: application/x-www-form-urlencoded

必填参数:
  symbol     = {pair}（格式 BTCUSDT，去掉 /）
  side       = BUY | SELL
  type       = LIMIT | MARKET
  quantity   = {quantity}
  timestamp  = {unix_ms}
  signature  = HMAC-SHA256({queryString}, BINANCE_API_SECRET)

限价单额外参数:
  timeInForce = GTC
  price       = {price}
```

## 签名方法

```
queryString = "symbol=BTCUSDT&side=BUY&type=LIMIT&..."
signature   = HmacSHA256(queryString, BINANCE_API_SECRET)
将 signature 附加到请求参数末尾
```

## 响应字段映射

```json
{
  "orderId": 12345678,
  "symbol": "BTCUSDT",
  "status": "FILLED | PARTIALLY_FILLED | NEW | REJECTED",
  "executedQty": "0.001",
  "cummulativeQuoteQty": "65.00",
  "fills": [{ "price": "65000", "qty": "0.001" }]
}
```

状态映射到接口层：

- `FILLED` → `filled`
- `PARTIALLY_FILLED` → `partial`
- `REJECTED` → `rejected`
- `CANCELED` → `cancelled`

## 止损止盈设置

Binance 通过 OCO 单实现止损止盈：

```
POST https://api.binance.com/api/v3/order/oco
参数: symbol, side(SELL), quantity, price(止盈), stopPrice(止损触发), stopLimitPrice(止损限价)
```

## 错误码对照

| Binance 错误码 | 含义               | 处理方式                 |
| -------------- | ------------------ | ------------------------ |
| -1013          | 金额低于最小值     | 提示用户增大数量         |
| -1021          | timestamp 超出范围 | 校准本地时间后重试       |
| -2010          | 余额不足           | 告知用户账户余额不足     |
| -1100          | 参数非法           | 检查 quantity/price 精度 |
