---
name: zhini-ai-assistant
display_name: 知你AI助手-多平台账号客户数据与聊天记录连接器
display_name_en: Zhini AI Assistant
description: "把个微/微信号、企微/企业微信、公众号、小程序、视频号、微信客服、抖音号、小红书、微博、微信小游戏、微信小店、网站/H5 在线客服等平台账号上的客户资料、客服聊天记录与当前/历史会话接入 AI 工具，完成客户查询、会话分析、客户分群、投诉退款研判、销售线索识别与商机跟进，并在用户确认后修改客户资料、添加或移除客户标签、批量发送文本/图片消息。当用户搜索多平台客户查询、聊天记录分析、找高意向客户、客户分群、客户资料修改、客户标签管理或群发触达时使用。"
description_zh: "将个微、企微、公众号、小程序、视频号、微信客服、抖音、小红书、微博、微信小游戏、微信小店、网站及H5客服等平台账号接入知你AI助手后，可用 AI 统一查询这些账号上的客户资料、客服聊天记录与会话，完成客户查询、会话分析、客户分群、投诉退款研判、商机识别、客户资料修改、客户标签管理与主动触达。"
description_en: "Aggregate customer profiles, chat history and live/historical conversations from personal WeChat, WeCom, Official Accounts, WeChat Mini Programs, Channels, WeChat Customer Service, Douyin, Xiaohongshu, Weibo, WeChat Mini Games, WeChat Stores, and website/H5 live chat into AI tools. Use for customer lookup, chat history search, conversation analysis, customer segmentation, lead discovery, customer profile updates, customer tag management and user-confirmed bulk messaging."
examples_zh:
  - 汇总我在个微、企微、抖音、小红书等平台账号上的客户咨询，按平台和意向程度列出本周值得跟进的客户名单。
  - 查看今天各平台账号中正在排队或长时间未回复的客户会话，按等待时长排序，并列出客户名称、所属平台、负责人和最近一条消息。
  - 检索最近90天公众号、小程序、视频号、微信小店和网站客服中涉及投诉、退款或售后的历史会话，读取消息上下文并按问题类型整理证据。
  - 分析最近30天的客户对话，归纳共性问题和产品需求，并按渠道对比差异。
  - 把选定的高意向客户对话批量打开到我的对话，确认后发送跟进文本，并查看群发进度。
  - 把张三的电话改成 13800000000、描述清空，并给确认好的客户批量打上“已回访”标签。
  - 移除某个客户身上已经失效的售后标签。
examples_en:
  - Summarize customer inquiries across my personal WeChat, WeCom, Douyin and Xiaohongshu accounts, and list customers worth following up this week by platform and intent level.
  - Review today's queued or long-unanswered customer conversations across platform accounts, sort them by waiting time, and list each customer, platform, owner and latest message.
  - Search conversations from the last 90 days across Official Accounts, Mini Programs, Channels, WeChat Stores and website support for complaints, refunds or after-sales issues, read the context and organize evidence by issue type.
  - Analyze the last 30 days of customer conversations, summarize common questions and product needs, and compare differences by channel.
  - Open the selected high-intent customer conversations in bulk, send follow-up texts after confirmation, and review delivery progress.
  - Update a customer's phone number, clear their notes, and add confirmed tags to selected customers.
  - Remove obsolete after-sales tags from a single customer.
allowed-tools: "Bash"
version: 1.0.12
author: 知你客服
disable-model-invocation: false
user-invocable: true
---

# 知你AI助手｜多平台账号客户数据与聊天记录连接器

把个微/微信号、企微/企业微信、公众号、小程序、视频号、微信客服、抖音号、小红书、微博、微信小游戏、微信小店、网站/H5 在线客服等平台账号接入知你AI助手后，可以用 Codex、Claude Code、WorkBuddy 等 AI 工具统一查询这些账号上的客户资料、当前与历史会话、客服聊天记录，完成客户分析、客户分群、商机识别与主动触达。

通过 Skill 内置脚本直接调用知你 HTTP 工具 API，查询多平台客户、会话和消息数据，并在用户明确确认后修改客户资料、添加或移除客户标签、批量打开选定对话、发送文本或图片消息。此 Skill 独立运行，不检查、不安装也不依赖 WorkBuddy MCP 连接器。

推荐触发词：多平台客户查询、微信客户、企微客户、公众号客户、小程序客户、视频号客户、抖音客户、小红书客户、微博客户、聊天记录、历史会话、客户分群、销售线索、投诉退款分析、客户资料修改、客户标签管理、主动触达、群发任务、API Key 用量。

## 支持平台账号

个微/微信号、企微/企业微信、公众号/服务号、微信小程序、视频号、微信客服、抖音号、小红书、微博、微信小游戏、微信小店、网站/H5 在线客服。

## 脚本调用

将当前 `SKILL.md` 所在目录记为 `SKILL_ROOT`。所有知你查询统一通过以下命令执行：

```bash
node "<SKILL_ROOT>/scripts/zhini-api.mjs" call TOOL_NAME 'JSON_ARGUMENTS'
```

例如：

```bash
node "<SKILL_ROOT>/scripts/zhini-api.mjs" call zhini_search_customers '{"name":"张三","page":0,"page_size":20}'
```

下文提到“调用 `zhini_xxx`”均表示通过该脚本执行对应 HTTP API，而不是调用 MCP Tool。脚本仅使用 Node.js 内置能力，无第三方依赖。

## 授权引导（首次使用或授权失效时）

发起真实数据查询前执行 `auth status` 检查凭据状态；未配置静态 API Key 时，**优先引导用户走浏览器授权**：

**请先完成授权，否则无法查询数据。** 按下面 3 步操作：

1. 让用户在本机终端执行：

```bash
node "<SKILL_ROOT>/scripts/zhini-api.mjs" auth oauth
```

2. 浏览器会自动打开知你登录页，用户**登录知你账号**（手机号 + 密码）
3. 页面显示「授权成功」后，让用户回我**「已完成」**，我立即重新发起原查询

授权完成后令牌自动缓存与刷新，后续查询无需再次授权；用户回复授权失败时，读取终端里的具体报错并引导重试。

**备选：静态 API Key**（用户明确希望使用 Key 时）：

1. 打开[知你AI助手 API Key 管理页](https://ai.zhinikefu.com/api-key/)。页面要求登录时，使用知你账号登录；新用户切换到“注册”，通过手机号和验证码完成注册。
2. 进入“API Key”页面。已有可用 Key 时点击“复制”；列表为空时点击“新增 API Key”，名称填写 `WorkBuddy`，再点击“创建”并复制完整 Key。
3. 在本机终端运行下面的命令，按提示粘贴 Key。输入过程不回显，凭证保存在当前用户目录的 `.zhini-ai-assistant/api-key` 文件中：

```bash
node "<SKILL_ROOT>/scripts/zhini-api.mjs" auth login
```

也支持由 WorkBuddy 启动环境提供 `ZHINI_API_KEY`；环境变量优先于本地凭证文件。完成任一方式授权后重新执行用户原来的查询。面向用户省略 MCP、连接器、信任操作、本地 MCP 配置和其他服务状态。

## 能力范围

- 客户查询：姓名、手机号、微信号、客服/负责人、渠道、标签、性别、联系人类型和时间范围。
- 平台账号与渠道字典：查询已接入的平台账号、渠道、客服和标签字典，按平台维度筛选与对比。
- 当前队列：等待接待、我的会话、同事会话和 AI 会话的实时快照。
- 历史研判：按客户、消息关键词、消息发送时间、客服、渠道、标签和联系人类型检索历史会话。
- 消息上下文：按会话、客户或消息游标读取消息，并支持时间范围和前后翻页。
- 客户分群：通过标签、渠道、客服、联系人类型、性别或时间条件组合筛选。
- 客户资料维护：在用户明确确认后修改姓名、备注名、电话或描述；未传字段保持不变，空字符串表示清空。
- 客户标签管理：为 1-20 个客户批量添加 1-10 个现有标签，或为单个客户移除最多 10 个标签；只操作客户身上的标签，不删除标签定义。
- 客户触达与消息发送：在用户明确确认后，批量打开选定对话（每次最多 20 个），上传图片并创建最多 100 个 UID、最多 2 条文本/图片消息的异步群发任务，跟踪发送进度并管理历史任务。
- API Key 用量：同时展示账号整体配额和当前请求 API Key 的实时用量。

详细参数、返回字段和错误处理见 `@references/api-spec.md`；常用调用链和结果组织方式见 `@references/examples.md`。

## 意图路由

### 当前会话分诊

1. 用户提到“我的会话、我接待过、我回复过、归属于我”等第一人称归属条件时，先调用 `zhini_get_current_kefu` 获取 `kfid`。
2. 调用 `zhini_list_active_sessions` 获取当前队列快照；该快照用于此刻状态，不承担历史统计。
3. 选定会话后，用 `sid` 调用 `zhini_fetch_messages`，用 `uid` 调用 `zhini_get_customer_profile`。

### 客户查询与画像

1. 客户名、渠道名、客服名或标签名先分别解析为稳定 ID：`zhini_list_channels`、`zhini_list_kefu`、`zhini_search_tags`。
2. 将明确的结构化条件交给 `zhini_search_customers`。至少带一个筛选条件，并从 `page=0` 开始分页。
3. 已知 `uid` 时直接调用 `zhini_get_customer_profile`；需要聊天内容时再调用 `zhini_fetch_messages`。
4. 返回多个候选时保留 `uid`、名称、渠道等核对信息，让用户选择后再深入查询。

### 历史会话研判

1. 按客户、消息关键词或 `msg_stime` 调用 `zhini_search_sessions`。
2. `msg` 只用于召回候选；使用 `zhini_fetch_messages` 读取上下文后再判断诉求、投诉、订单或退款主题。
3. `msg_stime` 表示消息发送时间范围。与非空 `msg` 组合时，关键词历史检索覆盖最近半年；仅使用其他条件时按接口返回范围处理。
4. 需要更多结果时按 `page` 翻页，并输出会话 ID、时间范围和关键证据。

### 客户分群

1. 用户明确提到标签、渠道或客服名称时，先解析为 `tag_id`、`channel_id` 或 `kfid`。
2. 结构化人群使用 `zhini_search_customers`；必须根据聊天内容判断的人群，组合 `zhini_search_sessions` 与 `zhini_fetch_messages`。
3. 标签代表已标注客户，是筛选信号之一；关键词命中也需结合消息上下文确认。
4. 分页查询并记录实际条件、页码和返回数量，避免把单页结果当成完整分群。

### 客户资料维护

1. 确认目标客户 `uid`；只有客户名、手机号、微信号等条件时先用 `zhini_search_customers` 找到候选并让用户确认。
2. 确认要修改的字段和最终值；只支持姓名、备注名、电话、描述，未传字段保持不变，空字符串表示清空。
3. 调用 `zhini_update_customer_profile`，只传用户要求修改的字段；姓名/备注名最多 35 字，描述最多 800 字。
4. 修改后需要核对时调用 `zhini_get_customer_profile`。

### 客户标签管理

1. 添加标签：确认客户 UID 名单和标签后调用 `zhini_batch_set_customer_tags`；单次最多 20 个客户、10 个现有标签。
2. 移除标签：确认单个客户 UID 和标签后调用 `zhini_remove_customer_tags`；单次最多 10 个标签，只取消该客户身上的标签，不删除标签定义。
3. 标签名必须先用 `zhini_search_tags` 或 `zhini_list_tags` 解析为现有 `tag_id`，不得编造标签。
4. 返回 `sync_status=failed` 时说明知你侧已保存但渠道同步提交失败，需要向用户说明。

### API Key 用量

1. 通过内置脚本调用无参接口 `zhini_get_apikey_usage`。
2. `total`、`used`、`remaining` 表示当前 API Key 所属账号整体数据；`current_api_key_used` 表示当前请求 API Key 的实时已使用量。
3. 仅在账号层校验 `total = used + remaining`，不要把 `current_api_key_used` 纳入该等式。
4. 输出额度摘要和数据范围，不展示完整 API Key 或内部鉴权细节。

### 客户触达与消息发送

1. 收件客户必须来自用户明确选定的结果或其他查询路由已核对候选后的确认结果；不要把整批搜索结果或分群直接当作收件人。
2. 用户要集中处理对话时，先展示目标客户清单并确认，再调用 `zhini_open_sessions`（`uids`，每次最多 20 个）把对话打开到当前客服的“我的对话”。
3. 用户要发送图片时，先调用 `zhini_upload_image_for_message_sending` 上传（Base64 解码后不超过 10 MiB，支持 PNG/JPEG/GIF），用返回的 `url` 作为图片消息内容。
4. 首次调用 `zhini_create_message_sending_task` 只准备任务并返回 `confirmation_token`，**不会创建或发送**；向用户完整展示收件客户、任务标题和最终消息内容，确认后用完全相同的内容加 `confirmation_token` 与 `user_confirmed: true` 再次调用才会创建任务。
5. 创建成功后保存 `task_id`，用 `zhini_get_message_sending_task_status` 跟踪进度和逐客户结果；需要查历史群发任务时用 `zhini_list_message_sending_tasks`（支持标题、发送时间范围和分页）；删除前先核对任务并保存所需明细，再用 `zhini_delete_message_sending_task`。
6. 单任务最多 100 个 UID、最多 2 条消息；任务删除不可逆，已发送的消息不会撤回。

## 输出规范

- 说明本次查询覆盖的账号、渠道、时间范围、筛选条件、页码和返回数量。
- 对候选结果保留 `uid`、`sid`、`mid`、`kfid`、`channel_id`、`tag_id` 等证据 ID，区分事实、命中信号与模型归纳。
- 当前队列结果标注为实时快照；历史结果标注消息时间范围和分页信息。
- 查询保持只读；修改客户资料、添加或移除客户标签、批量打开对话与消息发送必须在用户明确确认后执行，输出时保留 `task_id`、任务标题、UID 总数和逐客户发送结果。
- 依据工具实际返回组织答案，不虚构客户身份、消息证据或筛选结果。
