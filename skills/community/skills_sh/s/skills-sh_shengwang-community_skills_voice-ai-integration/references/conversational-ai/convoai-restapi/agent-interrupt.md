---
title: "打断智能体"
description: "打断指定智能体说话或思考。"
---

# 打断智能体

`POST /v2/projects/{appid}/agents/{agentId}/interrupt`

打断指定智能体说话或思考。

## 请求体

Content-Type: `application/json`

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |

### 请求示例

<details>
<summary>Example 1</summary>

```json
{}
```
</details>

## 响应

### default

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
