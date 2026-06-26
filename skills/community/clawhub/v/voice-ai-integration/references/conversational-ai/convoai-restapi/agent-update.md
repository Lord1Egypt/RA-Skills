---
title: "更新智能体配置"
description: "更新指定运行中智能体的部分参数配置。"
---

# 更新智能体配置

`POST /v2/projects/{appid}/agents/{agentId}/update`

更新指定运行中智能体的部分参数配置。

## 鉴权

任选其一：
- RTC Token：`Authorization: agora token="{RTC_TOKEN}"`
- Basic Auth：`Authorization: Basic base64("{SHENGWANG_CUSTOMER_KEY}:{SHENGWANG_CUSTOMER_SECRET}")`

## 参数

| 名称 | 位置 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `appid` | path | string | 是 | - | 你的项目使用的 [App ID](http://doc.shengwang.cn/doc/convoai/restful/get-started/enable-service#%E8%8E%B7%E5%8F%96-app-id)。 |
| `agentId` | path | string | 是 | - | 智能体实例 ID，即智能体的唯一标识。调用 [POST 创建对话式智能体](https://doc.shengwang.cn/doc/convoai/restful/convoai/operations/start-agent) 成功后在响应包体中获取。 |

## 请求体

Content-Type: `application/json`

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `properties` | object | 否 | - | - |
| &nbsp;&nbsp;`properties.token` | string | 否 | - | 用于鉴权的动态密钥（Token）。如果你的项目已启用 App 证书，则务必在该字段中传入你项目的动态密钥。详见[使用 Token 鉴权](https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication)。 |
| &nbsp;&nbsp;`properties.llm` | object | 否 | - | 大语言模型 (LLM) 设置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.system_messages` | object[] | 否 | - | 一组每次调用 LLM 时被附加在最前的预定义信息，用于控制 LLM 输出。可以是角色设定、提示词和回答样例等。要求与 OpenAI 协议兼容。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.params` | object | 否 | - | 在消息体内传输的 LLM 附加信息，例如使用的模型、最大 Token 数限制等。不同的 LLM 供应商支持的配置不同，请参考对应文档按需填入。 &gt; 该字段更新后将覆盖智能体创建时的配置。更新时，请确保传入完整的 `params` 字段。 |

### 请求示例

<details>
<summary>Example 1</summary>

```json
{
  "properties": {
    "token": "007eJxTYxxxxxxxxxxIaHMLAAAA0ex66",
    "llm": {
      "system_messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant. xxx"
        },
        {
          "role": "system",
          "content": "Previously, user has talked about their favorite hobbies with some key topics: xxx"
        }
      ],
      "params": {
        "model": "abab6.5s-chat",
        "max_token": 1024
      }
    }
  }
}
```
</details>

## 响应

### 200

- 若返回的状态码为 `200` 则表示请求成功。响应包体中包含本次请求的结果。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `agent_id` | string | 否 | - | 智能体唯一标识符。 |
| `create_ts` | integer | 否 | - | 智能体创建时间戳。 |
| `state` | string | 否 | - | 智能体运行状态： - `IDLE` (0)：空闲状态的智能体。 - `STARTING` (1)：正在启动的智能体。 - `RUNNING` (2)：正在运行的智能体。 - `STOPPING` (3)：正在停止的智能体。 - `STOPPED` (4)：已完成退出的智能体。 - `RECOVERING` (5)：正在恢复的智能体。 - `FAILED` (6)：执行失败的智能体。 |

**响应示例**

**Example 1**

```json
{
  "agent_id": "1NT29XOXFT4Jxxxx410TXRCFG10HI00",
  "create_ts": 173836896,
  "state": "RUNNING"
}
```

## 服务器

- `https://api.agora.io/cn/api/conversational-ai-agent`
