# UEXX Data Cloud API Catalog

Base URL: `https://bbs.uexx.com`

The skill should usually call the latest query endpoints and answer directly.

## Automatic Free Key

`POST /api/v1/free-key`

Returns a Free API Key. Limits:

- Same IP can request up to 3 Free Keys per day.
- Free Keys expire after 7 continuous days without use.
- Requests use `X-API-Key`.

## Latest Query Endpoints

- `GET /api/v1/query/fear-greed/latest`
- `GET /api/v1/query/altcoin-season/latest`
- `GET /api/v1/query/symbol/{symbol}/funding-rate/latest`
- `GET /api/v1/query/symbol/{symbol}/oi/latest`
- `GET /api/v1/query/symbol/{symbol}/long-short/latest`

## Natural Language Mapping

| User asks | Intent | Endpoint |
|---|---|---|
| 恐慌指数, 恐慌贪婪, market sentiment | `fear-greed` | `/api/v1/query/fear-greed/latest` |
| 山寨季, altcoin season | `altcoin-season` | `/api/v1/query/altcoin-season/latest` |
| 资金费率, funding | `funding-rate` | `/api/v1/query/symbol/{symbol}/funding-rate/latest` |
| OI, 持仓量, open interest | `oi` | `/api/v1/query/symbol/{symbol}/oi/latest` |
| 多空比, long short ratio | `long-short` | `/api/v1/query/symbol/{symbol}/long-short/latest` |

## Full Catalog

For all current datasets, call:

`GET /api/v1/public/api-guide`

Read `data_catalog`. It includes:

- dataset id
- name
- category
- Free/PRO plan
- history flag
- cadence
- JSON/CSV download paths

Use full download endpoints only when the user asks for history, raw data, CSV, or integration code.
