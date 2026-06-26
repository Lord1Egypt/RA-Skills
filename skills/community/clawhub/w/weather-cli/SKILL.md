---
name: weather-cli
description: 获取全球城市天气预报（使用 wttr.in 免费 API）
---

# Weather CLI

免费、无需 API Key 的全球天气预报工具。

## 安装依赖
确保已安装 `curl` 和 `jq`：
```bash
apt-get install -y curl jq  # Debian/Ubuntu
```

## 使用

```bash
# 获取北京天气（默认摄氏度）
weather Beijing

# 华氏温度
weather "New York" --unit f

# 获取特定城市的详细天气
weather "London" --full

# JSON 格式输出（用于脚本处理）
weather Tokyo --json
```

## 参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `location` | 城市名称（支持英文/中文） | 是 |
| `--unit` | 温度单位：`c`（摄氏度）或 `f`（华氏度） | 否，默认 `c` |
| `--full` | 显示完整天气信息（湿度、风速、气压） | 否 |
| `--json` | 输出 JSON 格式 | 否 |

## 示例输出

```
$ weather "Beijing"
北京, CN
═══════════════════════════════════════════
🌡️  温度: 15°C
☁️  天气: 晴
💨 风速: 3.6 km/h
💧 湿度: 45%
```

## 依赖
- `curl`: HTTP 请求
- `jq`: JSON 解析（仅 --json 模式需要）

## 数据来源
天气数据来自 [wttr.in](https://wttr.in) - 一个免费的无 API 限制天气服务。
