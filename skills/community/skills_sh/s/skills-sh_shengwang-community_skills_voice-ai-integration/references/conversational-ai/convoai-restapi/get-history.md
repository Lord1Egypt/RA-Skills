---
title: "获取智能体短期记忆"
description: "获取用户和智能体对话的短期记忆。 你可以在智能体运行期间 (`RUNNING`) 调用该 API 获取智能体创建到现在储存的短期记忆信息，包括： - 智能体创建和停止的时间戳 - 用户和智能体对话消息"
---

# 获取智能体短期记忆

`GET /v2/projects/{appid}/agents/{agentId}/history`

获取用户和智能体对话的短期记忆。
你可以在智能体运行期间 (`RUNNING`) 调用该 API 获取智能体创建到现在储存的短期记忆信息，包括：
- 智能体创建和停止的时间戳
- 用户和智能体对话消息

## 响应

### default

- 若返回的状态码为 `200` 则表示请求成功。响应包体中包含本次请求的结果。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `agent_id` | string | 否 | - | 智能体唯一标识。 |
| `start_ts` | integer | 否 | - | 智能体创建时间戳。 |
| `status` | string | 否 | - | 智能体运行状态。仅支持查询状态为 `RUNNING` (2)，即正在运行的智能体。 |
| `contents` | object[] | 否 | - | 智能体短期记忆。 |
| &nbsp;&nbsp;`contents[].role` | string | 否 | - | 消息发送者。可能为以下值： - `user`：用户。 - `assistant`：智能体。 |
| &nbsp;&nbsp;`contents[].content` | string | 否 | - | 消息内容。 |

**响应示例**

**Example 1**

```json
{
  "agent_id": "xxxx",
  "start_ts": 123,
  "status": "RUNNING",
  "contents": [
    {
      "role": "user",
      "content": "hello."
    },
    {
      "role": "assistant",
      "content": "hi, how can I help you?"
    }
  ]
}
```
