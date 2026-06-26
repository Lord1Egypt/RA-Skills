# 发送消息

## 注意事项

### 前提条件

- 应用需要开启[机器人能力](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-enable-bot-ability)。开启能力后需要发布版本才能生效，参考 [发布应用](https://open.feishu.cn/document/home/introduction-to-custom-app-development/self-built-application-development-process#baf09c7d)。
- 给用户发送消息时，用户需要在机器人的[可用范围](https://open.feishu.cn/document/home/introduction-to-scope-and-authorization/availability)内。
- 给群组发送消息时，机器人需要在该群组中，且在群组内拥有发言权限。

### 使用限制

- 为避免消息发送频繁对用户造成打扰，向同一用户发送消息的限频为 **5 QPS**、向同一群组发送消息的限频为群内机器人共享 **5 QPS**。
- 该接口仅支持在开发者后台创建的应用机器人调用，群自定义机器人无法调用该接口。了解群自定义机器人的使用方式，参见[自定义机器人使用指南](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)。

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
| 字段权限（敏感字段） | 获取用户 user ID (contact:user.employee_id:readonly) |

> **说明**：敏感字段仅在开启对应权限后才会返回；如无需获取这些字段，不建议申请。

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/im/v1/messages` |
|----------|---------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | 1000 次/分钟、50 次/秒 |
| 支持的应用类型 | Custom App、Store App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Authorization` | string | 是 | `tenant_access_token` 或 `user_access_token`<br>值格式："Bearer `access_token`"<br>示例值："Bearer u-7f1bcd13fc57d46bac21793a18e560"<br>**了解更多**：[如何选择与获取 access token](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-choose-which-type-of-token-to-use) |
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `receive_id_type` | string | 是 | 消息接收者 ID 类型。支持 open_id/union_id/user_id/email/chat_id<br>可选值：<br>- `open_id`：标识一个用户在某个应用中的身份<br>- `union_id`：标识一个用户在某个应用开发商下的身份<br>- `user_id`：标识一个用户在某个租户内的身份<br>- `email`：以用户的真实邮箱来标识用户<br>- `chat_id`：以群 ID 来标识群聊<br>**权限要求**：当值为 `user_id` 时，需要获取用户 user ID (contact:user.employee_id:readonly) |

### 请求体

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `receive_id` | string | 是 | 消息接收者的 ID，ID 类型与查询参数 `receive_id_type` 的取值一致。<br>说明：<br>- 给用户发送消息时，用户需要在机器人的可用范围内<br>- 给群组发送消息时，机器人需要在该群组中，且在群组内拥有发言权限<br>- 如果消息接收者为用户，推荐使用用户的 `open_id` |
| `msg_type` | string | 是 | 消息类型。可选值：<br>- `text`：文本<br>- `post`：富文本<br>- `image`：图片<br>- `file`：文件<br>- `audio`：语音<br>- `media`：视频<br>- `sticker`：表情包<br>- `interactive`：卡片<br>- `share_chat`：分享群名片（被分享的群名片有效期为 7 天）<br>- `share_user`：分享个人名片<br>- `system`：系统消息 |
| `content` | string | 是 | 消息内容，JSON 结构序列化后的字符串。该参数的取值与 `msg_type` 对应。<br>注意：<br>- JSON 字符串需进行转义<br>- 文本消息请求体最大不能超过 150 KB<br>- 卡片消息、富文本消息请求体最大不能超过 30 KB<br>- 如果使用卡片模板（template_id）发送消息，实际大小也包含模板对应的卡片数据大小 |
| `uuid` | string | 否 | 自定义设置的唯一字符串序列，用于在发送消息时请求去重。持有相同 uuid 的请求，在 1 小时内至多成功发送一条消息。<br>最大长度：50 字符 |

### 请求示例

#### cURL 请求示例

```bash
curl --location --request POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
--header 'Authorization: Bearer t-XXX' \
--header 'Content-Type: application/json; charset=utf-8' \
--data-raw '{
    "receive_id": "oc_84983ff6516d731e5b5f68d4ea2e1da5",
    "msg_type": "text",
    "content": "{\"text\":\"test content\"}"
}'
```

#### Python 请求示例

```python
import json
import requests

def send():
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type":"chat_id"}
    msg = "text content"
    msgContent = {
        "text": msg,
    }
    req = {
        "receive_id": "oc_xxx",  # chat id
        "msg_type": "text",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': 'Bearer xxx',  # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response

if __name__ == '__main__':
    send()
```

#### Go 请求示例

请参考[机器人自动拉群报警教程（含 Go 示例代码）](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-development-tutorial/determine-the-api-and-event-to-call)

#### 发送卡片请求示例

```json
{
  "receive_id": "ou_7d8a6e6df7621556ce0d21922b676706ccs",
  "msg_type": "interactive",
  "content": "{\"elements\":[{\"tag\":\"markdown\",\"content\":\"普通文本\\n\\n <at id=\\\"ou_cf986xxxx\\\"></at> <at id=\\\"ou_cf986xxxx\\\"></at> <at email=\\\"xxxx@example.com\\\"></at> <at id=\\\"all\\\"></at>\"}]}"
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
| `message_id` | string | 消息 ID。成功发送消息后，由系统生成的唯一 ID 标识 |
| `root_id` | string | 根消息 ID，仅在回复消息场景会有返回值 |
| `parent_id` | string | 父消息 ID，仅在回复消息场景会有返回值 |
| `thread_id` | string | 消息所属的话题 ID，仅在话题场景会有返回值 |
| `msg_type` | string | 消息类型 |
| `create_time` | string | 消息生成的时间戳。单位：毫秒 |
| `update_time` | string | 消息更新的时间戳。单位：毫秒 |
| `deleted` | boolean | 消息是否被撤回。发送消息时只会返回 false |
| `updated` | boolean | 消息是否被更新。发送消息时只会返回 false |
| `chat_id` | string | 消息所属的群 ID |
| `sender` | object | 消息的发送者信息 |
| `body` | object | 消息内容 |
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
| 400 | 230029 | User has resigned |
| 400 | 230034 | The receive_id is invalid |
| 400 | 230035 | Send Message Permission deny |
| 400 | 230036 | Tenant crypt key has been deleted |
| 400 | 230038 | Cross tenant p2p chat operate forbid |
| 400 | 230049 | The message is being sent |
| 400 | 230053 | The user has stopped the bot from sending messages |
| 400 | 230054 | This type of message is unavailable in the connection group |
| 400 | 230055 | The type of file upload does not match the type of message being sent |
| 400 | 230075 | Sending encrypted messages is not supported |
| 400 | 230099 | Failed to create card content |
| 400 | 232009 | Your request specifies a chat which has already been dissolved |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无 |

### 230099 子错误码

| 错误码 | 描述 |
|--------|------|
| 100290 | Failed to create card content, ext=ErrCode: 100290; ErrMsg: There is an invalid user resource(at/person) in your card |
| 11310 | Failed to create card content, ext=ErrCode: 11310; ErrMsg: %v; code:230099 |
| 200380 | Failed to create card content, ext=ErrCode: 200380; ErrMsg: template does not exist |
| 200381 | Failed to create card content, ext=ErrCode: 200381; ErrMsg: template is not visible to app |
| 200621 | Failed to create card content, ext=ErrCode: 200621; ErrMsg: parse card json err |
| 200732 | Failed to create card content, ext=ErrCode: 200732; ErrMsg: the actual type of the variable is inconsistent |
| 200737 | Failed to create card content, ext=ErrCode: 200737; ErrMsg: the format of the variable is incorrect |
| 200550 | Failed to create card content, ext=ErrCode: 200550; ErrMsg: chart spec is invalid |
| 200861 | Failed to create card content, ext=ErrCode: 200861; ErrMsg: cards of schema V2 no longer support this capability |
| 200570 | Failed to create card content, ext=ErrCode: 200570; ErrMsg: card contains invalid image keys |
| 200914 | Failed to create card content, ext=ErrCode: 200914; ErrMsg: table rows is invalid |
| 200915 | Failed to create card content, ext=ErrCode: 200915; ErrMsg: table rows name is invalid |
| 300240 | Failed to create card content, ext=ErrCode: 300240; ErrMsg: This application cannot retrieve audio information |
| 300230 | Failed to create card content, ext=ErrCode: 300230; ErrMsg: duplicate audio id |
| 300220 | Failed to create card content, ext=ErrCode: 300220; ErrMsg: audio elem don't support forward |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 发送消息内容 | [发送消息内容结构](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json) |
| 机器人权限配置 | [应用权限配置](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) |
| 用户相关的 ID 概念 | [用户身份介绍](https://open.feishu.cn/document/home/user-identity-introduction/introduction) |
| 权限范围校验 | [权限范围资源介绍](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) |
| 通用错误码 | [服务端通用错误码](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |