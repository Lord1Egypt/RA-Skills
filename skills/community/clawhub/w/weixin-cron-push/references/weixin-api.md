# 微信插件 API 参考

## 插件信息

- 包名：`@tencent-weixin/openclaw-weixin`
- 插件 ID：`openclaw-weixin`
- 渠道：`openclaw-weixin`
- 后端：`https://ilinkai.weixin.qq.com`

## 安装与登录

```bash
# 一键安装
npx -y @tencent-weixin/openclaw-weixin-cli install

# 启用
openclaw config set plugins.entries.openclaw-weixin.enabled true

# 扫码登录
openclaw channels login --channel openclaw-weixin

# 重启生效
openclaw gateway restart
```

## 账号文件

登录凭证保存在 `~/.openclaw/openclaw-weixin/accounts/<id>-im-bot.json`：

```json
{
  "token": "<bot-token>",
  "baseUrl": "https://ilinkai.weixin.qq.com",
  "userId": "<user-id>@im.wechat"
}
```

## 后端 API

所有接口 `POST`，JSON 格式。

### 通用 Header

| Header | 值 |
|--------|------|
| `Content-Type` | `application/json` |
| `AuthorizationType` | `ilink_bot_token` |
| `Authorization` | `Bearer <token>` |
| `X-WECHAT-UIN` | 随机 uint32 的 base64 |

### sendMessage

发送消息给用户：

```json
{
  "msg": {
    "to_user_id": "<用户ID>",
    "context_token": "<上下文令牌>",
    "client_id": "<客户端ID>",
    "message_type": 2,
    "message_state": 2,
    "item_list": [
      { "type": 1, "text_item": { "text": "你好" } }
    ]
  }
}
```

MessageType: 1=USER, 2=BOT
MessageState: 0=NEW, 1=GENERATING, 2=FINISH
Item type: 1=TEXT, 2=IMAGE, 3=VOICE, 4=FILE, 5=VIDEO

### getUpdates

长轮询获取新消息：

```json
{
  "get_updates_buf": ""
}
```

### getConfig

获取账号配置（typing ticket 等）：

```json
{
  "ilink_user_id": "<用户ID>",
  "context_token": "<可选>"
}
```

### sendTyping

```json
{
  "ilink_user_id": "<用户ID>",
  "typing_ticket": "<ticket>",
  "status": 1
}
```

status: 1=正在输入, 2=取消

### getUploadUrl

获取 CDN 上传预签名参数（发图片/文件前调用）。

## CDN 上传流程

1. 计算文件明文大小和 MD5
2. AES-128-ECB 加密文件，计算密文大小
3. 调用 getUploadUrl 获取 upload_param
4. PUT 上传加密文件到 CDN
5. 用 encrypt_query_param 构造 CDNMedia 引用

## 消息结构 (WeixinMessage)

| 字段 | 类型 | 说明 |
|------|------|------|
| seq | number | 消息序列号 |
| message_id | number | 消息唯一 ID |
| from_user_id | string | 发送者 |
| to_user_id | string | 接收者 |
| create_time_ms | number | 时间戳(ms) |
| message_type | number | 1=USER, 2=BOT |
| message_state | number | 0/1/2 |
| item_list | MessageItem[] | 内容列表 |
| context_token | string | 回复时需回传 |

## 相关路径

- 插件目录：`~/.openclaw/extensions/openclaw-weixin/`
- 账号配置：`~/.openclaw/openclaw-weixin/accounts/`
- 源码：`~/.openclaw/extensions/openclaw-weixin/src/`
