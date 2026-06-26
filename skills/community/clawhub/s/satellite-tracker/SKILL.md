---
name: Satellite Tracker
version: 1.1.0
license: MIT-0
description: >
  Real-time satellite and spacecraft tracking powered by SGP4 orbit prediction.
  Supports Tiangong (CSS), ISS, Hubble, or any NORAD catalog ID.
  Features real-time coordinates, speed, altitude, pass predictions, and geographic region display.
  Data source: Celestrak TLE (free, no API key required).
  实时追踪卫星和航天器位置。支持天宫空间站、ISS、天舟货运飞船等。
  输入卫星名或NORAD ID，输出实时坐标、速度、高度、所在区域。
  支持过境预测（输入观测者坐标）。
  数据源：Celestrak TLE + SGP4轨道预测，免费无需API Key。
author: fengyucn
category: space
tags: [satellite, orbit, space, tracking, 天宫, ISS, 天舟, SGP4, TLE, celestrak]
entry: track.py
config: []
---

# Satellite Tracker / 卫星追踪器

**Real-time satellite tracking for AI agents — no API key required.**
实时卫星追踪 —— 无需 API Key，开箱即用。

## When to Use / 何时使用

- User asks where a satellite or space station is / 用户问某颗卫星/空间站在哪
- User asks about Tiangong (CSS) or ISS location / 用户问天宫空间站或ISS位置
- User wants to track a spacecraft after launch / 用户想追踪发射后的航天器
- User wants satellite pass predictions / 用户想看卫星过境时间
- User is following a launch mission / 用户追踪发射任务

## Installation / 安装

```bash
pip install sgp4
```

## Usage / 用法

```bash
# Real-time position by name / 按名称查询
python3 skills/satellite-tracker/track.py --name 天宫
python3 skills/satellite-tracker/track.py --name ISS

# Real-time position by NORAD ID / 按NORAD ID查询
python3 skills/satellite-tracker/track.py --id 48274

# Pass predictions (requires observer coordinates) / 过境预测（需要观测者坐标）
python3 skills/satellite-tracker/track.py --name 天宫 --observer 28.2,112.9 --passes 5

# List all known satellites / 列出所有已知卫星
python3 skills/satellite-tracker/track.py --list

# Update TLE cache / 更新TLE缓存
python3 skills/satellite-tracker/track.py --update

# Continuous tracking mode / 持续追踪模式
python3 skills/satellite-tracker/track.py --name 天宫 --watch 60

# JSON output / JSON输出
python3 skills/satellite-tracker/track.py --name 天宫 --json
```

## Known Satellites / 已知卫星

| Name / 名称 | NORAD ID | Description / 说明 |
|---|---|---|
| 天宫 (Tiangong/CSS) | 48274 | 中国空间站 Chinese Space Station |
| ISS | 25544 | 国际空间站 International Space Station |
| 哈勃 (Hubble) | 20580 | 哈勃太空望远镜 Hubble Space Telescope |

New satellites (e.g. Tianzhou cargo spacecraft) get assigned NORAD IDs after launch.
Use `--update` to refresh TLE data, then search by ID.
天舟等新航天器发射后会分配NORAD ID，用 `--update` 更新后可追踪。

## Output / 输出示例

```
🛰️ 天宫 (CSS)
━━━━━━━━━━━━━━━━━━━━━━━
⏰ 北京时间: 2026-05-08 16:32:43
📍 纬度: 29.12°S
📍 经度: 170.84°E
📏 轨道高度: 384.9 km
🚀 飞行速度: 7.68 km/s (27656 km/h)
🌐 区域: 🌏 澳洲上空

📊 轨道参数 Orbital Parameters
  周期 Period: 92.1 min (15.6 orbits/day)
  倾角 Inclination: 41.47°
  远地点 Apogee: 388 km
  近地点 Perigee: 382 km
```

## Pass Prediction Output / 过境预测示例

```
🔭 天宫 过境预测 Pass Predictions
观测位置: 28.2000°N, 112.9000°E
━━━━━━━━━━━━━━━━━━━━━━━

第1次过境 Pass #1:
  ⏰ 北京时间: 2026-05-09 00:34:13
  📐 最大仰角 Max Elevation: 30.3°
  📍 地面距离 Ground Distance: 647 km
  📏 卫星高度 Altitude: 378 km
```

## Technical Details / 技术细节

| Item / 项目 | Detail / 说明 |
|---|---|
| Orbit model / 轨道模型 | SGP4 (Simplified General Perturbations) |
| Data source / 数据源 | Celestrak TLE (updated hourly) / 每小时更新 |
| Cache / 缓存 | Local JSON, 1-hour TTL / 本地JSON，1小时有效期 |
| Coordinate system / 坐标系 | TEME → ECEF via GMST rotation |
| Pass prediction / 过境预测 | Brute-force scan with 10s steps, 5° min elevation |

## Dependencies / 依赖

- `sgp4` (Python package / Python包)
- Internet connection for TLE data / 网络连接（获取TLE数据）

## License

MIT-0
