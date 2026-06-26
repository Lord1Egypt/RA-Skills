# ilink 协议关键点（踩坑笔记）

> 时间：2026-06-07
> 来源：OpenClaw 微信插件源码 + 实测

## 1. X-WECHAT-UIN 不是 session ID

源码明确：
```js
/** X-WECHAT-UIN header: random uint32 -> decimal string -> base64. */
function randomWechatUin() {
    const uint32 = crypto.randomBytes(4).readUInt32BE(0);
    return Buffer.from(String(uint32), "utf-8").toString("base64");
}
```

**每次都重新生成，零复用逻辑。** 它的设计目的：让 ilink 服务端**确认这不是重放请求**。

**误区**：用户（和早期我）以为"X-WECHAT-UIN 是某种 session"——其实它就是反重放噪点。

## 2. errcode -14 = SESSION_EXPIRED

源码：
```js
export const SESSION_EXPIRED_ERRCODE = -14;
```

**触发后果**：整个 bot 暂停 1 小时。源码：
```js
const SESSION_PAUSE_DURATION_MS = 60 * 60 * 1000;
```

**温柔的踢出** —— 给机会自愈，不是永久封号。

## 3. 业务层 vs HTTP 层

ilink 返的业务响应长这样：
```json
{"errcode":-14, "errmsg":"session timeout"}  ← 业务层失败但 HTTP 200
{}                                                  ← 空（某些场景）
{"ret":-2}                                         ← 业务层失败
```

**HTTP 200 ≠ 成功。必须看 `errcode` / `ret` 字段。**

## 4. sendmessage 必填字段

```json
{
  "msg": {
    "from_user_id": "",             // 留空
    "to_user_id": "<openid>",       // 含 @im.wechat 后缀
    "client_id": "<唯一 ID>",        // 每次推必须新
    "message_type": 2,              // 整数！
    "message_state": 2,             // 整数！
    "item_list": [{
      "type": 1,                    // 整数！
      "text_item": {"text": "..."}
    }],
    "context_token": "<可选>"
  },
  "base_info": {"channel_version": "2.4.4"}
}
```

**坑**：`message_type` / `message_state` / `item_list[].type` 必须是**整数**，不是字符串。

## 5. 必填请求头

```
Content-Type: application/json
AuthorizationType: ilink_bot_token
Authorization: Bearer <bot_token>
iLink-App-Id: <package.json ilink_appid>     = "bot"
iLink-App-ClientVersion: <uint32>             = "132100" (version 2.4.4)
X-WECHAT-UIN: <base64(随机 uint32)>          ← 每次新
```

`iLink-App-Id` 和 `iLink-App-ClientVersion` 来自：
- `package.json` 的 `ilink_appid` 字段
- `package.json` 的 `version` 字段 → `buildClientVersion()` 算法：`(major<<16)|(minor<<8)|patch`

## 6. 裸 curl ilink 在 macOS 上为什么 99% 不通

实测：
- `sendmessage` 裸 curl → **HTTP 000**（连接都建不上）
- `getupdates` 裸 curl → **HTTP 000** 或 server close

**根因（推测）**：
1. macOS 系统代理（`HTTPS_PROXY=127.0.0.1:6478`）干扰
2. ilink 服务端对**非 OpenClaw 内部连接**有反爬检测
3. CGN / 防火墙

**唯一可靠通路**：OpenClaw 插件内部维护的 **getupdates 长连接**反向投递。

## 7. openid 怎么拿

3 个方法：
1. 推送一次后看 ilink 返回（如果有 mirror）
2. OpenClaw 微信插件的 sync.json base64 解码
3. `~/.openclaw/openclaw-weixin/accounts/<id>-im-bot.context-tokens.json` 的 key
