---
title: "播报自定义消息"
description: "让指定智能体播报自定义消息。  与智能体对话期间，调用该接口可以让智能体使用 TTS 模块立刻播报自定义消息。智能体收到请求后，播报行为会打断当前说话和思考流程。"
---

# 播报自定义消息

`POST /v2/projects/{appid}/agents/{agentId}/speak`

让指定智能体播报自定义消息。

与智能体对话期间，调用该接口可以让智能体使用 TTS 模块立刻播报自定义消息。智能体收到请求后，播报行为会打断当前说话和思考流程。

## 请求体

Content-Type: `application/json`

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `text` | string | 是 | - | 播报的文本内容，最长不超过 512 字节 (bytes)。 |
| `priority` | string | 否 | - | 播报行为的优先级，支持设为以下值： - `"INTERRUPT"`：（默认）高优先级，打断并播报。智能体会终止当前交互，直接播报消息。 - `"APPEND"`: 中优先级，追加播报。智能体会在当前交互结束后播报消息。 - `"IGNORE"`: 低优先级，空闲时播报。如果此时智能体正在交互，智能体会直接忽略并丢弃要播报的消息；只有智能体不在交互中才会播报消息。 |
| `interruptable` | boolean | 否 | `true` | 是否允许用户说话打断智能体播报： - `true`：（默认）允许。 - `false`：不允许。 |

### 请求示例

<details>
<summary>Example 1</summary>

```json
{
  "text": "抱歉，对话内容不符合规范。",
  "priority": "INTERRUPT",
  "interruptable": false
}
```
</details>

## 响应

### 200

- 若返回的状态码为 `200` 则表示请求成功。响应包体为智能体信息，智能体开始播报指定内容。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `agent_id` | string | 否 | - | 对话式智能体 ID，即智能体唯一标识。 |
| `channel` | string | 否 | - | 智能体所在 RTC 频道名。 |
| `start_ts` | integer | 否 | - | 智能体创建时间戳。 |

**响应示例**

**Example 1**

```json
{
  "agent_id": "1NT29XxxxxxxxxELWEHC8OS",
  "channel": "test_channel",
  "start_ts": 1744877089
}
```
