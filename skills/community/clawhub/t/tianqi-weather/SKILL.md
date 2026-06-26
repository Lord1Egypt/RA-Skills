---
name: 天气
description: "获取天气预报和气温信息。使用场景：用户询问天气、温度、降雨、出行建议等。支持通过 wttr.in 查询全球城市天气，无需 API Key。"
emoji: 🌤️
---

# 天气查询技能

获取指定城市的当前天气和未来预报。

## 使用场景

✅ **适用：**

- "今天天气怎么样？"
- "明天会下雨吗？"
- "北京/上海天气"
- "周末出行要带伞吗？"
- 查询任意城市气温

❌ **不适用：**

- 历史天气数据
- 极端天气预警（请查询气象局）
- 气象数据分析

## 查询方式

### 当前天气

```bash
# 简洁格式
curl "wttr.in/北京?format=3"

# 详细当前天气
curl "wttr.in/北京?0"
```

### 预报查询

```bash
# 3天预报
curl "wttr.in/北京"

# 周预报
curl "wttr.in/北京?format=v2"
```

### 常用格式

```bash
# 城市+天气+温度+体感
curl -s "wttr.in/北京?format=%l:+%c+%t+(体感%f)"

# 是否下雨
curl -s "wttr.in/北京?format=%l:+%c+%p"
```

## 格式代码

- `%c` — 天气状况emoji
- `%t` — 温度
- `%f` — 体感温度
- `%w` — 风速
- `%h` — 湿度
- `%p` — 降水量
- `%l` — 地点

## 快速示例

**查询上海天气：**
```bash
curl -s "wttr.in/上海?format=%l:+%c+%t+(体感%f),+%w风,+%h湿度"
```

**查询明天会不会下雨：**
```bash
curl -s "wttr.in/广州?1&format=%c+%p"
```

## 支持格式

- 支持城市名：`curl wttr.in/深圳`
- 支持拼音：`curl wttr.in/Shenzhen`
- 支持机场代码：`curl wttr.in/PEK`
- 支持中文：`curl wttr.in/东京?format=3`

## 注意事项

- 无需 API Key
- 有请求频率限制，请勿频繁刷请求
- 支持全球主要城市
- 网络不稳定时可能需要重试
