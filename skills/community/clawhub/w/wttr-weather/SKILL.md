---
name: wttr-weather
description: How to check weather forecasts using wttr.in service. Make sure to use this skill whenever the user mentions weather, forecast, temperature, or wants to check weather conditions for any location. Supports 54+ languages, multiple output formats (terminal, JSON, PNG), moon phases, and custom locations worldwide.
---

# wttr.in 天气查询服务

> **💡 快捷工具**：本 skill 包含辅助脚本和参考文档
> - **Python 脚本**: `scripts/weather.py` - 多功能天气查询工具（统一使用）
> - **参考指南**: `references/quick-reference.md` - 速查手册


## 核心功能

wttr.in 是一个功能强大的基于控制台天气预报服务，支持多种输出格式和全球位置查询。

### 主要能力

1. **天气预报查询** - 支持全球任意地点的天气预报
2. **多格式输出** - ANSI 终端、HTML、PNG 图片、JSON、Prometheus 指标
3. **多语言支持** - 54+ 种语言，包括中文
4. **天文信息** - 月相、日出日落时间
5. **自定义格式** - 灵活配置输出内容
6. **一行输出** - 适合集成到 tmux、状态栏等

---

## 基本用法

### 标准查询（使用 Python 脚本）

```bash
# 当前位置（基于 IP）
python scripts/weather.py

# 指定城市
python scripts/weather.py Beijing
python scripts/weather.py Shanghai
python scripts/weather.py "New+York"
python scripts/weather.py London

# 使用 ~ 查询特殊地点（景点、山脉等）
python scripts/weather.py "~Eiffel+Tower"
python scripts/weather.py "~Mount+Everest"

# 机场代码查询
python scripts/weather.py PEX    # 北京首都机场
python scripts/weather.py PVG    # 上海浦东机场
python scripts/weather.py LAX    # 洛杉矶机场
```

### 单位设置

```bash
# 公制单位（摄氏度，默认除美国外）
python scripts/weather.py Beijing -u m

# 英制单位（华氏度）
python scripts/weather.py Beijing -u u

# 公制 + m/s 风速
python scripts/weather.py Beijing -u M
```

---

## 输出格式

### 1. 终端 ANSI/纯文本

```bash
# 标准输出（自动检测）
python scripts/weather.py Beijing

# 强制纯文本（无颜色）
python scripts/weather.py Beijing -f plain

# 限制为标准控制台字符
python scripts/weather.py Beijing -f compact
```

### 2. PNG 图片格式

```bash
# 下载 PNG 天气图
python scripts/weather.py Beijing -f png -o weather.png

# 透明背景
python scripts/weather.py Beijing -f png --transparent -o weather.png

# 自定义透明度 (0-255)
python scripts/weather.py Beijing -f png --transparent --transparency 150
```

### 3. JSON 格式（API 使用）

```bash
# 完整 JSON 数据
python scripts/weather.py Beijing -f json

# 精简 JSON（不含小时数据）
python scripts/weather.py Beijing -f json-lite
```

JSON 输出包含：
- `current_condition`: 当前天气状况
- `weather`: 天气预报数据
- `astronomy`: 天文信息（日出、日落、月相）

### 4. Prometheus 监控指标

```bash
# Prometheus 格式
python scripts/weather.py Beijing -f prometheus
```

---

## 一行输出格式（format 参数）

适合集成到 tmux、weechat、状态栏等。

### 预设格式

```bash
# 格式 1: 当前天气
python scripts/weather.py Beijing -f oneline --custom-format "1"
# 🌦 +11⁰C

# 格式 2: 详细信息
python scripts/weather.py Beijing -f oneline --custom-format "2"
# 🌦   🌡️+11°C 🌬️↓4km/h

# 格式 3: 位置 + 天气
python scripts/weather.py Beijing -f oneline --custom-format "3"
# Beijing: 🌦 +11⁰C

# 格式 4: 完整信息
python scripts/weather.py Beijing -f oneline --custom-format "4"
# Beijing: 🌦   🌡️+11°C 🌬️↓4km/h
```

### 自定义格式（%-notation）

| 代码 | 含义 | 代码 | 含义 |
|------|------|------|------|
| `%c` | 天气状况图标 | `%C` | 天气状况文本 |
| `%x` | 天气符号（纯文本） | `%h` | 湿度 |
| `%t` | 实际温度 | `%f` | 体感温度 |
| `%w` | 风速和方向 | `%l` | 位置名称 |
| `%m` | 月相 🌑🌒🌓🌔🌕🌖🌗🌘 | `%M` | 月龄 |
| `%p` | 降水量 (mm/3h) | `%P` | 气压 (hPa) |
| `%u` | UV 指数 (1-12) | `%D` | 黎明时间* |
| `%S` | 日出时间* | `%z` | 天顶时间* |
| `%s` | 日落时间* | `%d` | 黄昏时间* |
| `%T` | 当前时间* | `%Z` | 本地时区 |

*时间以本地时区显示

```bash
# 自定义输出示例
python scripts/weather.py Beijing --custom-format "%l:+%c+%t+%h+%w\n"
# Beijing: ⛅️ +7°C 45% ↓12km/h

# 多地点查询
python scripts/weather.py "Beijing:Shanghai:Guangzhou" -f oneline --custom-format "3"
```

---

## 数据丰富格式 (v2)

实验性功能，提供详细天气和天文信息。

```bash
# 使用 v2 格式
python scripts/weather.py Beijing -f v2

# 使用 Nerd Fonts（日间模式）
python scripts/weather.py Beijing -f v2-day

# 使用 Nerd Fonts（夜间模式）
python scripts/weather.py Beijing -f v2-night
```

包含信息：
- 温度和降水变化预测
- 月相（今天及未来 3 天）
- 当前天气状况、温度、湿度、风速、气压
- 时区信息
- 黎明、日出、正午、日落、黄昏时间
- 精确地理坐标

---

## 地图视图 (v3)

显示地理区域的天气信息。

```bash
# PNG 格式（浏览器）
python scripts/weather.py California -f v3

# Sixel 格式（支持内联图像的终端）
python scripts/weather.py Bayern -f v3
```

---

## 月相查询

```bash
# 当前位置月相
python scripts/weather.py -f moon

# 指定日期
python scripts/weather.py -f moon --moon-date 2025-12-25

# 作为天气查询的一部分
python scripts/weather.py Beijing --custom-format "%m"
# 🌖
```

---

## 多语言支持

```bash
# 通过语言参数设置
python scripts/weather.py Beijing -l zh
python scripts/weather.py Paris -l fr
python scripts/weather.py Berlin -l de
python scripts/weather.py Tokyo -l ja

# 查询非英文名称位置
python scripts/weather.py "станция+Восток"
python scripts/weather.py "~长城"
```

支持 54+ 种语言，包括：zh（中文）、en（英语）、fr（法语）、de（德语）、ru（俄语）、ja（日语）等。

---

## 集成示例

### tmux 状态栏

```tmux
# ~/.tmux.conf
set -g status-interval 60
# 使用 Python 脚本查询天气
WEATHER='#(python /path/to/weather.py Beijing -f oneline --custom-format "%%l:+%%c+%%t&period=60")'
set -g status-right "$WEATHER | %Y-%m-%d %H:%M"
```

### Shell 别名

```bash
# ~/.bashrc 或 ~/.zshrc
alias weather='python /path/to/weather.py'
alias weather-json='python /path/to/weather.py -f json'
```

### Python 程序集成

```python
from weather import WeatherQuery

weather = WeatherQuery("Beijing")

# 获取 JSON 数据
data = weather.json_full()
print(f"当前温度：{data['current_condition'][0]['temp_C']}°C")

# 获取一行输出
print(weather.oneline("3"))
```

---

## 使用建议

### 最佳实践

1. **自动查询场景**（如 tmux）设置合理更新间隔（60-300 秒）
2. **多地点查询** 使用 `:` 分隔，配合 `period` 参数
3. **脚本集成** 使用 JSON 格式 (`format=j1`) 便于解析
4. **终端显示** 确保字体支持 emoji（推荐 Noto Color Emoji）

### 常见问题

**Emoji 显示问题**：
- 安装 Noto Color Emoji 字体
- 配置 fontconfig 优先使用 emoji 字体
- 运行 `fc-cache -f -v` 刷新字体缓存

**终端不支持**：
- 使用 `?T` 参数强制纯文本
- 使用 `?d` 限制为标准字符

---

## API 参考

### 端点

| 端点 | 用途 |
|------|------|
| `wttr.in` | 标准天气预报 |
| `v2.wttr.in` | 数据丰富格式 |
| `v3.wttr.in` | 地图视图 |

### 查询参数

| 参数 | 说明 |
|------|------|
| `?m` | 公制单位 |
| `?u` | 英制单位 |
| `?M` | 公制 + m/s |
| `?T` | 纯文本 |
| `?d` | 限制字符 |
| `?format=X` | 输出格式 |
| `?lang=XX` | 语言代码 |
| `period=N` | 更新周期（秒） |

### 天气代码

| 代码 | 描述 |
|------|------|
| 113 | 晴朗/少云 |
| 116 | 局部多云 |
| 119 | 多云 |
| 122 | 阴天 |
| 176/263/266/293/296/299/302/305/308/353/356/359/386/389 | 各种降雨/雷暴 |
| 179/311/314/317/320/323/326/329/332/335/338/350/377 | 各种降雪/冰雹 |
| 143/182/248/260 | 雾/霾 |

---

## 相关资源

- 官方文档：https://wttr.in/:help
- 源码仓库：https://github.com/chubin/wttr.in
- 翻译贡献：/translation

---

## 使用流程总结

当用户需要查询天气时：

1. **确定位置** - 城市名、机场代码、特殊地点（加~）
2. **选择格式** - 终端显示、JSON API、PNG 图片
3. **设置参数** - 单位、语言、自定义输出
4. **执行查询** - 使用 curl/wget/httpie 或辅助脚本
5. **解析结果** - 直接显示或程序处理

---

## 辅助脚本使用

### Python 脚本 (`scripts/weather.py`)

功能丰富的查询工具，支持多种输出格式：

```bash
# 标准天气查询
python scripts/weather.py Beijing

# JSON 格式（适合程序处理）
python scripts/weather.py Beijing -f json

# 精简 JSON（不含小时数据）
python scripts/weather.py Beijing -f json-lite

# 一行输出（适合状态栏）
python scripts/weather.py Beijing -f oneline

# 自定义格式
python scripts/weather.py Tokyo --custom-format "%l: %c %t"

# 下载 PNG 图片
python scripts/weather.py Paris -f png -o weather.png

# 详细预报 (v2)
python scripts/weather.py Beijing -f v2

# 地图视图 (v3)
python scripts/weather.py California -f v3

# 月相查询
python scripts/weather.py -f moon

# 指定日期月相
python scripts/weather.py -f moon --moon-date 2025-12-25
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `location` | 地点名称（可选，默认为当前位置） |
| `-f, --format` | 输出格式：terminal, json, json-lite, oneline, png, v2, v2-day, v2-night, v3, plain, compact, prometheus, moon |
| `-l, --lang` | 语言代码（默认 zh） |
| `-u, --unit` | 单位：m=公制，u=英制，M=公制+m/s |
| `-o, --output` | 输出文件路径（PNG 格式用） |
| `--custom-format` | 自定义 format 参数（%-notation） |
| `--moon-date` | 月相查询日期 (YYYY-MM-DD) |
| `--transparent` | PNG 透明背景 |
| `--transparency` | PNG 透明度 (0-255) |

### 参考指南 (`references/quick-reference.md`)

速查手册，包含：
- 常用命令速查表
- 自定义格式代码对照
- 预设格式示例
- 支持的语言代码
- 天气代码对照表
- tmux 配置示例
- 故障排除指南

**建议**：查询具体参数或忘记语法时，参考 `references/quick-reference.md`
