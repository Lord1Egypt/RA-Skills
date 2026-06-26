---
name: feishu-calendar-v2
description: 飞书日历会议室预约调度助手，支持以用户身份进行会议预约、调整和管理。触发条件：用户提到会议、预约、会议室、日程、日历、调整会议、取消会议、邀请开会等。支持功能：(1) 查询可用会议室 (2) 创建日程事件 (3) 预约会议室 (4) 查询/修改/删除日程 (5) 智能预约（自然语言）。**特性：自动刷新 token，无需频繁授权。**
---

# 飞书日历会议室预约调度

以**用户身份**操作飞书日历，预约和管理会议室。

## ✨ 自动化特性

- **自动刷新 Token** - access_token 过期时自动用 refresh_token 刷新
- **多用户支持** - 保存多个用户的授权，按需切换
- **智能预约** - 支持自然语言输入（如"明天下午3点"）
- **默认用户** - 内置默认用户 ID，常用操作无需指定

## 🚀 快速开始

### 智能预约（推荐）

```bash
# 自然语言预约
scripts/calendar.sh smart-book "1910" "明天下午3点" "测试会议"
```

系统会自动：
1. 匹配会议室名称
2. 解析时间描述
3. 创建日程 + 预约会议室

### 完整预约流程

```bash
# 计算时间戳
START=$(date -d "tomorrow 15:00:00" +%s)
END=$((START + 3600))

# 预约会议
scripts/calendar.sh book-meeting "测试" $START $END "omm_0ea61a28b2e8fb102814b5b3fe6d586f"
```

## 📋 常用命令

### 会议室操作

```bash
# 查询会议室列表
scripts/calendar.sh list-rooms

# 查找特定会议室
scripts/calendar.sh list-rooms | grep "1910"
```

### 日程操作

```bash
# 获取主日历
scripts/calendar.sh get-primary-calendar

# 查询日程（时间戳）
scripts/calendar.sh list-events 1772800000 1772900000

# 创建日程
scripts/calendar.sh create-event "会议主题" 1772866800 1772870400

# 修改日程
scripts/calendar.sh update-event "evt_xxx" "新主题"

# 删除日程
scripts/calendar.sh delete-event "evt_xxx"
```

### 会议室预约

```bash
# 仅预约会议室（需要已有 event_id）
scripts/calendar.sh reserve-room "omm_xxx" 1772866800 1772870400 "evt_xxx"

# 完整预约（创建日程 + 预约会议室）
scripts/calendar.sh book-meeting "主题" 1772866800 1772870400 "omm_xxx"
```

## 🔐 授权管理

### 首次授权

```bash
# 生成授权链接
scripts/oauth.sh generate-auth

# 用户授权后，用 code 换取 token
scripts/oauth.sh exchange-token <code>
```

### 授权状态

```bash
# 检查授权状态
scripts/oauth.sh check-auth

# 查看已授权用户
scripts/oauth.sh list-users
```

**注意：** 授权后系统会自动保存 refresh_token，后续操作会自动刷新，无需重复授权。

## ⏰ 时间处理

### 日期转时间戳

```bash
# 明天下午3点
date -d "tomorrow 15:00:00 Asia/Shanghai" +%s

# 指定日期
date -d "2026-03-07 15:00:00" +%s

# 下周一
date -d "next monday 10:00:00" +%s
```

### 时间戳转日期

```bash
date -d @1772866800 '+%Y-%m-%d %H:%M:%S'
```

### 常用计算

```bash
START=$(date -d "tomorrow 15:00:00" +%s)
END=$((START + 3600))  # 1小时后
END=$((START + 1800))  # 30分钟后
END=$((START + 7200))  # 2小时后
```

## 📁 文件结构

```
feishu-calendar-v2/
├── SKILL.md              # 本文件
├── scripts/
│   ├── oauth.sh          # OAuth 授权（自动刷新）
│   └── calendar.sh       # 日历操作（智能预约）
└── references/
    └── api.md            # API 完整文档
```

## 🔧 配置

### 默认用户

在 `scripts/calendar.sh` 中修改：

```bash
DEFAULT_USER_OPEN_ID="ou_xxx"  # 你的飞书 open_id
```

### Token 存储

- 单用户：`/root/.openclaw/credentials/feishu-user-token.json`
- 多用户：`/root/.openclaw/credentials/feishu-authorized-users.json`

## ⚠️ 注意事项

1. **首次使用需授权** - 之后会自动刷新
2. **Scope 必传** - 授权链接包含日历权限 scope
3. **时区** - 使用 `Asia/Shanghai` 时区
4. **会议室冲突** - 预约前系统不会自动检查冲突

## 📖 详细文档

完整 API 参考：[references/api.md](references/api.md)
