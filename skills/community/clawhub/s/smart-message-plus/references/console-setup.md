# Console Setup Guide（钉钉/飞书/企业微信后台配置指引）

Everything you must click in the vendor consoles before the CLI works.
Verified against real apps on 2026-07-14 (DingTalk/Feishu) and 2026-07-17 (WeCom).

## 钉钉（open-dev.dingtalk.com）

### 1. 创建企业内部应用
- 开发者后台 → 应用开发 → 企业内部应用 → 创建
- 记录：**Client ID（=AppKey/robotCode）**、**Client Secret**

### 2. 添加机器人能力
- 应用 → 应用能力 → 机器人 → 开启
- 消息接收模式若不需要监听可任意；**修改后必须点「发布」**

### 3. 权限（应用 → 开发配置 → 权限管理）

| 权限 | 用途 | 必需性 |
|------|------|--------|
| Robot 消息相关（默认随机器人能力） | 单聊/群聊/撤回 | 必须 |
| `qyapi_get_department_list` 通讯录部门信息读 | 部门广播 builtin | 广播需要 |
| `qyapi_get_member` 成员信息读 | 部门成员列表 | 广播需要 |
| `qyapi_get_member_by_mobile` 手机号查成员 | `--to 手机号` | 推荐 |
| `qyapi_chat_manage` 群管理 | `--create-group` 建群 | 建群需要（开通即时生效，无需发版） |

### 场景群模板（可选高级路径，控制台常不可用）

钉钉普通群无法通过 API 添加机器人。理论上「场景群模板」可让机器人建群即在群内，但**实测控制台的模板创建页在浏览器中存在 bug**（依赖钉钉客户端 JSAPI，报 `DINGTALK-JSAPI ERROR 4040: notInDingTalk`，「可选应用」下拉无法加载）。若已有可用模板ID：`--create-group <群名> --with-bot --scene-template <模板ID>`（自动记住）。

**推荐做法**：直接建普通群，按建群后 CLI 输出的提醒手动把机器人加进群（群设置→机器人→添加，约30秒），然后 `--save-group` 改存 cid 通道即获全能力。

> 探测时若返回 `errcode=88, subcode=60011`，错误信息里会直接给出**申请链接**，点开即可。

### 4. 发布应用
- 版本管理与发布 → 发布。**开发版仅对开发者生效**，不发布其他人收不到。

### 5. 群聊准备
- 目标群 → 群设置 → 智能群助手 → 添加机器人 → 选你的应用机器人
- 群的 `openConversationId`（`cid` 开头）获取方式：
  a. 开一个临时 Stream 监听，在群里 @机器人 发一条消息，从事件里读 `conversationId`；
  b. 或企业内部应用通过 chatId 转换接口。
- 拿到后保存别名：`--save-group <群名> dingtalk <cidXXX==>`

## 飞书（open.feishu.cn）

### 1. 创建自建应用
- 开发者后台 → 创建企业自建应用
- 记录：**App ID**、**App Secret**

### 2. 权限（应用 → 开发配置 → 权限管理）

⚠️ **注意区分「应用身份」和「用户身份」权限** —— 本 CLI 使用 tenant_access_token，
只认**应用身份**权限。搜权限时看清类型列。

| Scope | 用途 | 必需性 |
|-------|------|--------|
| `im:message`（或 im:message:send_as_bot） | 发消息 | 必须 |
| `im:resource` | 上传图片/文件 | 图文件需要 |
| `contact:user.id:readonly` | 邮箱/手机号→open_id | 推荐 |
| `im:chat:readonly`（或 im:chat） | 群列表/群成员 | 推荐 |
| `im:chat`（应用身份，写权限） | `--create-group` 建群 | 建群需要；变更后须发版 |
| `contact:contact.base:readonly` 等通讯录读 | 部门广播 builtin | 广播需要 |

### 3. 发布版本（关键！）
- 权限**每次变更后**都要：版本管理与发布 → 创建版本 → 发布
- **可用范围**必须包含目标用户（否则单聊直接失败）

### 4. 群聊准备
- 目标群 → 设置 → 群机器人 → 添加机器人 → 选你的应用
- 群 chat_id（`oc_` 开头）：机器人进群后 CLI 侧可通过 `im/v1/chats` 列出
- 保存别名：`--save-group <群名> feishu <oc_xxx>`

## 企业微信（webhook 模式，当前唯一支持模式）

### 接入步骤（30 秒，无需管理后台）

1. 在企业微信里打开任意**纯内部群**（成员全是本企业的；外部群不支持群机器人）
2. 群右上角「···」→ **添加群机器人** → 新建（手机端部分版本无此入口，用 PC 端最稳）
3. 复制 **Webhook 地址**（形如 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx-xxxx-...`）
4. 保存为群别名即可发送：

```bash
$SCRIPT --save-group 告警群 wecom "<webhook地址>"
$SCRIPT --provider wecom --chat-id 告警群 --msg "内容"
```

注意：
- **一个 webhook = 一个群**；要发多个群就保存多个群别名
- 新版「智能机器人平台」的机器人资料页链接（openBotProfile）**不是** webhook，两套体系，别混
- 频率限制：每机器人 20 条/分钟
- webhook key 等同凭证，泄漏者可向群里发任意消息——按密钥对待

### 为什么没有全能力的 wecom-app 模式（重要背景）

企业微信自建应用 API（单聊/通讯录/建群/撤回）要求**企业可信 IP**：

1. 每次 API 调用都校验请求的**真实来源 IP** 是否在白名单（errcode=60020）
2. 配置可信 IP 前必须先设置「可信域名」或「接收消息服务器 URL」
3. **第三方云服务商的出口 IP 会被控制台直接拒绝**（实测腾讯云 IP 提示"以下IP属于第三方服务商，请配置本企业服务器的IP"）

因此托管容器/云环境（没有企业自有出口 IP）**客观无法使用自建应用模式**。若你的运行环境有企业自有服务器出口 IP，可等待/自行实现 wecom-app 模式（账号字段 corp_id / corp_secret / agent_id 已预留）。

## 常见错误速查

| 现象 | 原因 | 处理 |
|------|------|------|
| 钉钉 errcode=88 subcode=60011 | 缺权限 | 错误信息带申请链接，开通即可 |
| 钉钉 staffId.notExisted | userId 不对/不在企业内 | 核对 userId |
| 飞书 99991672 | 缺**应用身份**权限 | 错误信息带直达开通链接；开完记得发版 |
| 飞书 99991663/61 | token 失效 | CLI 自动重取；若持续，检查 Secret |
| 飞书 230020 | 撤回超 24h | 无法撤回，平台限制 |
| 飞书查 email/mobile 返回空 user_id | 目标账号未绑定该邮箱/手机号 | 用别名或群成员反查 |
| 消息 API 成功但人没收到 | 钉钉：查与机器人的单聊会话（可能没弹通知）；飞书：应用可用范围不含目标用户 | 分别检查 |
| 企微 errcode=93000 | webhook 无效/机器人被移出群 | 到群里重新获取 webhook |
| 企微 errcode=45009 | 频率限制（20条/分钟） | 稍后重试 |
| 企微 errcode=60020 | 自建应用可信 IP 校验失败 | webhook 模式不受影响；app 模式需企业自有出口 IP |
