---
name: zoom-meeting-admin
allowed-tools: Bash(python3 zoom-s2s.py:*) Read
compatibility: Requires Python 3.7+; performs HTTPS calls to zoom.us and api.zoom.us (network); writes a token cache to ~/.zoom-s2s-token.json (auto chmod 600); reads ZOOM_ACCOUNT_ID / ZOOM_CLIENT_ID / ZOOM_CLIENT_SECRET / ZOOM_USER_ID from a local .env.
description: List, create, delete, and query Zoom meetings, cloud recordings, and account users via a fixed CLI (scripts/zoom-s2s.py, 7 whitelisted actions) using Server-to-Server OAuth. Use when the user asks to schedule, reschedule, cancel, find, or look up a Zoom meeting; set up a recurring Zoom; pull cloud recordings or past meeting metadata; or look up account users. Triggers on phrases like "Zoom meeting", "zoom 会议", "约 Zoom", "取消 Zoom", "录像", "schedule a Zoom", "cancel the meeting", "who's on the call", "云录制". create_meeting requires explicit confirmation of topic, start_time, duration; delete_meeting requires --yes and visible confirmation. Agent must only invoke the 7 whitelisted CLI actions and must not modify the script, import internals, or call Zoom REST directly. Requires .env with ACCOUNT_ID/CLIENT_ID/CLIENT_SECRET/USER_ID. Documentation is in Chinese; outputs follow.
---

> ⚠️ **安全提示 — 凭证等同于账户管理员口令**
>
> 本 Skill 通过 `.env` 中的 `ZOOM_CLIENT_SECRET` 等 Server-to-Server OAuth 凭证访问 Zoom 账户。
> `ACCOUNT_ID + CLIENT_ID + CLIENT_SECRET` 三元组可换取 1 小时有效的账户级访问令牌，**能够读取该账户下所有会议元数据、云录像，并执行删除等破坏性操作**。
>
> **使用前请先完整阅读 [`## 凭证安全`](#凭证安全)**，遵守 `.gitignore`、`chmod 600`、最小 scope、专用 App、泄露应急等要求。
> 任何**修改脚本、import 内部函数、构造任意 payload 调用 `api_call`** 的尝试都构成越权，会被本文档明确禁止。

# Zoom Server-to-Server OAuth REST API

## 权限与约束

本 Skill 通过 `scripts/zoom-s2s.py` 调用 Zoom Server-to-Server OAuth REST API，不实现"通用 REST 代理"。

- **声明的工具**：`Bash(python3 zoom-s2s.py:*)`（仅执行本 skill 的 CLI 脚本）、`Read`（读取 SKILL.md、脚本源码、`.env.sample`、token cache 等）。
- **网络访问**：向 `https://zoom.us/oauth/token` 与 `https://api.zoom.us/v2/*` 发起 HTTPS 请求，传输头包含 `Authorization: Bearer <token>`。
- **文件写入**：在 `~/.zoom-s2s-token.json` 缓存访问令牌（已自动 `chmod 600`）。
- **凭证读取**：从仓库根目录的 `.env` 读取 `ZOOM_ACCOUNT_ID` / `ZOOM_CLIENT_ID` / `ZOOM_CLIENT_SECRET` / `ZOOM_USER_ID`。
- **允许的 Action（白名单）**——禁止构造任意 Zoom REST 请求或调用未列出的端点：
  - 会议：`list_meetings` / `get_meeting` / `create_meeting` / `delete_meeting`
  - 用户：`get_user` / `list_users`
  - 录像：`recordings`
- **越权防护**：脚本内部包含一个 `api_call` 函数供 CLI action 复用，但这是**私有实现细节，不是对外可调用的接口**。Agent 不得通过以下任何方式旁路调用白名单外的 Zoom 端点（如 `DELETE /users/{id}`、`PATCH /accounts/{id}` 等高风险端点）：
  - 修改 `scripts/zoom-s2s.py`、新增 CLI action、暴露 `api_call`；
  - `from zoom_s2s import api_call` 或以其他方式直接调用脚本内部函数；
  - 在调用本 Skill 的同时**另起进程**用相同凭证调任意 Zoom REST API（如 `curl` 直接打 `api.zoom.us`）；
  - 注入参数、拼接 URL、构造任意 JSON payload 绕过 CLI 校验逻辑。
  脚本遵循"最小暴露面"原则：CLI 只暴露 7 个白名单 action，**任何其他调用路径都视为越权**。
- **强人类确认**：`create_meeting` 与 `delete_meeting` 在执行前必须获得用户显式确认；`delete_meeting` 命令还需附加 `--yes` 参数。

## 凭证配置

在 `.env` 文件中配置（**仅 chmod 600，不要提交到任何 Git 仓库**）：

```env
ZOOM_ACCOUNT_ID=你的AccountID
ZOOM_CLIENT_ID=你的ClientID
ZOOM_CLIENT_SECRET=你的ClientSecret
ZOOM_USER_ID=你的用户邮箱或user_id
```

> ⚠️ 完整的安全规范见下一节 `## 凭证安全`。

**Token 获取方式**：Server-to-Server OAuth，机器对机器，无需用户交互授权。

## 凭证安全

`.env` 中的 `ZOOM_CLIENT_SECRET` 是长期有效的账户级凭据，等同于账户管理员口令。**必须**遵守：

- **加入 `.gitignore`**：本仓库 `.gitignore` 已包含 `.env`；同步确保 IDE、备份工具、文件同步（iCloud / Dropbox / OneDrive / 坚果云）不会自动上传该文件。
- **限制文件权限**：`chmod 600 .env`；`scripts/zoom-s2s.py` 缓存的 `~/.zoom-s2s-token.json` 同样敏感（已自动 `chmod 600`），**不要**复制到剪贴板、聊天窗口、终端截图、报错工单、AI 对话上下文或第三方日志服务。
- **不要在共享环境复用**：CI runner、公用跳板机、容器镜像、共享开发机中复用同一份凭据 ≈ 凭据公开。`Account ID + Client ID + Client Secret` 三元组可换得 1 小时有效的访问令牌。
- **最小权限**：按 `## 最小权限配置建议` 表按需开启 Scope；不需要的 Action 不要勾选对应权限；`delete_meeting` 之外的写权限（`meeting:write:update`、`user:write:*`、`account:write:*`）默认不要开。
- **独立 App**：为此 Skill 单独创建一个 Zoom Server-to-Server App，**不要**复用其他业务 App 的凭据；一旦泄露，旋转该 App 的凭据即可，不影响其他业务。
- **凭据泄露应急**：在 Zoom Marketplace 删除该 App → 重新创建并轮换 `ACCOUNT_ID` / `CLIENT_ID` / `CLIENT_SECRET` / `USER_ID` 四项 → `rm -f ~/.zoom-s2s-token.json` 强制下次重新认证 → 复盘泄露路径。

## Out of scope（不在本 Skill 范围内）

下列能力**不在**本 Skill 范围内；Agent 不应通过旁路调用 `api_call` 或 `curl` 等方式实现：

- Zoom **Webinar**（与 Meeting 是不同产品，API 不同，需 `webinar:*` scope）
- 注册表单、参会者注册管理、邮件 invite
- Zoom Phone / Zoom Chat / Zoom Whiteboard
- 会议期间的实时控制（mute / unmute / recording start-stop）
- 账户/账单/SSO 配置
- Chat 消息发送（`chat_message` 端点）

如需以上能力，请走 Zoom Web UI 或 Marketplace 上的专用 App。

## 核心脚本

`scripts/zoom-s2s.py` — 纯 Python，无外部依赖，兼容 Python 3.7+。

```bash
# 调用前先 cd 到 scripts/ 目录（skill 根目录下的 scripts/ 子目录）
cd scripts

# 获取帮助
python3 zoom-s2s.py help

# 列出即将到来的会议
python3 zoom-s2s.py list_meetings <user> <page_size> upcoming

# 获取单个会议详情
python3 zoom-s2s.py get_meeting <meeting_id>

# 创建会议 (start_time: YYYY-MM-DDTHH:MM:SS)
python3 zoom-s2s.py create_meeting "<主题>" "<start_time>" <时长分钟> [时区] [密码]
# 创建周期性会议（每周一，7次，每次120分钟；weekly_days="2" = Zoom 编码周一）
python3 zoom-s2s.py create_meeting "CSM公开课" "2026-05-23T08:00:00" 120 Asia/Shanghai "" 2 1 2 7
python3 zoom-s2s.py create_meeting "煎饼果子讨论会" "2026-05-05T10:00:00" 60 Asia/Shanghai

# 删除会议
python3 zoom-s2s.py delete_meeting <meeting_id>

# 获取云录像
python3 zoom-s2s.py recordings <user> <page_size>

# 获取用户信息
python3 zoom-s2s.py get_user [user]

# 列出账户下所有用户
python3 zoom-s2s.py list_users [page_size]
```

### 典型响应

`create_meeting` 成功返回（节选）：

```json
{
  "id": 85123456789,
  "topic": "每周一的产品同步",
  "type": 2,
  "start_time": "2026-08-24T20:00:00Z",
  "duration": 120,
  "timezone": "America/New_York",
  "join_url": "https://us05web.zoom.us/j/85123456789?pwd=...",
  "start_url": "https://us05web.zoom.us/s/85123456789?zak=...",
  "password": "abc123"
}
```

**Agent 应当**：
- 把 `join_url` 展示给用户（这是参会者链接）。
- 把 `id`（meeting_id）记下来备用。
- **不要**展示 `start_url`（这是主持人链接，含 host key 摘要，泄露后他人可代为启动会议）。

`list_meetings` 返回 `{meetings: [...], page_count, total_records}`；`recordings` 返回 `{recording_files: [...], ...}`。

## Token 缓存

脚本自动缓存 Token 到 `~/.zoom-s2s-token.json`（有效期约 50 分钟），重复调用无需每次重新认证。

## 常用操作快速参考

| 操作 | 命令 |
|------|------|
| 列出最近5个会议 | `list_meetings <user> 5 upcoming` |
| 列出最近10个历史会议 | `list_meetings <user> 10 past` |
| 创建明天10点会议 | `create_meeting "主题" "YYYY-MM-DDT10:00:00" 60 Asia/Shanghai` |
| 创建周期性会议（每周一） | `create_meeting "主题" "YYYY-MM-DDT20:00:00" 120 America/New_York "" 2 1 2 7` |
| 创建月度会议（每月15号） | `create_meeting "主题" "YYYY-MM-15T10:00:00" 60 Asia/Shanghai "" 3 1 15 12` |
| 创建月度会议（第N个周二） | `create_meeting "主题" "..." 60 ... "" 3 1 3 6 "" "" 2` |
| 获取会议详情 | `get_meeting <id>` |
| 删除会议 | `delete_meeting <id> --yes` |
| 获取云录像 | `recordings <user> 10` |

## 最小权限配置建议

根据实际使用场景按需开通 scope，不需要的功能不要授权：

| 功能 | 所需 Scope | 建议 |
|------|-----------|------|
| 列出会议 | `meeting:read:list_meetings` | ✅ 核心 |
| 查看会议详情 | `meeting:read:meeting` | ✅ 核心 |
| 创建会议 | `meeting:write:create` | 按需开启 |
| **删除会议** | `meeting:write:delete` | ⚠️ 谨慎开启 |
| **读取云录像** | `cloud_recording:read:list_user_recordings` | ⚠️ 谨慎开启 |
| **列出账户用户** | `user:read:list_users` | ⚠️ 谨慎开启 |

> 建议为此 Skill 单独创建一个 Zoom Server-to-Server App，不要复用已有 App 的凭证。

## Agent 调用规范

- **创建会议前**：向用户确认主题、时间、时长，再执行。
- **删除会议前**：必须向用户明确展示会议信息并获得确认，命令需附加 `--yes` 参数。
- **禁止超范围调用**：仅允许文档中列出的 Action，不得构造任意 Zoom REST API 请求。

## 执行后验证

- **create_meeting**：执行后展示返回的 `join_url` / `id` 给用户；记录 meeting_id 备用。
- **delete_meeting**：执行后立刻 `list_meetings <user> upcoming` 验证会议已消失，并向用户报告"已删除 meeting_id=..."。
- **任何失败**：展示原始错误（含 HTTP code + Zoom error message），**不要**把 Client Secret、access_token 或 `start_url` 写入日志/截图/对话上下文。

## 创建周期性会议

`create_meeting` 通过位置参数直接支持周期性会议（**无需绕过 CLI**）：

```bash
python3 zoom-s2s.py create_meeting "<主题>" "<start_time>" <duration> [timezone] [password] \
  [recurrence_type] [repeat_interval] [weekly_days] [end_times] [end_date_time] \
  [monthly_day] [monthly_weeks]
```

| 参数 | 适用 type | 说明 | 示例 |
|------|----------|------|------|
| `recurrence_type` | 全部 | 1=每日, 2=每周, 3=每月 | `2` |
| `repeat_interval` | 全部 | 每几周/天/月重复 | `1` |
| `weekly_days` | type=2, type=3+monthly_weeks | 周几字符串（Zoom 编码：**1=周日, 2=周一, 3=周二, ..., 7=周六**）| `"2"` = 周一, `"3,5"` = 周二+周四 |
| `end_times` | 全部 | 总共几次 | `7` |
| `end_date_time` | 全部 | 结束日期（二选一）| `"2026-10-06T00:00:00Z"` |
| `monthly_day` | type=3 | 每月第几天字符串（1-31，单值或逗号分隔）| `"15"` 或 `"1,15"` |
| `monthly_weeks` | type=3 | 每月第几个周次（-1=最后, 1-4），配合 `weekly_days` | `2` |

> ⚠️ **重要：`weekly_days` 是 Zoom 编码，不是 ISO 编码。** 1=周日（不是周一）。常见误用：
> - 想约周一 → `weekly_days="2"`（不是 `"1"`）
> - 想约周六 → `weekly_days="7"`（不是 `"6"`）
> - 想约周日 → `weekly_days="1"`

### 示例：每周一 20:00（EDT），共 7 次，每次 2 小时
```bash
python3 zoom-s2s.py create_meeting "每周一的产品同步" \
  "2026-08-24T20:00:00" 120 America/New_York "" 2 1 2 7
# weekly_days="2" = Zoom 编码 2 = 周一
```

### 示例：每月 15 号 10:00，共 12 次
```bash
python3 zoom-s2s.py create_meeting "月度复盘" \
  "2026-08-15T10:00:00" 60 Asia/Shanghai "" 3 1 15 12
# positional: topic, start_time, duration, tz, password, type=3, repeat=1, weekly_days=15, end_times=12
# 解释: monthly_day="15"（每月 15 号）
```

### 示例：每月第 2 个周二 20:00，共 6 次
```bash
python3 zoom-s2s.py create_meeting "月度董事会" \
  "2026-08-25T20:00:00" 60 America/New_York "" 3 1 3 6 "" "" 2
# positional: ..., type=3, repeat=1, weekly_days="3", end_times=6, end_date_time="", monthly_day="", monthly_weeks=2
# 解释: monthly_weeks=2 + weekly_days="3" = 每月第 2 个周二（Zoom 编码 3 = 周二）
```

**⚠️ 关键避坑：`weekly_days` / `monthly_day` 必须是字符串，不是数组！**

| 错误写法 | 正确写法 |
|---------|---------|
| `"weekly_days": [6]` | `"weekly_days": "6"`（单日） |
| `"weekly_days": ["6"]` | `"weekly_days": "6"` |
|  | `"weekly_days": "6,7"`（多日，**周五+周六**——Zoom 编码） |
|  | `"weekly_days": "2,3,5"`（**周一+周二+周四**——Zoom 编码） |
|  | `"weekly_days": "1,7"`（**周日+周六**——Zoom 编码两端） |
| `"monthly_day": [15]` | `"monthly_day": "15"` |
|  | `"monthly_day": "1,15"`（每月 1 号和 15 号） |

`weekly_days` Zoom 编码：1=周日，2=周一，3=周二，4=周三，5=周四，6=周五，7=周六。

## 踩坑记录

1. **scope 错误 (4711)**：某些 API（如 `get_user`）需要在 App 里开通对应 scope，又如 `list_meetings` 需要在 App 里开通 `meeting:read:list_meetings` 权限
2. **Token 有效期**：Server-to-Server Token 有效期 1 小时，脚本自动刷新并缓存
3. **用户 ID**：可用邮箱，也可用 `list_users` 查 user_id
4. **`weekly_days` / `monthly_day` 必须为字符串**：Zoom API 要求 `weekly_days`、`monthly_day` 是 `"6"` / `"15"` 这样的字符串，而非 `[6]` / `[15]` 数组，传数组会报 300 错误（CLI 已自动 `str()`，但调用方传入时仍需注意）。`weekly_days` 是 Zoom 编码（1=周日, 2=周一, ..., 7=周六），不是 ISO 编码。
5. **月度循环的两种写法**：`monthly_day` 表示"每月第几天"，`monthly_weeks + weekly_days` 表示"每月第几个周几"。两者二选一，不要同时给；同时给会让 Zoom 拒绝（300 错误）
