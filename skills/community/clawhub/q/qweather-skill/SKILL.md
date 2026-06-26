---
name: qweather
version: 0.5.0
description: 查询全球城市或者经纬度位置的实时天气、天气预报、空气质量等信息的技能。当用户询问某个城市或者经纬度的天气、气温、降雨、风向、空气质量时调用。
homepage: https://github.com/yinguobing/qweather-skill
required_env_vars:
  - QWEATHER_KID
  - QWEATHER_PROJECT_ID
  - QWEATHER_PRIVATE_KEY
  - QWEATHER_BASE_URL
  - QWEATHER_GEO_URL
primary_credential: QWEATHER_PRIVATE_KEY
metadata: {"openclaw":{"requires":{"env":["QWEATHER_KID","QWEATHER_PROJECT_ID","QWEATHER_PRIVATE_KEY","QWEATHER_BASE_URL","QWEATHER_GEO_URL"]},"primaryEnv":"QWEATHER_PRIVATE_KEY","homepage":"https://github.com/yinguobing/qweather-skill","install":[{"id":"qweather","kind":"cargo","package":"qweather","bins":["qw"],"label":"Install qweather via cargo"}]}}
---

# 和风天气查询技能

基于和风天气（QWeather）API，提供全球城市的天气查询能力。

## 安装
使用Cargo安装：
```bash
cargo install qweather
```

源码安装
```bash
cargo install --git https://github.com/yinguobing/qweather-skill.git
```

如果需要使用curl + install.sh安装请参考官方文档：
```url
https://github.com/yinguobing/qweather-skill
```

## 身份认证

使用 JWT 身份认证，**必须**配置以下环境变量：

```bash
export QWEATHER_KID="YOUR_KID"
export QWEATHER_PROJECT_ID="YOUR_PROJECT_ID"
export QWEATHER_PRIVATE_KEY="/path/to/qweather/private.pem"
export QWEATHER_BASE_URL="https://your-host.qweatherapi.com/v7"
export QWEATHER_GEO_URL="https://your-host.qweatherapi.com/geo/v2"
```

详情可在[和风天气控制台](https://console.qweather.com/project)获取。

## CLI 使用

全局入口为 `qw`。通过命令+子命令提供具体功能。

### 常用查询

```bash
# 地理位置
qw geo city-lookup 北京
qw geo reverse --lon 113.4695 --lat 23.1895    # 经纬度反查行政区划
qw geo top-city --range cn
qw geo poi-lookup 故宫 --type scenic
qw geo poi-range 116.40,39.90 --type scenic --radius 10

# 实时天气
qw weather now --city 北京

# 未来N天预报（daily 仅支持 3,7,10,15,30）
qw weather daily --city 北京
qw weather daily 7 --city 北京

# 逐小时预报（hourly 仅支持 24,72,168）
qw weather hourly --city 北京
qw weather hourly 72 --city 北京

# 格点天气（基于经纬度的高分辨率数据）
qw grid now --lon 116.40 --lat 39.90
qw grid daily --lon 116.40 --lat 39.90
qw grid daily 7 --lon 116.40 --lat 39.90
qw grid hourly --lon 116.40 --lat 39.90

# 分钟级降水（仅中国地区）
qw precipitation --lon 116.40 --lat 39.90

# 生活指数
qw indices --city 北京
qw indices --city 北京 --days 3d

# 天气预警
qw warning --city 北京

# 空气质量
qw air now --city 北京
qw air daily --city 北京
qw air daily 5 --city 北京
qw air hourly --city 北京
qw air station --city 北京

# 日出日落（--date 必选，格式 yyyyMMdd，最多未来 60 天）
qw sun --city 北京 --date 20260416

# 月升月落和月相（--date 必选，格式 yyyyMMdd，最多未来 60 天）
qw moon --city 北京 --date 20260416

# 太阳高度角（--date 必选；--time 格式 HHmm；--tz 时区偏移如 0800；-alt 海拔高度米）
qw solar --lon 116.40 --lat 39.90 --date 20260416 --time 1200 --tz 0800 --alt 43
```

### 定位方式

所有需要地理定位的命令支持以下三种方式（互斥，三选一）：
- `--city <name>`：城市名称，自动调用 geo API 解析为 Location ID 和坐标
- `--location-id <id>`：直接使用 Location ID
- `--lon <float>` + `--lat <float>`：经纬度坐标（必须同时提供）

### 命令行参数速查

**全局参数**（所有命令共享）：
- `--kid` / `--project-id` / `--private-key` / `--base-url` / `--geo-url`：覆盖环境变量
- `--lang`：语言（默认 `zh`）

**各命令专属参数**：
- `weather daily [DAYS]`：`3|7|10|15|30`（默认 3）
- `weather hourly [HOURS]`：`24|72|168`（默认 24）
- `grid daily [DAYS]`：`3|7`（默认 3）
- `grid hourly [HOURS]`：`24|72`（默认 24）
- `air hourly [HOURS]`：`24|72`（默认 24）
- `air daily [DAYS]`：`1|3|5`（默认 3）
- `indices --days <1d|3d>`（默认 `1d`）
- `sun --date yyyyMMdd` / `moon --date yyyyMMdd`
- `solar --date yyyyMMdd --time HHmm --tz 偏移 --alt 海拔`

### 参数限制

| 命令 | 参数 | 限制说明 |
|------|------|---------|
| `weather daily` | `[DAYS]` | 仅支持 `3,7,10,15,30` |
| `weather hourly` | `[HOURS]` | 仅支持 `24,72,168` |
| `grid daily` | `[DAYS]` | 仅支持 `3,7` |
| `grid hourly` | `[HOURS]` | 仅支持 `24,72` |
| `air daily` | `[DAYS]` | 仅支持 `1,3,5` |
| `air hourly` | `[HOURS]` | 仅支持 `24,72` |
| `sun` / `moon` | `--date` | 必选，格式 `yyyyMMdd`，**仅未来 60 天内（含今天）** |
| `solar` | `--date` / `--time` / `--tz` / `--alt` | 全部必填 |
