# 回复消息

## 注意事项

### 前提条件

- 应用需要开启[机器人能力](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-enable-bot-ability)。
- 回复用户消息（即单聊消息）时，用户需要在机器人的[可用范围](https://open.feishu.cn/document/home/introduction-to-scope-and-authorization/availability)内。
- 回复群消息时，机器人需要在群中，且拥有发言权限。

### 使用限制

为避免消息发送频繁对用户造成打扰，向同一用户发送消息的限频为 **5 QPS**、向同一群组发送消息的限频为群内机器人共享 **5 QPS**。

## 权限要求

### 必要权限

| 类型 | 名称 |
|------|------|
| 应用权限（开启任一即可） | 获取与发送单聊、群组消息 (im:message) |
| 应用权限（开启任一即可） | 以应用的身份发消息 (im:message:send_as_bot) |
| 应用权限（开启任一即可） | 发送消息V2 (im:message:send) |

#### 注意事项

1. **应用身份**发消息需申请下面三个权限之一：
   - 获取与发送单聊、群组消息（im:message）
   - 以应用的身份发消息（im:message:send_as_bot）
   - 发送消息V2【历史版本】（im:message:send）

2. **用户身份**发消息需同时申请以下两个权限：
   - 获取与发送单聊、群组消息（im:message）
   - 以用户身份发送消息（im:message.send_as_user）

### 可选权限

| 类型 | 名称 |
|------|------|
| - | - |

> **说明**：本接口无敏感字段权限要求。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/im/v1/messages/:message_id/reply` |
|----------|--------------------------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/reply) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token` 或 `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `message_id` | string | 是 | 待回复的消息的 ID。ID 获取方式：<br>- 调用发送消息接口后，从响应结果的 `message_id` 参数获取<br>- 监听接收消息事件，当触发该事件后可以从事件体内获取消息的 `message_id`<br>- 调用获取会话历史消息接口，从响应结果的 `message_id` 参数获取 |

### 请求体

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `content` | string | 是 | 消息内容，JSON 结构序列化后的字符串。该参数的取值与 `msg_type` 对应。<br>注意：<br>- JSON 字符串需进行转义<br>- 文本消息请求体最大不能超过 150 KB<br>- 卡片消息、富文本消息请求体最大不能超过 30 KB<br>- 如果使用卡片模板（template_id）发送消息，实际大小也包含模板对应的卡片数据大小 |
| `msg_type` | string | 是 | 消息类型。可选值：<br>- `text`：文本<br>- `post`：富文本<br>- `image`：图片<br>- `file`：文件<br>- `audio`：语音<br>- `media`：视频<br>- `sticker`：表情包<br>- `interactive`：卡片<br>- `share_chat`：分享群名片<br>- `share_user`：分享个人名片 |
| `reply_in_thread` | boolean | 否 | 是否以话题形式回复。取值为 true 时将以话题形式回复。<br>默认值：`false`<br>注意：如果要回复的消息已经是话题形式的消息，则默认以话题形式进行回复 |
| `uuid` | string | 否 | 自定义设置的唯一字符串序列，用于在回复消息时请求去重。不填则表示不去重。持有相同 uuid 的请求，在 1 小时内至多成功回复一条消息。<br>最大长度：50 字符 |

### 请求示例

#### cURL 请求示例

```bash
curl --location --request POST 'https://open.feishu.cn/open-apis/im/v1/messages/om_xxxxxx/reply' \
--header 'Authorization: Bearer t-xxxxxx' \
--header 'Content-Type: application/json; charset=utf-8' \
--data-raw '{
    "content": "{\"text\":\"test content\"}",
    "msg_type": "text",
    "uuid": "a0d69e20-1dd1-458b-k525-dfeca4015204"
}'
```

#### Python 请求示例

```python
import json
import requests

def reply(message_id):
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply"
    msg = "test content"
    msgContent = {
        "text": msg,
    }
    req = {
        "content": json.dumps(msgContent),
        "msg_type": "text",
        "uuid": "a0d69e20-1dd1-458b-k525-dfeca4015204"
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': 'Bearer xxx',  # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response

if __name__ == '__main__':
    reply("om_xxxxxx")
```

#### Go 请求示例

```go
import (
	"context"

	"github.com/larksuite/oapi-sdk-go/v3"
	"github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

func main() {
	// 创建 Client
	client := lark.NewClient("appID", "appSecret")

	// 创建请求对象
	req := larkim.NewReplyMessageReqBuilder().
		MessageId(`om_xxxxxx`).
		Content(`{"text":"test content"}`).
		MsgType(`text`).
		Uuid(`a0d69e20-1dd1-458b-k525-dfeca4015204`).
		Build()

	// 发起请求
	resp, err := client.Im.Message.Reply(context.Background(), req)
}
```

## 接口响应

### 响应头

| 名称 | 类型 | 描述 |
|------|------|------|
| - | - | 无额外响应头字段 |

### 响应体

| 字段 | 类型 | 描述 |
|------|------|------|
| `code` | int | 错误码，非 0 表示失败 |
| `msg` | string | 错误描述 |
| `data` | object | 响应数据 |
| `message_id` | string | 消息 ID。成功回复消息后，由系统生成的唯一 ID 标识 |
| `root_id` | string | 根消息 ID。在有多个回复的消息树中，`root_id` 为根消息的 `message_id` |
| `parent_id` | string | 父消息 ID。在有多个回复的消息树中，`parent_id` 为当前消息上一层的消息 `message_id` |
| `thread_id` | string | 消息所属的话题 ID（不返回说明该消息不是话题形式的消息） |
| `msg_type` | string | 消息类型 |
| `create_time` | string | 消息生成的时间戳。单位：毫秒 |
| `update_time` | string | 消息更新的时间戳。单位：毫秒 |
| `deleted` | boolean | 当前消息是否被撤回。回复消息时只会返回 false |
| `updated` | boolean | 当前消息是否被更新。回复消息时只会返回 false |
| `chat_id` | string | 消息所属的群 ID |
| `sender` | object | 当前消息的发送者信息 |
| `body` | object | 通过 `body` 内的 `content` 参数，返回当前的消息内容 |
| `mentions` | array | 发送的消息内，被 @ 的用户列表 |
| `upper_message_id` | string | 合并转发消息中，上一层级的消息 ID |

### 响应示例

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "message_id": "om_dc13264520392913993dd051dba21dcf",
        "root_id": "om_40eb06e7b84dc71c03e009ad3c754195",
        "parent_id": "om_d4be107c616aed9c1da8ed8068570a9f",
        "thread_id": "omt_d4be107c616a",
        "msg_type": "interactive",
        "create_time": "1615380573411",
        "update_time": "1615380573411",
        "deleted": false,
        "updated": false,
        "chat_id": "oc_5ad11d72b830411d72b836c20",
        "sender": {
            "id": "cli_9f427eec54ae901b",
            "id_type": "app_id",
            "sender_type": "app",
            "tenant_key": "736588c9260f175e"
        },
        "body": {
            "content": "{\"text\":\"@_user_1 test content\"}"
        },
        "mentions": [
            {
                "key": "@_user_1",
                "id": "ou_155184d1e73cbfb8973e5a9e698e74f2",
                "id_type": "open_id",
                "name": "Tom",
                "tenant_key": "736588c9260f175e"
            }
        ],
        "upper_message_id": "om_40eb06e7b84dc71c03e009ad3c754195"
    }
}
```

## 响应码定义

### 成功码

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 200 | 0 | 请求成功 |

### 客户端错误码 (4xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 400 | 230001 | Your request contains an invalid request parameter |
| 400 | 230002 | The bot can not be outside the group |
| 400 | 230006 | Bot ability is not activated |
| 400 | 230011 | The message is recalled |
| 400 | 230013 | Bot has NO availability to this user |
| 400 | 230015 | P2P chat can NOT be shared |
| 400 | 230017 | Bot is NOT the owner of the resource |
| 400 | 230018 | These operations are NOT allowed at current group settings |
| 400 | 230019 | The topic does NOT exist |
| 400 | 230020 | This operation triggers the frequency limit |
| 400 | 230022 | The content of the message contains sensitive information |
| 400 | 230025 | The length of the message content reaches its limit |
| 400 | 230027 | Lack of necessary permissions |
| 400 | 230028 | The messages do NOT pass the audit |
| 400 | 230035 | Send Message Permission deny |
| 400 | 230038 | Cross tenant p2p chat operate forbid |
| 400 | 230049 | The message is being sent |
| 400 | 230050 | The message is invisible to the operator |
| 400 | 230054 | This operation is not supported for this message type |
| 400 | 230055 | The type of file upload does not match the type of message being sent |
| 400 | 230071 | The group to which the message belongs does not support reply in thread |
| 400 | 230072 | Aggregated messages do not support reply in thread |
| 400 | 230075 | Sending encrypted messages is not supported |
| 400 | 230099 | Failed to create card content |
| 400 | 230111 | Action unavailable as the message will self-destruct soon |
| 400 | 232009 | Your request specifies a chat which has already been dissolved |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无 |

### 230099 子错误码

| 错误码 | 描述 |
|--------|------|
| 100290 | Failed to create card content, ext=ErrCode: 100290; ErrMsg: There is an invalid user resource(at/person) in your card |
| 200380 | Failed to create card content, ext=ErrCode: 200380; ErrMsg: template does not exist |
| 200381 | Failed to create card content, ext=ErrCode: 200381; ErrMsg: template is not visible to app |
| 200621 | Failed to create card content, ext=ErrCode: 200621; ErrMsg: parse card json err |
| 200732 | Failed to create card content, ext=ErrCode: 200732; ErrMsg: the actual type of the variable is inconsistent |
| 200550 | Failed to create card content, ext=ErrCode: 200550; ErrMsg: chart spec is invalid |
| 200861 | Failed to create card content, ext=ErrCode: 200861; ErrMsg: cards of schema V2 no longer support this capability |
| 200570 | Failed to create card content, ext=ErrCode: 200570; ErrMsg: card contains invalid image keys |
| 200914 | Failed to create card content, ext=ErrCode: 200914; ErrMsg: table rows is invalid |
| 200915 | Failed to create card content, ext=ErrCode: 200915; ErrMsg: table rows name is invalid |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 发送消息内容 | [发送消息内容结构](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json) |
| 机器人权限配置 | [应用权限配置](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 消息管理概述 | [消息管理概述](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/intro) |
| 话题概述 | [话题概述](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/thread-introduction) |
| 通用错误码 | [服务端通用错误码](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |