# push-server HTTP 接口参考

仅在需要「排查连通性」或「回查已推送消息」时阅读本文件。日常推送只看 SKILL.md 的工具说明即可。

## 0. 接口总览与调用约定（逐个用例测试前先看本节）

| # | Method | Path | 鉴权 | 成功时 `data` | 用户会怎么说（示例话术） |
|---|---|---|---|---|---|
| 1 | GET | `/services/public/ping` | 无 | `{status:"alive",service:"push-server",rows:[...]}`（`rows` 为公开示例通道） | 「推送失败了，帮我看看 push-server 还活着吗？」 |
| 2 | GET | `/oauth2/push/message/page` | Bearer | 分页对象：`current` / `total` / `totalPage` / `rows` | 「查一下最近推过哪些消息」「把第 2 页的推送记录列出来」 |
| 3 | GET | `/oauth2/push/message/detail` | Bearer | 单条消息对象（含 `viewCount`） | 「这条消息的正文是什么？」「那条通知有人看过吗？」 |
| 4 | GET | `/oauth2/push/channel/list` | Bearer | 父通道信息 + `rows`（无分页） | 「请查看 push-server 当前有哪些通道？」「我有没有浏览器通道？」 |
| 5 | POST | `/oauth2/push/channel/add` | Bearer | **新建的通道对象**（字段同 5.1 的 `rows[]`） | 「帮我新建一条钉钉通道」「加个 webhook 通道，地址是 …」 |
| 6 | POST | `/oauth2/push/channel/edit` | Bearer | `true` | 「把‘告警接收端’改名成生产告警」「停用那条钉钉通道」 |
| 7 | POST | `/oauth2/push/channel/deleteChannel` | Bearer | `true` | 「删掉那条没用的测试通道」 |
| 8 | POST | `/oauth2/push/channel/resetChannel` | Bearer | **新的 32 位通道码字符串**（唯一例外） | 「重置一下这条通道的通道码」 |
| 9 | POST | `/oauth2/push/channel/member/edit` | Bearer | `true` | 「把这条通道的推送人昵称改成构建机器人」 |

（`get_access_token` 是 MCP 工具不是 HTTP 接口，但它总在 2～9 之前调用，示例话术见第 2 节。）

约定（踩这几个坑最多）：

- **参数只能走 query 或 `application/x-www-form-urlencoded`**，`application/json` 的 body 会被完全忽略，表现就是「XXX 参数缺失或非法」。
- `page` / `limit` 缺省或 `<=0` 时回落 `1` / `10`；文本参数（`nickname`）空白串按缺失处理。
- 所有错误都是 **HTTP 200 + 非 0 业务码**，不要用 HTTP 状态码判成功；`401/403` 才是认证侧，令牌过期重新 `get_access_token` 即可。

## 1. 鉴权总则

| 凭证 | 发放方 | 用在哪 | 有效期          |
|---|---|---|--------------|
| 32 位通道码 | 一封传话控制台 | MCP 工具 Header `X-Push-Channel-Code` | 长期，仅重置后需替换   |
| `access_token` | MCP `get_access_token` | `Authorization: Bearer` 访问 `/oauth2/push/*` | **默认 7200 秒（2 小时）**，以返回的 `expires_in` 为准 |

两种凭证严格分离：**通道码不能放进 `Authorization` 头，令牌也不能用于 MCP 推送。**

下文 curl 用 `${CHANNEL_ACCESS_TOKEN}` 代指 `access_token`。

## 2. 获取令牌（MCP `get_access_token`）

用户话术示例：「帮我取一个 push-server 的令牌」「我要查通道列表，先换个令牌」「令牌好像过期了，重新拿一个」——凡是后面要调 `/oauth2/push/*`，都先走这一步。

| 参数 | 必填 | 说明 |
|---|---|---|
| `scope` | 否 | 该调用申请的 scope，必须是**该通道已登记范围的子集**，超出会返回错误并列出可用范围；不传则使用服务端默认值 `basic` |
| `channelCode` | 否 | 未预置 Header 时必填 |

成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiJ9.SIGNATURE_PART_OMITTED",
    "token_type": "Bearer",
    "expires_in": 7200,
    "scope": "basic"
  }
}
```

#### 令牌长什么样

`access_token` 是一段标准 JWT（`header.payload.signature` 三段式，以 `eyJ` 开头）。两条用得上的结论：

- 中段 payload 可以**直接解开**（base64url 解码，不需要密钥），里面有过期时间。想知道还剩多久，解它比自己记时间更准。
- 反过来，**不要拿前缀、长度或是不是 `eyJ` 开头去判断它合不合法**，也不用自己验签——原样塞进 `Authorization` 头即可。具体格式属于服务端实现细节，随时可能调整。

### 复用规则（省掉大量往返的关键）

`access_token` 签发后即**自包含**，业务接口本地就能校验，不需要每次回源。由此推出四条：

1. **一张令牌可以连打多个接口**。9 个 `/oauth2/push/*` 都只按 `Authorization` 认它，不区分接口。一轮「取令牌 → 查分页 → 查详情 → 改通道」的任务，**开头取一次就够**。
2. **重复获取不会顶掉旧的**。每次调用 `get_access_token` 都是独立签发，多次调用互不影响，不存在「取了新的，旧的立刻失效」。
3. **按 `expires_in` 倒计时**，别按固定经验值。默认 7200 秒，留 60~120 秒余量再重取即可。这个值可以在控制台改（有效区间 600~7200 秒），所以**以本次返回的为准**。
4. **不要写进文件 / 长期记忆**：属于会话级凭证，跨会话留着用只会换来难以定位的 401。

令牌本体不外泄，也不要出现在推送内容或日志里（见 SKILL.md 安全红线）。401/403 才需要重取；业务错误（`code` 非 0）与令牌无关。

> 注意 `access_token不正确请重新获取` 这条文案是个**误导源**：它在「令牌主体不是挂在父通道下的浏览器子通道」时同样会出现，此时重取多少次都一样。判定是不是真过期，看 HTTP 状态码 401/403，而不是看这句文案。

## 3. 连通性自检（匿名）

用户话术示例：「推送失败了，帮我看看 push-server 还活着吗？」「先确认下服务端是不是挂了」「MCP 连不上，帮我二分定位一下」。

```bash
curl -s https://www.phprm.com/services/public/ping
```

正常返回：

```json
{
  "code": 0,
  "message": "ok",
  "trace": "27b530cb0c4d4a6cbb66699b7ca42f8e",
  "data": {
    "status": "alive",
    "service": "push-server",
    "rows": [
      {
        "channelName": "在线体验",
        "pushType": 1,
        "pushTypeName": "website",
        "pushTypeDesc": "浏览器",
        "channelCode": "4d05f4abdb0a0c2a0269900809946903",
        "createTime": "2023-11-08 19:46:10",
        "webhookUrl": "",
        "signSecret": "",
        "status": 1,
        "channelMemberRelId": "1304170050492055552",
        "userId": "26990080",
        "nickname": "一封传话",
        "pushUrl": "https://push.phprm.com/message/share.html?channelCode=4d05f4abdb0a0c2a0269900809946903",
        "qrCodeUrl": "https://www.phprm.com/services/qr/c/1304170050458501120/9wpdp65a4ef4"
      }
    ]
  }
}
```

| 字段 | 说明 |
|---|---|
| `code` / `message` | 固定 `0` / `ok` |
| `trace` | 本次请求的追踪 ID，排查时把它报给服务端即可，无需解析 |
| `data.status` / `data.service` | 固定 `alive` / `push-server` |
| `data.rows[]` | **服务端预置的公开示例通道**，字段与 5.1 的 `rows[]` 一致（含 `pushUrl` / `qrCodeUrl` / `channelMemberRelId`）；列表中只保留**当前仍然可用**的通道，内容可能随时间变化，也可能为空 |
| `data.rows[].pushUrl` | 该通道的**分享/管理页面地址**（share.html），浏览器打开即可查看与管理该通道（非 website 类型为空） |
| `data.rows[].qrCodeUrl` | **推送记录页面**的二维码，扫码即可在手机上查看该通道的推送记录（非 website 类型为空）。给用户"在哪看消息"的入口时用这两个字段，不要自己拼 URL |

⚠️ 通道码即推送凭证，而 `rows[].channelCode` 是**匿名可得**的示范码：任何拿到它的人都能往这些通道推送。因此它们只能用于「用户同意后的链路自测」，绝不能当作某个用户自己的通道，更不要写进 `${PHPRM_CHANNEL_CODE}`。

- 无需任何 Header 凭证，除示例通道码外不含数据量或内部拓扑信息，匿名调用安全。
- **只在推送失败后用来二分定位**，不要把健康端点放进监控轮询。

| 检查结果 | 结论 | 下一步 |
|---|---|---|
| ping 返回 alive | 端点活着 | 问题在凭证/配置：核对通道码是否替换、`X-Push-Channel-Code` 名称是否写对、MCP 传输类型是否为 Streamable HTTP |
| ping 失败（连接层错误/超时） | 端点或网络异常 | 核对 URL、出网连通性、是否被代理拦截 |
| ping 和 MCP 都连不上 | 两者同源，共用同一层网关与后端 | 按上面「ping 失败」处理，不要再逐个重试工具 |
| 端点正常但客户端显示 MCP 未连接 | 客户端配置问题 | 核对客户端配置根键（`mcpServers` / `servers` 等）与自定义 Header 写法 |

这里的 ping 是**匿名 HTTP 端点**，和 MCP 的 JSON-RPC `ping` 方法不是一回事（后者同样需要 `X-Push-Channel-Code`）。

## 4. 消息查询 API

需要鉴权：`Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}`（`client_credentials` 令牌）。以下接口只能读取**当前令牌所属通道**的消息。

### 4.1 消息分页

用户话术示例：「查一下最近推过哪些消息」「把近 5 条推送记录列出来」「那条告警消息推成功了吗，帮我查一下记录」。

| 名称 | 位置 | 必填 | 说明 |
|---|---|---|---|
| `Authorization` | Header | 是 | `Bearer ${CHANNEL_ACCESS_TOKEN}` |
| `page` | Query | 否 | 页码，默认 1 |
| `limit` | Query | 否 | 每页条数，默认 10 |

```bash
curl --location "https://www.phprm.com/oauth2/push/message/page?page=2&limit=5" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"
```

返回示例：

```json
{
  "code": 0,
  "message": "REQUEST_SUCCESS",
  "data": {
    "current": "1",
    "total": "20",
    "totalPage": "4",
    "rows": [
      {
        "messageId": "1687512996693323778",
        "title": "DSH 推送",
        "content": "来自 DeepSeek Harness。",
        "notifyTime": "2026-10-01 15:34:10",
        "nickname": "哈哈",
        "messageUrl": "https://push.phprm.com/message/view.html?t=1687512996693323778&i=65686790&m=e0b91f6b6360a220"
      }
    ]
  }
}
```

只需关注以下字段，其余忽略：

| 字段 | 说明 |
|---|---|
| `code` | 0 表示成功，其余为业务错误码 |
| `message` | 错误描述 |
| `data.current` | 当前页码 |
| `data.total` | 总条数 |
| `data.totalPage` | 总页数（翻页前先比对它，超页返回空 `rows`） |
| `data.rows[].messageId` | 消息 ID（查详情时用它） |
| `data.rows[].title` | 消息标题 |
| `data.rows[].content` | 消息正文（Markdown 或 JSON 原文，两种都有可能） |
| `data.rows[].notifyTime` | 通知时间 |
| `data.rows[].nickname` | 发送者昵称 |
| `data.rows[].messageUrl` | 消息跳转链接 |

### 4.2 消息详情

用户话术示例：「这条消息的正文是什么？」「把那条通知的完整内容给我」「那条推送有人看过吗？」「把 messageId 1687502979776819203 这条的详情查出来」。

| 名称 | 位置 | 必填 | 说明 |
|---|---|---|---|
| `Authorization` | Header | 是 | `Bearer ${CHANNEL_ACCESS_TOKEN}` |
| `messageId` | Query | 是 | 消息 ID，来自分页返回的 `messageId`；缺失或非整数返回「messageId 参数缺失或非法」 |

```bash
curl --location "https://www.phprm.com/oauth2/push/message/detail?messageId=1687502979776819203" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"
```

返回示例：

```json
{
  "code": 0,
  "message": "请求成功",
  "data": {
    "channelName": "多个推送通道",
    "title": "DSH 推送",
    "content": "来自 DeepSeek Harness",
    "notifyTime": "2026-10-01 14:54:22",
    "messageUrl": "https://push.phprm.com/message/view.html?t=1687502979776819203&i=65673969&m=ffead72facb170d3",
    "viewCount": 3
  }
}
```

| 字段 | 说明 |
|---|---|
| `channelName` | 接收通道名 |
| `title` / `content` | 标题 / 正文；正文可能是 Markdown，也可能是 webhook 通道的 JSON 原文（接口不下发标识字段，按内容形态判断：能被解析成 JSON 就按代码块原样展示，否则按 Markdown 渲染） |
| `notifyTime` | 通知时间 |
| `viewCount` | 浏览次数 |
| `messageUrl` | 跳转链接（可直接给用户，也可渲染成 `<a>` 可点链接，只放行 `http`/`https`） |

## 5. 通道管理 API

- **成员能力只开放这 1 个接口**：5.6 改昵称。**其它成员相关功能（删除成员、成员列表分页、拉黑/恢复、邀请新成员加入、批量处理、成员高级设置等）没有对应的 HTTP 接口**，让用户登录[一封传话官网](https://push.phprm.com)控制台操作，不要用现有接口拼等价行为。
- **成员 ID（`channelMemberRelId`）只有一个来源**：5.1 通道列表 `data.rows[].channelMemberRelId`，即该子通道**创建人**的成员记录。只有 `pushType=1`（浏览器）的子通道行带这个值，其它类型子通道该字段为空；**没有成员分页接口可再查其它成员**，值为空就等于这个成员无法通过接口操作，**无论如何都不要自己拼 ID**。
- **目标通道用 `channelCode`（32 位）定位，只能取自通道列表返回的 `channelCode`**；长度不是 32 位一律返回「channelCode 参数缺失或非法」，**不要自己拼**。
- 「同组」= 目标通道与当前凭证通道的父通道（`pid`）相同；越组会返回业务错误码并提示「只能……同组通道」。
- **删除与重置对当前通道的限制不一样**：

  | 操作 | 是否真的按入参 `channelCode` 做识别 | 能否作用于当前凭证绑定的通道 |
  |---|---|---|
  | 删除 5.4 | 是：先把目标通道与自身通道比一次（相同即拒绝），再比 `pid` | ❌ 禁止，返回「不能删除当前应用绑定的通道」 |
  | 重置 5.5 | 只比 `pid`，**没有比对自身通道** | ⚠️ **允许**，直接返回新通道码 |
  | 停用 5.3（`status=0`） | 是：按 `channelCode` 反查出的目标通道 | ⚠️ **允许**，服务端不阻止停用自己，之后往该通道推送一律返回「通道未开启」 |

  因此**不存在「不能重置当前通道」的保护**。对自己通道做重置等于轮换自己的推送凭证，是一次单向操作：旧通道码立即作废，正在用它的 MCP Header、脚本、第三方机器人全部失效，直到替换成返回的新码。重置前先确认「这次就是要换码」，并确认手上有地方能把新码写回去。

  停用（5.3 传 `status=0`）同样没有自我保护：把**当前正在推送的通道**改成未启用后，所有发往它的消息都会被拒（「通道未开启」），且不会有任何提示告诉你「这条是自己的通道」。停用前先按 5.1「当前通道怎么找」认出当前通道并避开它；恢复就是再调一次 5.3 传 `status=1`。

### 5.1 拉取当前通道的下属通道列表（无分页）

用户话术示例：「请查看 push-server 当前有哪些通道？」「我名下都有什么通道？」「我有没有浏览器通道 / webhook 通道？」「找一下名字里带‘告警’的通道」「我的钉钉通道的通道码是多少？」

仅 Header 鉴权，不分页。返回结构固定为「顶层父通道信息 + `rows` 子通道列表」，但**顶层不一定就是当前通道**，取决于你复制的通道码来源。

| 参数 | 必填 | 说明 |
|---|---|---|
| `channelName` | 否 | 通道名**模糊**匹配（同时命中通道名与通道码），不传返回全部；空白串按缺失处理 |
| `pushTypeName` | 否 | 推送类型筛选，接受枚举名小写（`website`、`ding_talk_push`）或中文描述（`浏览器`、`钉钉群机器人`），完整表见 5.7；**不在枚举范围内返回「pushTypeName不在支持范围内」**，不会退化成全量列表 |

两个参数可同时传（取交集），都不传就是原来的全量列表。

```bash
curl --location "https://www.phprm.com/oauth2/push/channel/list" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"

# 按通道名模糊匹配
curl --location "https://www.phprm.com/oauth2/push/channel/list?channelName=告警" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"

# 按推送类型筛选（枚举名或中文描述都行）
curl --location "https://www.phprm.com/oauth2/push/channel/list?pushTypeName=website" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"
```

```json
{
  "code": 0,
  "message": "REQUEST_SUCCESS",
  "data": {
    "channelCode": "11111111111111111111111111aaaaaa",
    "channelName": "多个推送通道",
    "pushType": 10,
    "createTime": "2026-10-01 15:34:10",
    "rows": [
      {
        "channelName": "我的浏览器通道",
        "pushType": 1,
        "pushTypeName": "website",
        "pushTypeDesc": "浏览器",
        "channelCode": "22222222222222222222222222bbbbbb",
        "createTime": "2026-10-01 15:34:10",
        "webhookUrl": "",
        "signSecret": "",
        "status": 1,
        "channelMemberRelId": 998877665544332211,
        "userId": 831289282843013,
        "nickname": "张三",
        "pushUrl": "https://push.phprm.com/message/share.html?channelCode=22222222222222222222222222bbbbbb",
        "qrCodeUrl": "https://push.phprm.com/push/qrcode.html?c=22222222222222222222222222bbbbbb"
      }
    ]
  }
}
```

| 字段                                                             | 说明                                                                                                                                            |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `code` / `message`                                             | 0 表示成功，其余为业务错误码 / 错误描述                                                                                                                        |
| `data.channelCode` / `channelName` / `pushType` / `createTime` | 父通道（组）信息                                                                                                                                      |
| `data.rows[].channelName`                                      | 通道名称                                                                                                                                          |
| `data.rows[].pushType`                                         | 推送类型编码，见 5.7 枚举表                                                                                                                              |
| `data.rows[].pushTypeName`                                     | 推送类型标识（枚举名小写，如 `website`、`web_hook_push`）                                                                                                     |
| `data.rows[].pushTypeDesc`                                     | 推送类型描述（如「浏览器」「webhook推送」）                                                                                                                     |
| `data.rows[].channelCode`                                      | 该子通道的 32 位通道码：可直接当 MCP 凭证用、**是「当前通道怎么找」的比对依据**、也是 5.3/5.4/5.5 定位目标通道的唯一入参                                                                     |
| `data.rows[].webhookUrl`                                       | webhook 通道的接收地址，非 webhook 类型为空                                                                                                                |
| `data.rows[].signSecret`                                      | 钉钉 / 企业微信 / 飞书群机器人的加签 Secret，未启用加签或非这三类群机器人时为空                                                                                                  |
| `data.rows[].status`                                           | 通道状态（`1` 已启用 / `0` 未启用，见 5.8）                                                                                                                 |
| `data.rows[].channelMemberRelId`                               | **该子通道创建人的成员 ID**，`nickname` 同属这条成员记录；**成员接口入参的唯一来源**，可直接作为 5.6 的入参。**仅 `pushType=1`（浏览器）的子通道有值**，其余为 `null`（顶层 `data` 不带成员字段，也没有成员分页接口可查其它人） |
| `data.rows[].pushUrl`                                          | website 通道的分享/管理页面地址（share.html），打开即可查看与管理该通道，非 website 类型为空                                                                                                   |
| `data.rows[].qrCodeUrl`                                        | **推送记录页面**的二维码，扫码即可在手机上查看推送记录，非 website 类型为空                                                                                                 |

#### 通道码的层级与含义

用户复制过来的通道码来源不定，出现的位置可能也不同，出现在外层的属于组合通道，出现在rows集合里的是子通道：

| 复制的通道码是 | 列表里当前通道在哪 |
|---|---|
| 组合父通道 | 在**顶层 `data`**，不在 `rows` 里 |
| 浏览器子通道 | 在 `data.rows[]` 里 |

指定组合通道channelCode参数推送一次将自动给所有的子通道全部都推送一次，指定某个子通道码进行推送时只会推送到这个子通道。

### 5.2 新增通道

用户话术示例：「帮我新建一条钉钉通道」「加一个 webhook 通道，地址是 https://example.com/hook/push」「再开一条浏览器通道」。

`POST https://www.phprm.com/oauth2/push/channel/add`

> 🚧 **本接口是最后手段，不是首选**。同一个 `pushType` 只需一条通道：先拉 5.1 列表，有同类型且状态正常的通道就**复用**；确实没有才新建，且新建前先向用户说明「为什么还要再开一条」并取得确认。**不要重复创建相同类型的推送通道**——多开不会带来隔离性收益，只会让后续每次推送都要先决定发到哪条。

| 名称            | 必填 | 说明                                                                       |
|---------------|---|--------------------------------------------------------------------------|
| `channelName` | 是 | 通道名称                                                                     |
| `pushType`    | 是 | 推送类型编码，见 5.7                                                             |
| `webhookUrl`  | 否 | 接收地址。`webhook推送`、`企业微信/钉钉/飞书群机器人`、`BARK` 这几类必须是合法 URL；浏览器、组合、官方邮件可留空     |
| `signSecret`  | 否 | 钉钉 / 企业微信 / 飞书群机器人的加签密钥（加签 Secret）。仅这三类群机器人可传：启用加签时填入，长度 4~255；未启用加签留空，其他推送类型勿传 |

新通道的归属由服务端按当前令牌决定，**不要预先断言它挂在谁下面**（复制的是父通道码还是子通道码、有没有浏览器子通道，结果都不一样）。创建后用 5.1 复核它实际出现在哪一层，取它的 `channelCode` 再往下操作。

```bash
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/add" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelName=告警webhook接收端" \
  --data-urlencode "pushType=11" \
  --data-urlencode "webhookUrl=https://example.com/hook/push"
```

成功响应（`data` 就是新建的通道，字段与 5.1 的 `rows[]` 对齐：

```json
{
  "code": 0,
  "message": "REQUEST_SUCCESS",
  "data": {
    "channelName": "告警webhook接收端",
    "pushType": 11,
    "pushTypeName": "web_hook_push",
    "pushTypeDesc": "webhook推送",
    "channelCode": "33333333333333333333333333cccccc",
    "createTime": "2026-10-01 15:40:02",
    "webhookUrl": "https://example.com/hook/push",
    "status": 1,
    "userId": "2699080"
  }
}
```

仅新增浏览器类型通道时返回 `data.channelMemberRelId` 和 `data.nickname` , 可以取 `data.channelCode` 指定子通道进行推送, 不过仍然建议使用MCP 凭证或者5.1通道列表顶层channelCode的父通道码推送到所有子通道。

### 5.3 修改通道

用户话术示例（按意图分，`xx` 是通道名或通道码）：

| 用户怎么说 | 映射到 |
|---|---|
| 改名 / 改配置：「把‘告警接收端’改名成生产告警」「这条通道的 webhook 地址换成 …」 | `channelName` / `webhookUrl` 等，不动 `status` |
| **停用**：「将 xx 通道给关了」「请将 xx 通道给关闭」「把 xx 通道停掉」「关掉那条钉钉通道」「先别往 xx 通道推了」 | **`status=0`** |
| **启用**：「将 xx 通道开启」「把 xx 通道打开」「把浏览器通道重新启用」 | **`status=1`** |

口语里的「关 / 关闭 / 停掉 / 别推了」一律按**停用（`status=0`）**处理，「开启 / 打开 / 重新启用」按**启用（`status=1`）**处理；拿不准是停用还是启用就先问用户，不要猜。

`POST https://www.phprm.com/oauth2/push/channel/edit`

| 名称 | 必填 | 说明 |
|---|---|---|
| `channelCode` | 是 | 目标通道码（取自 5.1 的 `channelCode`，32 位）；长度不是 32 位返回「channelCode 参数缺失或非法」，查不到返回「通道不存在」，不同组返回「只能修改同组通道」 |
| `channelName` | 否 | 新名称 |
| `webhookUrl` | 否 | 与 5.2 同义，传了才覆盖 |
| `qrCodeRefresh` | 否 | 是否刷新二维码，`0` 不刷新（缺省）/ `1` 刷新 |
| `status` | 否 | 通道状态，**只传 `1`（已启用）/ `0`（未启用）**，见 5.8；不传则保持原状态 |

```bash
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/edit" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelCode=22222222222222222222222222bbbbbb" \
  --data-urlencode "channelName=告警接收端(生产)" \
  --data-urlencode "status=1"
```

只改开关状态时不用带其它字段：

```bash
# 停用：将 xx 通道给关了 / 关闭 / 停掉
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/edit" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelCode=22222222222222222222222222bbbbbb" \
  --data-urlencode "status=0"

# 启用：将 xx 通道开启 / 打开
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/edit" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelCode=22222222222222222222222222bbbbbb" \
  --data-urlencode "status=1"
```

关于 `status` 的四条约定：

- **`status` 只能传数字**（`0` / `1`）。传空串、`true` 之类的非数字值不会得到业务错误码，而是服务端异常——遇到这种情况改参数，不要重试。
- **停用当前正在用的通道 = 自断推送**：未启用（`0`）的通道在推送侧直接返回「通道未开启」，而服务端**不阻止**你停用自己（对「当前通道」的保护只有删除那一处）。改状态前先按 5.1「当前通道怎么找」确认目标不是当前通道；恢复就是再传一次 `status=1`。
- 另有两种服务端会自动处理状态的情况，不必手动干预：处于暂停态的通道在修改后会被拉回已启用；已经停用的通道再次停用会返回未授权。

### 5.4 删除非当前通道

用户话术示例：「删掉那条没用的测试通道」「把那条旧的 webhook 通道删了」。

`POST https://www.phprm.com/oauth2/push/channel/deleteChannel`

| 名称 | 必填 | 说明 |
|---|---|---|
| `channelCode` | 是 | 目标通道码（32 位，取自 5.1）；等于当前凭证通道时报「不能删除当前应用绑定的通道」，不同组时报「只能删除同组通道」 |

```bash
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/deleteChannel" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelCode=22222222222222222222222222bbbbbb"
```

**删除不可恢复**，同组成员与历史消息一并失效。执行前先用 5.1 复核 `channelCode`。

🚫 **禁止删除 `${PHPRM_CHANNEL_CODE}` 对应的那条通道**（它正是当前凭证在用的通道）。服务端会拦，返回「不能删除当前应用绑定的通道」；收到这个响应就停止，**不要换 `channelCode` 重试或换凭证绕过**。

### 5.5 重置通道

用户话术示例：「重置一下这条通道的通道码」「这条通道的码可能泄露了，换一个新的」「帮我轮换当前通道的凭证」。

`POST https://www.phprm.com/oauth2/push/channel/resetChannel`

| 名称 | 必填 | 说明 |
|---|---|---|
| `channelCode` | 是 | 目标通道码（32 位，取自 5.1）；缺失或长度不是 32 位返回「channelCode 参数缺失或非法」；目标通道不存在返回「通道不存在」；不同 `pid` 返回「只能重置同组通道」 |

⚠️ **没有「不能重置当前通道」这道保护**——传自己的 `channelCode` 同样会成功（服务端只校验存在 + 同组）。这既是轮换自身凭证的唯一途径，也是最危险的误操作来源：执行后必须立刻把新码写回 MCP Header。

```bash
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/resetChannel" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelCode=22222222222222222222222222bbbbbb"
```

成功返回 **新通道码字符串**：

```json
{"code": 0, "message": "RESET_SUCCESS", "data": "33333333333333333333333333cccccc"}
```

这也是 SKILL.md 里「通道码仅在重置后需要替换」的来源。想轮换自己正在用的凭证时，本接口是唯一途径 —— 换完立刻把 `data` 里返回的新码写进 `X-Push-Channel-Code`，中间这段时间的推送请求会被服务端判为无效通道码。

**成功之后按目标是不是当前通道分两条路**（当前通道按 5.1「当前通道怎么找」认：先比 `data.channelCode`，再比 `data.rows[].channelCode`）：

| 目标 | 要改 `${PHPRM_CHANNEL_CODE}` 吗 | 必做 |
|---|---|---|
| 当前通道 | 要 | ① 在对话里把新码原样告诉用户 ② 自己尝试把本地 MCP 配置中 `push-server` 的 `X-Push-Channel-Code` 改成新码 ③ 改不了就明确告诉用户改哪个文件的哪个字段 ④ 提醒重连 MCP 才生效 ⑤ 发一条极简推送验证 `code:0` |
| 其它通道 | 不动 | 新码归目标通道所有；需要往它推送时用工具入参 `channelCode` 临时指定即可，客户端 Header 保持不变 |

重置后写回新码的步骤见本节（5.5）表格；SKILL.md 的「安全红线」与「成功判定与失败处理」也有相关约束。

### 5.6 修改成员昵称

用户话术示例：「把这条通道的推送人昵称改成构建机器人」「改一下浏览器通道那个成员的昵称」。

`POST https://www.phprm.com/oauth2/push/channel/member/edit`

| 名称 | 必填 | 说明                                                                        |
|---|---|---------------------------------------------------------------------------|
| `channelMemberRelId` | 是 | 成员 ID，只能取自 5.1 `data.rows[].channelMemberRelId`（子通道创建人, 目前仅支持修改浏览器通道成员昵称） |
| `nickname` | 是 | 新昵称；空白串视为缺失，返回参数错误。服务端限制最长 16 个字符                                         |

```bash
curl --location --request POST "https://www.phprm.com/oauth2/push/channel/member/edit" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}" \
  --data-urlencode "channelMemberRelId=1234567890" \
  --data-urlencode "nickname=构建机器人"
```

> 成员侧只有这一个接口：没有成员分页、没有删除成员，其它成员操作（拉黑/恢复、删除、邀请加入、批量处理）都只能去官网控制台。

### 5.7 pushType 枚举表

`pushTypeName` 为枚举名小写，`pushTypeDesc` 为描述，两者都由服务端按下表填充：

| `pushType` | `pushTypeName` | `pushTypeDesc` |
|---|---|---|
| 1 | `website` | 浏览器 |
| 6 | `enterprise_wx_push` | 企业微信群机器人 |
| 7 | `ding_talk_push` | 钉钉群机器人 |
| 8 | `lark_push` | 飞书群机器人 |
| 10 | `multi_channel_push` | 组合 |
| 11 | `web_hook_push` | webhook推送 |
| 16 | `bark_ios_push` | BARK |
| 29 | `telegram_push` | Telegram |
| 30 | `discord_push` | Discord |
| 50 | `official_email` | 官方邮件 |
| 51 | `qq_email` | QQ邮箱 |
| 52 | `netease_three_email` | 163邮箱 |
| 53 | `netease_two_email` | 126邮箱 |
| 54 | `sohu_email` | 搜狐邮箱 |
| 55 | `china_mobile_nine_email` | 139邮箱 |
| 56 | `china_telecom_nine_email` | 189邮箱 |
| 57 | `sina_email` | 新浪邮箱 |
| 58 | `aliyun_email` | 阿里云邮箱 |

未在上表中的编码属于服务端尚未支持的类型，接口会当作无效类型处理。

### 5.8 通道状态（status）

`channel/list` 返回的 `status` 与 `channel/edit` 的入参 `status` 取值一致：

| `status` | 含义 | 对 agent |
|---|---|---|
| `1` | 已启用，正常接收推送 | ✅ 可传 |
| `0` | 未启用（手动停用），往它推送返回「通道未开启」 | ✅ 可传 |

即：**agent 只在 `0` / `1` 之间切换**，其它取值不属于 agent 的能力范围。

### 5.9 「推送到 xx 通道」时该用哪个通道码（判定顺序，命中即停）

用户话里的「xx 通道」可能是**通道码**、**推送类型**、或**通道名**。目标是把它变成 `send_push_message` / `send_multi_message` 的 `channelCode` 入参。**只能走下面四条路之一：禁止自己拼码、禁止拿 ping 里的示例通道码顶替、禁止拿 `${PHPRM_CHANNEL_CODE}` 顶替。**

**一次性配置建议**（能省掉后面绝大多数查列表）：在官网复制**组合类型（`pushType=10`）父通道**的 32 位通道码作为 `${PHPRM_CHANNEL_CODE}`，并把浏览器 / 钉钉 / 邮箱等子通道挂在它下面——往父通道推一次，它下面所有子通道都会收到。

判定用的正则：`^[0-9a-fA-F]{32}$`（32 位十六进制，小写）。

| 步骤 | 命中条件 | 该做什么 | 要先 `get_access_token` + `/channel/list` 吗 |
|---|---|---|---|
| 1 | `xx` 匹配正则，**且不等于** `${PHPRM_CHANNEL_CODE}` | 它就是目标通道码，作为 `channelCode` 直接推送 | **不需要**，直接推 |
| 2 | `xx` 匹配正则，**且等于** `${PHPRM_CHANNEL_CODE}` | 走默认通道推送，不传 `channelCode`（Header 里已经是它） | **不需要**，直接推 |
| 3 | 不匹配正则，但 `xx` 命中 5.7 表的 `pushTypeDesc` 或 `pushTypeName`（如「浏览器」/ `website`） | 取表里对应的 `pushTypeName`，调 `GET /oauth2/push/channel/list?pushTypeName=website` | 需要 |
| 4 | 不匹配正则，也没命中 5.7 表 | 把 `xx` 当通道名：`GET /oauth2/push/channel/list?channelName=xx`（模糊匹配） | 需要 |

第 3 / 4 步拿到 `rows[]` 之后，按条数收尾：

- **1 条**：直接取它的 `channelCode` 推送。
- **多条**：把候选的 `channelName` + `pushTypeDesc` 列给用户选一条，或请用户给出完整通道名后再查一次。**不要自己挑一条、不要并发推多条。**
- **0 条**：如实告诉用户没有这个通道。**不要**退回 `${PHPRM_CHANNEL_CODE}` 顶替，也不要顺势新建（新建要先问，见 5.2）。
- `pushTypeName` 传了枚举外的值（例如「微信」，正确写法是「企业微信群机器人」）会返回「pushTypeName不在支持范围内」→ 改走第 4 步按名字查，不要重试同一个值，建议修改通道名后按 `channelName`进行精准匹配。

三个例子对号入座：

| 用户的话 | 命中 | 动作 |
|---|---|---|
| 「推送到 4d05f4abdb0a0c2a0269900809946903」 | 步骤 1（32 位码，且不是默认码） | 直接把它作为 `channelCode` 推送，**不取令牌、不查列表** |
| 「推送到浏览器通道」 | 步骤 3（`pushTypeDesc` = 浏览器） | `pushTypeName=website` 查列表，取 `rows[].channelCode` |
| 「推送到采集入库通道」 | 步骤 4（既不是码、也不是类型） | `channelName=采集入库` 模糊查列表，取 `rows[].channelCode` |

步骤 1 的入参示例（`send_push_message`）：

```json
{
  "channelCode": "4d05f4abdb0a0c2a0269900809946903",
  "head": "采集结果已就绪",
  "body": "{\"title\":\"xxx\",\"items\":[{\"id\":1,\"name\":\"示例\"}]}"
}
```

`send_multi_message` 同理：在 `messages[]` 的每一项里放该项自己的 `channelCode`，不传的那项走 Header 默认通道。

## 6. 常见错误码处理

### 6.1 按接口预期的失败响应（用例对照用）

| 接口 | 预期失败 `message` | 触发条件                                               |
|---|---|----------------------------------------------------|
| 全部写接口 | `通道不存在` | 令牌对应的通道已被删除（五个 member/channel 接口都先做这一步）        |
| `member/edit` | `channelMemberRelId 参数缺失或非法` | 未传或不是整数                                            |
| `member/edit` | `nickname 参数缺失或为空` | 未传，或去掉前后空白后为空                         |
| `channel/add` | `channelName/pushType 参数缺失或非法` | 任一缺失（空白 `channelName` 同样算缺失）                       |
| `channel/edit` | `channelCode 参数缺失或非法` / `通道不存在` / `只能修改同组通道` | 依次发生；`status` 不是 `0` / `1` 时同样按参数错误返回，非数字则直接抛解析异常        |
| `channel/deleteChannel` | `channelCode 参数缺失或非法` → `不能删除当前应用绑定的通道` → `通道不存在` → `只能删除同组通道` | 注意**先**判自身再判存在/同组                                  |
| `channel/resetChannel` | `channelCode 参数缺失或非法` → `通道不存在` → `只能重置同组通道` | 没有「不能重置当前通道」这一环                                    |
| `message/detail` | `messageId 参数缺失或非法` | `messageId` 未提供或非整数                                |
| `channel/list` | `pushTypeName不在支持范围内` | `pushTypeName` 既不是枚举名也不是中文描述（如「微信」这类要写全「企业微信群机器人」） |

写操作的成功分支统一是 `{"code":0,...,"data":true}`；**只有 `resetChannel` 的 `data` 是新通道码字符串**。

### 6.2 处理建议

| 现象 | 原因 | 处理 |
|---|---|---|
| 401 / `invalid_token` | 令牌已过期 | 重新调用 `get_access_token` 后重试 |
| `Requested scope is out of the client's registered scopes` | 申请的 scope 超出通道客户端登记范围 | 去掉该 scope，或在控制台给该客户端补登记 |
| 非 0 业务码 + 空 `data` | 通道不存在/无权限/参数非法 | 按返回的 `message` 提示处理，不要重试同一份参数 |
| 分页返回空 `rows` | 该通道暂无数据，或 `page` 超出总页数 | 先 `total` 校验页数再翻页 |
| 「XXX 参数缺失或非法」 | 必填参数没传或不是数字/不是整数 | 核对参数名与类型；这类响应是刻意的业务码，不是 500 |
| 「channelCode 参数缺失或非法」 | 未提供，或长度不是 32 位 | 传 `channel/list` 返回的 `channelCode`（32 位十六进制字符串，不是数字 ID） |
| 「通道不存在」 | 目标已删除，或该通道码不属于该组 | 重新拉一次列表 |
| 「只能修改/删除/重置同组通道」 | 目标通道与当前凭证通道 `pid` 不同 | 选同一父通道下的 `channelCode` |
| 「不能删除当前应用绑定的通道」 | 试图删除令牌所属的通道 | 换通道先换凭证；当前通道不能自删（**仅删除有此保护**） |
| 重置后推送全部失败 | 旧通道码已失效，且服务端不会拦自己重置自己 | 用返回的新通道码替换客户端 Header 中的 `X-Push-Channel-Code`；这一步漏了，后续所有推送都以鉴权失败告终 |
