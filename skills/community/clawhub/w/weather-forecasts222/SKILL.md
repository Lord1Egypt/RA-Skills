---
name: weather-forecast
description: "查询天气预报，支持城市名/坐标，提供当前天气和预报信息，包含图标展示。"
metadata:
  {
    "openclaw": {
      "emoji": "☀️",
      "requires": { "bins": ["curl", "python3"] },
      "user-invocable": true
    }
  }
---

# Weather Forecast ☀️

查询天气预报，支持城市名、拼音、IP自动定位。

## 使用方式

用户说"查天气"、"今天天气怎么样"、"北京天气"时触发。

## 脚本

```
python3 skills/weather-forecast/scripts/weather.py <城市名或拼音>
```

## 输出格式

- 当前温度、体感温度、湿度、风速
- 天气状况 + 对应图标
- 未来3天简单预报

## 图标映射

天气图标存储在 `assets/icons/` 目录，文件名格式：`{condition}.svg`

支持图标：sunny、cloudy、rainy、snowy、stormy、foggy、windy、partly_cloudy

## 依赖

- Python 3
- curl（调用 wttr.in API）
- 无需 API Key

## 参考

详见 `references/` 目录