---
title: "查询智能体状态"
description: "查询指定智能体实例的当前运行状态。"
---

# 查询智能体状态

`GET /v2/projects/{appid}/agents/{agentId}`

查询指定智能体实例的当前运行状态。

## 鉴权

任选其一：
- RTC Token：`Authorization: agora token="{RTC_TOKEN}"`
- Basic Auth：`Authorization: Basic base64("{SHENGWANG_CUSTOMER_KEY}:{SHENGWANG_CUSTOMER_SECRET}")`

## 参数

| 名称 | 位置 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `appid` | path | string | 是 | - | 你的项目使用的 [App ID](http://doc.shengwang.cn/doc/convoai/restful/get-started/enable-service#%E8%8E%B7%E5%8F%96-app-id)。 |
| `agentId` | path | string | 是 | - | 智能体实例 ID，即智能体的唯一标识。调用 [POST 创建对话式智能体](https://doc.shengwang.cn/doc/convoai/restful/convoai/operations/start-agent) 成功后在响应包体中获取。 |

## 响应

### 200

- 若返回的状态码为 `200` 则表示请求成功。响应包体中包含本次请求的结果。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `message` | string | 否 | - | 请求信息。 |
| `start_ts` | integer | 否 | - | 智能体创建时间戳。 |
| `stop_ts` | integer | 否 | - | 智能体停止时间戳。 |
| `status` | string | 否 | - | 智能体运行状态： - `IDLE` (0)：空闲状态的智能体。 - `STARTING` (1)：正在启动的智能体。 - `RUNNING` (2)：正在运行的智能体。 - `STOPPING` (3)：正在停止的智能体。 - `STOPPED` (4)：已完成退出的智能体。 - `RECOVERING` (5)：正在恢复的智能体。 - `FAILED` (6)：执行失败的智能体。 |
| `agent_id` | string | 否 | - | 智能体唯一标识。 |

**响应示例**

**Example 1**

```json
{
  "message": "agent exits with reason: xxxx",
  "start_ts": 1735035893,
  "stop_ts": 1735035900,
  "status": "FAILED",
  "agent_id": "1NT29X11GQSxxxxxNU80BEIN56XF"
}
```

## 服务器

- `https://api.agora.io/cn/api/conversational-ai-agent`
