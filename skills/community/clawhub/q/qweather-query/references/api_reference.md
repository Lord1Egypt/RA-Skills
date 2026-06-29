# 和风天气 API 参考文档

## 概述

本参考文档记录了和风天气开发服务的 API 接口详情。所有 API 请求均使用 HTTPS，数据返回格式为 JSON（Gzip 压缩）。

## 认证方式

在请求 URL 的查询参数中传入 `key={api_key}`：

```
https://{api_host}/v7/weather/now?location=101010100&key={api_key}
```

`api_host` 和 `api_key` 从项目根目录的 `qweather_config.json` 读取。

---

## 通用约定

- **基地址**：`https://{api_host}`
- **数据格式**：JSON，Gzip 压缩
- **请求方式**：GET
- **认证**：查询参数 `key={api_key}`
- **数据单位**：默认公制（摄氏度、公里/小时、百帕、毫米等）
- **时区**：ISO 8601 格式，默认东八区
- **状态码**：`200` 成功，其他值参考和风天气状态码文档

---

## 一、GeoAPI - 城市搜索

查询地理位置信息，获取后续天气查询所需的 LocationID 和经纬度。

**端点**：`/geo/v2/city/lookup`

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `location` | string | 是 | 查询地区名称（中文城市名，最少 1 个汉字） |
| `range` | string | 否 | 搜索范围，固定 `cn`（中国） |
| `number` | int | 否 | 返回结果数量，默认 3，范围 1-20 |
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/geo/v2/city/lookup?location=深圳&range=cn&number=3&key={api_key}
```

**返回 JSON 字段**：

```json
{
  "code": "200",
  "location": [
    {
      "name": "深圳",
      "id": "101280601",
      "lat": "22.54",
      "lon": "114.06",
      "adm2": "深圳",
      "adm1": "广东省",
      "country": "中国",
      "tz": "Asia/Shanghai",
      "utcOffset": "+08:00",
      "isDst": "0",
      "type": "city",
      "rank": "10",
      "fxLink": "https://www.qweather.com/weather/shenzhen-101280601.html"
    }
  ],
  "refer": {
    "sources": ["QWeather"],
    "license": ["QWeather Developers License"]
  }
}
```

**关键字段**：
- `location[0].id`：LocationID，用于后续天气 API 查询
- `location[0].name`：城市/地区名称
- `location[0].lat`：纬度（用于空气质量、预警 API）
- `location[0].lon`：经度（用于空气质量、预警 API）
- `location[0].adm1`：一级行政区域（省/直辖市）
- `location[0].adm2`：二级行政区域（市/区）

---

## 二、实时天气 API

获取指定地区的实时天气数据，延迟约 5-20 分钟。

**端点**：`/v7/weather/now`

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `location` | string | 是 | LocationID（从 GeoAPI 获取）或 `经度,纬度` |
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/v7/weather/now?location=101280601&key={api_key}
```

**返回 JSON 字段 - `now` 对象**：

| 字段 | 说明 |
|------|------|
| `obsTime` | 数据观测时间 |
| `temp` | 温度（摄氏度） |
| `feelsLike` | 体感温度（摄氏度） |
| `icon` | 天气状况图标代码 |
| `text` | 天气状况文字描述（晴、多云、阴、雨、雪等） |
| `wind360` | 风向 360 角度 |
| `windDir` | 风向文字描述（东北风、南风等） |
| `windScale` | 风力等级 |
| `windSpeed` | 风速（公里/小时） |
| `humidity` | 相对湿度（百分比） |
| `precip` | 过去 1 小时降水量（毫米） |
| `pressure` | 大气压强（百帕） |
| `vis` | 能见度（公里） |
| `cloud` | 云量（百分比，可能为空） |
| `dew` | 露点温度（可能为空） |

---

## 三、逐日天气预报 API

获取指定地区未来多天的每日天气预报。

**端点**：`/v7/weather/{days}`

**{days} 可选值**：`3d`（3 天）、`7d`（7 天）、`10d`（10 天）、`15d`（15 天）、`30d`（30 天）

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `location` | string | 是 | LocationID 或 `经度,纬度` |
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/v7/weather/7d?location=101280601&key={api_key}
```

**返回 JSON 字段 - `daily[]` 数组元素**：

| 字段 | 说明 |
|------|------|
| `fxDate` | 预报日期 |
| `tempMax` | 当天最高温度 |
| `tempMin` | 当天最低温度 |
| `textDay` | 白天天气状况文字描述 |
| `textNight` | 夜间天气状况文字描述 |
| `windDirDay` | 白天风向 |
| `windScaleDay` | 白天风力等级 |
| `windSpeedDay` | 白天风速（公里/小时） |
| `windDirNight` | 夜间风向 |
| `windScaleNight` | 夜间风力等级 |
| `windSpeedNight` | 夜间风速（公里/小时） |
| `humidity` | 相对湿度（百分比） |
| `precip` | 当天总降水量（毫米） |
| `pressure` | 大气压强（百帕） |
| `vis` | 能见度（公里） |
| `cloud` | 云量（百分比，可能为空） |
| `uvIndex` | 紫外线强度指数 |
| `sunrise` | 日出时间（高纬度地区可能为空） |
| `sunset` | 日落时间（高纬度地区可能为空） |
| `moonrise` | 月升时间（可能为空） |
| `moonset` | 月落时间（可能为空） |
| `moonPhase` | 月相名称 |

---

## 四、逐小时天气预报 API

获取指定地区未来数小时的逐小时天气预报。

**端点**：`/v7/weather/{hours}`

**{hours} 可选值**：`24h`（24 小时）、`72h`（72 小时）、`168h`（168 小时/7 天）

**参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `location` | string | 是 | LocationID 或 `经度,纬度` |
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/v7/weather/24h?location=101280601&key={api_key}
```

**返回 JSON 字段 - `hourly[]` 数组元素**：

| 字段 | 说明 |
|------|------|
| `fxTime` | 预报时间 |
| `temp` | 温度（摄氏度） |
| `icon` | 天气状况图标代码 |
| `text` | 天气状况文字描述 |
| `wind360` | 风向 360 角度 |
| `windDir` | 风向文字描述 |
| `windScale` | 风力等级 |
| `windSpeed` | 风速（公里/小时） |
| `humidity` | 相对湿度（百分比） |
| `pop` | 降水概率（百分比，可能为空） |
| `precip` | 降水量（毫米） |
| `pressure` | 大气压强（百帕） |
| `cloud` | 云量（百分比，可能为空） |
| `dew` | 露点温度（可能为空） |

---

## 五、实时空气质量 API

获取指定经纬度坐标的实时空气质量数据（1x1 公里精度）。

**端点**：`/airquality/v1/current/{latitude}/{longitude}`

**路径参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `latitude` | decimal | 是 | 纬度（十进制，小数点后最多两位），从 GeoAPI 的 `location[0].lat` 获取 |
| `longitude` | decimal | 是 | 经度（十进制，小数点后最多两位），从 GeoAPI 的 `location[0].lon` 获取 |

**查询参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/airquality/v1/current/22.54/114.06?key={api_key}
```

**返回 JSON 字段**：

`indexes[]` - 空气质量指数，取第一个元素（`indexes[0]`）：

| 字段 | 说明 |
|------|------|
| `code` | AQI 标准代码（`us-epa`、`qaqi` 等） |
| `name` | AQI 标准名称 |
| `aqi` | AQI 数值 |
| `aqiDisplay` | AQI 数值文本 |
| `level` | 等级（数值，可能为空） |
| `category` | 类别描述（优、良、轻度污染等，可能为空） |
| `primaryPollutant.code` | 首要污染物代码（可能为空） |
| `primaryPollutant.name` | 首要污染物名称（可能为空） |
| `primaryPollutant.fullName` | 首要污染物全称（可能为空） |
| `health.effect` | 健康影响描述（可能为空） |
| `health.advice.generalPopulation` | 一般人群健康建议（可能为空） |
| `health.advice.sensitivePopulation` | 敏感人群健康建议（可能为空） |

`pollutants[]` - 污染物数据：

| 字段 | 说明 |
|------|------|
| `code` | 污染物代码（`pm2p5`、`pm10`、`no2`、`o3`、`co`、`so2`） |
| `name` | 污染物名称 |
| `fullName` | 污染物全称 |
| `concentration.value` | 浓度值 |
| `concentration.unit` | 浓度单位（`μg/m3`、`ppb`、`ppm`） |

---

## 六、天气预警 API

获取指定经纬度坐标当前生效的官方天气预警信息。

**端点**：`/weatheralert/v1/current/{latitude}/{longitude}`

**路径参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `latitude` | decimal | 是 | 纬度（十进制，小数点后最多两位） |
| `longitude` | decimal | 是 | 经度（十进制，小数点后最多两位） |

**查询参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `localTime` | boolean | 否 | `true` 返回本地时间，默认 `false` 返回 UTC（建议设为 `true`） |
| `key` | string | 是 | 认证 API Key |

**示例**：
```
GET https://{api_host}/weatheralert/v1/current/22.54/114.06?localTime=true&key={api_key}
```

**返回 JSON 字段**：

`metadata`：

| 字段 | 说明 |
|------|------|
| `zeroResult` | `true` 表示无预警信息 |

`alerts[]` - 预警信息数组：

| 字段 | 说明 |
|------|------|
| `id` | 预警唯一标识 |
| `senderName` | 发布机构名称（可能为空） |
| `issuedTime` | 发布时间 |
| `eventType.name` | 预警事件类型名称（大风、暴雨等） |
| `eventType.code` | 预警事件类型代码 |
| `severity` | 严重程度 |
| `color.code` | 预警颜色代码（`blue`、`yellow`、`orange`、`red`） |
| `effectiveTime` | 生效时间（可能为空） |
| `onsetTime` | 事件预计开始时间（可能为空） |
| `expireTime` | 失效时间 |
| `headline` | 预警简要标题 |
| `description` | 预警详细描述 |
| `instruction` | 防御指南 |
| `messageType.code` | 预警状态（`new`=新增、`update`=更新、`cancel`=取消） |
