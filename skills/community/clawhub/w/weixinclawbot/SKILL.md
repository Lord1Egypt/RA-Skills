---
name: weixinclaw-proactive-push
description: 通过 WorkBuddy 已连接的 ClawBot 微信 bot 通道（weixinClawBot / ilink bot，非微信客服号）主动向老板微信推送文本/图片/文件/视频。当用户要求"通过 ClawBot 主动推送/给老板发微信/微信主动推送测试/微信独立消息/发图片给老板/发文件给老板"时使用。协议严格对齐腾讯官方插件 @tencent-weixin/openclaw-weixin@2.4.6（src/api + src/messaging + src/cdn）。
---

> 📦 **本 skill 源码仓库**：https://github.com/NoahEleven/weixinclaw-proactive-push （公开，欢迎 clone / 提 Issue）
>
> 🔒 **隐私红线（务必遵守）**：本 skill 运行时**只读本机凭据、不写出任何密钥、日志不打印 token 明文**。
> 分享 / 备份 / 提交时，**严禁**携带以下文件（含 bot 完整凭证 / 老板微信 id）：
> - `~/.workbuddy/settings.json`（含完整 `botToken`、`userId`）
> - `~/.workbuddy/claw-state/weixin/`（cursor 游标内含 bot 凭证镜像 `get_updates_buf`）
> 本仓库**只含 `SKILL.md` + `send.js`**，接收方用自己的 `settings.json` 即可，无需你提供任何密钥。

# 微信(ClawBot)主动推送（weixinClawBot / ilink bot）

## 背景
WorkBuddy 迁移自 OpenClaw。微信主动推送能力其实**一直活着**，藏在
`~/.workbuddy/settings.json` 的 `claw/users/<uid>/channels/weixinClawBot` 里——
它是 ClawBot 的微信 bot 通道（ilink bot，polling 模式），对接 `https://ilinkai.weixin.qq.com`。

> ⚠️ **这不是微信客服号**：微信客服号走公众平台客服消息 API（48 小时会话限制），
> 而本通道是 WorkBuddy / ClawBot 内置的 bot 通道，走 ilink bot API，可随时主动推送，不受客服号限制。

协议实现**严格对齐腾讯官方插件 `@tencent-weixin/openclaw-weixin@2.4.6`**
（npm 包，含 `src/api/api.ts`、`src/api/types.ts`、`src/messaging/*`、`src/cdn/*`）。
关键常量、请求头、item 结构、AES 加密、错误码检查均与官方保持一致。

> ⚠️ `openclaw-weixin-cli` 不需要装（那是 OpenClaw 的通道安装器，对 WorkBuddy 无用）。

## 何时用
- "通过 ClawBot 主动推一条消息给老板"（文本默认空 context_token，无需激活；详见下方机制专节）
- "微信主动推送测试""给老板发条微信 bot 消息"
- "发张图/发个文件/发段视频给老板"（context_token 自动读取，详见机制专节）
- 定时任务把结果主动推到老板微信（ClawBot bot 消息，非对话气泡）

## 怎么跑
脚本自动读 `settings.json` 取凭据与收件人，向老板微信发消息：

```bash
NODE="C:/Users/<USER>/.workbuddy/binaries/node/versions/22.22.2/node.exe"   # 将 <USER> 换成你的 Windows 用户名
SKILL="C:/Users/<USER>/.workbuddy/skills/weixinclaw-proactive-push/send.js"  # ⚠️ 必须指到 send.js；只传目录会 MODULE_NOT_FOUND（无 package.json main）

# 文本（默认空 context_token，无需激活；详见下方机制专节）
"$NODE" "$SKILL" "🦐 你的消息内容"

# 从文件读长文本
"$NODE" "$SKILL" --text-file 内容.txt

# 图片 + 可选说明（context_token 自动读取）
"$NODE" "$SKILL" --image 截图.png --caption "看这张图"

# 文件 + 文件名 + 可选说明（context_token 自动读取）
"$NODE" "$SKILL" --file 报告.pdf --name "周报.pdf" --caption "请查阅"

# 视频（context_token 自动读取）
"$NODE" "$SKILL" --video clip.mp4

# 显式指定 token（极端兜底：手动传入一个已知有效的 context_token）
"$NODE" "$SKILL" "回复内容" --context <context_token>
```

- 不传参数 → 发送默认测试文案（文本）。
- 跑的时候若因沙箱拦截网络，加 `dangerouslyDisableSandbox: true`（或在弹窗点允许）。
- 成功标志：终端打印 `[weixinclaw] OK`，老板微信里会收到一条 **ClawBot bot 消息**（不是对话气泡）。

## 凭据从哪来（settings.json）
```
claw/users/<uid>/channels/weixinClawBot = {
  "enabled": true,
  "channelId": "<你的 bot channelId，从你的 settings.json 读取>",
  "botToken":  "<完整 botToken 串，含 accountId: 前缀；脚本自动从你的 settings.json 读取，无需手填>",  // 完整 token = Bearer 凭据
  "baseUrl":   "https://ilinkai.weixin.qq.com",                                // apiBaseUrl
  "accountId": "<你的 bot accountId，从你的 settings.json 读取>",
  "userId":    "<老板的 im.wechat id = to_user_id；脚本自动从你的 settings.json 读取>",                       // 老板的 im.wechat id = to_user_id
  "connectionMode": "polling"
}
```

> 🔒 以上字段均为接收方**自己**的 `settings.json` 内容，无需分享者提供。脚本只读取、不写出。

## 🔴 关键机制：context_token（2026-07-09 定稿）

### 文本默认空 token；只有媒体才带 cursor buf
- **⚠️ 2026-08-28 实测修正**：服务端行为已收紧——**会话过期后，连空 token 的文本也会 `ret:-2 "prepare failed"`**。
  "文本无需激活" 的旧结论已失效；激活后文本/媒体在当天会话窗口内都正常。
- **文本推送**：`msg.context_token` 默认传【空串】（会话存活时即可发送）。
- **媒体推送（图片 / 文件 / 视频）**：**必须**带非空 `context_token`，
  唯一来源是 cursor 游标里的 `get_updates_buf`（见下）。空 token 发媒体会 `ret:-2`。
- **任何被拒（`ret:-2`）都要激活**：需要老板/用户在微信给 ClawBot 发消息激活后重跑（详见排错表）。

### 协议层自激活：已验证无解（2026-08-28 全端点实测）
- 真正的 `context_token` 是**每条收到的消息自带**的（官方 inbound.js：*"contextToken is issued per-message
  by the Weixin getupdates API and must be echoed verbatim in every outbound send"*），
  服务端用它校验**用户侧下行会话**（约 1 天无用户消息即过期），这是微信 bot 反骚扰设计，客户端无法绕过。
- 以下手段**全部无效**（都能调通但救不活会话）：
  - `ilink/bot/msg/notifystart`（生命周期通知，ret:0，无效果）
  - `ilink/bot/getconfig` + `ilink/bot/sendtyping`（typing_ticket 可正常拿到、sendtyping ret:0，无效果）
  - 先发文本再发媒体（文本自身也被拒，无效果）
  - 重复调 `getupdates` / 重读 cursor buf（buf 凭证本身有效，死的是会话，不是凭证）
- **不受会话校验的端点**：`getupdates`、`getuploadurl`、CDN 上传、`getconfig`、`sendtyping`、`notifystart` 都能通；
  唯一卡 `sendmessage` 的 "prepare"（下行会话准备）这一步。
- 唯一激活方式 = **用户在微信给 ClawBot 发一条消息**（可用 PC 微信 UI 自动化代发，属协议外手段）。

### 媒体的 context_token 来源：cursor 游标里的 `get_updates_buf`

- host 实时把 ilink 接收会话游标写进
  `~/.workbuddy/claw-state/weixin/<ACCOUNT_ID>_im.bot.cursor.json` 的 `get_updates_buf` 字段。
- 该字段值是 **base64 编码的 protobuf**；我们**把整段 base64 串原样**当作 `context_token` 用
  （不是解码出来的 botToken 串，也不是里面的 accountId 段）。

> ✅❌ **读取铁律（违反任何一条都会 ret:-2，这是"编码读取方式"的要害）**
> 1. **以 UTF-8 文本**读 `cursor.json` → ② `JSON.parse` → ③ 取 `get_updates_buf` 字段的【字符串值】 →
>    ④ **原样**作为 `context_token`。
> 2. ❌ 严禁对这串做任何变换：**base64 解码、重新编码、trim、URL-decode、转义、换行、截断、大小写改写**。
>    base64 串里全是 `A-Za-z0-9+/=` 字符，JSON 安全，**直接原样塞进 `context_token` 字段即可**。
> 3. ❌ 不要"聪明地"解析 / 改写 / 重组这个串——它就是个不透明令牌，服务端的校验逻辑你是看不见的，任何本地变换都只会让它失效。
> 4. ✅ 直接用本仓库的 `send.js`（已封装以上全部），**不要手工拼请求**——手工拼最容易在读取这步翻车。

- **凭证稳定、不要误判**：`botToken` / `accountId` 段（形如 `<ACCOUNT_ID>`）约 **1 天**才轮换一次，期间**一直有效、不变是正常的**，它**不是**失效信号，别拿它判断 buf 是否过期。
- **文本无需激活**：文本走空 token，会话闲置多久都能发（实测跨十几小时）；只有出现 `ret:-2` 时才需激活。
- **媒体激活一次可长期使用**：媒体带 cursor buf，只要此前已激活过且没收到 `ret:-2`，就可持续推送，**不需要每次推送前都重新发消息**。
- **文本被拒 = id 变了，也要激活**：文本平时空 token 能发；一旦文本 `ret:-2`，大概率底层 bot id 轮换，**同样**先发消息激活再重跑。
- ⚠️ **未激活时反复直接重跑必定再次 `ret:-2`**——请务必先完成"发消息激活"这个动作，再重跑命令。
- 实测：媒体用 buf 当 `context_token` + 完整 `botToken` 当 Bearer ⇒ `{}` 成功，且不读 context-token.json、无需轮询。
- 编码细节：`get_updates_buf` 解码后为约 78 字节 protobuf，含 `botId`(varint) + 账号标识 +
  botToken 明文段（`accountId@im.bot:secret`）。

> 🔒 `get_updates_buf` 内嵌了 bot 凭证副本，**绝不要**把它粘贴到聊天、Issue、或随仓库提交。

### `im.bot.cursor.json` 文件的更新机制（务必分清"文件刷新"和"buf 轮换"两件事）

文件路径：`~/.workbuddy/claw-state/weixin/<ACCOUNT_ID>_im.bot.cursor.json`
（`<ACCOUNT_ID>` = bot accountId 段，如同一个 bot 换了凭证/会话，文件名的这段会变，会出现新的一份 cursor 文件）。

**① 文件何时被创建**
- 该文件由 host（WorkBuddy 后台的 ilink bot 长轮询）维护。**通道必须先建立过会话**才会有这个文件——
  即老板/用户曾在微信给 ClawBot 发过消息、host 侧建立了接收游标。
- 若目录里没有任何 `*_im.bot.cursor.json`：让老板/用户**先在微信给 ClawBot 发一条消息**，host 才会写出该文件。

**② 文件 mtime（修改时间）——host 实时刷新，别拿它当判断依据**
- host 在**每一轮长轮询写盘游标**时都会更新该文件的 mtime，非常频繁，且**与你是否发消息无关**（是 host 侧实时行为，不是你触发的）。
- ⚠️ 因此 **绝不能用 mtime（"多久没变 / 刚变过"）来判断 buf 是否新鲜、是否需要刷新**——mtime 一直在变，但 `get_updates_buf` 的值**未必**跟着变。这是最容易误判的点。

**③ `get_updates_buf` 内容（真正的 token）——稳定，靠"激活"刷新，不靠时间猜**
- 这才是我们要的 token。它在 bot 凭证/会话有效期内**保持稳定**（`accountId` 段约 1 天轮换一次，期间不变属正常）。
  - 判断是否需要刷新，**唯一依据是「实际推送是否被服务端拒绝（`ret:-2`）」**：
    - 被拒＝当前 buf 暂时不可发送 → **让老板/用户在微信给 ClawBot 发一条消息激活**（host 随即刷新游标），再重跑 `send.js` 自动读最新 buf 重发即可。
    - 只要不被拒，**激活一次即可在较长时间内反复推送**（实测跨十几小时仍能成功），不需要每次推送前都发消息激活。
    - ⚠️ **不要**把 mtime 变化、或"buf 值有没有变"当成判断条件——这两者都不决定可发送性，纯属干扰。
- `send.js` 收到 `-2` 会【清晰报错并退出】，不内置轮询等待（"等待刷新"退步逻辑已彻底删除）；由你手动激活后重跑命令即可。

### send.js 的取值优先级
```
文本：ctx = --context 显式传入 ＞ 【空串】（默认，无需 cursor / 激活）
媒体：ctx = --context 显式传入 ＞ 读最新 <ACCOUNT_ID>_im.bot.cursor.json 的 get_updates_buf（默认走这条）
```
（媒体的 `get_updates_buf` 为空、或任何推送被拒 `ret:-2`（含文本被拒＝id 变了）时：
**先让老板/用户自己在微信给 ClawBot 发一条消息激活**（host 随即刷新游标），再重跑 `send.js`；
仍失败再走 `--context <token>` 显式兜底。）

## 🔴 关键坑（必看，否则必失败）
1. **Bearer token 必须用完整 `botToken` 串**（含 `accountId:` 前缀），即
   `<完整 botToken 串（含 accountId: 前缀），从你的 settings.json 读取>`。
   只取冒号后的短串会返回 `errcode:-14 session timeout`，推送失败。
2. **协议常量对齐官方 `@tencent-weixin/openclaw-weixin@2.4.6`**（不要再用旧值）：
   - `channel_version = "2.4.6"`（早期实现误用 `cbc-1.0.0`，现已对齐官方）
   - `iLink-App-ClientVersion = 132102`（= `buildClientVersion("2.4.6")`）
   - `iLink-App-Id = "bot"`，`bot_agent = "OpenClaw"`
3. **文本默认空 `context_token` 即可**；**媒体推送必须带有效 `context_token`**（见上节），否则 `ret:-2` 拒收。文本若也被拒 `ret:-2`，大概率 bot id 轮换，需激活。

## 发送契约（对齐官方 ilink bot 协议）
- 端点：`POST {baseUrl}/ilink/bot/sendmessage`
- 请求头（完整，缺一不可）：
  - `Authorization: Bearer <完整botToken>`
  - `AuthorizationType: ilink_bot_token`
  - `X-WECHAT-UIN: <随机4字节uint32的base64>`
  - `iLink-App-Id: bot`
  - `iLink-App-ClientVersion: 132102`
  - `Content-Type: application/json`
- Body（文本）：
```json
{
  "msg": {
    "from_user_id": "",
    "to_user_id": "<boss的im.wechat id>",
    "client_id": "<16位随机hex>",
    "message_type": 2,
    "message_state": 2,
    "item_list": [{ "type": 1, "text_item": { "text": "消息内容" } }],
    "context_token": "<从 cursor 读取的 get_updates_buf>"
  },
  "base_info": { "channel_version": "2.4.6", "bot_agent": "OpenClaw" }
}
```
- `item_list` 类型：`1=文本` / `2=图片` / `4=文件` / `5=视频`（text 超 4000 字自动分片）。
- 成功判定：`sendmessage` 返回 `{}`（host 视 `ret` 缺失为成功）；`ret` 非零（如 `-2`）即失败。
- 会话存活自检：`POST {baseUrl}/ilink/bot/getupdates` 返回无 `errcode` 即健康。

## 富媒体流程（图片/文件/视频）
0. **context_token 自动从 cursor 游标读取**（详见上方机制专节），无需手动准备。没有会 `ret:-2`。
1. 生成 16 字节随机 AES 密钥 `aesKey`，`aesKeyHex = aesKey.toString('hex')`。
2. `POST /ilink/bot/getuploadurl`，body：`filekey, media_type(1=IMAGE/2=VIDEO/3=FILE), to_user_id, rawsize, rawfilemd5, filesize(密文长), aeskey(aesKeyHex), no_need_thumb`。
3. 取响应 `upload_full_url`（或旧版 `upload_param` 拼 `https://novac2c.cdn.weixin.qq.com/c2c/upload?encrypted_query_param=...&filekey=...`）。
4. `POST` 密文（AES-128-ECB(PKCS7) 加密后的文件）到该 URL，`Content-Type: application/octet-stream`。
5. 取响应头 `x-encrypted-param` 作为下载令牌 `encrypt_query_param`。
6. 构造 item：`media = { encrypt_query_param, aes_key: base64(aesKeyHex), encrypt_type: 1 }`，
   图片加 `mid_size`，文件加 `file_name`+`len`，视频加 `video_size`。
7. `POST /ilink/bot/sendmessage`，`msg.context_token` = 有效 token。

## 排错
| 现象 | 原因 | 解决 |
|------|------|------|
| `errcode:-14 session timeout` | 用了短 token | 改用完整 `botToken` 串 |
| `FAILED: API ret=-2` (errmsg `prepare failed`) | **用户侧下行会话过期**（约 1 天无用户消息即失效，2026-08-28 实测文本/媒体都受此校验，协议内无自激活手段，见上方专节） | **【必须】先到微信给 ClawBot 发一条任意消息**（激活下行会话），**激活后再重跑本命令**，`send.js` 自动读最新 buf 重发。⚠️ 未激活时反复直接重跑必定再次 `ret:-2`；不要拿 mtime 或"buf 值变没变"当判断条件；`send.js` 收到 `-2` 会清晰报错并退出（不内置轮询）；仍失败再显式 `--context <token>` 兜底 |
| 网络超时 / fetch 失败 | 默认沙箱拦截出网 | 加 `dangerouslyDisableSandbox: true` 或点允许 |
| 通道找不到 | settings.json 路径/字段变了 | 按上文"凭据从哪来"手动核对路径 |
| 走错通道 | 误用 MCP 的 weixin/wecom | 确认用 `weixinClawBot`（ClawBot），不是 MCP connector |
| 富媒体上传失败 | `getuploadurl` 未返回 url / CDN 缺 `x-encrypted-param` | 检查 botToken 完整、网络可达 CDN |
| 文本类文件（.txt/.md）中文乱码 | 源文件 UTF-8 无 BOM，微信/Windows 按 GBK 解码 | send.js 已自动为文本类文件补 UTF-8 BOM，无需手动处理 |
| `文件不存在: ...` | 传入的媒体路径错误 | 检查 `--image/--file/--video` 指向的文件路径 |
| `缺少 botToken` / `缺少 userId` | settings.json 的 weixinClawBot 配置不完整 | 按"凭据从哪来"补全字段 |
