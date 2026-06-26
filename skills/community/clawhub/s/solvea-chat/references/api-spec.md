# Solvea Chat API Spec

## POST /bot/{botId}/chat

向指定机器人发送消息，获取 AI 客服回复。

### 认证

```
X-Token: <SOLVEA_API_KEY>
```

### Path 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| botId | Long | 机器人 ID，从环境变量 SOLVEA_BOT_ID 读取 |

### Request Body（精简版）

```json
{
  "chatId": "会话ID，相同ID视为同一会话",
  "message": "用户消息内容"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| chatId | string | 否 | 不填则系统自动生成。**传相同 chatId 可保持多轮对话上下文** |
| message | string | 是 | 本轮用户消息 |

### Response Body

```json
{
  "chatId": "A1B2C3D4E5F6",
  "type": "MESSAGE",
  "content": "AI 回复内容",
  "handoff": false,
  "inWorkHour": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| chatId | string | 会话 ID，**下次调用需传回此值以保持上下文** |
| type | string | `MESSAGE`=正常回复；`CONFUSED`=无法处理；`TO_AGENT`=转人工；`NOTHING`=无操作 |
| content | string | AI 回复内容，type 为 MESSAGE 时有值 |
| handoff | boolean | 是否需要转人工 |

### 错误码

| HTTP | 说明 |
|------|------|
| 400 | 参数错误 |
| 401 | X-Token 无效 |
| 404 | botId 不存在 |
