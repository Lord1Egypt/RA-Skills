---
name: AndonQ
description: 腾讯云 AndonQ 工单与智能客服助手 — 不切窗口、不排队，即刻获得腾讯云全产品线专业解答。支持工单查询（列表/详情/流水）、集团工单与需求单管理，以及腾讯云全产品线智能问答。当用户查询工单、查看工单详情、咨询腾讯云产品问题（如 CVM、轻量应用服务器、COS 等）、查询集团工单/需求单，或要求找人工客服时使用。
---

# ☁️ AndonQ — 腾讯云工单与智能客服助手

核心能力：**工单查询**（列表查询、详情查询，TC3-HMAC-SHA256 签名鉴权）+ **智能客服多轮问答**（SSE 流式响应，免鉴权）。工单模块与智能客服完全独立，统一输出格式。

---

## 一、鉴权方式

### 1.1 工单查询（GetMCTicketList / GetMCTicketById）

使用腾讯云 API **AK/SK 签名认证**（TC3-HMAC-SHA256），通过环境变量配置密钥：

- `TENCENTCLOUD_SECRET_ID` — 腾讯云 SecretId（必填）
- `TENCENTCLOUD_SECRET_KEY` — 腾讯云 SecretKey（必填）

密钥获取地址：https://console.cloud.tencent.com/cam/capi

**凭据权限要求**：请使用**最小权限、可随时吊销**的子账号密钥，不要使用主账号密钥。
本 Skill 只需要工单相关的读取权限。

**推荐方式 — 会话级注入（不落盘）**

优先从密钥管理器读取，仅注入当前会话，命令结束即失效：

```bash
# macOS 钥匙串示例
export TENCENTCLOUD_SECRET_ID="$(security find-generic-password -s tencentcloud-secret-id -w)"
export TENCENTCLOUD_SECRET_KEY="$(security find-generic-password -s tencentcloud-secret-key -w)"
```

其他可用方案：`pass`、1Password CLI（`op read`）、HashiCorp Vault、企业密钥管理服务。

**备选方式 — 写入 shell 配置文件（有风险，请知悉后再用）**

若确实需要跨会话持久化，可写入 `~/.zshrc` / `~/.bashrc`：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="your-secret-id"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="your-secret-key"' >> ~/.zshrc
source ~/.zshrc
```

Windows PowerShell（写入用户级环境变量）：
```powershell
[Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_ID", "your-secret-id", "User")
[Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_KEY", "your-secret-key", "User")
```

> ⚠️ **持久化的代价**：这样做会把长期有效的明文密钥留在磁盘上。该文件会被备份、
> 被同步工具上传、被其他本地进程读取，且泄露后不会有任何提示。
> 选择此方式时请确保密钥为最小权限子账号密钥，并定期轮换。
>
> **Agent 不应主动替用户执行写入操作**，应说明两种方式的差异，由用户自行选择。

### 1.2 智能问答（SmartQA）

无需 AK/SK，uin 和 skey 默认为空。直接调用即可。

> ⚠️ **数据出境提示**：SmartQA 会把你输入的问题**以及多轮对话的上下文**发送到
> 腾讯云在线客服服务（`cloud.tencent.com` / `andon.cloud.tencent.com`）进行处理。
> 这些内容离开本地环境，且可能被服务端留存用于客服记录。
>
> 请不要在提问中包含密钥、内部主机名、客户数据或其他敏感信息。
> 首次为用户调用 SmartQA 时，应主动告知这一点。

---

## 二、前置检查

运行需要 AK/SK 的接口前，**必须先确保环境变量已生效**。如果是新会话或环境变量刚写入配置文件，先执行：

```bash
source ~/.zshrc   # macOS / zsh 用户
# 或
source ~/.bashrc  # Linux / bash 用户
```

然后运行环境检测：

```bash
python3 {baseDir}/check_env.py
```

支持参数：
- `--quiet` — 静默模式，仅输出错误信息
- `--skip-update` — 跳过版本更新检查

返回码含义：
- `0` = 环境就绪（密钥配置正常）
- `1` = Python 版本不满足要求（需 3.7+）
- `2` = AK/SK 未配置或无效
- `4` = Skill 版本过旧，需要更新

> **智能问答（SmartQA）无需前置检查**，可直接使用。

---

## 三、可用接口（共 9 个）

### 3.0 GetCurrentTime — 获取当前时间

返回当前时间和常用时间范围预设（最近 7/30/90/365 天），用于构造查询参数。无需鉴权，本地执行。

- **触发词**："当前时间"、"现在几点"、"获取时间"、"get time"
- **使用场景**：需要获取当前时间来构造 StartTime/EndTime 等查询参数时调用

```bash
python3 {baseDir}/scripts/andon-api.py -a GetCurrentTime -d '{}'
```

返回示例：
```json
{
  "success": true,
  "action": "GetCurrentTime",
  "data": {
    "now": "2026-03-24 18:30:00",
    "today": "2026-03-24",
    "timestamp": 1742816600,
    "presets": {
      "last_7d": {"startTime": "2026-03-17 18:30:00", "endTime": "2026-03-24 18:30:00"},
      "last_30d": {"startTime": "2026-02-22 18:30:00", "endTime": "2026-03-24 18:30:00"},
      "last_90d": {"startTime": "2025-12-24 18:30:00", "endTime": "2026-03-24 18:30:00"},
      "last_180d": {"startTime": "2025-09-26 18:30:00", "endTime": "2026-03-24 18:30:00"},
      "last_365d": {"startTime": "2025-03-24 18:30:00", "endTime": "2026-03-24 18:30:00"}
    }
  },
  "requestId": ""
}
```

### 3.1 GetMCTicketList — 查询工单列表

查询**当前账户**下的工单列表，默认按创建时间倒序返回。

- **触发词**：“查询工单”、“工单列表”、“我的工单”、“看看工单”、“有哪些工单”、“list tickets”、“my tickets”
- **详细文档**：使用前加载 `{baseDir}/references/GetMCTicketList.md`

> **数据范围**：默认**只返回当前账号自己的工单**。
> 加上 `--include-organization` 才会同时查询 `DescribeOrganizationTickets`
> 并按 `TicketId` 去重合并，此时返回结果会扩大到**集团范围**的工单，
> 可能包含其他成员的工单标题、UIN 与问题描述。
>
> Agent 不应默认加这个参数。只有当用户明确要求查看集团/成员工单时才使用，
> 并在返回前说明数据范围已扩大。合并模式下任一来源失败会被静默忽略，
> 因此结果可能不完整。

```bash
# 默认查询（最新 20 条，仅本账号工单）
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{}'

# 按状态过滤（待处理 + 处理中）
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{"StatusIdList":[0,1]}'

# 关键词搜索
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{"Search":"CVM","PageSize":10}'

# 显式扩大到集团范围（需用户明确要求）
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{}' --include-organization
```

返回示例：
```json
{
  "success": true,
  "action": "GetMCTicketList",
  "data": {
    "tickets": [{"TicketId": "202603244502", "Question": "CVM 无法登录", "StatusId": 1}],
    "total": 15
  },
  "requestId": "xxx"
}
```

### 3.2 GetMCTicketById — 查询工单详情

根据工单 ID 查询详情，包含沟通记录（Comments）。必填参数：`TicketId`。

- **触发词**：“工单详情”、“查看工单”、“工单进展”、“工单状态”、“这个工单怎么样了”、“ticket detail”、“check ticket”
- **详细文档**：使用前加载 `{baseDir}/references/GetMCTicketById.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketById -d '{"TicketId":"202603244502"}'
```

返回示例：
```json
{
  "success": true,
  "action": "GetMCTicketById",
  "data": {
    "TicketId": "202603244502",
    "Question": "CVM 无法登录",
    "StatusId": 1,
    "Comments": [{"Content": "您好，请检查安全组配置", "Role": "support"}]
  },
  "requestId": "xxx"
}
```

### 3.3 SmartQA — 智能客服问答

调用腾讯云 Andon 智能客服进行产品咨询，支持多轮对话。无需鉴权。

- **触发词**："腾讯云工单"、"腾讯云客服"、"腾讯云智能客服"、"问下客服"、"咨询腾讯云"、"腾讯云怎么..."、"腾讯云如何..."、"CVM怎么..."、"轻量应用服务器..."、"对象存储..."
- **详细文档**：使用前加载 `{baseDir}/references/SmartQA.md`

**单轮问答：**
```bash
python3 {baseDir}/scripts/smartqa-api.py -q "轻量应用服务器如何登录"
```

**多轮对话**（复用 sessionId 和 agentSessionId）：
```bash
# 第一轮
python3 {baseDir}/scripts/smartqa-api.py -q "对象存储COS如何设置跨域访问"
# 返回 sessionId 和 agentSessionId 后，追问
python3 {baseDir}/scripts/smartqa-api.py -q "如果我用的是Python SDK呢" \
  --session-id QT1HHP284PW9 --agent-session-id 1002079011
```

返回示例：
```json
{
  "success": true,
  "action": "SmartQA",
  "data": {
    "answer": "腾讯云服务器（CVM）支持通过控制台和API两种方式重启实例...",
    "intention": "profession",
    "recommendQuestions": ["云服务器如何重启", "轻量应用服务器如何重启实例"],
    "sessionId": "JL7JX8C51GAS",
    "agentSessionId": "1002078124"
  }
}
```

### 3.4 DescribeOrganizationTickets — 集团成员工单列表

查询集团成员的工单列表，支持按时间范围、分页等过滤。

- **触发词**："集团工单"、"成员工单"、"organization tickets"
- **详细文档**：使用前加载 `{baseDir}/references/DescribeOrganizationTickets.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a DescribeOrganizationTickets -d '{"StartTime":"<last_180d.startTime>","EndTime":"<last_180d.endTime>","Offset":0,"Limit":10}'
```

### 3.5 DescribeTicket — 查看工单详情（集团）

根据工单 ID 查询集团工单详情。自动注入 Region=ap-guangzhou。

- **触发词**："查看集团工单"、"工单详情"、"describe ticket"
- **详细文档**：使用前加载 `{baseDir}/references/DescribeTicket.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a DescribeTicket -d '{"TicketId":"11046458"}'
```

### 3.6 DescribeTicketOperation — 查询工单流水

查询工单的操作流水记录。注意 TicketId 是 Integer 类型；自动注入 Region=ap-guangzhou。

- **触发词**："工单流水"、"操作记录"、"ticket operation"
- **详细文档**：使用前加载 `{baseDir}/references/DescribeTicketOperation.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a DescribeTicketOperation -d '{"TicketId":7334156,"Offset":0,"Limit":10}'
```

### 3.7 DescribeOrganizationStories — 集团成员需求单列表

查询集团成员的需求单列表，支持按时间范围、分页等过滤。

- **触发词**："需求单列表"、"集团需求单"、"organization stories"
- **详细文档**：使用前加载 `{baseDir}/references/DescribeOrganizationStories.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a DescribeOrganizationStories -d '{"StartTime":"<last_180d.startTime>","EndTime":"<last_180d.endTime>","Offset":0,"Limit":10}'
```

### 3.8 DescribeOrganizationStory — 需求单详情

根据需求单 ID 查询详情，包含评论列表。

- **触发词**："需求单详情"、"查看需求单"、"story detail"
- **详细文档**：使用前加载 `{baseDir}/references/DescribeOrganizationStory.md`

```bash
python3 {baseDir}/scripts/andon-api.py -a DescribeOrganizationStory -d '{"StoryId":1010239}'
```

---

## 四、统一输出格式

所有接口输出为统一 JSON 格式，通过 `success` 字段区分成功与失败。

### 成功响应

```json
{
  "success": true,
  "action": "GetMCTicketList / GetMCTicketById / SmartQA",
  "data": { ... },
  "requestId": "xxx"
}
```

### 失败响应

```json
{
  "success": false,
  "action": "...",
  "error": {
    "code": "错误码",
    "message": "错误描述"
  }
}
```

### 脚本层面错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `InvalidParameterValue` | 参数校验失败 | 检查输入格式 |
| `MissingCredentials` | 未配置 AK/SK 环境变量 | 配置密钥 |
| `NetworkError` | 网络超时或连接失败 | 检查网络，重试 |
| `SessionCreateFailed` | SmartQA 会话创建失败 | 可能是暂时性问题，重试 |
| `EmptyResponse` | SSE 流中无回答内容 | 问题格式不支持 |
| `HttpError` | HTTP 状态码非 200 | 检查 API 状态 |
| `ParseError` | 响应不是有效 JSON | 检查网络环境 |

### 常见 API 错误码（工单操作）

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `AuthFailure` | AK/SK 不正确或已过期 | 检查密钥配置 |
| `ResourceNotFound` | 工单 ID 不存在 | 检查 TicketId 是否正确 |
| `InternalError` | 腾讯云内部错误 | 重试或联系支持 |
| `RequestLimitExceeded` | 请求频率超限 | 降低调用频率 |

---

## 五、展示规则

### 5.1 智能问答成功

- `answer` 字段可能包含 Markdown（标题、列表、代码块、图片链接），**原样传递**展示
- 若 `recommendQuestions` 非空，展示为编号列表供用户追问
- 若 `smartTool` 字段存在，表示返回的是产品操作组件引用（如 SDK 面板），非自然语言回答
- 若 `partial: true`，提示："回答可能不完整（流被中断）"
- `intention` 字段说明意图类型：`profession` = 产品知识问答，`hanxuan` = 寒暄/闲聊

### 5.2 工单列表

以表格形式展示，包含工单 ID、问题描述、状态、创建时间。状态显示中文名：

| StatusId | 状态 |
|----------|------|
| 0 | 待处理 |
| 1 | 处理中 |
| 2 | 待确认 |
| 3 | 已完成 |
| 4 | 已关闭 |
| 5 | 已取消 |
| 6 | 重新打开 |
| 7 | 待补充 |

- `toBeAddCount > 0` 时提示用户有工单需要补充信息
- `toConfirmCount > 0` 时提示用户有工单待确认
- 底部显示总数和当前页码

### 5.3 工单详情

分段展示：基本信息（状态、产品、时间）+ 问题描述 + 沟通记录。

- `Comments` 按时间顺序展示，标注角色（客服/用户）
- 若 `StatusId == 7`（待补充），提醒用户需要补充信息
- 若有附件（`ReturnCosUrl=true`），展示为可点击链接

### 5.4 多轮对话

**必须保留**返回的 `sessionId` 和 `agentSessionId`，追问时传入，实现上下文连续对话。

### 5.5 集团工单列表

以表格形式展示，包含工单 ID、标题、状态、创建时间、UIN、渠道。

### 5.6 工单详情（集团）

分段展示：基本信息（状态、渠道、优先级）+ 问题描述。

优先级映射：

| Priority | 等级 |
|----------|------|
| -1 | L1 |
| 0 | L2 |
| 1 | L3 |
| 2 | L4 |

### 5.7 工单流水

按时间顺序展示操作列表，标注操作类型（认领/转单/派单/回复）和操作人。

### 5.8 集团需求单列表

以表格形式展示，包含需求单 ID、标题、状态、创建时间、UIN。

### 5.9 需求单详情

分段展示：基本信息 + 评论列表。

- 评论中 `[br]` 转换为换行
- 评论中 `[img]` 提取为图片链接

### 5.10 人工客服引导

当用户明确表示要找**人工客服**、**转人工**、**联系客服**、**在线客服**时，直接给出链接：

> 您可以通过以下链接联系腾讯云人工客服：
> https://cloud.tencent.com/online-service?from=claw&redirectType=0

- **触发词**："找人工"、"转人工"、"人工客服"、"联系客服"、"在线客服"、"我要找人"、"talk to human"、"human support"
- 无需调用任何接口，直接输出上述链接即可

---

## 六、调试

启用详细输出查看原始请求/响应：
```bash
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{}' -v
python3 {baseDir}/scripts/smartqa-api.py -q "..." -v
```

Dry-run 模式仅展示 payload，不发送请求：
```bash
python3 {baseDir}/scripts/andon-api.py -a GetMCTicketList -d '{}' -n
python3 {baseDir}/scripts/smartqa-api.py -q "..." -n
```

---

## 七、安全与权限声明

### 7.1 所需凭证

| 环境变量 | 必填 | 用途 |
|---------|------|------|
| `TENCENTCLOUD_SECRET_ID` | 工单操作必填 | 腾讯云 API SecretId |
| `TENCENTCLOUD_SECRET_KEY` | 工单操作必填 | 腾讯云 API SecretKey |

> SmartQA 的 uin 和 skey 默认为空。

### 7.2 网络访问范围

本 Skill 仅连接以下腾讯云官方域名：

| 域名 | 用途 |
|------|------|
| `tandon.tencentcloudapi.com` | 工单 API（列表、详情） |
| `cloud.tencent.com` | SmartQA 会话创建 |
| `andon.cloud.tencent.com` | SmartQA 聊天（SSE 流） |

### 7.3 数据安全

- **密钥读取**：脚本本身只从环境变量读取 AK/SK，不写入文件、日志，也不会把密钥
  发送到签名头以外的任何地方
- **凭据持久化由用户决定**：本 Skill 的脚本不会创建配置文件、不缓存数据。
  但若用户按 §1.1 的**备选方式**把 AK/SK 写入 `~/.zshrc` / `~/.bashrc` 或 Windows
  用户级环境变量，则密钥会以明文长期留存在磁盘上 —— 这是用户环境的持久化，
  不是脚本的行为，但风险真实存在。推荐使用 §1.1 的会话级注入方式避免落盘。
- **SSL 验证**：所有 HTTPS 请求启用完整 SSL 证书验证（证书链 + 主机名）
- **纯 Python 实现**：无需 curl、openssl、jq 等外部依赖

### 7.4 数据范围与外发

- **SmartQA 会把问题和多轮上下文发送到腾讯云**（见 §1.2），内容离开本地环境。
- **工单接口返回敏感数据**：工单标题、问题描述、沟通记录、UIN、企业名称、
  处理人、操作流水、附件链接等。展示给用户时按需呈现，不要在无关上下文中转述，
  也不要写入日志或粘贴到第三方服务。
- **默认只查个人工单**：`GetMCTicketList` 默认仅返回当前账号的工单。
  如需同时查询集团范围工单，必须显式传入 `--include-organization`
  （见 §3.1）—— 该参数会显著扩大返回数据的范围，应先向用户确认。
- **`-v` / `-n` 输出包含敏感内容**：verbose 会打印原始请求/响应，dry-run 会打印
  payload 与签名头元数据。不要在共享终端、录屏或日志中使用这两个模式。

---

## 八、参考文档

使用某个接口前，**建议先加载对应的接口文档**获取完整参数说明和展示规则：

- **工单列表**：`{baseDir}/references/GetMCTicketList.md` — 状态码映射、过滤参数、分页说明
- **工单详情**：`{baseDir}/references/GetMCTicketById.md` — 评论分页、附件 URL、响应字段
- **智能问答**：`{baseDir}/references/SmartQA.md` — 多轮对话指南、响应类型、产品问题示例
- **集团工单列表**：`{baseDir}/references/DescribeOrganizationTickets.md` — 集团成员工单查询参数、分页说明
- **工单详情（集团）**：`{baseDir}/references/DescribeTicket.md` — 集团工单详情字段、优先级映射
- **工单流水**：`{baseDir}/references/DescribeTicketOperation.md` — 操作记录类型、分页说明
- **集团需求单列表**：`{baseDir}/references/DescribeOrganizationStories.md` — 集团需求单查询参数、分页说明
- **需求单详情**：`{baseDir}/references/DescribeOrganizationStory.md` — 需求单详情字段、评论格式说明
