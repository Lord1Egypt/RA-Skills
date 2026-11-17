# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/astro-natal`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 鉴权：只认 `Payment-Proof`，不需要账号、密码或登录态
- 服务 ID：`API_03827B1FF76346B4`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| year | int | 是 | 出生年，限 1900~2100（星历表范围） |
| month | int | 是 | 月 |
| day | int | 是 | 日 |
| h | int | 是 | 时，24 小时制 |
| m | int | 是 | 分 |
| birth_place | string | 是 | 出生地，建议「省+市」 |
| country | string | 否 | 国家代码，默认 `CN` |

```json
{
  "year": 1995,
  "month": 8,
  "day": 4,
  "h": 5,
  "m": 52,
  "birth_place": "浙江杭州",
  "country": "CN"
}
```

## 返回（200）

```json
{
  "report": {
    "sun": "太阳落座",
    "moon": "月亮落座",
    "mercury": "水星落座",
    "venus": "金星落座",
    "mars": "火星落座",
    "jupiter": "木星落座",
    "saturn": "土星落座",
    "uranus": "天王星落座",
    "neptune": "海王星落座",
    "pluto": "冥王星落座",
    "asc": "上升",
    "desc": "下降",
    "aspects": ["主要相位"],
    "fu": "福点",
    "bei": "北交点"
  },
  "meta": {}
}
```

字段以实际返回为准。`meta` 为计算元信息，不向用户展示。

## 错误

- `400` `{"error": "..."}`，常见为日期不合法、地点无法识别
- `503` 端点配置未就绪
- `402` 需要付款，见 `payment.md`
- `500` 服务异常
