# 定位与天气服务 API

## IP 定位

根据 IP 地址获取位置（精度到城市），常用于显示当地城市天气预报、初始化用户城市等非精确定位场景。

**接口**: `GET /ws/location/v1/ip`

**请求参数**:
- `key` (必填): 开发密钥
- `ip` (可选): IP地址，不传则使用请求来源IP
- `output` (可选): 返回格式，`json`/`jsonp`

**请求示例**:
```
GET /ws/location/v1/ip?key=YOUR_KEY&ip=114.242.249.146
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "request_id": "xxx",
  "result": {
    "ip": "114.242.249.146",
    "location": {
      "lat": 39.90469,
      "lng": 116.40717
    },
    "ad_info": {
      "nation": "中国",
      "province": "北京市",
      "city": "北京市",
      "district": "",
      "adcode": 110000,
      "nation_code": 156
    }
  }
}
```

---

## 天气查询

查询指定位置的实况天气、未来天气预报或逐小时预报，支持按行政区划编码或经纬度查询。

**接口**: `GET /ws/weather/v1/`

**请求参数**:
- `key` (必填): 开发密钥
- `adcode` (二选一): 行政区划代码（支持市级和区/县级，如 `110000` 为北京市，`130681` 为涿州市）
- `location` (二选一): 坐标，格式 `纬度,经度`（获取坐标所在区县的天气数据，与 adcode 二选一）
- `type` (可选): 查询天气类型
  - `now` — 实时天气（**默认**）
  - `future` — 未来天气预报（默认当天+3天）
  - `hours` — 未来24小时逐小时预报
- `get_md` (可选): 仅在 `type=future` 时生效，控制预报天数
  - `0`（默认）— 当天+未来3天
  - `1` — 当天+未来6天
- `added_fields` (可选): 附加字段，多个用**逗号** `,` 分隔
  - `alarm` — 预警信息（仅 `type=now` 时有效）
  - `index` — 生活指数（仅 `type=future` 时有效）
  - `air` — 空气质量信息（所有 type 均可用）
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`
- `callback` (可选): JSONP 回调函数名

**请求示例**:

查询北京实况天气（按行政区划编码）:
```
GET /ws/weather/v1/?key=YOUR_KEY&adcode=110000
```

查询海淀区实况天气 + 预警（按经纬度）:
```
GET /ws/weather/v1/?key=YOUR_KEY&location=39.984154,116.307490&type=now&added_fields=alarm
```

查询未来6天预报 + 生活指数:
```
GET /ws/weather/v1/?key=YOUR_KEY&adcode=110000&type=future&get_md=1&added_fields=index
```

查询逐小时预报:
```
GET /ws/weather/v1/?key=YOUR_KEY&adcode=110000&type=hours
```

---

### 实况天气响应（type=now）

```json
{
  "status": 0,
  "message": "Success",
  "result": {
    "realtime": [
      {
        "province": "北京市",
        "city": "北京市",
        "district": "海淀区",
        "adcode": 110108,
        "update_time": "2026-03-18 11:05",
        "infos": {
          "weather": "晴天",
          "temperature": 9,
          "wind_direction": "东北风",
          "wind_power": "3-4级",
          "wind_power_v2": "3级",
          "humidity": 9,
          "air_pressure": 1018
        },
        "alarms": [],
        "air": {
          "aqi": 65,
          "pm10": 45,
          "pm25": 32,
          "no2": 28,
          "o3": 78,
          "so2": 5,
          "co": 0.6
        }
      }
    ]
  }
}
```

> `alarms` 和 `air` 字段仅在请求 `added_fields=alarm` / `added_fields=air` 时返回。

**实况天气字段说明** (`infos`):

| 字段 | 类型 | 说明 |
|------|------|------|
| weather | string | 天气状况（晴天/多云/阴天/小雨等） |
| temperature | number | 当前温度（℃） |
| wind_direction | string | 风向（东北风/南风等） |
| wind_power | string | 风力等级（如 微风/2-3级/3-4级） |
| wind_power_v2 | string | 风力等级精确版（如 3级） |
| humidity | number | 相对湿度（%） |
| air_pressure | number | 气压（hPa） |

**预警信息字段** (`alarms[]`，需 `added_fields=alarm`):

| 字段 | 类型 | 说明 |
|------|------|------|
| type_name | string | 预警类型（大风/暴雨/高温等） |
| level_name | string | 预警级别（蓝色/黄色/橙色/红色） |
| title | string | 预警标题 |
| pub_content | string | 预警发布内容 |

**空气质量字段** (`air`，需 `added_fields=air`):

| 字段 | 类型 | 说明 |
|------|------|------|
| aqi | number | 空气质量指数 |
| pm10 | number | PM10 浓度 |
| pm25 | number | PM2.5 浓度 |
| no2 | number | NO₂ 浓度 |
| o3 | number | O₃ 浓度 |
| so2 | number | SO₂ 浓度 |
| co | number | CO 浓度 |

---

### 未来天气预报响应（type=future）

```json
{
  "status": 0,
  "message": "Success",
  "result": {
    "forecast": [
      {
        "province": "北京市",
        "city": "北京市",
        "district": "海淀区",
        "adcode": 110108,
        "update_time": "2026-03-18 07:00",
        "infos": [
          {
            "date": "2026-03-18",
            "week": "星期三",
            "day": {
              "weather": "晴",
              "temperature": 15,
              "wind_direction": "北风",
              "wind_power": "微风",
              "humidity": 20
            },
            "night": {
              "weather": "晴",
              "temperature": 3,
              "wind_direction": "北风",
              "wind_power": "微风",
              "humidity": 35
            }
          }
        ],
        "indexes": [
          {
            "index_date": "2026-03-18",
            "ids": [
              { "name": "穿衣指数", "level": "较冷", "desc": "建议穿厚外套" },
              { "name": "紫外线指数", "level": "弱", "desc": "辐射较弱" }
            ]
          }
        ],
        "air": [
          {
            "air_date": "2026-03-18",
            "aqi": 65
          }
        ]
      }
    ]
  }
}
```

> `indexes` 仅在 `added_fields=index` 时返回。`air` 数组仅在 `added_fields=air` 时返回。

**预报天气字段说明** (`infos[]`):

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 日期（2026-03-18） |
| week | string | 星期 |
| day | object | 白天天气（含 weather/temperature/wind_direction/wind_power/humidity） |
| night | object | 夜晚天气（字段同 day） |

**生活指数字段** (`indexes[]`，需 `added_fields=index`):

| 字段 | 类型 | 说明 |
|------|------|------|
| index_date | string | 日期 |
| ids | array | 生活指数列表，每项含 name/level/desc |

---

### 逐小时预报响应（type=hours）

```json
{
  "status": 0,
  "message": "Success",
  "result": {
    "forecast_hours": [
      {
        "province": "北京市",
        "city": "北京市",
        "district": "海淀区",
        "adcode": 110108,
        "update_time": "2026-03-18 11:00",
        "infos": [
          {
            "hour": "2026-03-18 12:00:00",
            "info": {
              "weather": "晴",
              "temperature": 12,
              "wind_direction": "北风",
              "wind_power": "微风"
            }
          },
          {
            "hour": "2026-03-18 13:00:00",
            "info": {
              "weather": "晴",
              "temperature": 13,
              "wind_direction": "北风",
              "wind_power": "微风"
            }
          }
        ]
      }
    ]
  }
}
```

**逐小时字段说明** (`infos[]`):

| 字段 | 类型 | 说明 |
|------|------|------|
| hour | string | 时间（2026-03-18 12:00:00） |
| info | object | 该小时天气详情（含 weather/temperature/wind_direction/wind_power） |

---

### 重要注意事项

1. **`type` 参数是单选**，不能用 `|` 合并多个类型（如 `type=now|future` 是错误的），需要多种数据时需发多次请求
2. **`added_fields` 用逗号 `,` 合并**，如 `added_fields=alarm,air`
3. **`alarm` 只在 `type=now` 下生效**，`index` 只在 `type=future` 下生效
4. **响应中 `realtime`/`forecast`/`forecast_hours` 都是数组**，通常只有一个元素（对应查询的区县）
5. **预报天数**：默认 3 天，设置 `get_md=1` 可扩展到 6 天
