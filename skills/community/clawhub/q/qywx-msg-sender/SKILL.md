---
name: qywx-msg-sender
description: >
  通过企业微信群机器人 Webhook 发送消息通知。支持文本、Markdown、Markdown V2（表格）、图片、文件消息。
  支持发送到指定会话（chatid）或通过名称发送（需先注册 webhook URL）。
  适用场景：服务告警、定时任务结果推送、数据报告发送、任何需要通知企业微信群的情况。
---

# 企业微信消息推送（群机器人 Webhook）

## 项目结构

```
qywx-msg-sender/
├── scripts/
│   ├── wecom_common.sh       # 公共函数库（参数解析、注册表、发送封装）
│   ├── send_text.sh          # 发送文本消息（支持 @成员）
│   ├── send_markdown.sh      # 发送 Markdown 消息
│   ├── send_markdown_v2.sh   # 发送 Markdown V2 消息（支持表格）
│   ├── send_image.sh         # 发送图片消息（base64 直传，≤2MB）
│   ├── send_file.sh          # 发送文件消息（先上传获取 media_id，≤20MB）
│   ├── register_chat.sh      # 注册会话（绑定名称、URL、chatid）
│   ├── list_chats.sh         # 列出所有已注册的会话
│   └── unregister_chat.sh    # 删除已注册的会话
└── SKILL.md                  # 本文档
```

## 依赖要求

- `curl`（HTTP 客户端）
- `jq`（JSON 处理，版本 ≥ 1.6）

## 配置参数

所有发送脚本支持以下可选参数：

| 参数 | 环境变量 | 说明 |
|------|----------|------|
| `--to <name>` | - | 通过名称发送（推荐，需先注册） |
| `--url <url>` | `WECOM_WEBHOOK_URL` | Webhook URL |
| `--chatid <id>` | `WECOM_CHATID` | 指定会话 ID |

**优先级**：`--to`（从注册表读取 url + chatid）> `--url`/`--chatid` > 环境变量

### Webhook URL 获取

企业微信群 → 右上角「...」→ 群机器人 → 添加 → 复制 Webhook 地址

### 会话 ID (chatid) 说明

- **默认行为**：不指定 chatid 时，消息发送到创建机器人的群
- **指定会话**：通过 `--chatid` 参数可发送到其他会话
- **获取方式**：从群机器人回调事件中提取 chatid

## 会话注册表

支持通过名称发送消息，注册时绑定 webhook URL、chatid 和会话类型。

### 注册格式

```
name -> { url, chatid, chat_type }
```

- `chat_type`: `group`（群聊，默认）或 `single`（私聊）

### 注册会话

```bash
# 注册群聊（发送到 webhook 默认群）
bash scripts/register_chat.sh "研发群" "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"

# 注册群聊（发送到指定会话）
bash scripts/register_chat.sh "告警群" "https://...?key=yyy" "wrkSFfCgAAxxxxxx"

# 注册私聊（chat_type=single）
bash scripts/register_chat.sh "张三" "https://...?key=zzz" "wokSFfCgAAyyyyyy" "single"
```

### 查看已注册

```bash
bash scripts/list_chats.sh
```

输出示例：
```
已注册的会话 (3 个):
========================================
研发群:
  类型: group
  URL: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
  ChatID: (默认群)

告警群:
  类型: group
  URL: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy
  ChatID: wrkSFfCgAAxxxxxx

张三:
  类型: single
  URL: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz
  ChatID: wokSFfCgAAyyyyyy
```

### 删除注册

```bash
bash scripts/unregister_chat.sh "研发群"
```

### 注册表位置

默认：`~/.wecom/chat_registry.json`

可通过环境变量自定义：
```bash
export WECOM_REGISTRY_FILE="/path/to/registry.json"
```

## 消息类型对比

| 类型 | 脚本 | 特点 | 限制 |
|------|------|------|------|
| 文本 | `send_text.sh` | 纯文本，支持 @成员 | - |
| Markdown | `send_markdown.sh` | 富文本，标题/加粗/链接等 | 4096 字节 |
| Markdown V2 | `send_markdown_v2.sh` | 支持**表格**和多行代码块 | - |
| 图片 | `send_image.sh` | base64 直传，无需上传 | 2MB，jpg/png |
| 文件 | `send_file.sh` | 自动上传获取 media_id | 20MB |

### Markdown vs Markdown V2

| 特性 | Markdown | Markdown V2 |
|------|----------|-------------|
| 基础语法 | `# 标题`、`**加粗**`、`*斜体*`、`` `代码` ``、`[链接](url)`、`> 引用` | 同左 |
| 表格 | ❌ 不支持 | ✅ 支持 |
| 多行代码块 | ❌ 不支持 | ✅ 支持 ` ``` ` |
| 内容限制 | 4096 字节 | 较宽松 |
| 兼容性 | 更好（旧版客户端） | 需较新版本 |

**选择建议**：
- 简单消息 → 用 `markdown`（轻量、兼容性好）
- 需要表格或代码块 → 必须用 `markdown_v2`

## 使用方式

所有脚本都支持 `--to`、`--url`、`--chatid` 参数。

### 文本消息

```bash
# 通过名称发送（推荐）
bash scripts/send_text.sh --to "研发群" "部署完成"

# 通过 URL 发送（临时使用）
bash scripts/send_text.sh --url "https://...?key=xxx" "消息内容"

# @ 指定成员（userid）
bash scripts/send_text.sh --to "研发群" "服务异常，请处理" "zhangsan"

# @ 所有人
bash scripts/send_text.sh --to "研发群" "紧急告警" "@all"
```

### Markdown 消息

```bash
bash scripts/send_markdown.sh --to "研发群" "## 服务状态\n**API**: 正常\n**DB**: 正常"

bash scripts/send_markdown.sh --to "研发群" "$(cat report.md)"
```

支持：`# 标题`、`**加粗**`、`*斜体*`、`` `代码` ``、`[链接](url)`、`> 引用`

### Markdown V2 消息（表格）

```bash
bash scripts/send_markdown_v2.sh --to "研发群" "## 每日数据

| 指标 | 数值 |
|------|------|
| 请求数 | 1,234 |
| 错误率 | 0.1% |
| P99 | 230ms |"
```

### 图片消息

```bash
bash scripts/send_image.sh --to "研发群" /path/to/screenshot.png
```

### 文件消息

```bash
bash scripts/send_file.sh --to "研发群" /path/to/report.xlsx
```

## 示例：服务每日报告

```bash
MSG=$(cat <<'EOF'
## 服务每日报告（2026-01-02）

**整体概况**
> 总请求: 68,019  |  活跃用户: 117  |  错误率: 0.02%

**资源消耗 Top 3**
1. app-gen-code — 6,137 次，$567
2. app-tools — 635 次，$168
3. zhangsan — 1,066 次，$97
EOF
)
bash scripts/send_markdown.sh --to "研发群" "$MSG"
```

带表格的版本（使用 markdown_v2）：

```bash
MSG=$(cat <<'EOF'
## 服务每日报告（2026-01-02）

| 排名 | 名称 | 调用次数 | 消费 |
|------|------|---------|------|
| 1 | app-gen-code | 6,137 | $567 |
| 2 | app-tools | 635 | $168 |
| 3 | zhangsan | 1,066 | $97 |
EOF
)
bash scripts/send_markdown_v2.sh --to "研发群" "$MSG"
```

## 典型工作流

```bash
# 1. 首次使用：注册常用会话（绑定 webhook URL）
bash scripts/register_chat.sh "研发群" "https://...?key=xxx"
bash scripts/register_chat.sh "告警群" "https://...?key=yyy" "wrkSFfCgAAxxxxxx"

# 2. 日常使用：通过名称发送（无需记住 URL 和 chatid）
bash scripts/send_text.sh --to "研发群" "部署完成"
bash scripts/send_markdown.sh --to "告警群" "## 告警\n服务异常"

# 3. 查看已注册
bash scripts/list_chats.sh
```
