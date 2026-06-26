---
name: windows-calendar-sync
description: 将提醒同步到 Windows / Outlook 日历。当用户提到「提醒我」「设置提醒」「加到日历」「同步到日历」「日程」「calendar」「日历」时，使用此技能。支持 Microsoft Graph API 设备代码流认证，无需 Web 服务器，直接写入用户 Outlook 日历。
---

# Windows 日历同步

将提醒和日程写入用户本人的 **Microsoft Outlook 日历**（即 Windows 日历），同步到所有设备。

## 认证（首次使用）

### 一键引导配置（首次运行必选）

运行配置向导，脚本会自动引导你完成 Azure AD 应用注册 + OAuth 登录：

```powershell
python "C:\Users\johnx\.qclaw\skills\windows-calendar-sync\scripts\setup_and_auth.py"
```

脚本会自动：
1. 打开 Azure 门户 → 引导注册免费 Azure AD 应用（获取 Client ID）
2. 打开浏览器 → 设备代码登录 Microsoft 账户
3. 保存 token → 验证日历访问
4. **全程约 2-3 分钟，Token 有效期约 90 天（自动刷新）**

> Azure AD 应用注册是免费的，无需信用卡，只需要一个 Microsoft 账户。

### 再次认证（token 过期后）

同样运行上面的命令，脚本检测到已有 Client ID 会跳过注册步骤，直接进行登录。

---

## 工作流程

当用户提出以下类型的请求时，触发本技能：

1. **创建提醒 + 同步日历**：「明天 10 点提醒我开会，同步到日历」
2. **直接创建日历事件**：「在日历里加一个下周一的周会」
3. **查询日历**：「看看我这周有什么日程」
4. **删除日历事件**：「把那个提醒从日历里删掉」

**工作流程：**
1. 解析用户意图，提取：标题、开始时间、结束时间/时长、提醒设置、是否重复
2. 构造 ISO 8601 时间格式（如 `2026-04-15T10:00:00`）
3. 调用 `calendar_sync.py add` 将事件写入 Outlook 日历
4. 告知用户事件已创建，可通过 Windows 日历或 Outlook 查看

---

## 核心脚本

### `scripts/calendar_sync.py` — 添加 / 查询 / 删除日历事件

**添加事件：**
```powershell
python "C:\Users\johnx\.qclaw\skills\windows-calendar-sync\scripts\calendar_sync.py" add `
  --title "团队周会" `
  --start "2026-04-16T09:00:00" `
  --duration 60 `
  --reminder 15
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` / `-t` | ✅ | 事件标题 |
| `--start` / `-s` | ✅ | 开始时间，ISO 8601 格式 |
| `--end` / `-e` | 与 `--duration` 二选一 | 结束时间 |
| `--duration` / `-d` | 与 `--end` 二选一 | 持续分钟数（默认30分钟） |
| `--reminder` / `-r` | 否 | 提前多少分钟提醒（默认15，设为0则不提醒） |
| `--body` / `-b` | 否 | 事件描述 |
| `--location` / `-l` | 否 | 地点 |
| `--category` / `-c` | 否 | 分类标签（可多次指定） |

**列出未来事件：**
```powershell
python "C:\Users\johnx\.qclaw\skills\windows-calendar-sync\scripts\calendar_sync.py" list --days 7
```

**删除事件：**
```powershell
python "C:\Users\johnx\.qclaw\skills\windows-calendar-sync\scripts\calendar_sync.py" delete <event_id>
```

---

## 时间解析规则

将自然语言时间转换为 ISO 8601：

| 用户输入 | 解析结果 | 示例 |
|----------|----------|------|
| 明天 10 点 | `2026-04-13T10:00:00` | |
| 今天下午 3 点半 | `2026-04-12T15:30:00` | |
| 下周一早上9点 | 下一个周一 09:00 | |
| 周五 18:00 | 本周/下周周五 18:00 | 结合当前日期判断 |
| 2 小时后 | 当前时间 + 2h | |

**时区**：始终使用 `Asia/Shanghai`（中国用户），Windows 上自动检测本地时区。

---

## 与 OpenClaw Cron 提醒的配合

创建定时提醒时，建议**同时做两件事**：

1. **创建 OpenClaw Cron 任务**（即时精确提醒，通过 App/消息推送）
2. **写入 Windows 日历**（可视化日程，同步到所有设备）

示例 — 用户说「每天早上 8 点提醒我做运动」：

```python
# 1. 创建 cron 任务（精确提醒）
cron.schedule("0 8 * * *", message="运动时间到！💪", repeat="daily")

# 2. 写入日历（可视化作息安排）
# 调用 calendar_sync.py:
python "C:\Users\johnx\.qclaw\skills\windows-calendar-sync\scripts\calendar_sync.py" add `
  --title "🏃 运动时间" `
  --start "2026-04-13T08:00:00" `
  --duration 60 `
  --reminder 10
```

---

## 注意事项

1. **认证文件位置**：`scripts/token_store.json`，不要移动或删除
2. **Token 有效期**：约 90 天，过期后脚本会自动尝试刷新，刷新失败会引导重新认证
3. **权限说明**：只需 `Calendars.ReadWrite`，不读写邮件或文件
4. **事件链接**：创建成功后会返回 `webLink`，可直接在浏览器打开
5. **Microsoft 账户**：支持 personal Microsoft account (Outlook.com / Hotmail / Live) 和工作/学校账户 (Microsoft 365)

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `access_token` 获取失败 | 运行 `authenticate.py` 重新认证 |
| Token 已过期 | 删除 `token_store.json`，重新运行 `authenticate.py` |
| 事件时间显示错误 | 确认 `--start` 使用 ISO 8601 格式，带 `T` 分隔符 |
| 提醒没响 | 检查 Outlook/Windows 日历的通知权限是否开启 |
| 想删除事件但不知道 ID | 先运行 `list` 命令查找事件 ID |
