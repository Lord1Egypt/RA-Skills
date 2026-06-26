# API 说明

## 来源

- API key 来源说明：`https://github.com/Entropy-Increase-Team/`

## 接口

- `GET https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true`
- Header: `X-API-Key: <key>`

## 运行要求

- Python 3
- Python 包：`requests`
- 环境变量：`ROCOM_API_KEY`（或使用 `--api-key` 参数）

## 本 skill 使用的字段

- `data.merchantActivities[]`
- `name`
- `start_date`
- `get_props[]`
- `get_pets[]`
- `icon_url`
- `start_time`
- `end_time`

## 过滤规则

仅保留满足以下条件的商品：

- `start_time <= now < end_time`

## 轮次说明

按北京时间 4 个时段显示当前轮次：

- 08:00-12:00
- 12:00-16:00
- 16:00-20:00
- 20:00-24:00
