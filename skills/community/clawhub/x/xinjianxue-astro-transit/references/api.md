# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/astro-transit`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 鉴权：只认 `Payment-Proof`，不需要账号、密码或登录态
- 服务 ID：`API_30A623BF818C4A71`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| year | int | 是 | 出生年，限 1900~2100（星历表范围） |
| month | int | 是 | 月 |
| day | int | 是 | 日 |
| h | int | 是 | 时，24 小时制 |
| m | int | 是 | 分 |
| birth_place | string | 是 | 出生地 |
| country | string | 否 | 出生国家代码，默认 `CN` |
| current_place | string | 是 | 当前所在地，决定行运起算时刻 |
| current_country | string | 否 | 当前国家代码 |
| transit_at | string | 否 | 指定行运时刻，仅调试用；正常不传，取当前时间 |

```json
{
  "year": 1995,
  "month": 8,
  "day": 4,
  "h": 5,
  "m": 52,
  "birth_place": "浙江杭州",
  "country": "CN",
  "current_place": "上海",
  "current_country": "CN"
}
```

## 返回（200）

```json
{
  "report": {
    "constellations": [
      {
        "constellation_name": "白羊座",
        "house": 9,
        "natal_stars": "本命落在该星座的星体",
        "transit_stars": "行运经过该星座的星体"
      }
    ],
    "natal_aspects": ["本命相位"],
    "transit_natal_aspects": ["行运与本命的相位"]
  },
  "meta": {
    "time_mode": "",
    "birth_clock": "",
    "true_solar": "",
    "chart_time": "",
    "place": "",
    "current": "",
    "transit_time": "行运起算时刻",
    "transit_time_basis": "起算依据，如：当前所在地当地时间"
  }
}
```

`meta` 用于向用户解释起算时刻，不整段展示。

## 错误

- `400` `{"error": "..."}`，常见为日期不合法、出生地或当前所在地无法识别
- `503` 端点配置未就绪
- `402` 需要付款，见 `payment.md`
- `500` 服务异常
