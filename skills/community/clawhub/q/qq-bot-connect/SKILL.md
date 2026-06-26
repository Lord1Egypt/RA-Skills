---
name: qqbot-connect
description: QQBot 消息主动推送技能。当需要向 QQ 用户或群发送消息时使用此技能。支持：(1) 主动发送消息到 QQ 对话框 (2) 发送图片/语音/文件等富媒体 (3) 群发消息。触发词：发送 QQ、推送 QQ、QQ 消息、发送到 QQ、QQ 发送。
---

# QQBot Connect

QQ 机器人消息推送技能。

## ⚠️ 首次使用必读

**配置文件位置：**
- `C:\Users\21115\.qclaw\skills\qqbot-connect\config.json`
- `E:\QClaw\skills\qqbot-connect\config.json`
（改成自己的位置）

**当前配置的 openid：**
```
openid: （修改成自己的openid）
type: c2c (私聊)
name: 主人
```

**发送格式：**
```
qqbot:c2c:4AFDDAB3E1ABB0B75D790C12B22086EF
```

## 核心规则

**必须使用 `message` 工具发送消息！**

### 消息发送格式

| 类型 | target 参数 | channel 参数 |
|------|-------------|-------------|
| 私聊 | `qqbot:c2c:{openid}` | `qqbot` |
| 群聊 | `qqbot:group:{groupid}` | `qqbot` |

### 发送文本消息

```json
{
  "action": "send",
  "channel": "qqbot",
  "target": "qqbot:c2c:4AFDDAB3E1ABB0B75D790C12B22086EF",
  "message": "要发送的消息内容"
}
```

### 发送富媒体

使用 `<qqmedia>` 标签：

```
<qqmedia>/path/to/image.jpg</qqmedia>
<qqmedia>/path/to/file.pdf</qqmedia>
```

支持的格式：
- 图片：`.jpg`, `.png`, `.gif`, `.webp`, `.bmp`
- 语音：`.silk`, `.wav`, `.mp3`, `.ogg`, `.aac`, `.flac`
- 视频：`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`
- 文件：其他扩展名

## 使用流程

1. **用户请求发送消息** → 如"发送 hello 到 QQ"
2. **读取 config.json** → 获取 openid
3. **拼接 target** → `qqbot:c2c:` + openid
4. **使用 message 工具发送**
5. **确认发送成功** → 返回结果给用户

## 配置文件格式

```json
{
  "_readme": "QQ-bot-connect 配置文件",
  "default": {
    "openid": "4AFDDAB3E1ABB0B75D790C12B22086EF",
    "type": "c2c",
    "name": "主人"
  },
  "_format": {
    "c2c_private": "qqbot:c2c:{openid}",
    "group": "qqbot:group:{groupid}"
  }
}
```

## 常见问题

### 如何知道用户的 openid？

在 OpenClaw 控制 UI 中：
1. 打开左侧 QQ 机器人对话面板
2. 查看对话标题栏显示的会话标识
3. 格式如：`qqbot:c2c:4AFDDAB3E1ABB0B75D790C12B22086EF`

### 发送失败怎么办？

1. 检查 target 格式是否正确（必须是 `qqbot:c2c:{openid}`）
2. 确保 openid 与当前对话匹配
3. 确认 QQ 机器人已正确配置

### 如何修改默认 openid？

编辑 `config.json` 中的 `default.openid` 字段。

### 如何发送给不同的 QQ 用户？

可以临时指定 openid：
- 用户说"发送 XX 到 123456789" → 使用 `qqbot:c2c:123456789`
- 用户说"发送 XX 到群 987654321" → 使用 `qqbot:group:987654321`
