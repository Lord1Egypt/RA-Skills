---
title: "获取智能体列表"
description: "检索符合指定条件的智能体列表。"
---

# 获取智能体列表

`GET /v2/projects/{appid}/agents`

检索符合指定条件的智能体列表。

## 鉴权

任选其一：
- RTC Token：`Authorization: agora token="{RTC_TOKEN}"`
- Basic Auth：`Authorization: Basic base64("{SHENGWANG_CUSTOMER_KEY}:{SHENGWANG_CUSTOMER_SECRET}")`

## 参数

| 名称 | 位置 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `appid` | path | string | 是 | - | 你的项目使用的 [App ID](http://doc.shengwang.cn/doc/convoai/restful/get-started/enable-service#%E8%8E%B7%E5%8F%96-app-id)。 |
| `channel` | query | string | 否 | - | 查询指定频道名下的智能体列表。 |
| `from_time` | query | integer | 否 | - | 查询列表开始时间戳 (s)，默认为 1 天前。 |
| `to_time` | query | integer | 否 | - | 查询列表结束时间戳 (s)，默认为当前时刻。 |
| `state` | query | string | 否 | `2` | 指定需要查询智能体的状态，单次查询不支持指定多种状态：&lt;li&gt;`IDLE` (0)：空闲状态的智能体。&lt;/li&gt;&lt;li&gt;`STARTING` (1)：正在启动的智能体。&lt;/li&gt;&lt;li&gt;`RUNNING` (2)：正在运行的智能体。&lt;/li&gt;&lt;li&gt;`STOPPING` (3)：正在停止的智能体。&lt;/li&gt;&lt;li&gt;`STOPPED` (4)：已完成退出的智能体。&lt;/li&gt;&lt;li&gt;`RECOVERING` (5)：正在恢复的智能体。&lt;/li&gt;&lt;li&gt;`FAILED` (6)：执行失败的智能体。&lt;/li&gt; |
| `limit` | query | integer | 否 | `20` | 分页获取单次返回的最大条数。 |
| `cursor` | query | string | 否 | - | 分页游标，即分页起始位置的 `agent_id`。 |

## 响应

### 200

- 若返回的状态码为 `200` 则表示请求成功。响应包体中包含本次请求的结果。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `data` | object | 否 | - | - |
| &nbsp;&nbsp;`data.count` | integer | 否 | - | 本次返回的智能体数量。 |
| &nbsp;&nbsp;`data.list` | object[] | 否 | - | 满足条件的智能体列表。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`data.list[].start_ts` | integer | 否 | - | 智能体创建时间戳。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`data.list[].status` | string | 否 | - | 智能体运行状态： - `IDLE` (0)：空闲状态的智能体。 - `STARTING` (1)：正在启动的智能体。 - `RUNNING` (2)：正在运行的智能体。 - `STOPPING` (3)：正在停止的智能体。 - `STOPPED` (4)：已完成退出的智能体。 - `RECOVERING` (5)：正在恢复的智能体。 - `FAILED` (6)：执行失败的智能体。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`data.list[].agent_id` | string | 否 | - | 智能体唯一标识。 |
| `meta` | object | 否 | - | 返回列表的元信息。 |
| &nbsp;&nbsp;`meta.cursor` | string | 否 | - | 分页游标。 |
| &nbsp;&nbsp;`meta.total` | integer | 否 | - | 满足本次查询条件的智能体总数量。 |
| `status` | string | 否 | - | 请求状态。 |

**响应示例**

**Example 1**

```json
{
  "data": {
    "count": 1,
    "list": [
      {
        "start_ts": 1735035893,
        "status": "RUNNING",
        "agent_id": "1NT29X11GQSxxxxx80BEIN56XF"
      }
    ]
  },
  "meta": {
    "cursor": "",
    "total": 1
  },
  "status": "ok"
}
```

## 服务器

- `https://api.agora.io/cn/api/conversational-ai-agent`
