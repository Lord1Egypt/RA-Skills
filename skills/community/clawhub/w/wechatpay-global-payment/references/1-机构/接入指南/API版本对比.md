# API 版本对比与升级指引（境外机构）

微信支付境外业务目前提供两个主要 API 版本：**V2** 和 **V3 Global**。本文档说明两者区别、产品能力差异、以及从 V2 升级 V3 的指引。

> ‼️ **境外推荐使用 V3**：所有 `/v3/global/...` 接口、付款码 V3 化、新能力（跨境分账 / 委托代扣 / 海关报关 / H5 权限申请）仅 V3 提供。如非历史原因，**新接入直接使用 V3**。

---

## 1. 版本概览

| 维度 | API V2 | API V3 Global |
|------|--------|--------------|
| **数据格式** | XML | JSON |
| **签名方式** | MD5 / HMAC-SHA256 | RSA（非对称加密，`WECHATPAY2-SHA256-RSA2048`） |
| **API Key 用途** | 签名和验签 | 敏感信息的 AES 加解密 |
| **证书用途** | 双向 TLS 验证（HTTPS 客户端证书）| 请求签名和验签 |
| **请求方法** | 仅 POST | GET / POST / PUT / DELETE（RESTful）|
| **请求头** | 无特殊要求 | `Authorization`（WECHATPAY2-SHA256-RSA2048）|
| **错误格式** | XML 中 return_code + return_msg | JSON 中 code + message + detail |
| **URL 前缀**（境外） | 极少使用 | `/v3/global/...`（统一前缀） |
| **安全等级** | 中 | 高（证书签名 + 加密传输） |
| **维护状态** | 存量维护（不新增功能） | **境外主力版本，持续迭代** |

---

## 2. 各版本支持的产品（境外机构视角）

| 产品 | API V2 | API V3 Global |
|------|--------|--------------|
| 付款码支付（Quick Pay）| ✅ | ✅ ⭐ |
| Native 支付 | ✅ | ✅ |
| 公众号支付（JSAPI）| ✅ | ✅ |
| 小程序支付 | ✅ | ✅ |
| APP 支付 | ✅ | ✅ |
| H5 支付 | ✅ | ✅ |
| **委托代扣**（Auto Debit）| ❌ | ✅（仅 V3）|
| **跨境分账**（Profit Sharing）| ❌ | ✅（仅 V3）|
| **海关报关** | ✅ | ✅ |
| **子商户进件** | ✅ | ✅ |
| **H5 支付权限申请** | ❌ | ✅（仅 V3）|
| 退款 | ✅ | ✅ |
| 对账单下载 | ✅ | ✅ |

⚠️ **核心结论**：境外 V3 已覆盖 V2 的所有能力 + 新能力。**新项目直接用 V3**。

---

## 3. 是否强制升级

**不强制。已接入 V2 的机构可继续使用 V2 接口，仍正常可用。**

但建议升级，原因：
- V2 所有接口已停止新功能开发
- **跨境分账、委托代扣、H5 权限申请**等新能力**仅 V3** 支持
- V3 安全性更高（RSA + AES）
- V3 是 RESTful 风格，更易维护
- ⚠️ **境外付款码已 V3 化**，与境内"付款码仅 V2"不同；从境内迁移到境外时，付款码相关代码必须重写

---

## 4. V2 → V3 升级指引

### 4.1 哪些参数可复用

| 参数 | 是否可复用 | 说明 |
|------|-----------|------|
| `sp_appid` / `sub_appid` | ✅ | 同一 AppID 可在 V2 和 V3 共用 |
| `sp_mchid` / `sub_mchid` | ✅ | 机构号 / 子商户号无变化 |
| `sub_openid` / `sp_openid` | ✅ | OpenID 体系不变 |

### 4.2 哪些需要重新准备

| 项 | V2 | V3 |
|---|----|----|
| **API 密钥** | V2 API Key（签名/验签） | V3 必须**单独设置 APIv3 密钥**（AES 加解密）|
| **证书** | 双向 TLS 证书（apiclient_cert.pem + apiclient_key.pem）| 商户证书序列号 + 私钥（用于 RSA 签名） |
| **平台证书** | 不需要 | **必须下载**微信支付平台证书（用于验签）|

### 4.3 升级步骤

```
Step 1：在商户平台设置 APIv3 密钥
  ↓
Step 2：获取机构证书序列号（用 OpenSSL 查看已有证书）
  ↓
Step 3：下载平台证书（调 V3 的 /v3/global/certificates，用 APIv3 密钥解密）
  ↓
Step 4：改造签名逻辑（从 HMAC-SHA256 → RSA）
  ↓
Step 5：改造请求格式（XML → JSON）
  ↓
Step 6：改造回调解密（V3 回调是加密的，用 APIv3 密钥解密）
  ↓
Step 7：小流量灰度（V2 和 V3 并行运行）
  ↓
Step 8：完全切换到 V3
```

### 4.4 双版本并行时注意

在升级过渡期，同一机构号可能同时处理 V2 和 V3 订单：
- **订单号** 共享同一命名空间（V2 和 V3 的 `out_trade_no` 不能重复）
- **回调** 可能并存，需要**各自的 notify_url**
- **对账** 同一账单包含 V2 和 V3 的交易
- **退款** 支付用 V2，退款可以用 V3（但建议用同版本）

### 4.5 证书要求

V3 强制要求：
- ⚠️ **必须**使用微信支付签发的**商户证书**（不可自签名）
- 商户证书的序列号放在 `Authorization` 头中
- 平台证书必须通过 API 下载（不能直接使用旧证书）

---

## 5. 回调差异

### 5.1 V2 回调

```xml
<xml>
  <return_code>SUCCESS</return_code>
  <out_trade_no>20230101123456</out_trade_no>
  <total_fee>100</total_fee>
  <sign>ABC123...</sign>
</xml>
```

- **明文传输**
- 验签：用 API Key 做 MD5/HMAC-SHA256

### 5.2 V3 回调

```json
{
  "id": "...",
  "event_type": "TRANSACTION.SUCCESS",
  "resource": {
    "algorithm": "AEAD_AES_256_GCM",
    "ciphertext": "加密内容",
    "nonce": "...",
    "associated_data": "..."
  }
}
```

- **敏感内容加密传输**
- 需用 APIv3 密钥**解密** `ciphertext`
- 解密后才能拿到订单号、金额等信息
- 验签：用平台证书公钥做 RSA

### 5.3 改造要点

从 V2 切到 V3 的回调处理：
1. 解析 JSON（不是 XML）
2. 验签：获取平台证书 → RSA 验签
3. 解密：提取 `resource.ciphertext` → AES-256-GCM 解密
4. 解析解密后的 JSON 获取订单信息
5. 应答格式：`{"code": "SUCCESS", "message": "成功"}`（JSON，不是 XML）

详细回调设计见 [📄 回调处理](./回调处理.md)。

---

## 6. URL 地址对比

| 接口 | V2 | V3 Global |
|------|----|-----|
| JSAPI 下单 | XML POST | `/v3/global/transactions/jsapi` |
| Native 下单 | XML POST | `/v3/global/transactions/native` |
| APP 下单 | XML POST | `/v3/global/transactions/app` |
| H5 下单 | XML POST | `/v3/global/transactions/h5` |
| 付款码支付 | ⚠️ 境外已 V3 化 | `/v3/global/transactions/micropay` |
| 查单 | XML POST | `/v3/global/transactions/out-trade-no/{}` |
| 关单 | XML POST | `/v3/global/transactions/out-trade-no/{}/close` |
| 撤销 | XML POST | `/v3/global/transactions/out-trade-no/{}/reverse` |
| 退款 | XML POST | `/v3/global/refund/domestic/refunds`（V3 退款路径） |
| 退款查询 | XML POST | `/v3/global/refund/domestic/refunds/{out_refund_no}` |
| 跨境分账 | ❌ 不支持 | `/v3/global/profit-sharing/orders` 等 |
| 子商户进件 | XML POST | `/v3/global/applyment4sub/applyment/` |

V3 使用 RESTful 设计，URL 更清晰语义化。

---

## 7. 金额单位

- V2 和 V3 **都是分**（最小货币单位的整数）
- `total_fee` (V2) = `amount.total` (V3)
- 1 元 = 100 分
- 境外多币种场景：`amount.currency` 必填，按 ISO 4217 三位字母代码

---

## 8. 升级常见问题

### Q1：V2 和 V3 可以同时用吗？
**A**: 可以。同一机构号可同时调 V2 和 V3 接口。建议在升级过渡期双跑，稳定后下线 V2。

### Q2：升级后原来的机构证书还能用吗？
**A**:
- V2 的"双向 TLS 证书"和 V3 的"签名证书" **是同一套**证书（apiclient_cert.pem + apiclient_key.pem）
- V3 不再用证书做 TLS 握手，而是用证书的**公钥做 RSA 签名**
- 所以**无需换新证书**，但需要额外：
  - 获取证书**序列号**（用 OpenSSL 查）
  - **单独设置 APIv3 密钥**

### Q3：V3 回调能用 V2 的密钥验签吗？
**A**: **不能**。V3 回调验签用**平台证书公钥**（通过 API 下载），与 V2 的 API Key 完全无关。

### Q4：升级到 V3 后用户支付体验有变化吗？
**A**: **完全没有**。用户端感知的只是"微信支付调起"，服务端用 V2 还是 V3 不影响用户。

### Q5：V2 会什么时候下线？
**A**: 微信支付**暂未公布** V2 的下线时间。但考虑到：
- 新功能只在 V3 上
- 安全性考虑

建议**主动**升级，不要等官方下线通知。

### Q6：境外付款码为什么已经 V3 化？
**A**:
- 境内付款码因为历史原因仍是 V2（XML + MD5）
- 境外付款码**直接以 V3 形态发布**（JSON + RSA）
- 这是从境内迁移到境外时**最容易踩坑**的差异点
- 迁移时付款码相关代码必须重写为 V3

### Q7：V3 接口有限流吗？
**A**: 有，但限制宽松：
- 单机构号默认 **600 QPS**
- 不同接口可能独立限流
- 触发限流返回 `RATE_LIMITED`

### Q8：境外 V3 与境内 V3 的差异？
**A**: 主要差异：
- 域名不同（`apihk` vs `api`）
- 路径前缀不同（`/v3/global/...` vs `/v3/pay/...`）
- 必须传 `amount.currency`（境内默认 CNY）
- 必带字段统一为 `sp_mchid + sub_mchid`（境内分直连商户 / 服务商）
- 证书与密钥**完全独立**，境内境外不通用

---

## 9. 相关文档

- 签名验签详解：[📄 签名与验签规则](./签名与验签规则.md)
- 通用开发参数：[📄 开发参数获取](./开发参数获取.md)
- 回调处理：[📄 回调处理](./回调处理.md)
- 网络问题排查：[📄 网络问题指引](./网络问题指引.md)
- V2 升级 V3 官方指南：https://pay.weixin.qq.com/doc/global/v3/zh/4013080935
