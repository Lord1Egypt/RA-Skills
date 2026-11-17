# API contract (Alipay AI pay-per-use official protocol)

服务基址由 `--api-base`（或环境变量 `SRV_API_BASE`）给出，下文写作 `{base}`。

## 端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `{base}/health` | 健康检查 |
| POST | `{base}/api/v1/render` | 资源端点：402 → 付款 → 携 `Payment-Proof` 重放 → 交付 |
| GET | `{base}/api/v1/render/{out_trade_no}/artifacts/{name}` | 下载已交付产物 |

> 本协议**没有**订单查询端点。状态不明时用**同一** `Payment-Proof` 重放同一请求即可：
> 服务端按订单幂等，不会重复扣费，也不会重复发资源。

## POST {base}/api/v1/render

请求体：

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `world_id` | string | `sr-video-demo` | 世界标识 |
| `genesis_seed` | int | `42` | 创世种子 |
| `agent_count` | int | `5` | 灵魂数量 |
| `tick_from` / `tick_to` | int | `0` / `149` | tick 区间（含端点） |
| `framing.resolution` | [w, h] | `[854, 480]` | 输出分辨率 |
| `framing.fps` | int | `30` | 必须是 10 的整数倍 |
| `shot` | object | `{"preset": "demo"}` | 镜头图：预设名或内联 `shots` |
| `samples` | int | `3` | 抽样 PNG 数量 |
| `tier` | string | `R1` | 渲染档（R2 尚未实现） |

### 未付款 → HTTP 402

响应头 `Payment-Needed` = **Base64URL 编码的账单 JSON**，两层结构：

```json
{
  "protocol": {
    "out_trade_no": "ORDER_1792435862849_03d563d1dc93",
    "amount": "0.20",
    "currency": "CNY",
    "resource_id": "/api/v1/render",
    "pay_before": "2026-10-20T03:14:03.729010+08:00",
    "seller_signature": "<应用私钥 RSA2 签名>",
    "seller_sign_type": "RSA2",
    "seller_unique_id": "2088xxxxxxxxxxxx"
  },
  "method": {
    "seller_name": "商户名",
    "seller_id": "2088xxxxxxxxxxxx",
    "seller_app_id": "2021xxxxxxxxxxxx",
    "goods_name": "第二现实可复现视频渲染服务",
    "seller_unique_id_key": "seller_id",
    "service_id": "API_xxxxxxxx"
  }
}
```

商家签名的入参固定 8 个字段，按 key 字典序拼成 `k=v&k=v`：
`amount`、`currency`、`goods_name`、`out_trade_no`、`pay_before`、`resource_id`、
`seller_id`、`service_id`。

响应体（仅调试用，智能体支付依据是响应头）：

```json
{ "code": "Payment-Needed", "message": "需要支付", "out_trade_no": "...", "amount": "0.20",
  "currency": "CNY", "goods_name": "..." }
```

### 已付款 → HTTP 200

请求头必须带 `Payment-Proof`（Base64URL 的
`{protocol:{payment_proof, trade_no}, method:{client_session}}`），**请求体必须与第一次完全一致**。

```json
{
  "resource_id": "/api/v1/render",
  "content": { "status": "success",
               "artifacts": [ { "name": "world.mp4", "size": 1234, "sha256": "...",
                 "url": "/api/v1/render/<out_trade_no>/artifacts/world.mp4" } ],
               "manifest": { "...": "签名清单摘要" } },
  "trade_no": "2026...",
  "out_trade_no": "ORDER_...",
  "already_fulfilled": false,
  "fulfillment_confirmed": true
}
```

同时返回响应头 `Payment-Validation` = Base64URL 的
`{trade_no, out_trade_no, validated: true, resource_id}`——它是资源归属证明，客户端应校验。

## 错误语义

| HTTP | 含义 | 客户端动作 |
|---|---|---|
| 400 | 参数超出档位上限 | 拆分渲染或换更大档位 |
| 401 | 付款凭证非法 | 不交付；重新付款 |
| 402 | 未付款、验付未通过或账单过期 | 走 `pay` → `complete`；**不返回任何资源** |
| 404 | 产物不存在 | 先确认订单已履约 |
| 502 | 资源已生成但履约确认失败 | **用同一 Payment-Proof 重试**（不重复扣费、不重复发资源） |

## 幂等与防重复扣费

- 订单在返回 402 前**已落库**（`out_trade_no` 唯一索引），付款凭证回来能映射回本地订单。
- 验付成功仍要校验：`active=true`、金额一致、`out_trade_no` 一致、`resource_id` 一致、
  订单状态允许履约——任一不满足即回 402，不发资源。
- 履约权用事务原子抢占：**只生成一次资源**；重复请求复用已持久化结果。
- 履约确认失败只重试确认，订单停留在"待确认"，不重复生成资源、不重复扣费。
- 生产环境关键字段（金额、`resource_id`、交易号）为空一律按异常处理；沙箱容错逻辑不得带进生产。

## 沙箱与生产

| 项 | 沙箱 | 生产 |
|---|---|---|
| 网关 | `https://openapi-sandbox.dl.alipaydev.com/gateway.do` | `https://openapi.alipay.com/gateway.do` |
| `service_id` | `api_mock_service_id` | 服务市场注册返回的真实 `serviceId` |
| 单价 | 固定 0.01 元/次 | 各档位在服务市场登记的单价 |

三处价格必须一致：支付宝服务登记价 = 服务端账单价 = SkillHub 详情页展示价。
