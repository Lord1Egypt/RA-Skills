---
name: variflight-aviation
description: 航班信息查询 Skill（飞常准官方 MCP）- 实时航班动态、航线搜索、舒适度评估、机场天气、中转规划、实时定位
version: 1.0.4
author: lixiao
license: MIT

metadata:
  openclaw:
    emoji: "✈️"
    category: "travel"
    tags: ["flight", "aviation", "travel", "weather", "transport", "mcp", "variflight"]

    env:
      - X_VARIFLIGHT_KEY

    requirements: |
      系统要求：
      - Node.js >= 18.0.0
      - npx（随 Node.js 自带）

      配置要求：
      1. 前往 https://ai.variflight.com/keys 注册并获取 API Key
      2. 在 config.local.json 中填写 "apiKey"，或设置环境变量 X_VARIFLIGHT_KEY

    os:
      - darwin
      - linux
      - win32

    permissions:
      - network
      - env-read
      - file-read
---

## 功能概述

本 Skill 接入 [飞常准（VariFlight）官方 MCP 服务](https://ai.variflight.com)，提供国内外航班全量数据查询。无需 Python/uvx，通过 `npx` 按需启动 MCP 服务器。

数据来源：飞常准是中国最大的航班数据服务商，覆盖国内外全量航班，含实时动态、准点率历史、飞机实时位置、舒适度指数等。

## 配置说明

### 方法 1：本地配置文件（推荐）

创建 `config.local.json`（已加入 .gitignore）：

```json
{
  "apiKey": "your_variflight_key_here"
}
```

### 方法 2：环境变量

```bash
export X_VARIFLIGHT_KEY="your_variflight_key_here"
```

前往 [https://ai.variflight.com/keys](https://ai.variflight.com/keys) 注册免费账号获取 Key（注册即赠 50 元体验额度）。

## 可用命令

### 1. info - 航班详情查询

```bash
@variflight-aviation info <fnum> [date]
```

按航班号查询详细信息：出发/到达时间、延误、机型、准点率、值机柜台、行李转盘等。

**示例：**
```bash
@variflight-aviation info CA1501
@variflight-aviation info CA1501 2026-03-17
```

### 2. search - 航班搜索

```bash
@variflight-aviation search <dep> <arr> [date]
```

查询两机场之间的所有航班。支持机场三字码（PEK）或城市三字码（BJS）。

**示例：**
```bash
@variflight-aviation search PEK SHA
@variflight-aviation search SZX PEK 2026-03-17
```

### 3. track - 实时航班追踪

```bash
@variflight-aviation track <fnum> [date]
```

查询航班今日实时状态（起降时间、延误、飞行阶段），并尝试获取飞机实时经纬度位置。

**示例：**
```bash
@variflight-aviation track CA1501
```

### 4. comfort - 乘机舒适度评估

```bash
@variflight-aviation comfort <fnum> [date]
```

获取飞常准「飞行幸福指数」，涵盖机型、座椅、餐食、准点率等综合评分。

**示例：**
```bash
@variflight-aviation comfort CA1501
@variflight-aviation comfort MU2157 2026-03-17
```

### 5. weather - 机场天气

```bash
@variflight-aviation weather <airport>
```

查询机场未来3天天气预报（今日/明日/后日），数据来自飞常准气象服务。

**示例：**
```bash
@variflight-aviation weather PEK
@variflight-aviation weather SHA
```

### 6. transfer - 中转方案规划

```bash
@variflight-aviation transfer <dep> <arr> [date]
```

查询两城市间的中转航班方案，推荐使用城市三字码。

**示例：**
```bash
@variflight-aviation transfer BJS LAX 2026-03-17
@variflight-aviation transfer SHA LHR
```

## 常用代码对照

| 城市/机场 | 机场代码 | 城市代码 |
|----------|---------|---------|
| 北京首都 | PEK | BJS |
| 北京大兴 | PKX | BJS |
| 上海虹桥 | SHA | SHA |
| 上海浦东 | PVG | SHA |
| 广州白云 | CAN | CAN |
| 深圳宝安 | SZX | SZX |
| 成都天府 | TFU | CTU |
| 香港 | HKG | HKG |
| 东京成田 | NRT | TYO |
| 新加坡 | SIN | SIN |
| 伦敦希思罗 | LHR | LON |
| 纽约肯尼迪 | JFK | NYC |
| 洛杉矶 | LAX | LAX |

## 飞常准 MCP 工具对照

| 命令 | 飞常准 MCP 工具 |
|------|--------------|
| `info` | `searchFlightsByNumber` |
| `search` | `searchFlightsByDepArr` |
| `track` | `searchFlightsByNumber` + `getRealtimeLocationByAnum` |
| `comfort` | `flightHappinessIndex` |
| `weather` | `getFutureWeatherByAirport` |
| `transfer` | `getFlightTransferInfo` |

## 故障排除

### 错误：API Key 未配置
**解决**：在 `config.local.json` 中设置 `apiKey`，前往 https://ai.variflight.com/keys 获取

### 错误：npx 命令找不到
**解决**：确认已安装 Node.js（`node -v`），npx 随 npm 一同安装

### 首次运行较慢
**原因**：npx 首次自动下载 `@variflight-ai/variflight-mcp` 包  
**解决**：手动预下载：`npx -y @variflight-ai/variflight-mcp`

## 相关链接

- [飞常准 MCP 官网](https://ai.variflight.com)
- [获取 API Key](https://ai.variflight.com/keys)
- [官方使用文档](https://bcnucz2nnop8.feishu.cn/wiki/SDFDwQIaAiM3hxk6uyhcJxSkn2b)
- [@variflight-ai/variflight-mcp on npm](https://www.npmjs.com/package/@variflight-ai/variflight-mcp)
- [Model Context Protocol 规范](https://modelcontextprotocol.io/)

## 许可证

MIT License © 2026 lixiao
