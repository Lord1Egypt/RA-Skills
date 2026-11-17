# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/meihua`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 鉴权：只认 `Payment-Proof`，不需要账号、密码或登录态
- 服务 ID：`API_DA2844084C6840DB`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| n1 | int | 是 | 第一个数，1 ~ 999999999 |
| n2 | int | 是 | 第二个数，1 ~ 999999999 |
| question | string | 否 | 所问之事 |
| current_place | string | 否 | 当前所在地，不必主动索取 |
| current_country | string | 否 | 当前国家代码 |

```json
{
  "n1": 8,
  "n2": 23,
  "question": "这次合作能不能成"
}
```

不传 `current_place` / `current_country` 时，服务端按北京时间起卦。

## 返回（200）

```json
{
  "success": true,
  "data": {
    "question": "这次合作能不能成",
    "numbers": [8, 23],
    "time": "起卦时间",
    "upper": { "number": 0, "name": "", "symbol": "", "element": "" },
    "lower": { "number": 0, "name": "", "symbol": "", "element": "" },
    "dong_yao": 0,
    "ben": { "name": "", "yao": "" },
    "hu": { "name": "" },
    "bian": { "name": "", "yao": "" },
    "cuo": { "name": "" },
    "zong": { "name": "" },
    "ti": { "name": "", "element": "" },
    "yong": { "name": "", "element": "" },
    "ti_yong": "体用关系",
    "bian_ti_yong": "变卦体用关系"
  },
  "text": "卦辞与爻辞说明"
}
```

## 错误

- `400` `{"success": false, "error": "..."}`
- `503` 端点配置未就绪
- `402` 需要付款，见 `payment.md`
- `500` 服务异常
