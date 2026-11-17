# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/report`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 服务 ID：`API_114161C46CE74BDE`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| birth | string | 是 | 出生时间 `YYYY-MM-DD HH:MM` |
| place | string | 是 | 出生地 |
| country | string | 否 | 国家代码，默认 `CN` |
| gender | string | 否 | 男 / 女 |
| current | string | 否 | 当前时间，缺省取服务器当前时间 |
| current_place | string | 否 | 当前所在地 |
| current_country | string | 否 | 当前国家代码 |

```json
{
  "birth": "1995-08-04 05:52",
  "place": "浙江杭州",
  "country": "CN",
  "gender": "女"
}
```

## 返回（200）

返回该用户的特征编码报告，形式为若干「编码 → 内容」条目：稳定人格底色、四类场景表现、四类心理模式，以及 L2~L5 动态特征。

维度以实际返回为准。缺某个维度时，直接说明该维度本次未覆盖，不做推测。

## 错误

- `400` 参数不合法，响应含 `error`
- `401` 未登录或凭证无效
- `402` 需要付款，见 `payment.md`
- `500` 服务异常
