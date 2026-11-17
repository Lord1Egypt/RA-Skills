# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/tarot`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 鉴权：只认 `Payment-Proof`，不需要账号、密码或登录态
- 服务 ID：`API_06CD669CDD174221`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| spread | string | 是 | 所选牌阵编号，如 `3.b`，用于订单记录与对账 |
| draws | int[] | 是 | 本次抽牌顺序，1~78 的整数，不能重复，1~12 张 |

```json
{
  "spread": "3.b",
  "draws": [12, 45, 7]
}
```

用户所问之事留在对话里，由 AI 自己掌握；后端只收牌阵、收号码，出牌，不解牌。

## 返回（200）

外层与其它收款端点一致，业务结果在 `content` 字符串里，解析后为：

```json
{
  "status": "success",
  "service_slug": "tarot",
  "resource_id": "/api/xinjianxue/aipay/tarot",
  "out_trade_no": "订单号",
  "goods_name": "心鉴学 · 塔罗专业版（50种牌阵）",
  "generated_at": "生成时间",
  "result": {
    "spread": "3.b",
    "deck_size": 78,
    "cards": [
      {
        "slot": 1,
        "number": 12,
        "name": "圣杯八",
        "orientation": "逆位",
        "arcana": "小阿尔卡纳",
        "suit": "圣杯",
        "element": "水",
        "rank": "八",
        "meaning": "该牌在此正逆位下的牌义",
        "keywords": ["关键词"],
        "nature": "牌性",
        "advice": "建议"
      }
    ]
  }
}
```

`cards` 已按 `draws` 的顺序排列，`slot` 从 1 开始，直接对应牌阵位次。

## 错误

- `400` `{"code":"INVALID_REQUEST","message":"..."}`：缺 spread / draws，或号码越界、重复
- `402` 需要付款，见 `payment.md`
- `502` 资源生成失败，可用同一 `Payment-Proof` 重试
- `503` 端点配置未就绪
