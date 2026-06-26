# Smart Email 用户指南

> 本文档面向最终用户，提供安装、配置、测试和使用的完整指南。

---

## 功能特性

- **多邮箱支持** — QQ、126、163、Outlook 一键配置
- **AI 智能判断** — 支持 OpenAI / Anthropic / Subagent 三种分析方式
- **消息队列架构** — outbox 机制，支持失败重试，不丢失消息
- **多渠道推送** — Telegram、钉钉、企业微信、飞书等 OpenClaw 支持的所有渠道
- **本地归档** — 原始邮件(.eml)、Markdown、附件完整保存
- **每日汇总** — 每天 11:00 和 17:00 自动生成邮件摘要
- **多模态分析** — 可选开启，AI 同时分析邮件中的图片内容

---

## 快速开始（5分钟上手）

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置环境变量

**⚠️ 注意：如果 `~/.openclaw/.env` 已存在，请勿复制，直接编辑现有文件即可！**

1. 检查是否已有 `.env` 文件：
```bash
ls -la ~/.openclaw/.env
```

2. 如果文件不存在，复制模板（**仅首次使用**）：
```bash
cp .env.example ~/.openclaw/.env
```

3. 编辑 `~/.openclaw/.env`，填写以下信息：

```bash
# ========== 邮箱配置（必填） ==========
# 使用授权码，不是登录密码！获取方式见下方说明
SMART_EMAIL_QQ_EMAIL=your_qq@qq.com
SMART_EMAIL_QQ_AUTH_CODE=your_auth_code

# ========== AI 配置（必填） ==========
# 选择 AI 分析方式：openai | anthropic | subagent
SMART_EMAIL_LLM_PROVIDER=openai

# OpenAI 兼容 API（当 LLM_PROVIDER=openai 时使用）
SMART_EMAIL_OPENAI_API_URL=https://api.example.com/v1
SMART_EMAIL_OPENAI_API_KEY=your_api_key
SMART_EMAIL_OPENAI_MODEL=gpt-4o-mini

# Anthropic API（当 LLM_PROVIDER=anthropic 时使用）
SMART_EMAIL_ANTHROPIC_API_KEY=your_api_key
SMART_EMAIL_ANTHROPIC_API_URL=https://api.minimaxi.com/anthropic
SMART_EMAIL_ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Subagent 并发数（当 LLM_PROVIDER=subagent 时使用）
SMART_EMAIL_SUBAGENT_CONCURRENCY=5

# ========== 发送渠道配置（必填） ==========
# 渠道类型: telegram | dingtalk | wecom | feishu
SMART_EMAIL_DELIVERY_CHANNEL=telegram
# 目标用户/群组 ID
SMART_EMAIL_DELIVERY_TARGET=@your_username
```

**如何获取配置信息：**
- **邮箱授权码**: QQ邮箱 → 设置 → 账户 → 开启 IMAP/SMTP 服务 → 生成授权码
- **API 配置**: 使用任意 OpenAI 兼容的模型服务商（如 Kimi、DeepSeek、OpenAI、Claude 等），填写对应的 API URL、API Key 和模型名称
- **Telegram 用户ID**: 向 @userinfobot 发送消息获取
- **飞书用户ID**: 在飞书开放平台创建应用，获取 user_id 或 open_id

### 第三步：初始化

```bash
python3 -m smart_email init
```

成功后会显示：
- ✅ 配置验证通过
- ✅ 目录结构已创建
- ✅ 数据库已初始化

---

## 新手引导：4步测试流程（推荐）

> **💡 建议：新用户推荐按顺序完成以下 4 个测试，可帮助确认系统各环节正常工作**

---

### ✅ 步骤 1：验证配置（初始化测试）

**目的**：确认配置正确，目录和数据库已创建

```bash
python3 -m smart_email init
```

**预期结果**：
```
✅ 配置验证通过
✅ 目录结构已创建: ~/.openclaw/workspace/smart-email-data/
✅ 数据库已初始化
```

**如果失败**：检查 `.env` 文件路径和内容是否正确

---

### ✅ 步骤 2：测试邮件收取与AI分析

**目的**：验证邮件下载 → AI 分析 → 生成消息文件完整流程

```bash
# 测试最近12小时的邮件（默认）
python3 -m smart_email test-check

# 或测试最近24小时
python3 -m smart_email test-check --since 24h
```

**测试模式特点**：
- 📁 邮件保存到 `tmp/` 目录（不会污染正式数据）
- 📝 消息生成到 `tmp/outbox/pending/` 目录
- 🏷️ 消息标题带 `[测试]` 前缀
- 🗄️ 使用临时数据库
- ✉️ **不会实际发送任何消息**

**预期结果**：
1. 显示正在检查的邮箱
2. 显示下载的邮件数量
3. AI 分析每封邮件（约 2-5 秒/封）
4. 紧急邮件生成消息文件到 `tmp/outbox/pending/`

**超时说明**：AI 分析需要时间，建议设置 **10 分钟** 超时

---

### ✅ 步骤 3：测试每日汇总

**目的**：验证定时汇总功能

```bash
python3 -m smart_email test-digest
```

**预期结果**：`tmp/outbox/pending/` 目录下生成一条测试汇总消息文件

---

### ✅ 步骤 4：测试消息分发

**目的**：验证消息分发到用户渠道功能

```bash
python3 -m smart_email test-dispatch
```

**测试模式特点**：
- 读取 `tmp/outbox/pending/` 中的消息
- **不会实际发送到用户渠道**（仅模拟）
- 显示发送预览

**预期结果**：显示待发送消息数量和发送预览

---

## 完成测试后

完成以上 **4 个推荐测试** 后，即可进入正式使用阶段：

1. `init` - 配置验证通过
2. `test-check` - 邮件收取和 AI 分析正常
3. `test-digest` - 每日汇总正常
4. `test-dispatch` - 消息分发正常

---

## 正式启用（推荐方式）

完成以上 4 步测试后，**强烈推荐使用 OpenClaw 内置 Cron 自动运行**：

### 方式一：自动定时任务（⭐ 推荐）

```bash
# 一键添加到 OpenClaw cron（自动创建 3 个任务）
python3 -m smart_email setup-cron --apply
```

这会创建三个定时任务：
- `smart-email-check`: 每30分钟检查新邮件，生成紧急消息到 outbox
- `smart-email-digest`: 每日11:00和17:00生成汇总消息到 outbox
- `smart-email-dispatch`: 每5分钟将 outbox 消息发送到用户渠道

**验证任务是否创建成功：**
```bash
openclaw cron list
```

**手动管理任务：**
```bash
# 查看任务列表
openclaw cron list

# 删除任务（如需重新配置）
openclaw cron remove --id <job-id>
```

### 方式二：手动运行（适用于调试或临时执行）

```bash
# 检查新邮件（下载 + AI分析 + 生成消息到 outbox）
python3 -m smart_email check

# 生成每日汇总消息到 outbox
python3 -m smart_email digest

# 分发 outbox 消息到用户渠道
python3 -m smart_email dispatch
```

---

## 高级配置

### 高级环境变量

```bash
# AI 并发限制（默认5，避免触发 API 限制）
SMART_EMAIL_MAX_CONCURRENT=5

# 每次检查最多分析的邮件数（默认 20）
SMART_EMAIL_ANALYZE_LIMIT=20

# LLM 重试次数（默认 3）
SMART_EMAIL_LLM_RETRY_COUNT=3

# LLM 重试间隔基数秒（默认 1，指数退避）
SMART_EMAIL_LLM_RETRY_BASE_DELAY=1

# 多模态分析开关（可选，默认 false）
SMART_EMAIL_MULTIMODAL_ANALYSIS=false

# 每次检查最多下载的邮件数（默认 50）
SMART_EMAIL_DOWNLOAD_LIMIT=50

# 检查间隔（分钟，默认 30）
SMART_EMAIL_CHECK_INTERVAL=30

# 每日汇总时间（默认 11:00,17:00）
SMART_EMAIL_DIGEST_TIMES=11:00,17:00
```

### 多模态分析（可选功能）

Smart Email 支持多模态 AI 分析，开启后 AI 在分析邮件时会同时输入邮件正文中的图片内容。

**开启方法**：在 `~/.openclaw/.env` 中添加：
```bash
SMART_EMAIL_MULTIMODAL_ANALYSIS=true
```

**注意事项**：
- **API 消耗**: 多模态分析会消耗更多 API 额度
- **分析速度**: 包含图片的邮件分析速度会变慢
- **图片范围**: 仅分析邮件正文中的内嵌图片（inline images），普通附件不作为输入
- **支持的格式**: PNG、JPEG、GIF、WebP

---

## 常见问题

**Q: 邮箱密码和授权码有什么区别？**
A: 授权码是邮箱提供的专用密码，用于第三方应用登录。QQ邮箱在设置 → 账户 → 开启 IMAP 服务后可以生成。

**Q: 测试模式会真的发送消息吗？**
A: 不会。测试模式**只生成消息文件到 `tmp/outbox/pending/`，不会实际发送到用户渠道**。

**Q: 如何查看生成的消息？**
A: 消息文件位于 `outbox/pending/` 目录（正式版）或 `tmp/outbox/pending/` 目录（测试版）。使用 `cat` 命令查看 JSON 内容。

**Q: 消息发送失败怎么办？**
A: 发送失败的消息会保留在 `outbox/pending/`，下次 `dispatch` 任务会自动重试。

**Q: AI 分析很慢怎么办？**
A: 可以调整 `SMART_EMAIL_MAX_CONCURRENT` 增加并发数，或先使用 `download` 命令批量下载，再使用 `analyze` 批量分析。

**Q: 如何通过邮件ID查看原邮件？**
A: 使用 `get-email` 命令：
```bash
# 查询邮件ID对应的文件路径
python3 -m smart_email get-email qq_20250321_143022_abc123

# 输出JSON格式
python3 -m smart_email get-email qq_20250321_143022_abc123 --format json

# 查询测试目录
python3 -m smart_email get-email qq_20250321_143022_abc123 --test
```

---

## 目录结构

所有本地文件统一存放在 `~/.openclaw/workspace/smart-email-data/`：

```
~/.openclaw/workspace/
└── smart-email-data/           # Skill 数据根目录
    ├── mail-archives/          # 正式邮件存档（按日期组织）
    │   └── 2025-03-10/
    │       └── qq_20250310_143022/
    │           ├── email.eml   # 原始邮件
    │           ├── email.md    # Markdown格式
    │           └── attachments/# 附件目录
    ├── outbox/                 # 消息队列
    │   ├── pending/            # 待发送消息
    │   │   └── 20250310_143022.json
    │   └── sent/               # 已发送归档
    │       └── 2025-03-10/
    │           └── 20250310_143022.json
    ├── tmp/                    # 测试目录（结构与正式一致）
    │   ├── mail-archives/      # 测试邮件存档
    │   ├── outbox/             # 测试消息队列
    │   │   ├── pending/        # 测试待发送消息
    │   │   └── sent/           # 测试已发送归档
    │   └── logs/               # 测试日志
    ├── logs/                   # 运行日志
    └── data/
        ├── mail_tracker.db     # 邮件追踪数据库
        └── config.json         # 配置文件
```

---

## CLI 命令参考

| 命令 | 说明 |
|------|------|
| `init` | 初始化配置和目录 |
| `check` | 检查新邮件（下载 + AI分析） |
| `check --test` | 测试模式检查 |
| `digest` | 生成每日汇总 |
| `digest --test` | 测试模式汇总 |
| `dispatch` | 分发 outbox 消息到用户渠道 |
| `dispatch --test` | 测试模式分发（不实际发送） |
| `download` | 仅下载邮件到本地（不分析） |
| `analyze` | 批量分析本地已下载邮件 |
| `get-email <id>` | 通过邮件ID查询原文件路径 |
| `clean` | 删除正式版数据（保留配置） |
| `clean-test` | 删除测试版数据 |
| `setup-cron --apply` | 一键添加定时任务 |
| `test-check` | 阶段1测试：邮件检查与AI分析 |
| `test-digest` | 阶段2测试：每日汇总 |
| `test-dispatch` | 阶段3测试：消息分发 |
| `test-error` | 测试错误通知功能 |

---

## 更新记录

### v2.4 (2026-03-29)

**多 Provider 支持**：
- AI 分析支持 OpenAI / Anthropic / Subagent 三种方式
- 新增 `SMART_EMAIL_LLM_PROVIDER` 选择分析方式
- 新增 `test-error`、`get-email`、`clean-test` 命令
- 新增 AI 重试策略和分析数量控制配置

### v2.3 (2026-03-25)

- 简化邮件ID格式，美化消息显示，添加 Agent 使用指南

### v2.2 (2026-03-21)

- 新增邮件ID标识和 `get-email` 查询功能

### v2.1 (2026-03-18)

- 新增 `dispatch` 命令和定时任务，支持多渠道自动发送
- 消息队列架构，支持失败重试

### v2.0 (2026-03-18)

- 重构为消息队列架构
