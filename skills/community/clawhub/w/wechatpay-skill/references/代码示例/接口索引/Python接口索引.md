# Python代码示例 - 接口索引

> 微信支付V3 API Python实现代码索引

## 下单接口

| 接口 | 文件路径 | 说明 |
|------|----------|------|
| JSAPI下单 | [JSAPI支付.md](./JSAPI支付/JSAPI支付.md) | 公众号内网页支付 |
| 小程序下单 | [小程序支付.md](./小程序支付/小程序支付.md) | 微信小程序内支付 |
| Native下单 | [Native支付.md](./Native支付/Native支付.md) | PC网站二维码扫码 |
| APP下单 | [APP支付.md](./APP支付/APP支付.md) | iOS/Android原生App |

## 支付相关

| 接口 | 文件路径 | 说明 |
|------|----------|------|
| 调起支付签名 | 各支付方式文件内 | 返回给前端的签名参数 |
| 查询订单 | [JSAPI支付.md](./JSAPI支付/JSAPI支付.md) | 商户订单号查单 |
| 关闭订单 | [JSAPI支付.md](./JSAPI支付/JSAPI支付.md) | 超时未支付关单 |

## 退款

| 接口 | 文件路径 | 说明 |
|------|----------|------|
| 申请退款 | [退款.md](./退款/退款.md) | 全额/部分退款 |
| 查询退款 | [退款.md](./退款/退款.md) | 查询退款状态 |

## 回调处理

| 接口 | 文件路径 | 说明 |
|------|----------|------|
| 支付回调处理 | [回调处理.md](./回调处理/回调处理.md) | 验签、解密、业务处理 |
| 退款回调处理 | [回调处理.md](./回调处理/回调处理.md) | 退款状态变更 |

## 通用功能

所有支付方式的退款和回调处理逻辑相同，可复用：
- [退款.md](./退款/退款.md)
- [回调处理.md](./回调处理/回调处理.md)

## 快速开始

```python
from wechatpayv3 import WechatPay

# 配置
pay = WechatPay(
    mchid="1234567890",
    serial_no="XXXXXXXXXXXXXXXXXXXXXXXX",
    private_key="-----BEGIN PRIVATE KEY-----...",
    appid="wxa5f5c1d6e8f9a2b3",
    api_v3_key="0123456789abcdef0123456789abcdef"
)

# JSAPI支付
result = pay.jsapi_prepay(
    out_trade_no="ORDER123456",
    description="商品",
    total_fee=100,
    openid="oUpF8xxxx",
    notify_url="https://example.com/notify"
)
```

## 依赖安装

```bash
pip install requests cryptography flask
```
