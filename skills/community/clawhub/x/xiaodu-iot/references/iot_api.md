# IoT设备控制API指南

## 概述

小度IoT MCP服务器提供了对智能家居设备的控制能力，包括灯光、窗帘、开关等。本文档详细介绍了IoT设备的控制API。

## MCP服务器配置

### 1. 服务器类型
本地命令模式（通过npx运行）

### 2. 配置命令
```json
{
  "mcpServers": {
    "xiaodu-iot": {
      "command": "npx",
      "args": ["-y", "dueros-iot-mcp"],
      "env": {
        "ACCESS_TOKEN": "YOUR_ACCESS_TOKEN_HERE"
      }
    }
  }
}
```

### 3. 配置文件位置
```
~/openclaw/workspace/config/mcporter.json
```

## 可用工具

### 1. GET_ALL_DEVICES_WITH_STATUS
获取所有IoT设备及其状态。

**参数**: 无

**返回**: JSON格式的设备列表，包含：
- `devices`: 设备数组
  - `applianceName`: 设备名称
  - `roomName`: 房间名称
  - `deviceType`: 设备类型
  - `status`: 设备状态
  - `capabilities`: 设备能力

**示例**:
```bash
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS
```

### 2. IOT_CONTROL_DEVICES
控制IoT设备。

**参数**:
- `action`: 控制动作
  - `turnOn`: 打开设备
  - `turnOff`: 关闭设备
  - `up`: 向上/打开（窗帘）
  - `down`: 向下/关闭（窗帘）
  - `set`: 设置数值（如亮度、温度）
- `applianceName`: 设备名称
- `roomName`: 房间名称
- `value`: 设置值（仅当action=set时使用）

**示例**:
```bash
# 打开书桌灯
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="书桌灯" \
  roomName="客厅"

# 关闭书桌灯
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOff" \
  applianceName="书桌灯" \
  roomName="客厅"

# 打开主卧布帘
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="up" \
  applianceName="布帘" \
  roomName="主卧"
```

### 3. GET_ALL_SCENES
获取所有场景列表。

**参数**: 无

**返回**: JSON格式的场景列表

**示例**:
```bash
mcporter call xiaodu-iot.GET_ALL_SCENES
```

### 4. TRIGGER_SCENES
触发场景。

**参数**:
- `sceneName`: 场景名称

**示例**:
```bash
mcporter call xiaodu-iot.TRIGGER_SCENES \
  sceneName="回家模式"
```

## 设备分类

### 1. 灯光类设备
- 书桌灯
- 洗衣机灯
- 走廊灯
- 镜前灯
- 面板灯
- 厨房灯

**支持操作**:
- `turnOn`: 打开
- `turnOff`: 关闭
- `set`: 设置亮度（0-100）

### 2. 窗帘类设备
- 布帘（主卧、次卧）
- 纱帘（主卧、次卧）

**支持操作**:
- `up`: 打开窗帘
- `down`: 关闭窗帘
- `set`: 设置开合百分比（0-100）

### 3. 开关面板
- 左键（多个房间）
- 右键（多个房间）

**支持操作**:
- `turnOn`: 打开
- `turnOff`: 关闭
- `toggle`: 切换状态

### 4. 场景面板
- 右键（场景面板模式）

**支持操作**:
- 触发预设场景

### 5. 其他设备
- 换气扇
- 智能投屏
- 按钮

## 设备命名规范

### 1. 设备名称
设备名称应清晰描述设备功能，如：
- `书桌灯`
- `主卧布帘`
- `走廊左键`

### 2. 房间名称
房间名称应使用标准命名，如：
- `客厅`
- `主卧`
- `次卧`
- `厨房`
- `走廊`
- `儿童房`

## 控制策略

### 1. 单个设备控制
```bash
# 精确控制单个设备
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="书桌灯" \
  roomName="客厅"
```

### 2. 批量设备控制
```bash
# 批量控制同一房间的多个设备
for device in "书桌灯" "走廊灯" "面板灯"; do
  mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
    action="turnOn" \
    applianceName="$device" \
    roomName="客厅"
  sleep 1
done
```

### 3. 场景触发
```bash
# 触发回家模式场景
mcporter call xiaodu-iot.TRIGGER_SCENES \
  sceneName="回家模式"
```

## 错误处理

### 1. 常见错误
- `设备未找到`: 检查设备名称和房间名称
- `设备离线`: 检查设备电源和网络连接
- `操作不支持`: 检查设备能力

### 2. 错误处理示例
```bash
if ! mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="书桌灯" \
  roomName="客厅"; then
  echo "控制失败，检查设备状态"
  # 重试或使用备用方案
fi
```

## 性能优化

### 1. 批量操作
- 使用脚本进行批量控制
- 添加适当延迟避免设备过载
- 并行控制非相关设备

### 2. 状态缓存
- 缓存设备状态减少API调用
- 定期刷新缓存
- 监听设备状态变化

### 3. 异步控制
对于非紧急操作，使用异步方式控制设备。

## 安全注意事项

### 1. 权限控制
- 仅控制授权设备
- 验证操作权限
- 记录操作日志

### 2. 操作限制
- 避免频繁操作
- 设置操作频率限制
- 防止误操作

### 3. 数据保护
- 保护Access Token
- 加密通信数据
- 定期更换凭证

## 调试技巧

### 1. 查看设备状态
```bash
# 查看所有设备状态
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS | jq '.devices[] | {name: .applianceName, room: .roomName, status: .status}'

# 查看特定房间设备
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS | jq '.devices[] | select(.roomName=="客厅")'
```

### 2. 测试控制命令
```bash
# 测试简单控制
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="书桌灯" \
  roomName="客厅" \
  --verbose

# 查看原始响应
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="书桌灯" \
  roomName="客厅" \
  --raw
```

### 3. 监控日志
查看MCP服务器运行日志，了解详细错误信息。