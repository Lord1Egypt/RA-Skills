---
name: wechat-sender
description: 通过OpenClaw微信通道主动发送消息。Use when: (1) 用户要求发送微信消息, (2) 需要主动推送微信通知, (3) 定时发送微信消息, (4) 批量发送微信消息。支持文字、图片、文件等多种消息类型。
---

# WeChat Sender Skill

通过OpenClaw的`openclaw-weixin`通道主动发送微信消息。

## 工作原理

本Skill利用OpenClaw Gateway与微信客户端的WebSocket连接，通过发送特定格式的消息包实现主动推送。

## 前置条件

1. **OpenClaw Gateway已运行**
   ```bash
   openclaw gateway status
   ```

2. **微信通道已配置**
   - `openclaw-weixin` 插件已启用
   - 微信客户端已扫码登录

3. **目标联系人已存在聊天记录**
   - 首次使用前需先收到对方消息或手动发送过消息

## 使用方法

### 发送文字消息

```python
# 使用脚本发送
python3 scripts/send_message.py --to "联系人备注名" --text "消息内容"

# 示例
python3 scripts/send_message.py --to "张三" --text "你好，这是一条测试消息"
```

### 发送图片

```python
python3 scripts/send_message.py --to "联系人备注名" --image "/path/to/image.jpg"
```

### 发送文件

```python
python3 scripts/send_message.py --to "联系人备注名" --file "/path/to/document.pdf"
```

## 安全限制

| 限制项 | 说明 |
|-------|------|
| **联系人白名单** | 只能发送给已存在的聊天对象 |
| **频率限制** | 个人号20条/分钟，超过会被限制 |
| **内容审核** | 敏感词会被拦截 |
| **用户确认** | 首次使用需用户显式授权 |

## API参考

### 发送消息接口

```python
POST http://127.0.0.1:18789/api/wechat/send
Content-Type: application/json

{
  "channel": "openclaw-weixin",
  "recipient": {
    "type": "user",  // user | group
    "name": "联系人备注名"
  },
  "message": {
    "type": "text",  // text | image | file
    "content": "消息内容"
  }
}
```

### 响应格式

```json
{
  "success": true,
  "messageId": "msg-xxx",
  "timestamp": 1701234567890
}
```

## 错误处理

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| `E001` | 未登录微信 | 检查微信通道状态 |
| `E002` | 联系人不存在 | 确认备注名正确，或先接收对方消息 |
| `E003` | 频率限制 | 等待60秒后重试 |
| `E004` | 消息内容违规 | 检查敏感词 |

## 脚本说明

- `scripts/send_message.py` - 发送消息主脚本
- `scripts/contact_manager.py` - 联系人管理
- `scripts/auth_helper.py` - 授权验证

## 相关文档

- `references/wechat-api.md` - 微信API详细说明
- `references/rate-limits.md` - 频率限制详情
