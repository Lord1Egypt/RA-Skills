---
name: push-server
slug: push-server
displayName: 一封传话推送
display_name: 一封传话推送
display_name_en: Aggregated Push
summary: 通过 push server MCP 向用户推送通知（批量采集时可一次推多条webhook）并用短期令牌回查消息
homepage: https://push.phprm.com/mcp.html
tags: [push, notification, mcp, webhook]
license: MIT
description: Send push notifications to users via the push server MCP, push one message per source of a batch collection with send_multi_message, query pushed messages through OAuth2 HTTP APIs, or onboard a personal channel without registration via create_auth_session + poll_auth_session (Gitee / GitHub / Feishu / DingTalk login). Use this skill when a task result must be reported, an important Markdown/JSON notification must reach the user's IM client, browser or webhook API, a batch collection must fan out to one message per source, pushed messages need to be listed or opened, channels need managing, or the user has no channel yet and needs a registration-free onboarding. (Head + Markdown/JSON body, optional jump link; emoji formatting rules for human-readable messages.)
description_zh: 通过 push server MCP 向用户推送消息通知或将抓取内容推送至业务服务器；支持 send_multi_message 在批量采集时按来源推送多条（可各带自己的通道码）、用 OAuth2 HTTP 接口查询历史消息，并可经 create_auth_session + poll_auth_session 免注册开通本人通道（Gitee / GitHub / 飞书 / 钉钉 登录授权）。当需要向用户 IM 客户端、浏览器或 webhook API 发送 Markdown/JSON 格式的重要通知、批量采集需按来源逐条推送、需拉取/查看已推送消息、或要免注册开通道时使用本技能。（标题 + Markdown/JSON 正文，可选跳转链接；人读消息用 emoji 提升扫读效率）
description_en: Push message notifications to users through the push server MCP, push scraped content to a business server, fan out several messages of a batch collection via send_multi_message, read back message history over OAuth2 HTTP APIs, or onboard a personal channel registration-free via create_auth_session + poll_auth_session (Gitee / GitHub / Feishu / DingTalk login). Use this skill when an important notification in Markdown or JSON format must reach the user's IM client, browser, or webhook API, when a batch collection needs one message per source, when past pushed messages need to be listed or opened, or when a user with no channel yet needs to be onboarded without registering on the website. (Head + Markdown/JSON body, optional jump link; emoji formatting rules for human-readable messages.)
category: utilities
version: 1.6.3
author: teakong
---

# 一封传话推送

> **优先级总则**：本文件所有规范（emoji 用法、单条还是多条、Markdown 与 JSON 的选择、body 结构、示例）都是**用户没表态时的缺省基线**。用户一旦明确偏好（如「不要 emoji」「分开推送」「就要表格」），以用户为准，冲突规则自动让位；没提的部分仍按缺省。

通过 `push-server` MCP 向用户汇报任务成果、向通知通道（IM 客户端、浏览器、webhook API）发送重要通知，把抓取内容以 JSON 推到用户自己的业务服务器，或用短期令牌经 HTTP 接口回查历史消息。

## 工具分工

| 工具 | 用途 |
|---|---|
| `send_push_message` | 推送一条消息，绝大多数场景用它 |
| `send_multi_message` | 仅批量采集/跨通道，一次 1~32 条，每条可带自己的通道码 |
| `get_access_token` | 用通道码换短期令牌，供后面的 HTTP 业务接口 |
| `create_auth_session` / `poll_auth_session` | 免注册开通道（见「免注册获取通道码」），不需要通道码 |

> 前三个只认 Header `X-Push-Channel-Code`；HTTP 业务接口只认 `Authorization: Bearer <access_token>`。**通道码不能当 Bearer 用，令牌也不能拿去推送。**

## 何时调用

- 当用户明确要求发送通知或汇报执行结果时。
- 用户**还没有通道码、又不想去官网注册**时 → 用 `create_auth_session` + `poll_auth_session` 让 Agent 免注册开通一条本人通道，详见「免注册获取通道码」。
- 用户**明确要求分开推**时（「分别推送」「分开推送」「每个 X 单独推一条」「一条一条发」「这个单独发我」）→ `send_multi_message`，照做。**不要替用户合并成一条。**
- **批量采集**时（一批并列结果每条各推一条，如「批量采集这 20 个页面」），或需要把结果同时推送到不同通道（不同通道码）时 → `send_multi_message`。
- 用户要求「整理成表格」「做成报告」「汇总给我」时 → **单条 `send_push_message`，body 写 Markdown 表格**。表格是用来横向对比的，拆成多条就废了。
- 需要把采集到的结构化内容以 JSON 推送到用户自己的服务器（webhook 通道）时。
- 需要列出或打开已推送过消息（分页、详情）时 → 先取令牌，再用 HTTP 接口。
- 需要管理通道本身时（看下有哪些通道、改成员昵称、新增/修改/删除/重置通道）→ 先取令牌，再用 HTTP 接口，规则详见 [references/api.md](references/api.md)。

## 参考文件（按需读取）

| 要什么 | 读哪个 |
|---|---|
| 结构化数据落库（JSON 写法） | [references/example.md](references/example.md) 第 1 节 |
| 场景模板（采集/告警/CI/订单等 11 类） | example.md 第 2~12 节（第 13 节反例） |
| 通道管理 / 消息回查 / 字段枚举错误码 | [references/api.md](references/api.md) |

组装内容前先看 example.md 最接近的场景照改，比从零写快也不易漏「head 结论先行」「📌 下一步」。

## 配置（用户必读）

安装 skill ≠ 配置通道，必须先完成两步，否则无法推送：

1. 在 [一封传话](https://push.phprm.com/mcp.html) 注册并建推送通道，获取 32 位通道码。（不想注册？走「免注册获取通道码」。）
2. 在 AI 助手添加远程 MCP（Streamable HTTP 类型），填入：

```json
{
  "mcpServers": {
    "push-server": {
      "url": "https://www.phprm.com/services/push/mcp",
      "headers": {
        "X-Push-Channel-Code": "${PHPRM_CHANNEL_CODE}",
        "X-Mcp-Source": "trae"
      }
    }
  }
}
```

- **名称**固定 `push-server`；**URL** 如上；**Headers**：`X-Push-Channel-Code` 32 位通道码（必配，否则收不到），`X-Mcp-Source` 客户端标识（可选，如 `trae`/`workbuddy`/`coze`，仅服务端日志区分来源）。
- **传输类型** Streamable HTTP（非 SSE）。部分客户端需显式 `"type": "streamable-http"`（多数）或 `"streamableHttp"`（WorkBuddy 驼峰），不认该字段就整行删掉。

> MCP 端点**匿名可连接**：没配通道码也能连上并列出 5 个工具（2 推送 + 1 令牌 + 2 免注册）。**工具列表出现 ≠ 凭证有效**，只有真推送成功才算。排查时直接核对 Header 名与通道码是否被真正替换，别反复重连服务器。

## 免注册获取通道码

给没账号、不想注册官网的用户，`create_auth_session` + `poll_auth_session` 两个工具现场开一条**本人**系统预设通道。**授权只发生在用户浏览器与官网之间，Agent 全程不碰任何第三方 code/token，只回传一封传话自己的通道码。**

流程：1) 先问登录方式，调 `create_auth_session(provider=…)` 得 `sessionId`+`authUrl`（600 秒有效）；2) 用浏览器打开 `authUrl` 完成第三方授权；3) 用 `sessionId` 轮询 `poll_auth_session`：`pending` 按 `pollInterval` 等，`success` 时把返回的 `channelCode` 写入 `X-Push-Channel-Code`（客户端不自动写时用返回的 `mcpConfig`），`expired`/`consumed`/`failed` 立即停止重开。

`provider` 枚举以 `tools/list` 返回的 `inputSchema.provider.enum` 为准（当前 `feishu`/`dingtalk`/`gitee`/`github`，服务端可扩，勿硬编码校验）。

**红线**：绝不索要、记录或转发任何第三方 code/access_token；`sessionId` 一次性、无凭证价值，领码即弃。

## 凭证模型

| 场景 | 入口 | 凭证 |
|---|---|---|
| 推送单条 | MCP `send_push_message` | Header `X-Push-Channel-Code` |
| 推送多条 | MCP `send_multi_message` | Header `X-Push-Channel-Code` |
| 换令牌 | MCP `get_access_token` | Header `X-Push-Channel-Code` |
| 业务 API | HTTP `/oauth2/push/*` | `Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}` |
| 健康自检 | HTTP `/services/public/ping` | 无 |

- **通道码** 32 位长期凭证，仅出现在 MCP Header/入参；重置后才需换。
- **access_token** 短期（默认 `expires_in` 7200 秒=2 小时），是 **RS256 JWT**（`eyJ` 开头三段式），直接当不透明字符串用，别校验前缀/长度/验签。
- **一轮任务只取一次令牌并复用**（9 个接口认同一 Bearer），按 `expires_in` 缓存、留 60~120 秒余量；别持久化。`401/403` 才是失效信号（「令牌不正确」也可能出现在「当前令牌主体不是浏览器子通道」时，重取无用，别循环重试）。

## ping 示例通道（可借用）

`/services/public/ping` 匿名，返回 `rows` 公开示例通道（字段同 `channel/list`，含 `pushUrl`/`qrCodeUrl`/`channelMemberRelId`）。`pushUrl` 打开即该通道**分享/管理页（share.html）**；`qrCodeUrl` 扫码即手机**推送记录页**。给「在哪看消息」入口时优先用这两个字段，别自己拼 URL。

- 它是别人的公开示范通道，任何人可往里推，**绝不能当自己默认通道**，更别填 `${PHPRM_CHANNEL_CODE}`。
- 唯一允许用途：用户明确同意后做一次链路自测；成功即结束，别把正式通知发这里。常规推送仍用用户本人通道码。

## 业务 API（HTTP）

除 ping 外全是 `/oauth2/push/*`：**先 `get_access_token` 换令牌 → 带 `Authorization: Bearer` 调用**，令牌一轮只取一次。

调用约定：参数只认 query 或 form-urlencoded（JSON body 被忽略）；错误一律 HTTP 200 + 非 0 业务码，靠 `code` 判定，仅 `401/403` 是令牌失效；归属由令牌自身决定；别跟控制台 `/services/push/*` 混用。写操作成功 `{"code":0,"data":true}`，两例外：`resetChannel` 的 `data` 是新通道码；`channel/add` 的 `data` 是含 `channelCode` 的新通道对象（可直接当 MCP 凭证）。

| 用途 | Method | Path | 参数 | 成功 `data` |
|---|---|---|---|---|
| 健康自检（匿名） | GET | `/services/public/ping` | 无 | `{status,service,rows}``（`rows` 为示例通道，见「ping 里的示例通道」） |
| 消息分页 | GET | `/oauth2/push/message/page` | `page`,`limit`(缺省1/10) | 分页对象 |
| 消息详情 | GET | `/oauth2/push/message/detail` | `messageId` | 单条+`viewCount` |
| 通道列表 | GET | `/oauth2/push/channel/list` | `channelName`,`pushTypeName` | 父通道+`rows`（浏览器子通道另带 `pushUrl` / `qrCodeUrl`） |
| 新增通道 | POST | `/oauth2/push/channel/add` | `channelName`,`pushType` 必填；`webhookUrl`/`signSecret` 可选 | 新通道对象 |
| 修改通道 | POST | `/oauth2/push/channel/edit` | `channelCode`+字段，含 `status`（`1` 启用 / `0` 停用） | `true` |
| 删除通道 | POST | `/oauth2/push/channel/deleteChannel` | `channelCode` | `true` |
| 重置通道 | POST | `/oauth2/push/channel/resetChannel` | `channelCode` | **新的通道码字符串** |
| 改成员昵称 | POST | `/oauth2/push/channel/member/edit` | `channelMemberRelId`,`nickname`(≤16) | `true` |

字段/枚举/边界细则见 [references/api.md](references/api.md)，做通道操作前先读。

## 执行步骤

1. **确认通道码**：占位符未解析且用户没给时，向用户索取本人 32 位码，**不猜、不用别人通道码**；拿到后默认显式传 `channelCode`**——远端 schema 把 `channelCode` 列进了 `required`，无条件传可以避免客户端的严格校验卡住这一步（详见「工具参数」）。
2. **选工具**：默认单条 `send_push_message`。升多条仅三种：用户要分开推 / 批量采集 / 发到不同通道。表格报告走单条 Markdown 表格。显式措辞优先。
3. **组装**：`head`(≤200 纯文本)、`body`(≤50000，Markdown/JSON)、`url`(≤500)。webhook 入库 → `body` 裸 JSON 零 emoji，字段对齐对方表、带批次号与采集时间；人读 → head 前置结论 emoji，body 用状态灯/结果符排版（见下节）。简单结果可只给 `head`。
4. **发送前清洗（强制）**：URL 外层反引号会污染接收端 showdown 渲染时的 `href`/`src`，导致链接点不动/图片裂图。逐条把 `body`/`url` 中 `` `https://...` `` 与 `](`https://...`)` 形式都去掉外层反引号。反例 `点[详情](`https://...`)`，正例 `点[详情](https://...)`。反引号只用于文件名/命令/代码标识。
5. 调用已注册的 `push-server` MCP 工具（本 skill 不是服务器，不能把 skill 名当 server 调）。
6. 成功：`{"code":0,...}` 且 `data.messageIdList` 非空；`send_multi_message` 任一失败即整次失败。
7. 回看历史推送内容：先 `get_access_token` 再调 [references/api.md](references/api.md) 的分页/详情。

## 工具参数

`channelCode` 远端 schema 标为 `required`、Header 预置时可省——两说并存，严格客户端可能仍报缺参。**始终显式传 `channelCode`**（与 Header 同源）。`body` 支持 Markdown/纯文本/JSON，按字符串原文转发、不在服务端解析（不支持 HTML 是渲染侧约束，非传输侧）。

### send_push_message
| 字段 | 必填 | 说明 |
|---|---|---|
| `head` | 是 | 标题，纯文本，支持 Unicode ≤200 |
| `body` | 否 | Markdown/JSON ≤50000（不支持 HTML）；JSON 用于 webhook，按字符串原文转发、不渲染 |
| `url` | 否 | 跳转链接 ≤500 |
| `channelCode` | 条件 | 覆盖 Header；不传用 `X-Push-Channel-Code` |

### send_multi_message
| 字段 | 必填 | 说明 |
|---|---|---|
| `messages` | 是 | 数组，1~32 项，每项 `{ head 必填, body, url, channelCode }` |
| `messages[].head` | 是 | 同上，逐项必填 |
| `messages[].channelCode` | 否 | 该项单独指定通道；不传则用工具级 `channelCode` / Header 通道码 |
| `channelCode` | 条件必填 | 工具级默认通道；不传则用 Header |

> 任一条失败整次失败；超 32 条拆多次。默认单条，表格报告一律单条。

### get_access_token
| 字段 | 必填 | 说明                      |
|---|---|-------------------------|
| `channelCode` | 条件 | 不传取 Header `X-Push-Channel-Code` |
| `scope` | 否 | 已登记 scope 子集，服务端默认 `basic` |

`expires_in` 是秒数（默认 7200=2 小时），据此决定何时重取，别臆测成几分钟。同一张令牌可连续调多个业务接口。

### create_auth_session

> **授权仅发生在用户浏览器与官网之间**，Agent 全程不接触第三方 `code`/`access_token`，只回传一封传话自己的通道码。完整流程见「免注册获取通道码」。

| 字段 | 必填 | 说明 |
|---|---|---|
| `provider` | 是 | 登录方式，以 `tools/list` 枚举为准（feishu/dingtalk/gitee/github），勿硬编码 |

返回 `{ sessionId, authUrl, expiresIn }`（会话默认 600 秒有效）。`authUrl` 用系统浏览器打开，或作为可点击链接给用户，让他在浏览器里完成第三方授权。

### poll_auth_session
| 字段 | 必填 | 说明 |
|---|---|---|
| `sessionId` | 是 | 上一步返回的会话 ID |

按返回的 `pollInterval` 轮询，三种终止态：

| 状态 | 处理 |
|---|---|
| `pending` | 按 `pollInterval` 继续轮询 |
| `success` | 服务端已把**只发一次**的本人通道码发回来。立刻把 `channelCode` 写进 `X-Push-Channel-Code`；客户端不会自己写配置时，直接用返回的 `mcpConfig`（按 `X-Mcp-Source` 对齐该客户端原生形状） |
| `expired` / `consumed` / `failed` | 立即停止，提示用户重新调 `create_auth_session` |

## 内容排版：emoji 可读化

> 本节为缺省偏好，用户说「不要 emoji」等时按用户来。

**先判去向**：`body` 是 JSON（webhook 入库）→ head/body **都不加** emoji（接收方解析/入库，emoji 污染字段）；其余给人看 → 加。

**head**：`<emoji> + 空格 + 结论短语`，一条一个、结论先行、≤30 字符为宜。

| 场景 | emoji | 示例 |
|---|---|---|
| 成功 / 完成 | 🎉 | `🎉 代码优化完成` |
| 失败 / 崩溃 | 💣 | `💣 构建失败：单测未通过 3 项` |
| 警告 / 阈值告警 | ⚠️ | `⚠️ 磁盘剩余不足 10%` |
| 报告 / 统计 / 周报 | 📊 | `📊 每日情报已生成` |
| 数据采集 | 📥 | `📥 采集完成：128 页` |
| 待确认 / 待办 | 👀 | `👀 需要你确认：合并 PR #42` |

更多场景模板见 [references/example.md](references/example.md) 第 2~12 节。

**body**：状态灯（🟢健康/🟡警戒/🔴危险/⚪未执行）表程度，结果符（✅通过/❌不通过/⚠️有风险）表二元判定，同一条不许混用。清单项 `- ✅ xxx`、指标行 `- 🟢 响应 120ms ｜ 🔴 错误率 3.2%`。

**emoji 红线**：① 不承载唯一信息（写 `❌ 失败` 不写 `❌`）；② 同类语义全篇统一；③ 一行最多一个；④ 不进代码/命令/URL/JSON 字段值；⑤ 老系统显示方框就改纯文本。

## 安全红线

- 通道码仅出现在 MCP Header、工具入参、给用户的回复里；不硬编码进代码/仓库，不写入 head/body/url。
- 推送内容禁止明文密码、令牌、私钥、Cookie；提及只脱敏（「令牌已刷新」而非令牌值）。
- 只用用户本人通道码；`send_multi_message` 逐项复核目标。
- 不把 access_token 写进内容或日志；短期令牌同样不外泄。
- 不删除 `${PHPRM_CHANNEL_CODE}` 主通道（服务端也拒）；删子通道前再向用户确认一次。
- 重置主通道前确认是轮换凭证（不可逆、旧码即废），按 [references/api.md](references/api.md) 5.5 把新码写回 Header，漏一步断推。

## 成功判定与失败处理

- 成功：`{"code":0,...}` 含 `messageIdList`。
- MCP 不可用或返回非 `code:0` → 如实告知失败原因；**不得降级为 HTTP 直推，更不得谎称已发送**。
- 排查按错误驱动，正常流程先直接推送；失败（连接层）→ ping（`alive` 则查凭证/配置；失败则查 URL/网络/传输类型）。ping 与消息接口格式见 [references/api.md](references/api.md)，勿高频轮询。

## 示例

真实推送前先看 [references/example.md](references/example.md)（第 1 节入库完整版，第 2~12 节 11 类人读场景，第 13 节反例）。下面是最小骨架：

**webhook 入库（JSON 零 emoji）**
```json
{ "head": "采集批次 2026-10-03T10:32",
  "body": "{\"batchId\":\"20261003-1032\",\"total\":48,\"items\":[{\"sku\":\"SKU1001\",\"name\":\"降噪耳机\",\"price\":899,\"stock\":132}]}" }
```

**任务汇报（含跳转链接）**
```json
{ "head": "🎉 代码优化完成",
  "body": "## ✅ 优化清单\n- ✅ 性能：P95 降 38%\n- ✅ 稳定性：补异常捕获",
  "url": "https://example.com/pr/123" }
```

其余模板（告警分级、表格报告、批量采集）见 [references/example.md](references/example.md)。

**成功响应**

```json
{"code": 0, "message": "请求成功", "data": {"messageIdList": ["1680030476695388161"]}}
```
