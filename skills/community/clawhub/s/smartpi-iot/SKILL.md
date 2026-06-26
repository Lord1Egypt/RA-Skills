---
name: smartpi-iot
description: 智能公元 IoT 设备控制插件。可控制灯光、加湿器、窗帘等设备，支持查询设备状态。
author: namishisu
version: 1.0.0
homepage: https://smartpi.cn/
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠",
        "requires": { "bins": ["curl"] },
        "config":
          {
            "env":
              {
                "SMARTPI_TOKEN":
                  {
                    "description": "智能公元 API 访问令牌",
                    "required": true,
                  },
                "SMARTPI_DEVICE_KEY":
                  {
                    "description": "设备编号",
                    "required": true,
                  },
              },
          },
      },
  }
---

# 智能公元 IoT 技能

控制智能公元（SmartPi）IoT 设备，包括灯光、加湿器、窗帘等。

## 配置

**必需环境变量：**

```bash
export SMARTPI_TOKEN="your-api-token"
export SMARTPI_DEVICE_KEY="your-device-key"
```

或在 OpenClaw 配置中设置：

```json
{
  "env": {
    "SMARTPI_TOKEN": "your-api-token",
    "SMARTPI_DEVICE_KEY": "your-device-key"
  }
}
```

## API 基础地址

```
https://mcp.aimachip.com
```

---

## 命令

### 💡 灯光控制

#### 控制灯开关

```bash
curl -X POST https://mcp.aimachip.com/plugin/control/switch_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "switch_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'",
    "value": 1
  }'
```

**参数：**
- `value`: `0` (关闭) 或 `1` (打开)

#### 查询灯开关状态

```bash
curl -X POST https://mcp.aimachip.com/plugin/query/switch_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "switch_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'"
  }'
```

#### 控制灯光亮度

```bash
curl -X POST https://mcp.aimachip.com/plugin/control/slider_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "slider_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'",
    "value": 50
  }'
```

**参数：**
- `value`: 亮度值 (0-100)

#### 查询灯光亮度

```bash
curl -X POST https://mcp.aimachip.com/plugin/query/slider_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "slider_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'"
  }'
```

---

### 💨 加湿器控制

#### 控制加湿器开关

```bash
curl -X POST https://mcp.aimachip.com/plugin/control/power_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "power_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'",
    "value": 1
  }'
```

**参数：**
- `value`: `0` (关闭) 或 `1` (打开)

#### 查询加湿器状态

```bash
curl -X POST https://mcp.aimachip.com/plugin/query/power_1/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "power_1",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'"
  }'
```

---

### 🪟 窗帘控制

#### 控制窗帘开关

```bash
curl -X POST https://mcp.aimachip.com/plugin/control/switch_2/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "switch_2",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'",
    "value": 1
  }'
```

**参数：**
- `value`: `0` (关闭) 或 `1` (打开)

#### 查询窗帘状态

```bash
curl -X POST https://mcp.aimachip.com/plugin/query/switch_2/1773819411753 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "switch_2",
    "deviceKey": "'$SMARTPI_DEVICE_KEY'",
    "token": "'$SMARTPI_TOKEN'"
  }'
```

---

## 快速命令

### 脚本封装

创建 `~/.openclaw/workspace/skills/smartpi-iot/scripts/iot-control.sh`：

```bash
#!/bin/bash

BASE_URL="https://mcp.aimachip.com"
TOKEN="${SMARTPI_TOKEN}"
DEVICE_KEY="${SMARTPI_DEVICE_KEY}"

control() {
  local action=$1
  local value=$2
  curl -s -X POST "${BASE_URL}/plugin/control/${action}/1773819411753" \
    -H "Content-Type: application/json" \
    -d "{\"action\": \"${action}\", \"deviceKey\": \"${DEVICE_KEY}\", \"token\": \"${TOKEN}\", \"value\": ${value}}"
}

query() {
  local action=$1
  curl -s -X POST "${BASE_URL}/plugin/query/${action}/1773819411753" \
    -H "Content-Type: application/json" \
    -d "{\"action\": \"${action}\", \"deviceKey\": \"${DEVICE_KEY}\", \"token\": \"${TOKEN}\"}"
}

case "$1" in
  light-on)   control switch_1 1 ;;
  light-off)  control switch_1 0 ;;
  light-query) query switch_1 ;;
  brightness) control slider_1 "$2" ;;
  humidifier-on)  control power_1 1 ;;
  humidifier-off) control power_1 0 ;;
  humidifier-query) query power_1 ;;
  curtain-open)  control switch_2 1 ;;
  curtain-close) control switch_2 0 ;;
  curtain-query) query switch_2 ;;
  *) echo "Usage: $0 {light-on|light-off|light-query|brightness|humidifier-on|humidifier-off|humidifier-query|curtain-open|curtain-close|curtain-query}" ;;
esac
```

---

## 使用示例

### 在 OpenClaw 中调用

```bash
# 开灯
exec: curl -X POST https://mcp.aimachip.com/plugin/control/switch_1/1773819411753 -H "Content-Type: application/json" -d '{"action":"switch_1","deviceKey":"YOUR_DEVICE_KEY","token":"YOUR_TOKEN","value":1}'

# 查询灯光状态
exec: curl -X POST https://mcp.aimachip.com/plugin/query/switch_1/1773819411753 -H "Content-Type: application/json" -d '{"action":"switch_1","deviceKey":"YOUR_DEVICE_KEY","token":"YOUR_TOKEN"}'

# 设置灯光亮度 50%
exec: curl -X POST https://mcp.aimachip.com/plugin/control/slider_1/1773819411753 -H "Content-Type: application/json" -d '{"action":"slider_1","deviceKey":"YOUR_DEVICE_KEY","token":"YOUR_TOKEN","value":50}'

# 打开加湿器
exec: curl -X POST https://mcp.aimachip.com/plugin/control/power_1/1773819411753 -H "Content-Type: application/json" -d '{"action":"power_1","deviceKey":"YOUR_DEVICE_KEY","token":"YOUR_TOKEN","value":1}'

# 打开窗帘
exec: curl -X POST https://mcp.aimachip.com/plugin/control/switch_2/1773819411753 -H "Content-Type: application/json" -d '{"action":"switch_2","deviceKey":"YOUR_DEVICE_KEY","token":"YOUR_TOKEN","value":1}'
```

---

## 响应格式

### 控制响应

```json
{
  "status": "success",
  "message": "操作成功"
}
```

### 查询响应

```json
{
  "data": {
    "data": 1,
    "status": "success"
  }
}
```

**状态值说明：**
- `0` = 关闭
- `1` = 打开

---

## 注意事项

1. **令牌安全**：不要将 `SMARTPI_TOKEN` 提交到版本控制
2. **设备编号**：确保 `SMARTPI_DEVICE_KEY` 与你的设备匹配
3. **API 限制**：避免频繁调用，建议添加请求间隔
4. **网络要求**：确保可以访问 `mcp.aimachip.com`

---

## 获取更多信息

- 官方网站：https://smartpi.cn/
- API 文档：查看设备管理后台

---

**作者**: namishisu  
**版本**: 1.0.0  
**许可证**: MIT
