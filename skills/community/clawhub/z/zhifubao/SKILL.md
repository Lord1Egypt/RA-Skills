---
name: "支付宝"
version: "1.0.0"
description: "支付宝开放平台接入指南。Use for: (1) 选对支付产品——当面付/APP支付/手机网站/电脑网站/小程序支付的适用场景与费率结构, (2) 沙箱联调、RSA2 签名与异步通知验签的正确姿势, (3) 高频报错排查（ISV权限不足/签名错误/回调不来）。Alipay Open Platform integration guide: payment-product selection, sandbox testing, RSA2 signing, and async-notification pitfalls."
tags: ["alipay", "zhifubao", "payment", "openapi", "fintech"]
author: "ClawSkills Team"
category: "finance"
---

# 支付宝开放平台接入 Skill

面向要接支付宝支付的开发者：先选对产品，再按正确姿势联调，
最后避开异步通知的经典大坑。

## 第一步：选对支付产品

| 产品 | 场景 | 用户操作 |
|------|------|----------|
| 当面付 | 线下扫码（顾客扫店家/店家扫顾客） | 出示付款码或扫商家码 |
| APP 支付 | 自家原生 App 内 | 拉起支付宝 App |
| 手机网站支付 | 手机 H5 页面 | 跳支付宝 H5 或拉起 App |
| 电脑网站支付 | PC 网页 | 扫码或登录支付 |
| 小程序支付 | 支付宝小程序内 | 免跳转 |
| 周期扣款/预授权 | 订阅、押金 | 一次签约多次扣 |

选型速判：线下收银→当面付；App→APP支付；微信里的 H5 无法用支付宝，
要么引导浏览器打开要么换微信支付（见 `weixin` skill 支付章节）。

## 接入正确姿势

1. **先沙箱后生产**：开放平台控制台有独立沙箱环境（沙箱 AppID、
   沙箱网关、沙箱版支付宝 App），联调全流程跑通再切生产参数
2. **密钥体系（RSA2）**：开发者生成应用私钥/公钥，公钥传平台换
   **支付宝公钥**。记牢方向：**请求用你的私钥签名，验回调用
   支付宝公钥验签**——两对密钥四把钥匙，混了必翻车
3. **用官方 SDK**：alipay-sdk 有 Java/PHP/Python/Node/Go 版，
   签名/验签/加解密全封装，不要手写签名
4. **接口协议**：统一网关 `openapi.alipay.com/gateway.do`，
   method 参数区分接口（如 `alipay.trade.precreate` 当面付预下单、
   `alipay.trade.page.pay` 电脑网站支付），参数以官方文档为准

## 异步通知（notify）经典大坑

- 回调处理完必须回写纯字符串 `success`（不是 JSON），否则支付宝
  会按 4m/10m/…间隔重发 8 次，你会看到"重复回调"
- **必须验签 + 幂等**：验支付宝公钥签名防伪造，按 out_trade_no
  幂等防重复入账
- 本地开发收不到回调是正常的（公网不可达），用内网穿透或沙箱
  轮询查单（`alipay.trade.query`）兜底
- 金额校验：回调里的 total_amount 要和你订单金额比对，防篡改

## 高频报错排查

| 报错 | 根因 | 处理 |
|------|------|------|
| ISV 权限不足 (isv.insufficient-isv-permissions) | 产品没签约或没绑定到该 App | 控制台确认产品状态"已生效" |
| 签名错误 (invalid-signature) | 密钥对不匹配/字符集不一致/参数拼接错 | 用 SDK；检查是否误用沙箱密钥打生产 |
| 系统繁忙 (aop.ACQ.SYSTEM_ERROR) | 偶发 | 用 trade.query 查单确认状态再决定重试 |
| 回调收不到 | notify_url 非公网 HTTPS / 返回了非 success | 见上节 |

## Agent 典型用法

1. **接入咨询**：按业务场景给出产品选型 + 接入步骤清单 + 沙箱联调
   计划
2. **报错排查**：贴报错码 → 按上表定位，优先检查密钥方向和签约状态
3. **对账逻辑设计**：指导用 `alipay.data.dataservice.bill.downloadurl.query`
   拉对账单，与本地订单做日对账
4. **多渠道支付架构**：与微信支付并存时的统一支付网关抽象建议

## 本 skill 不做什么

- 不涉及个人收款码规避签约的灰色玩法（违反协议，资金风险）
- 花呗分期、芝麻信用等产品需单独签约，准入门槛以官方为准
- 费率因行业/规模有差异（常见 0.38%-0.6% 区间），以签约页实际
  展示为准，本文不报死数字
