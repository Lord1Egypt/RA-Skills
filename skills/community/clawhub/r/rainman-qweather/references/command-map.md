# Command Map

| Command | Endpoint | Required Flags | Optional Flags |
| --- | --- | --- | --- |
| `lookup` | `GET /geo/v2/city/lookup` | `--location` | `--adm`, `--range` |
| `now` | `GET /v7/weather/now` | `--location` | `--lang`, `--unit` |
| `forecast` | `GET /v7/weather/{days}d` | `--location` | `--days`, `--lang`, `--unit` |
| `indices` | `GET /v7/indices/1d` | `--location` | `--type` |

## Flag Details

| Flag | Format | Default | Example |
| --- | --- | --- | --- |
| `--location` | City name, LocationID, or `lon,lat` | - | `北京`, `101010100`, `116.41,39.92` |
| `--adm` | Administrative division filter | - | `北京`, `广东` |
| `--range` | ISO 3166 country code | - | `cn`, `us` |
| `--days` | Forecast days: `3`, `7` | `3` | `7` |
| `--lang` | Language code | `zh` | `en`, `zh` |
| `--unit` | `m` (metric) or `i` (imperial) | `m` | `i` |
| `--type` | Life index type IDs, comma-separated | `0` (all) | `3,5` |

## Life Index Types (China)

| ID | Name |
| --- | --- |
| 0 | 全部 |
| 1 | 运动指数 |
| 2 | 洗车指数 |
| 3 | 穿衣指数 |
| 4 | 钓鱼指数 |
| 5 | 紫外线指数 |
| 6 | 旅游指数 |
| 7 | 过敏指数 |
| 8 | 舒适度指数 |
| 9 | 感冒指数 |
| 10 | 空气污染扩散条件指数 |
| 11 | 空调开启指数 |
| 12 | 太阳镜指数 |
| 13 | 化妆指数 |
| 14 | 晾晒指数 |
| 15 | 交通指数 |
| 16 | 防晒指数 |

## Exit Codes
- `0`: success
- `2`: input or config error
- `3`: network / timeout / HTTP transport error
- `4`: API business error (code != "200")
- `5`: unexpected internal error

## Configuration
- `QWEATHER_API_KEY`: API key from console
- `QWEATHER_API_HOST`: Per-developer host (e.g. `xxxxx.re.qweatherapi.com`)
- Auth: key passed as query parameter `key=`
