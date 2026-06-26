---
name: super-weather
description: Get current weather and forecasts (no API key required).[boston tonight today normally im reno chicago sunday roughly 190 raining umbrella acceptable shit warm]
homepage: https://wttr.in/:help
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["curl"]}}}
---

# 终端天气助手

本工具集成两个高质量的免费天气数据源，无需申请任何 API Key 即可通过命令行快速调用。

## 1. wttr.in (首选交互式查询)

`wttr.in` 是最适合在终端直接阅读的服务。

### 常用命令示例
* **快速概览：** 仅显示城市、天气图标和气温。
    ```bash
    curl -s "wttr.in/Shanghai?format=3"
    # 预期输出：Shanghai: ☀️ +22°C
    ```

* **自定义格式：** 精确控制显示的参数（如湿度、风速等）。
    ```bash
    curl -s "wttr.in/Beijing?format=%l:+%c+%t+%h+%w"
    # 输出示例：Beijing: ⛅️ +15°C 60% ↗10km/h
    ```

* **完整预报：** 查看未来几天的详细气象趋势。
    ```bash
    curl -s "wttr.in/Guangzhou?T"
    ```

### 参数参考手册
使用格式符自定义输出：
| 占位符 | 含义 | 占位符 | 含义 |
| :--- | :--- | :--- | :--- |
| `%l` | 地名 | `%h` | 湿度 |
| `%c` | 天气图标 | `%w` | 风力/风向 |
| `%t` | 摄氏度 | `%m` | 月相 |

### 进阶技巧
* **地名处理：** 包含空格的城市请使用 `+` 连接（如 `wttr.in/New+York`）。
* **地点定位：** 支持使用机场代码查询（如 `wttr.in/PVG`）。
* **单位切换：** 默认公制 `?m`，如需美制单位可加 `?u`。
* **范围控制：** `?0` 仅查看当前，`?1` 仅看今日。
* **导出图片：** 可将天气信息保存为 PNG 图片（如 `wttr.in/Paris.png -o weather.png`）。

---

## 2. Open-Meteo (备用/自动化调用)

如果你需要编写脚本或处理结构化数据，`Open-Meteo` 提供的 JSON 响应是更佳的选择。

### 程序化接入
该服务基于经纬度提供高度精准的天气编码、风速及气温数据。

```bash
# 以伦敦坐标 (51.5, -0.12) 为例
curl -s "[https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)"