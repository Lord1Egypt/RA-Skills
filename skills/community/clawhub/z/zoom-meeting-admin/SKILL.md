---
name: zoom-meeting-admin
allowed-tools: Bash(python3:*) Bash(ls:*) Bash(cat:*) Read
compatibility: Requires Python 3.7+, network access to zoom.us and api.zoom.us, and a local .env with Zoom Server-to-Server OAuth credentials.
description: Manage Zoom meetings, cloud recordings, and account users via a Server-to-Server OAuth REST script. Use this skill when the user wants to list, view, create, or delete a scheduled Zoom meeting; query cloud recordings for a user; or look up account users. Actions are restricted to a fixed list (list/get/create/delete meeting, get/list user, list recordings) — the script does not perform arbitrary Zoom API calls. create_meeting and delete_meeting require explicit user confirmation before execution. Requires a Zoom Server-to-Server OAuth app and a local .env with ACCOUNT_ID, CLIENT_ID, CLIENT_SECRET, USER_ID.
---

# Zoom Server-to-Server OAuth REST API

## 权限与约束

本 Skill 通过 `scripts/zoom-s2s.py` 调用 Zoom Server-to-Server OAuth REST API，不实现"通用 REST 代理"。

- **声明的工具**：`Bash(python3:*)`（执行 `scripts/zoom-s2s.py`）、`Bash(ls:*)` / `Bash(cat:*)`（查看脚本输出与缓存）、`Read`（读取凭证文件与文档）。
- **网络访问**：向 `https://zoom.us/oauth/token` 与 `https://api.zoom.us/v2/*` 发起 HTTPS 请求，传输头包含 `Authorization: Bearer <token>`。
- **文件写入**：在 `~/.zoom-s2s-token.json` 缓存访问令牌（已自动 `chmod 600`）。
- **凭证读取**：从仓库根目录的 `.env` 读取 `ZOOM_ACCOUNT_ID` / `ZOOM_CLIENT_ID` / `ZOOM_CLIENT_SECRET` / `ZOOM_USER_ID`。
- **允许的 Action（白名单）**——禁止构造任意 Zoom REST 请求或调用未列出的端点：
  - 会议：`list_meetings` / `get_meeting` / `create_meeting` / `delete_meeting`
  - 用户：`get_user` / `list_users`
  - 录像：`recordings`
- **越权防护**：脚本未导出 `api_call` 给上层调用；不得通过修改脚本、注入参数、拼接 URL 等方式旁路调用白名单外的 Zoom 端点（如 `DELETE /users/{id}`、`PATCH /accounts/{id}` 等高风险端点）。
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

## 核心脚本

`scripts/zoom-s2s.py` — 纯 Python，无外部依赖，兼容 Python 3.7+。

```bash
cd ~/.agents/skills/zoom-meeting-admin/scripts

# 获取帮助
python3 zoom-s2s.py help

# 列出即将到来的会议
python3 zoom-s2s.py list_meetings <user> <page_size> upcoming

# 获取单个会议详情
python3 zoom-s2s.py get_meeting <meeting_id>

# 创建会议 (start_time: YYYY-MM-DDTHH:MM:SS)
python3 zoom-s2s.py create_meeting "<主题>" "<start_time>" <时长分钟> [时区] [密码]
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

## Token 缓存

脚本自动缓存 Token 到 `~/.zoom-s2s-token.json`（有效期约 50 分钟），重复调用无需每次重新认证。

## 常用操作快速参考

| 操作 | 命令 |
|------|------|
| 列出最近5个会议 | `list_meetings <user> 5 upcoming` |
| 列出最近10个历史会议 | `list_meetings <user> 10 past` |
| 创建明天10点会议 | `create_meeting "主题" "YYYY-MM-DDT10:00:00" 60 Asia/Shanghai` |
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

## 创建周期性会议

创建 `type=8`（周期性会议）的 `recurrence` 参数说明：

| recurrence.type | 说明 | 可用字段 | 是否可用 |
|---|---|---|---|
| 1 | 每日循环（Daily） | `end_date_time` 或 `count` | ✅ |
| 2 | 每周循环（Weekly） | `weekly_days`（字符串）, `end_date_time` 或 `count` | ✅ |
| 3 | 每月循环（Monthly） | `monthly_day` 或 `monthly_weeks` + `weekly_days` | ✅ |

**⚠️ 关键避坑：`weekly_days` 必须是字符串，不是数组！**

| 错误写法 | 正确写法 |
|---------|---------|
| `"weekly_days": [6]` | `"weekly_days": "6"` |
| `"weekly_days": ["6"]` | `"weekly_days": "6"`（单日） |
|  | `"weekly_days": "6,0"`（多日，周六+周日） |

**weekly_days 取值**：1=周一 ~ 7=周日

**示例**：创建 5月23日-24日（周六日）的周期性会议：
```python
payload = {
    "topic": "CSM公开课",
    "type": 8,
    "start_time": "2026-05-23T08:00:00",
    "duration": 540,
    "timezone": "Asia/Shanghai",
    "recurrence": {
        "type": 2,
        "repeat_interval": 1,
        "weekly_days": "6,0",   # 周六+周日，字符串！
        "end_date_time": "2026-05-24T00:00:00Z"
    },
    "settings": {
        "host_video": True,
        "participant_video": True,
        "join_before_host": False,
        "mute_upon_entry": False
    }
}
```

**多日示例**（周一+周三+周五）：
```python
"weekly_days": "1,3,5"
```

## 踩坑记录

1. **scope 错误 (4711)**：某些 API（如 `get_user`）需要在 App 里开通对应 scope，又如 `list_meetings` 需要在 App 里开通 `meeting:read:list_meetings` 权限
2. **Token 有效期**：Server-to-Server Token 有效期 1 小时，脚本自动刷新并缓存
3. **用户 ID**：可用邮箱，也可用 `list_users` 查 user_id
4. **`weekly_days` 必须为字符串**：Zoom API 要求 `weekly_days` 是 `"6"` 这样的字符串，而非 `[6]` 数组，传数组会报 300 错误