# push-server

一个 [Agent Skill](https://github.com/vercel-labs/agent-skills)，通过 [一封传话](https://push.phprm.com/mcp.html) 的 `push-server` MCP 服务器，让 AI 助手（Trae、Claude、Workbuddy、OpenClaw 等）主动向您汇报任务成果或发送重要通知。

- 纯 MCP 调用，无需脚本与任何运行时依赖。
- **支持把采集结果结构化入库（商业链路）**：`body` 可直接传 JSON，经 Webhook 类型通道**原样转发**到您自己的业务接收端（不参与 Markdown 渲染），落地成商品库、线索库、工单、时序指标等真实数据。AI 负责采集清洗、push-server 负责投递、您的服务端负责入库。
- 支持 Markdown 正文与点击跳转链接，推送到您的浏览器、IM 客户端、邮件等通知通道。
- 支持 `send_multi_message` 一次调用推送多条消息（1~32 条，每条可指定自己的通道码），适合**批量采集**与多步骤汇报。
- 支持查询已推送消息：先用 `get_access_token` 换短期令牌，再调用 `/oauth2/push/message/*` 查分页与详情。
- 支持通道管理：用同一令牌调用 `/oauth2/push/channel/*`，查看下属通道列表、管理成员、**新增/修改/删除/重置通道**（`channel/edit` 可用 `status` 传 `1` 启用 / `0` 停用）；**相同类型（`pushType`）的通道只建一条、够用就复用**，不要把同一类推送拆成多条。成员侧只开放 1 个接口（改昵称），其余成员功能（删除成员、成员列表分页、拉黑/恢复、邀请加入、批量处理）请在官网控制台完成。
- 内置发送前 URL 反引号清洗规则，保证接收端链接可点、图片不裂。

## 安装

通过 [`skills`](https://www.npmjs.com/package/skills) CLI 安装：

```bash
# 安装到当前项目
npx skills add teakong/push-server

# 或安装到全局（所有 agent 可用）
npx skills add teakong/push-server -g
```

## 配置

**安装 skill ≠ 配置通道**，两者互相独立，必须都完成才能推送：

1. 在 [一封传话](https://push.phprm.com/mcp.html) 注册账号并创建推送通道，获取 32 位通道码。
2. 在 AI 客户端添加远程 MCP 服务器。以 Trae CN 为例：AI 侧边对话框右上角 **设置 → MCP → + 添加 → 手动添加**，选择 Streamable HTTP 类型，粘贴下面的 JSON 并替换通道码：

```json
{
  "mcpServers": {
    "push-server": {
      "url": "https://www.phprm.com/services/push/mcp",
      "headers": {
        "X-Push-Channel-Code": "换成你自己的32位通道码",
        "X-Mcp-Source": "trae"
      }
    }
  }
}
```

字段说明：

- **名称**：`push-server`（固定，必须与 skill 中调用的服务器名一致）
- **URL**：`https://www.phprm.com/services/push/mcp`
- **Headers**：
  - `X-Push-Channel-Code`：您的 32 位通道码（必须配置，否则无法接收推送）
  - `X-Mcp-Source`：客户端标识（可选，仅用于服务端日志区分来源，可填 `trae`、`workbuddy`、`coze` 等任意值，按自己的客户端改）
- **传输类型**：Streamable HTTP（不是 SSE）。部分客户端要求 JSON 里显式声明 `type`，两种写法按客户端二选一、不要同时写：`"type": "streamable-http"`（Trae / Cursor / Cline 等多数客户端）或 `"type": "streamableHttp"`（WorkBuddy 等驼峰写法）；不认该字段的客户端整行删掉即可。

Claude Code、Cursor 等其他客户端同理，在各自的 MCP 配置中添加同名 HTTP 服务器即可。配置保存在本地客户端，不会进入任何代码仓库。

> ⚠️ 通道码等同推送凭证，请勿提交进代码库或打印到日志。

### 凭证分工（务必区分）

| 场景 | 入口 | 凭证 |
|---|---|---|
| 推送单条 | MCP `send_push_message` | Header `X-Push-Channel-Code` |
| 推送多条 | MCP `send_multi_message` | Header `X-Push-Channel-Code` |
| 换取令牌 | MCP `get_access_token` | Header `X-Push-Channel-Code` |
| 查询消息等业务 API | HTTP `https://www.phprm.com/oauth2/push/*` | `Authorization: Bearer <access_token>` |
| 健康自检 | HTTP `https://www.phprm.com/services/public/ping` | 无需凭证 |

通道码不能当 Bearer 用，`access_token` 也不能拿去推送。

`access_token` 默认有效期 **7200 秒（2 小时）**，以返回的 `expires_in` 为准。同一张令牌可以在本次任务里连续调用多个业务接口（9 个 `/oauth2/push/*` 都认它），重复调用 `get_access_token` 也不会顶掉旧的 —— 所以一轮任务只在开头取一次即可，不必每个接口前都换。它属于会话级凭证，不要持久化。它的本体是一段 RS256 签名的 JWT（`eyJ` 开头的三段式），不是 `sk-` 之类的前缀串，当不透明字符串用即可。

### 在豆包网页版使用

豆包网页版不支持 `npx skills` 安装技能，但电脑版支持自定义 HTTP 连接器，分两步接入：

1. **添加连接器**：左侧导航「技能·连接器·伙伴」→ 右上角「新建」→「新建自定义连接器」，填写：
   - 服务器名称：`push-server`
   - 传输类型：`HTTP`
   - 服务器 URL：`https://www.phprm.com/services/push/mcp`
   - 自定义 Headers：
     - `X-Push-Channel-Code`：你的 32 位通道码
     - `X-Mcp-Source`：`doubao`
2. **新建专属智能体**：创建一个智能体，把 [SKILL.md](SKILL.md) 的正文（去掉开头 `---` frontmatter）粘贴到「人设与回复逻辑/指令」中，并在技能里勾选刚建的 `push-server` 连接器。之后在该智能体对话中完成任务，它即会按本技能规范主动推送。

> 通道码只填在连接器 Headers 中，不要写进智能体的公开指令。不建智能体也能在对话中直接要求「用 push-server 推送通知」，但规范遵守不如专属智能体稳定。

## 用法

安装并配置好 MCP 后，直接让 agent「任务完成后给我推送一条通知」即可。服务端提供 5 个工具——**3 个正常链路工具**（推送×2 + 令牌×1，按用途分工如下表）和 **2 个免注册工具**（`create_auth_session` / `poll_auth_session`，无通道码也可开通本人通道，详见下方「免注册开通通道」）：

| 工具 | 用途 |
|------|------|
| `send_push_message` | 推送一条消息，绝大多数场景用它 |
| `send_multi_message` | 一次调用推送多条（1~32），每条可指定自己的通道码 |
| `get_access_token` | 用通道码换短期 `access_token`，供 `/oauth2/push/*` 业务接口使用；返回里有 `expires_in`（默认 7200 秒） |

> 这三个工具的 `channelCode` 在远端 schema 里都标了必填，但服务端允许 Header 已预置时省略：Header 未配置时必须显式传；Header 已配置、客户端却仍报缺参时，把同一串通道码显式填进 `channelCode` 即可（值与 Header 一致，不要改配置或换工具）。

**推送单条 —— `send_push_message`**

| 字段 | 必填 | 说明 |
|------|------|------|
| `head` | 是 | 消息标题，纯文本，200 字符以内；人读消息建议前置一个结论 emoji（见「用 emoji 提升可读性」） |
| `body` | 否 | 正文，支持 **Markdown / 纯文本 / JSON**（不支持 HTML），50,000 字符以内；内容为字符串原文转发。JSON 用于 Webhook 通道推送，接收端按原文解析（详见 SKILL.md「工具参数」） |
| `url` | 否 | 点击跳转链接（如 PR 地址、构建日志），500 字符以内 |
| `channelCode` | 条件必填 | 指定通道码，覆盖 Header 中的 `X-Push-Channel-Code`；Header 预置时服务端可省，但远端 schema 标了必填（见下方提示） |

**批量采集时一次推送多条 —— `send_multi_message`**

> 只在三种情况用：**用户明确要求分开推**、**批量采集**（每个来源一条）、**发到不同通道**。用户要「表格 / 报告」时一律走单条 + Markdown 表格。

| 字段 | 必填 | 说明 |
|------|------|------|
| `messages` | 是 | 数组，1~32 项，每项 `{ head, body, url, channelCode }` |
| `messages[].head` | 是 | 逐项必填，规则同单条的 `head` |
| `messages[].channelCode` | 否 | 该条单独指定通道，覆盖工具级 `channelCode` / Header 通道码 |
| `channelCode` | 条件必填 | 工具级兜底通道码，作为所有未单独指定项的默认通道；不传则用 Header（同样 schema 标必填、Header 预置时可省） |

多条并发推送，**任一条失败则整次调用失败**并返回第一条失败原因；超过 32 条需拆成多次调用。

**换取令牌—— `get_access_token`**

| 字段 | 必填 | 说明 |
|------|------|------|
| `channelCode` | 条件必填 | 要换令牌的通道码；不传则取 Header `X-Push-Channel-Code`（schema 同样标了必填） |
| `scope` | 否 | 必须是该通道客户端已登记 scope 的子集；不传则使用服务端默认值 `basic` |

**免注册开通通道（`create_auth_session` + `poll_auth_session`）**

适用于**没账号、不想注册官网**的用户。Agent 现场替他开一条本人系统预设通道，**授权那一跳只在用户浏览器与官网之间完成**，Agent 全程不接触任何第三方 `code` / `access_token`，最终只回传一封传话自己的通道码。

1. 调 `create_auth_session(provider=…)`，**先问用户用哪种登录方式**（`feishu` / `dingtalk` / `gitee` / `github`，以 `tools/list` 返回的 `inputSchema.provider.enum` 为准，不要硬编码）。返回 `sessionId` + `authUrl`（会话 600 秒有效）。
2. 把 `authUrl` 用系统浏览器打开或作为可点击链接给用户，让他在浏览器里完成第三方授权。
3. 用 `sessionId` 轮询 `poll_auth_session`：`pending` 就按 `pollInterval` 继续等；`success` 时把**只发一次**的本人通道码写进 `X-Push-Channel-Code`（客户端不会自己写配置时直接用返回的 `mcpConfig`）；`expired` / `consumed` / `failed` 立即停止，提示重新 `create_auth_session`。
4. **红线**：绝不向用户索要、也不替 Agent 记录或转发任何第三方 `code` / `access_token`；`sessionId` 是单次性的，领到通道码即丢弃。

**先看这条消息给谁。** 第一类是结构化数据落到你自己的业务系统（商业入库链路），第二类是给人看的通知。

采集内容落到业务服务（Webhook 通道，`body` 为 JSON 文本，**不加 emoji**）：

```json
{
  "head": "采集批次 2026-10-03T10:32",
  "body": "{\"batchId\":\"20261003-1032\",\"source\":\"shop.example.com/new\",\"collectedAt\":\"2026-10-03T10:32+08:00\",\"total\":48,\"items\":[{\"sku\":\"SKU1001\",\"name\":\"降噪耳机\",\"price\":899,\"stock\":132},{\"sku\":\"SKU1002\",\"name\":\"机械键盘\",\"price\":459,\"stock\":3}]}"
}
```

`head` 也是纯文本（接收端常拿它当批次号或去重键入库），`body` 必须是裸 JSON、不能包 Markdown 围栏。多源批量入库、线索入库、监控与舆情批次的完整写法见 [references/example.md](references/example.md) 第 1 节。

简单任务可以只提供 `head`：

```json
{
  "head": "🎉 构建已完成"
}
```

任务汇报示例：

```json
{
  "head": "🎉 代码优化完成",
  "body": "## ✅ 优化清单\n- ✅ **性能**：减少冗余会话查找，P95 下降 38%\n- ✅ **稳定性**：补充异常捕获与重试\n- ⚠️ **兼容性**：旧版客户端需灰度验证",
  "url": "https://example.com/pr/123"
}
```

一次推送多条（批量采集 / 不同通道）：

```json
{
  "channelCode": "换成你自己的32位通道码",
  "messages": [
    { "head": "🎉 构建已完成", "body": "- ✅ 主分支构建 #128 通过\n- 🟢 耗时 3m12s", "url": "https://example.com/build/128" },
    { "head": "⏳ 部署已开始", "body": "预发环境正在部署，预计 5 分钟", "channelCode": "换成你自己的另一个32位通道码" }
  ]
}
```

### 用 emoji 提升可读性

通知栏里纯文本是一片灰，扫读成本高。给人看的消息（Markdown `body` 或不传 `body`）建议：

- `head` 前置**一个**结论 emoji，格式 `<emoji> + 空格 + 结论`，如 `🎉 构建已完成`、`💣 构建失败：单测未通过 3 项`、`⚠️ 磁盘剩余不足 10%`、`🚀 v2.4.0 已发布`、`📥 采集完成：128 页`。
- `body` 用**状态灯**表达程度（🟢 健康 / 🟡 警戒 / 🔴 危险），用**结果符**表达判定（✅ 通过 / ❌ 失败 / ⚠️ 有风险但不阻塞），如 `- 🟢 响应 120ms`、`## ❌ 失败项`。
- **Webhook / JSON 通道一律不加 emoji**——`body` 是数据结构不是文档，emoji 会污染字段值。

完整映射表、补充 emoji 与红线见 [SKILL.md](SKILL.md) 的「内容排版：emoji 可读化」。

## 回查已推送的消息

1. 调用 MCP `get_access_token` 换取短期 `access_token`（`scope` 必须是该通道客户端已登记范围的子集，不传则用服务端默认值 `basic`；`channelCode` 不传则取 Header `X-Push-Channel-Code`）。
2. 用它请求 OAuth2 业务接口：

```bash
curl --location "https://www.phprm.com/oauth2/push/message/page?page=1&limit=10" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"
```

消息详情只需传 `messageId`（来自分页返回的 `rows`）。完整的参数、响应字段与错误码见 [references/api.md](references/api.md)。

## 管理通道

同一个令牌还能管理当前凭证所属的通道：

```bash
# 下属通道列表（不分页；可用 channelName 模糊匹配、pushTypeName 筛选）
curl --location "https://www.phprm.com/oauth2/push/channel/list" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${CHANNEL_ACCESS_TOKEN}"
```

返回的 `data.rows[].channelCode` 可直接当新的 MCP 推送凭证；同一份响应里 `pushType=1`（浏览器）那几行还带 `channelMemberRelId`，即**该子通道创建人的成员 ID**，是改昵称这个唯一成员接口的**入参来源**（没有成员分页接口，也没有删除成员接口），并额外返回 `pushUrl`（浏览器打开即该通道的分享/管理页面）与 `qrCodeUrl`（推送记录页面的二维码，扫码用手机查看推送记录）。此外还有通道新增/修改/删除/重置与改昵称共 5 个接口，参数与约束见 [references/api.md](references/api.md)；新增通道除 `channelName` / `pushType` 外，群机器人类可传 `signSecret` 签名。其中「新增通道」是最后手段：先在上面的列表里找同 `pushType` 的现有通道复用，确实没有再新建。

> ⚠️ 删除通道不可恢复（服务端禁止删除当前凭证绑定的通道，`${PHPRM_CHANNEL_CODE}` 对应的那条永远别删）；重置通道会**立即作废旧通道码**。
> 重置自己的通道是允许的（这也是轮换凭证的唯一途径），但重置后必须：把新码告诉用户 → 自己尝试替换 MCP 配置里的 `X-Push-Channel-Code` → 提醒重连 → 发一条推送验证。重置别人（同组子通道）不用动 Header。

推送失败时不要先猜原因，用匿名健康端点二分定位：

```bash
curl -s https://www.phprm.com/services/public/ping
```

返回 `{"code":0,"message":"ok","data":{"status":"alive","service":"push-server"}}` 说明端点活着，问题在凭证或客户端配置。

该端点还会带回一小段服务端维护的**公开示例通道**（`rows`）：想先验证链路时，可在用户同意后把它的 `channelCode` 通过工具的 `channelCode` 参数传一次做自测，**不要写进 MCP 配置、也不要拿它收正式通知**。

## 工作原理

1. Agent 完成任务后，按 [SKILL.md](SKILL.md) 规范将成果总结为 `head` / Markdown `body`。
2. 组装文案时可参考 [references/example.md](references/example.md)：第 1 类是**结构化数据入库**（Webhook JSON，零 emoji，商业链路主力）；第 2~12 节是 11 类人读场景（签到 / 采集 / 监控告警 / 备份 / CI / 表格报告与批量采集 / 订单物流 / 行情账单 / 快递出行天气 / 安全事件 / 日报周报），第 13 节是反例对照，每类含成功、失败、告警三种分支写法，照骨架改即可。
3. 发送前对每条消息的 `body`、`url` 执行 URL 反引号清洗，避免接收端 showdown 转换后链接失效。
4. 通过 MCP 协议调用 `send_push_message` / `send_multi_message`，由一封传话服务端投递到通道。
5. 服务端返回 `{"code":0, ...}` 且包含 `messageIdList` 即发送成功（多条时是所有消息 ID 的并集）；非 `code:0` 时 Agent 必须如实告知失败原因，不得降级为 HTTP 直调推送或谎报成功。

> **你的偏好优先。** 上面所有规范都只是缺省基线——emoji 用法、单条还是多条、要不要表格、标题怎么写。直接告诉 Agent 你的偏好即可，例如「不要 emoji」「就要表格」「分开推送」「标题别加表情」，与之冲突的缺省规则自动让位，其余没提到的部分按缺省走。
>
> 默认情况下 Agent **推单条**；只有三种情况会用 `send_multi_message`：**批量采集**、**跨通道发送**、**你明确要求分开推送**。而你要表格 / 报告时不会被拆成多条。

## License

MIT
