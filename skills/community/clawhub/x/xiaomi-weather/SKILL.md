---
name: xiaomi-weather
description: "中国天气查询（小米天气 App 同款数据源）。支持城市名/城市代码，实时天气、多日预报、空气质量、降水概率、日出日落。数据与小米天气 App 完全一致，比 wttr.in 更适合国内使用。"
homepage: https://github.com/huanghui0906/API/blob/master/XiaomiWeather.md
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "install":
          [
            {
              "id": "curl",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl",
            },
            {
              "id": "python3",
              "kind": "apt",
              "formula": "python3",
              "bins": ["python3"],
              "label": "Install python3",
            },
          ],
      },
  }
---

# xiaomi-weather.sh 小米天气查询

查询中国城市天气，数据源为**小米天气 App 同款接口**（weatherapi.market.xiaomi.com），
国内数据准确、响应快。支持实时天气、逐日预报、空气质量、降水概率、日出日落。

## 用法

```bash
xiaomi-weather.sh 武汉              # 武汉 5天预报（默认）
xiaomi-weather.sh 武汉 3            # 武汉 3天预报
xiaomi-weather.sh 101200101         # 直接传城市代码
xiaomi-weather.sh --json 武汉       # 输出原始 JSON（适合脚本处理）
xiaomi-weather.sh --help            # 帮助
```

## 支持的城市

- 内置 45+ 常用城市代码（北上广深、各省会、主要地级市），见 `references/cities.tsv`
- 其他城市自动从远程城市库匹配（需联网）
- 也可以直接用 9 位城市代码（如北京 `101010100`、武汉 `101200101`）

## 输出说明

- 📍 城市 + 实时天气（天气现象 / 温度 / 体感 / 湿度 / 风力）
- 📅 逐日预报：天气（白天→夜间）、温度区间、AQI 空气质量、降水概率
- 🌅 今天的日出日落时间
- 天气代码：0=晴 1=多云 2=阴 3=雾 7=雷阵雨 8=阵雨 9=大雨 10=中雨 11=小雨 14=阵雪

## 实现细节

- 接口：`https://weatherapi.market.xiaomi.com/wtr-v3/weather/all`
- 参数：`locationKey=weathercn:{城市代码}`、`appKey=weather20151024`、`sign=zUFJoAR2ZVrDy1vF3D07`、`isGlobal=false`、`locale=zh_cn`、`days=1~15`
- 依赖：`curl` + `python3`（格式化输出）
- 网络异常时自动报错，不静默失败
