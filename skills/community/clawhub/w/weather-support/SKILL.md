---
name: weather-support
description: 国内天气查询技能 - 基于uapis.cn免费API。支持全国3000+城市，无需注册和API密钥。
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---

# 国内天气查询

当用户询问天气时，使用uapis.cn免费API查询实时天气信息。该API支持全国3000+城市，无需注册和API密钥。

## API 调用示例

### 基本查询（通过城市名）
```bash
# 查询北京天气
curl 'https://uapis.cn/api/v1/misc/weather?city=北京'

# 查询上海天气
curl 'https://uapis.cn/api/v1/misc/weather?city=上海'

# 查询区县级别（如深圳福田区）
curl 'https://uapis.cn/api/v1/misc/weather?city=福田区'
```

### 响应格式
```json
{
  "province": "陕西省",
  "city": "渭南市",
  "adcode": "610500",
  "weather": "晴",
  "weather_icon": "100",
  "temperature": 9.9,
  "wind_direction": "微风",
  "wind_power": "",
  "humidity": 83,
  "report_time": "2026-03-10 23:27:02"
}
```

## 字段说明
- `province` - 省份
- `city` - 城市名称
- `adcode` - 行政区划代码
- `weather` - 天气状况（晴、阴、雨、雪等）
- `weather_icon` - 天气图标代码
- `temperature` - 实时温度（°C）
- `wind_direction` - 风向
- `wind_power` - 风力等级
- `humidity` - 相对湿度（%）
- `report_time` - 报告时间
