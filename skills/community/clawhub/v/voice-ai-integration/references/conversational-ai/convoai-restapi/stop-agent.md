---
title: "停止对话式智能体"
description: "停止指定的对话式智能体实例，并让智能体退出 RTC 频道。"
---

# 停止对话式智能体

`POST /v2/projects/{appid}/agents/{agentId}/leave`

停止指定的对话式智能体实例，并让智能体退出 RTC 频道。

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

- 若返回的状态码为 `200` 则表示请求成功。响应包体为空。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

## 服务器

- `https://api.agora.io/cn/api/conversational-ai-agent`
