---
name: qweather
description: 和风天气 QWeather API 调用。当用户查询天气、获取天气预报（今日/7天/24小时）、空气质量、天气指数等与天气相关请求时使用此技能。支持城市代码/城市名/经纬度定位。注意：仅在用户明确要求使用和风天气或需要免费API天气数据时使用，否则默认用 agent-browser + weather.com.cn。
---

# 和风天气 QWeather API

## 快速使用

```bash
# 实时天气（默认杭州）
python3 ~/.openclaw/workspace/skills/qweather/scripts/qweather.py now

# 7天预报
python3 ~/.openclaw/workspace/skills/qweather/scripts/qweather.py 7d

# 24小时逐时
python3 ~/.openclaw/workspace/skills/qweather/scripts/qweather.py 24h

# 指定城市（城市代码）
python3 ~/.openclaw/workspace/skills/qweather/scripts/qweather.py now 101210101
```

## 支持接口

| 接口 | 说明 | 示例 |
|------|------|------|
| `now` | 实时天气 | 温度/风力/湿度/降水等 |
| `7d` | 7天预报 | 每日高低温/天气/风力 |
| `24h` | 24小时逐时 | 每小时温度/天气 |
| `air` | 空气质量 | AQI/PM2.5/PM10等 |
| `indices` | 生活指数 | 穿衣/紫外线/运动等 |

## 常用城市代码

| 城市 | 代码 |
|------|------|
| 杭州 | 101210101 |
| 上海 | 101020100 |
| 北京 | 101010100 |
| 深圳 | 101280601 |
| 广州 | 101280101 |
| 成都 | 101270101 |
| 南京 | 101190101 |
| 苏州 | 101190401 |
| 宁波 | 101210401 |
| 厦门 | 101230201 |

其他城市代码查询：https://dev.qweather.com/docs/api/geo/

## API 配置

- **Host**: `na6heya3mr.re.qweatherapi.com`
- **Key**: `2e5290bfa33242d2bf74ab196aae6e19`
- **协议**: HTTPS + Gzip压缩

## 注意事项

- 免费版每日 1000 次调用额度，非商业使用
- 返回数据需注明来源：QWeather（和风天气）
- Key 有域名/IP安全限制，如更换服务器需更新白名单
- 实时天气更新延迟约 5-10 分钟
