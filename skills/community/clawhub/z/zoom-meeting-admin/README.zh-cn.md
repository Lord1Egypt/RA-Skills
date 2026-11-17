# SKILL of Zoom Server-to-Server OAuth REST API 

用 Server-to-Server OAuth 直接调 Zoom meeting REST API，不需要 VPS，不需要 MCP 协议，管理和安排ZOOM会议。

> [EN](README.md) | 中文

## 配置步骤

1. 需要先手动登录 https://marketplace.zoom.us/
2. 在 "Develop" 下拉菜单选 "build app", 创建一个 `Server-to-Server OAuth`类型的APP
3. 添加必要的OAuth Scope。
4. 获取相关凭证密码
5. 激活APP
6. 在AI agent中调用此 SKILL

## 凭证配置

> ⚠️ **`.env` 中的 `ZOOM_CLIENT_SECRET` 等同于账户管理员口令。** 持有 `ACCOUNT_ID + CLIENT_ID + CLIENT_SECRET` 三元组即可换取 1 小时有效的账户级访问令牌，**能读取该账户下所有会议元数据、云录像，并执行删除等破坏性操作**。
>
> - 千万不要把 `.env` 提交到 git。确认你的 IDE、备份工具、文件同步服务（iCloud / Dropbox / OneDrive / 坚果云）没有自动上传该文件。
> - `chmod 600 .env`。脚本缓存的 token 文件 `~/.zoom-s2s-token.json` 由脚本自动 `chmod 600`。
> - **按需开通最小 scope**（见下表）。未用到的功能不要勾选对应权限；不要轻易开启 `meeting:write:delete`、`cloud_recording:read:*`、`user:read:list_users`。
> - 为本 Skill **单独创建一个** Server-to-Server App，不要复用其他业务 App 的凭据。
> - 一旦泄露：在 Zoom Marketplace 删除该 App → 重新创建并轮换四项值 → `rm -f ~/.zoom-s2s-token.json` 强制重新认证。

编辑 `.env` 文件，填入你的 Zoom Server-to-Server OAuth App 凭证：

```env
ZOOM_ACCOUNT_ID=你的AccountID
ZOOM_CLIENT_ID=你的ClientID
ZOOM_CLIENT_SECRET=你的ClientSecret
ZOOM_USER_ID=你的用户邮箱或user_id
```


## 需要的 OAuth Scope

在 Zoom Marketplace 你的 Server-to-Server OAuth App 里开通：

| Scope | 用途 |
|-------|------|
| `meeting:read:list_meetings` | 列出会议 |
| `meeting:write:create` | 创建会议 |
| `meeting:write:delete` | 删除会议 |
| `cloud_recording:read:list_user_recordings` | 查看云录像 |
| `user:read:list_users` | 列出用户 |
| `user:read:user` | 获取用户信息 |

## 快速开始

```bash
cd ~/.agents/skills/zoom-s2s-oauth/scripts

# 列出最近5个会议
python3 zoom-s2s.py list_meetings service@uperform.cn 5 upcoming

# 创建会议 (start_time 格式: YYYY-MM-DDTHH:MM:SS)
python3 zoom-s2s.py create_meeting "煎饼果子讨论会" "2026-05-05T10:00:00" 60 Asia/Shanghai

# 获取云录像
python3 zoom-s2s.py recordings service@uperform.cn 10
```

## 目录结构

```
zoom-s2s-oauth/
├── SKILL.md           # AI Agent 调用说明
├── README.md          # 本文件
├── .env               # 凭证配置 (不要提交到 git!)
└── scripts/
    └── zoom-s2s.py    # 主脚本 (纯 Python3，无外部依赖)
```


## 对比：MCP vs Server-to-Server REST

| | MCP 方式 | Server-to-Server REST |
|---|---|---|
| 需要 VPS | ✅ 需要 (OAuth 回调) | ❌ 不需要 |
| 协议 | MCP (JSON-RPC) | 标准 REST (Python 无外部依赖) |
| Token | User-Managed OAuth | Server-to-Server OAuth |
| 复杂度 | 高 (代理+OAuth) | 低 (直接调) |
| 功能 | Zoom MCP 工具集 | 7 个白名单 CLI action（list/get/create/delete meeting、get/list user、list recordings） |

如果你只需要调用 Zoom 会议/录像等核心功能，Server-to-Server REST 方式更简单。
