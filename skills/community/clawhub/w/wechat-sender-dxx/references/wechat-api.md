# 微信发送 API 参考文档

## 接口端点

```
POST http://127.0.0.1:18789/api/wechat/send
```

## 请求头

| Header | 值 | 说明 |
|-------|---|------|
| Content-Type | application/json | 必须 |
| X-Requested-With | wechat-sender-skill | 标识来源 |

## 请求参数

### 基础结构

```json
{
  "channel": "openclaw-weixin",
  "recipient": {
    "type": "user|group",
    "name": "联系人备注名"
  },
  "message": {
    "type": "text|image|file",
    "content": "消息内容或文件路径"
  },
  "timestamp": 1701234567890
}
```

### 字段说明

#### recipient 对象

| 字段 | 类型 | 必需 | 说明 |
|-----|-----|-----|------|
| type | string | 是 | user=个人, group=群聊 |
| name | string | 是 | 微信中的备注名或昵称 |

#### message 对象

| 字段 | 类型 | 必需 | 说明 |
|-----|-----|-----|------|
| type | string | 是 | text=文字, image=图片, file=文件 |
| content | string | 是 | 文字内容或Base64编码的文件数据 |
| filename | string | 否 | 文件名（仅文件类型） |

## 响应格式

### 成功响应

```json
{
  "success": true,
  "messageId": "msg-abc123",
  "timestamp": 1701234567890,
  "recipient": {
    "type": "user",
    "name": "张三"
  }
}
```

### 错误响应

```json
{
  "success": false,
  "error": "联系人不存在",
  "error_code": "E002",
  "timestamp": 1701234567890
}
```

## 错误代码

| 代码 | 说明 | 解决方案 |
|-----|------|---------|
| E001 | 未登录微信 | 检查微信通道状态，重新扫码登录 |
| E002 | 联系人不存在 | 确认备注名正确，或先接收对方消息 |
| E003 | 频率限制 | 等待60秒后重试 |
| E004 | 消息内容违规 | 检查敏感词，修改内容后重试 |
| E005 | 文件不存在 | 检查文件路径是否正确 |
| E999 | 未知错误 | 查看详细错误信息或联系管理员 |

## 频率限制

| 类型 | 限制 | 说明 |
|-----|-----|------|
| 个人号 | 20条/分钟 | 超过会被临时限制 |
| 消息间隔 | 3秒 | 建议每条消息间隔至少3秒 |
| 每日上限 | 200条 | 避免被判定为营销号 |

## 使用示例

### 发送文字消息

```bash
curl -X POST http://127.0.0.1:18789/api/wechat/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "openclaw-weixin",
    "recipient": {
      "type": "user",
      "name": "张三"
    },
    "message": {
      "type": "text",
      "content": "你好，这是一条测试消息"
    }
  }'
```

### 发送图片

```bash
# 将图片转为base64
IMAGE_BASE64=$(base64 -w 0 /path/to/image.jpg)

curl -X POST http://127.0.0.1:18789/api/wechat/send \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"openclaw-weixin\",
    \"recipient\": {
      \"type\": \"user\",
      \"name\": \"张三\"
    },
    \"message\": {
      \"type\": \"image\",
      \"content\": \"${IMAGE_BASE64}\"
    }
  }"
```

### 发送到群聊

```bash
curl -X POST http://127.0.0.1:18789/api/wechat/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "openclaw-weixin",
    "recipient": {
      "type": "group",
      "name": "工作群"
    },
    "message": {
      "type": "text",
      "content": "大家好，群里通知一件事..."
    }
  }'
```

## 安全注意事项

1. **仅限已存在的聊天对象**
   - 首次发送前，需要先收到对方消息或手动发送过消息
   - 不支持发送给完全陌生的人

2. **内容审核**
   - 微信会自动审核消息内容
   - 敏感词、违规内容会被拦截

3. **防止滥用**
   - 批量发送大量消息可能导致账号被限制
   - 建议控制发送频率，模拟人工操作

4. **隐私保护**
   - 不要发送敏感个人信息
   - 授权文件(.auth.json)应妥善保管

## 技术实现说明

当前Skill使用模拟HTTP请求方式与OpenClaw Gateway通信。实际实现需要：

1. OpenClaw Gateway开放微信发送API
2. 微信客户端保持在线状态
3. 维护联系人会话映射关系

**注意**: 当前脚本为框架实现，实际发送功能需依赖OpenClaw Gateway的API支持。在Gateway未开放对应API前，脚本会以"模拟模式"运行。
