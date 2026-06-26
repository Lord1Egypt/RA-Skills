---
name: xiaodu-control
description: 小度智能设备控制技能。用于控制小度音箱、IoT设备、查看设备列表、语音播报等。当用户需要控制小度智能设备、查询设备状态、发送语音指令或管理智能家居时使用此技能。
---

# 小度智能设备控制技能

## 概述

此技能提供对小度智能设备的全面控制能力，包括：
- 小度音箱设备控制（语音指令、播报）
- IoT设备控制（灯光、窗帘、开关等）
- 设备列表查看和状态监控
- 语音播报和消息推送

## 前置条件

在使用此技能前，确保已正确配置：
1. **MCP服务器配置**：已配置小度音箱和IoT的MCP服务器
2. **Access Token**：有效的百度DuerOS access_token
3. **设备发现**：已运行设备发现脚本获取设备列表

## 核心功能

### 1. 设备列表查看

查看所有在线的小度设备：

```bash
# 查看小度音箱设备列表
mcporter call xiaodu.list_user_devices

# 查看IoT设备列表
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS
```

### 2. 小度音箱控制

#### 发送语音指令
```bash
# 发送语音指令到指定设备
mcporter call xiaodu.control_xiaodu \
  command="现在几点了？" \
  cuid="YOUR_DEVICE_CUID" \
  client_id="YOUR_CLIENT_ID"
```

#### 语音播报
```bash
# 播报自定义文本
mcporter call xiaodu.xiaodu_speak \
  text="你好，我是OpenClaw AI助手" \
  cuid="YOUR_DEVICE_CUID" \
  client_id="YOUR_CLIENT_ID"
```

### 3. IoT设备控制

#### 控制灯光
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
```

#### 控制窗帘
```bash
# 打开主卧布帘
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="up" \
  applianceName="布帘" \
  roomName="主卧"

# 关闭主卧布帘
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="down" \
  applianceName="布帘" \
  roomName="主卧"
```

#### 控制开关面板
```bash
# 打开走廊灯
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
  action="turnOn" \
  applianceName="左键" \
  roomName="走廊"
```

### 4. 场景控制

#### 获取场景列表
```bash
mcporter call xiaodu-iot.GET_ALL_SCENES
```

#### 触发场景
```bash
mcporter call xiaodu-iot.TRIGGER_SCENES \
  sceneName="回家模式"
```

## 实用脚本

### 设备列表更新脚本
查看 [scripts/update_devices.sh](scripts/update_devices.sh) - 自动更新设备列表并保存到文件

### 批量控制脚本
查看 [scripts/batch_control.sh](scripts/batch_control.sh) - 批量控制多个设备

### 语音播报脚本
查看 [scripts/speak_message.sh](scripts/speak_message.sh) - 向指定设备发送语音播报

## 设备管理

### 设备文件位置
- **小度音箱设备列表**: `~/openclaw/workspace/xiaodu_devices.md`
- **IoT设备列表**: `~/openclaw/workspace/xiaodu_iot_devices.md`
- **更新日志**: `~/openclaw/workspace/logs/xiaodu_update_*.log`

### 自动更新系统
设备列表每天凌晨2:00自动更新，确保设备信息最新。

## 故障排除

### 常见问题

1. **MCP服务器连接失败**
   - 检查access_token是否过期（有效期30天）
   - 验证MCP服务器配置是否正确

2. **设备无响应**
   - 确认设备在线状态
   - 检查设备CUID和Client ID是否正确
   - 验证网络连接

3. **权限问题**
   - 确保access_token有足够的设备控制权限
   - 检查设备是否已授权给当前应用

### 调试命令
```bash
# 测试MCP服务器连接
mcporter config list

# 查看服务器状态
mcporter call xiaodu.list_user_devices | head -5

# 测试简单指令
mcporter call xiaodu.control_xiaodu command="小度小度" cuid="YOUR_DEVICE_CUID" client_id="YOUR_CLIENT_ID"
```

## 最佳实践

1. **设备选择**：使用设备文件中的最新设备信息
2. **错误处理**：所有命令都应包含错误检查
3. **日志记录**：重要操作记录到日志文件
4. **批量操作**：使用脚本进行批量控制，避免手动重复
5. **定期更新**：利用自动更新系统保持设备信息最新

## 参考文档

- [小度音箱MCP配置指南](references/xiaodu_mcp.md)
- [IoT设备控制API](references/iot_api.md)
- [设备管理最佳实践](references/device_management.md)
- [故障排除手册](references/troubleshooting.md)