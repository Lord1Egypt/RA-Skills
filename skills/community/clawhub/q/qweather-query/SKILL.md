---
name: qweather
description: 使用和风天气API查询国内城市的实时天气、逐小时天气、每日天气及空气质量、预警等信息。Use when the user asks about current weather, forecasts, temperature, precipitation, wind, or air quality for a location in China。
agent_created: true
---

# 和风天气查询

使用和风天气 API 查询中国城市天气信息。支持实时天气、逐小时预报、每日预报、空气质量及天气预警。

## 前置配置检查

开始任何天气查询之前，先读取 skill 目录下的 `qweather_config.json` 文件（与 SKILL.md 同目录）：

```json
{
  "api_host": "",
  "api_key": ""
}
```

若文件不存在，或 `api_host` 为空，或 `api_key` 为空，立即退出，向用户输出：

```
未配置和风天气 API，请在 skill 目录下的 qweather_config.json 中填写以下信息：

- api_host：API 请求地址。登录 https://console.qweather.com ，在「设置」→「API Host」获取。
- api_key：API 密钥。登录 https://console.qweather.com ，在「凭据管理」获取。

格式示例：
{
  "api_host": "your-api-host",
  "api_key": "your-api-key"
}
```

配置有效后，所有 API 请求的基地址为 `https://{api_host}`，认证方式为在 URL 查询参数中附加 `key={api_key}`。

## 核心查询流程

**必须严格遵循以下顺序，不可跳过步骤：**

### 第一步：GeoAPI 获取城市 LocationID

使用城市名称（中文）调用 GeoAPI 获取精确位置信息。**禁止直接使用城市名称调用天气 API。**

```
GET https://{api_host}/geo/v2/city/lookup?location={城市名}&range=cn&number=3&key={api_key}
```

从返回的 JSON 中提取：
- `location[0].id` → LocationID（用于实时天气、逐日、逐小时 API）
- `location[0].name` → 城市名称（用于输出）
- `location[0].lat` → 纬度（用于空气质量、预警 API）
- `location[0].lon` → 经度（用于空气质量、预警 API）

若返回 `location` 数组为空或 `code` 不为 `200`，告知用户未找到该城市，终止查询。

### 第二步：根据用户关注的信息类型调用对应 API

分析用户意图，选择对应的 API。必要时可同时调用多个 API 获取完整信息。

| 用户关注 | API 端点 | 参数来源 |
|----------|----------|----------|
| 实时天气 | `/v7/weather/now?location={LocationID}` | GeoAPI 的 `id` |
| 逐小时预报 | `/v7/weather/24h?location={LocationID}` | GeoAPI 的 `id` |
| 每日预报 | `/v7/weather/7d?location={LocationID}` | GeoAPI 的 `id` |
| 空气质量 | `/airquality/v1/current/{lat}/{lon}` | GeoAPI 的 `lat`/`lon` |
| 天气预警 | `/weatheralert/v1/current/{lat}/{lon}?localTime=true` | GeoAPI 的 `lat`/`lon` |

详细的 API 请求格式、参数和返回字段说明见 `references/api_reference.md`。

### 第三步：格式化输出

严格按以下格式输出，字段缺失时直接省略对应行，不要臆造数据。

## 输出格式

### 实时天气

```markdown
**地点**：{name}
**时间**：{obsTime 格式化，如 2026年6月10日}
**天气**：{text}
**温度**：{temp}°C
**体感温度**：{feelsLike}°C
- 降水概率：{pop}%（若从逐小时 API 获取了降水概率，否则省略此行）
- 风速：{windDir} {windScale} 级
- 相对湿度：{humidity}%
- 空气质量：{category}（若同时查询了空气质量，否则省略此行）

**来源：和风天气**
```

### 逐日预报

按日期分组，每组之间空一行：

```markdown
**地点**：{name}

**{fxDate}**：{textDay}，{tempMin}°C ~ {tempMax}°C，{windDirDay} {windScaleDay} 级

**{fxDate}**：{textDay}，{tempMin}°C ~ {tempMax}°C，{windDirDay} {windScaleDay} 级

**来源：和风天气**
```

### 逐小时预报

按时间分组，每组之间空一行：

```markdown
**地点**：{name}

**{fxTime 小时部分} 时**：{text}，{temp}°C，{windDir} {windScale} 级，降水概率 {pop}%

**{fxTime 小时部分} 时**：{text}，{temp}°C，{windDir} {windScale} 级，降水概率 {pop}%

**来源：和风天气**
```

### 空气质量

```markdown
**地点**：{name}
**AQI**：{aqi}，{category}
- PM2.5：{pm2p5 浓度} μg/m³
- PM10：{pm10 浓度} μg/m³
- 首要污染物：{primaryPollutant}（若为空则省略）

**来源：和风天气**
```

### 天气预警

```markdown
**地点**：{name}

**{headline}**
- 类型：{eventType.name}
- 状态：{messageType 状态描述}
- 生效时间：{effectiveTime} ~ {expireTime}
- 内容：{description}

**来源：和风天气**
```

若无预警（`metadata.zeroResult` 为 `true`），输出：

```markdown
**地点**：{name}
当前无生效中的天气预警。

**来源：和风天气**
```

## 通用规则

1. **多地点或多时段分组**：按地点或时间分组展示，组与组之间空一行。
2. **API 失败处理**：若某个 API 调用失败（`code` 不为 `200`）或返回空数据，直接省略该部分，不臆造数据。
3. **字段缺失处理**：若某些字段为空或不存在，直接从输出中省略对应行，保持输出简洁。
4. **禁止替代查询**：绝不要通过 WebSearch 或其他方式自行补做天气查询。所有天气数据必须来自和风天气 API。
5. **来源标注**：每次输出末尾必须保留 `**来源：和风天气**`。
6. **时间格式化**：将 ISO 8601 格式时间转换为用户友好的中文格式（如 `2026年6月10日 14:30`）。
7. **curl 调用加 `--compressed`**：和风天气返回 Gzip 压缩数据，curl 必须使用 `--compressed` 选项。
8. **查询范围**：`range=cn` 仅查询中国境内的城市。若用户查询海外城市，告知当前仅支持中国城市查询。
