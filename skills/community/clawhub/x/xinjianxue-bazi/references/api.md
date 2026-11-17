# 接口契约

- 地址：`https://api.xinjianxue.com/api/xinjianxue/aipay/bazi`
- 方法：POST，`Content-Type: application/json`
- 单价：6 元/次
- 鉴权：只认 `Payment-Proof`，不需要账号、密码或登录态
- 服务 ID：`API_D4CE7E4CCCFF4177`

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| year | int | 是 | 出生年，限 1950~2030（节气表范围） |
| month | int | 是 | 月 |
| day | int | 是 | 日 |
| h | int | 是 | 时，24 小时制 |
| m | int | 是 | 分 |
| gender | string | 是 | 男 / 女 |
| birth_place | string | 是 | 出生地，建议「省+市」 |
| country | string | 否 | 国家代码，默认 `CN` |

```json
{
  "year": 1995,
  "month": 8,
  "day": 4,
  "h": 5,
  "m": 52,
  "gender": "男",
  "birth_place": "浙江杭州",
  "country": "CN"
}
```

## 返回（200）

```json
{
  "success": true,
  "data": {
    "bazi": "四柱字符串",
    "bazi_parts": { "year": "", "month": "", "day": "", "time": "" },
    "wuxing_ymj": "五行统计",
    "wuxing_text": "五行说明",
    "qiyun": "起运描述",
    "qiyun_date": "起运日期",
    "shunni": "顺排 / 逆排",
    "birth_clock": "出生钟表时间",
    "birth_true_solar": "真太阳时",
    "dayun": [
      {
        "index": 1,
        "name": "大运名",
        "ganzhi": "干支",
        "start": "起始年份",
        "end": "结束年份",
        "wuxing": "五行",
        "wuxing_delta": { "水": 0.0, "木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0 },
        "years": [
          { "year": 2026, "gz": "流年干支", "start": "", "end": "", "wuxing": "", "wuxing_delta": {} }
        ]
      }
    ],
    "pre_qiyun_years": []
  }
}
```

字段以实际返回为准；示例中省略的字段不要凭空补。

## 错误

- `400` `{"success": false, "error": "..."}`
- `503` 端点配置未就绪
- `402` 需要付款，见 `payment.md`
- `500` 服务异常
