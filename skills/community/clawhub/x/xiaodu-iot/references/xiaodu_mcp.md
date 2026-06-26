# 小度音箱MCP配置指南

## 概述

小度音箱MCP（Model Context Protocol）服务器提供了通过API控制小度智能设备的能力。本文档详细介绍了MCP服务器的配置和使用方法。

## MCP服务器配置

### 1. 服务器URL
```
https://xiaodu.baidu.com/dueros_mcp_server/mcp/
```

### 2. 认证方式
使用HTTP Header进行认证：
```
ACCESS_TOKEN: <your_access_token>
```

### 3. Access Token获取
Access Token通过百度DuerOS开放平台获取，有效期30天。需要定期刷新。

### 4. 配置命令
```bash
# 添加MCP服务器配置
mcporter config add xiaodu \
  https://xiaodu.baidu.com/dueros_mcp_server/mcp/ \
  --header "ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE"
```

## 可用工具

### 1. list_user_devices
获取用户的所有小度设备列表。

**参数**: 无

**返回**: JSON格式的设备列表，包含：
- `devices`: 设备数组
  - `cuid`: 设备唯一标识
  - `client_id`: 客户端ID
  - `device_name`: 设备名称
  - `device_type`: 设备类型
  - `online`: 在线状态

**示例**:
```bash
mcporter call xiaodu.list_user_devices
```

### 2. control_xiaodu
向小度设备发送语音指令。

**参数**:
- `command`: 语音指令文本
- `cuid`: 设备CUID
- `client_id`: 设备Client ID

**示例**:
```bash
mcporter call xiaodu.control_xiaodu \
  command="现在几点了？" \
  cuid="YOUR_DEVICE_CUID" \
  client_id="YOUR_CLIENT_ID"
```

### 3. xiaodu_speak
让小度设备播报自定义文本。

**参数**:
- `text`: 播报文本
- `cuid`: 设备CUID
- `client_id`: 设备Client ID

**示例**:
```bash
mcporter call xiaodu.xiaodu_speak \
  text="你好，我是OpenClaw AI助手" \
  cuid="YOUR_DEVICE_CUID" \
  client_id="YOUR_CLIENT_ID"
```

### 4. xiaodu_take_photo
让带摄像头的设备拍照。

**参数**:
- `cuid`: 设备CUID
- `client_id`: 设备Client ID

**注意**: 需要设备支持摄像头功能。

### 5. push_resource_to_xiaodu
向设备推送资源（图片/视频/音频）。

**参数**:
- `cuid`: 设备CUID
- `client_id`: 设备Client ID
- `resource_type`: 资源类型（image/video/audio）
- `resource_url`: 资源URL

## 设备信息

### 设备标识
每个小度设备有两个关键标识：
1. **CUID**: 设备唯一标识，格式如 `XXXXXXXXXXXXXX`
2. **Client ID**: 客户端ID，格式如 `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

### 设备类型
- 智能音箱
- 智能中控屏
- 智能屏
- 带屏设备
- 智能电视
- 智能健身镜

## 最佳实践

### 1. 设备选择
- 优先选择在线设备
- 根据房间位置选择合适设备
- 带屏设备支持更多功能

### 2. 指令设计
- 语音指令要自然、简洁
- 避免过长或复杂的指令
- 考虑设备响应时间

### 3. 错误处理
- 检查设备在线状态
- 处理网络超时
- 记录操作日志

### 4. 性能优化
- 批量操作添加延迟
- 避免频繁调用API
- 缓存设备信息

## 常见问题

### Q1: Access Token过期怎么办？
A: Access Token有效期为30天，需要定期刷新。可以通过百度DuerOS开放平台重新获取。

### Q2: 设备无响应怎么办？
A: 检查：
1. 设备是否在线
2. 网络连接是否正常
3. CUID和Client ID是否正确
4. Access Token是否有效

### Q3: 如何获取设备CUID和Client ID？
A: 使用 `list_user_devices` 工具获取所有设备信息，从中提取需要的设备标识。

### Q4: 支持哪些设备类型？
A: 支持所有小度智能设备，包括音箱、中控屏、电视、健身镜等。具体功能取决于设备硬件能力。

### Q5: 语音播报有长度限制吗？
A: 建议播报文本不超过500字符，过长的文本可能被截断或导致播报失败。

## 调试技巧

### 1. 测试连接
```bash
# 测试MCP服务器连接
mcporter config list | grep xiaodu

# 测试简单指令
mcporter call xiaodu.list_user_devices | head -5
```

### 2. 查看详细错误
```bash
# 启用详细输出
mcporter call xiaodu.list_user_devices --verbose

# 查看HTTP响应
mcporter call xiaodu.list_user_devices --raw
```

### 3. 监控网络请求
使用网络监控工具查看MCP服务器请求和响应。

## 安全注意事项

1. **保护Access Token**: 不要泄露Access Token
2. **权限控制**: 确保只有授权设备可控制
3. **操作审计**: 记录所有控制操作
4. **频率限制**: 避免过于频繁的API调用