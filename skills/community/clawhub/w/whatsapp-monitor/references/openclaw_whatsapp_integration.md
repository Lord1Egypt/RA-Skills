# OpenClaw WhatsApp 渠道集成指南

## 概述

本技能使用 OpenClaw 的 WhatsApp 渠道来监控消息。OpenClaw 通过 WhatsApp Web 协议提供消息收发功能。

## 前提条件

### 1. OpenClaw WhatsApp 渠道

确保 OpenClaw 已安装并配置 WhatsApp 渠道：

```bash
# 检查 OpenClaw 状态
openclaw status

# 启用 WhatsApp 渠道
openclaw channels enable whatsapp
```

### 2. 设备配对

#### 方法一：WhatsApp Web 配对（推荐）

1. **启动 OpenClaw WhatsApp 服务**
   ```bash
   openclaw whatsapp start
   ```

2. **获取配对二维码**
   ```bash
   openclaw whatsapp qr
   ```
   或通过 OpenClaw Web UI 查看二维码。

3. **扫描二维码**
   - 在手机上打开 WhatsApp
   - 点击右上角菜单 → 链接设备 → 扫描二维码
   - 扫描 OpenClaw 显示的二维码

4. **验证配对状态**
   ```bash
   openclaw whatsapp status
   ```
   应显示设备状态为 "connected"。

#### 方法二：WhatsApp Business API

如果需要使用 WhatsApp Business API：

1. **获取 API 凭证**
   - 访问 Facebook Developer Portal
   - 创建 WhatsApp Business 应用
   - 获取 Phone Number ID 和 Access Token

2. **配置 OpenClaw**
   ```yaml
   # config/channels/whatsapp.yaml
   whatsapp:
     enabled: true
     type: "business"
     phone_number_id: "YOUR_PHONE_NUMBER_ID"
     access_token: "YOUR_ACCESS_TOKEN"
     webhook_verify_token: "YOUR_VERIFY_TOKEN"
   ```

## API 端点

### 获取消息

```http
GET http://localhost:18789/api/v1/channels/whatsapp/messages
```

**查询参数：**
- `target` (可选): 聊天 ID 或名称
- `limit` (可选): 返回消息数量，默认 50
- `since` (可选): ISO 时间戳，获取此时间之后的消息

**响应示例：**
```json
{
  "success": true,
  "messages": [
    {
      "id": "message_123",
      "timestamp": "2024-01-01T12:00:00Z",
      "sender": "+1234567890",
      "sender_name": "John Doe",
      "content": "Hello, this is a test message",
      "type": "text",
      "chat_id": "1234567890-1234567890@g.us",
      "chat_name": "Work Group"
    }
  ]
}
```

### 发送消息

```http
POST http://localhost:18789/api/v1/channels/whatsapp/send
```

**请求体：**
```json
{
  "to": "+1234567890",
  "message": "Hello from OpenClaw!"
}
```

### 获取聊天列表

```http
GET http://localhost:18789/api/v1/channels/whatsapp/chats
```

**响应示例：**
```json
{
  "success": true,
  "chats": [
    {
      "id": "1234567890-1234567890@g.us",
      "name": "Work Group",
      "type": "group",
      "unread_count": 5,
      "last_message": "See you tomorrow!"
    }
  ]
}
```

### 获取联系人列表

```http
GET http://localhost:18789/api/v1/channels/whatsapp/contacts
```

### 获取渠道状态

```http
GET http://localhost:18789/api/v1/channels/whatsapp/status
```

## 监控目标配置

### 聊天标识符格式

1. **个人聊天**: `+1234567890@c.us`
2. **群聊**: `1234567890-1234567890@g.us`

### 获取聊天 ID

```bash
# 列出所有聊天
openclaw whatsapp chats

# 查找特定聊天
openclaw whatsapp chats --search "Work Group"
```

## 故障排除

### 常见问题

1. **设备未连接**
   ```
   错误: WhatsApp 设备未配对
   ```
   **解决方案**: 重新扫描二维码配对

2. **消息获取失败**
   ```
   错误: 无法获取消息 (HTTP 404)
   ```
   **解决方案**: 检查 WhatsApp 渠道是否启用

3. **连接超时**
   ```
   错误: 连接超时
   ```
   **解决方案**: 
   - 检查网络连接
   - 重启 OpenClaw WhatsApp 服务
   ```bash
   openclaw whatsapp restart
   ```

### 日志查看

```bash
# 查看 WhatsApp 渠道日志
openclaw logs whatsapp

# 查看详细调试信息
openclaw logs whatsapp --level debug
```

### 重新配对

如果需要重新配对设备：

1. **注销当前设备**
   ```bash
   openclaw whatsapp logout
   ```

2. **重新启动服务**
   ```bash
   openclaw whatsapp restart
   ```

3. **扫描新二维码**
   ```bash
   openclaw whatsapp qr
   ```

## 高级配置

### 消息过滤

在配置文件中可以设置消息过滤规则：

```json
{
  "targets": [
    {
      "name": "工作群",
      "type": "group",
      "identifier": "1234567890-1234567890@g.us",
      "filters": {
        "only_unread": true,
        "exclude_media": false,
        "min_length": 3,
        "exclude_senders": ["+0987654321"]
      }
    }
  ]
}
```

### 批量处理配置

```json
{
  "monitoring": {
    "scan_interval_minutes": 5,
    "batch_size": 10,
    "max_age_hours": 24,
    "retry_attempts": 3,
    "retry_delay_seconds": 30
  }
}
```

## 性能优化

### 减少 API 调用

1. **增加扫描间隔**: 设置为 5-10 分钟
2. **使用批量处理**: 收集多条消息后一次性处理
3. **缓存消息 ID**: 避免重复处理相同消息

### 内存管理

1. **限制消息缓存**: 保留最近 1000 条消息
2. **定期清理**: 自动清理旧消息
3. **压缩存储**: 使用 gzip 压缩历史数据

## 安全注意事项

1. **保护凭证**: 不要提交 API 密钥到版本控制
2. **限制访问**: 仅允许可信 IP 访问 API
3. **数据加密**: 敏感数据应加密存储
4. **定期审计**: 检查日志和访问记录

## 监控和告警

### 健康检查

```bash
# 检查 WhatsApp 渠道状态
openclaw whatsapp status

# 测试消息发送
openclaw whatsapp send --to "+1234567890" --message "Test message"
```

### 告警配置

设置监控告警：

```yaml
# 当 WhatsApp 断开连接时告警
alerts:
  - name: "whatsapp_disconnected"
    condition: "whatsapp.status != 'connected'"
    channels: ["email", "slack"]
    message: "WhatsApp 连接断开，请检查设备配对"
```

## 更新和维护

### 更新 OpenClaw

```bash
# 更新 OpenClaw
openclaw update

# 重启服务
openclaw restart
```

### 备份配置

```bash
# 备份 WhatsApp 配置
openclaw config export --channel whatsapp > whatsapp_config_backup.yaml

# 恢复配置
openclaw config import --channel whatsapp < whatsapp_config_backup.yaml
```

## 支持资源

- OpenClaw 文档: https://docs.openclaw.ai
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- 飞书开放平台: https://open.feishu.cn
- 问题反馈: GitHub Issues 或 OpenClaw Discord