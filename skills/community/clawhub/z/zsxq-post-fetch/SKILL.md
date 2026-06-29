---
name: zsxq-post-fetch
description: 知识星球帖子抓取助手 — 默认通过官方 zsxq-cli OAuth/Keychain 登录态抓取用户已授权账号可访问的帖子，支持全部/精华筛选、关键词搜索、单帖详情、日期范围导出、多星球配置、Markdown 和附件整理。本 Skill 应在用户需要查看、汇总、检索或导出知识星球内容时使用。
user-invocable: true
metadata:
  clawdbot:
    requires:
      bins:
        - node
        - zsxq-cli
      node: ">=18"
    auth:
      primary: zsxq-cli auth login
      status: zsxq-cli auth status
      legacyEnv: ZSXQ_TOKEN
    configFiles:
      - config.json
      - groups.json
---

# 知识星球帖子抓取助手

从指定知识星球抓取最新帖子内容，支持全部帖子、精华过滤、关键词搜索、单帖详情、日期范围、Markdown 导出和附件下载。所有自然语言输出使用**中文**。

默认后端是官方 `zsxq-cli`，认证由 `zsxq-cli auth login` 完成。旧的 `ZSXQ_TOKEN` + 私有 HTTP API 仅作为显式 legacy fallback。

---

## 认证与环境

### 默认官方 CLI 认证

执行前优先检查：

```bash
zsxq-cli auth status
```

如果未登录，提示用户运行：

```bash
zsxq-cli auth login
```

不要读取、导出或展示官方 CLI 存入 Keychain 的 token。

### legacy HTTP fallback

只有当用户明确要求 legacy HTTP，或环境/配置已设置以下任一项时，才使用旧 HTTP 路径：

```bash
export ZSXQ_BACKEND=http
```

```json
{
  "backend": "http"
}
```

该路径才需要：

```bash
export ZSXQ_TOKEN="your_zsxq_access_token"
```

不要把真实 `ZSXQ_TOKEN` 写入仓库文件、聊天回复、日志或发布包。

### 依赖安装

首次使用运行：

```bash
bash {baseDir}/install.sh
```

安装脚本会检测 Node.js 和 `zsxq-cli`；缺失 `zsxq-cli` 时会尝试 `npm install -g zsxq-cli`。安装脚本不会自动登录。

---

## 配置文件

### `{baseDir}/config.json`

```json
{
  "backend": "cli",
  "attachment_dir": "~/.openclaw/workspace/zsxq",
  "download_attachments": true
}
```

字段说明：
- `backend`：默认 `cli`；只有显式设置为 `http` 才使用 legacy HTTP fallback
- `attachment_dir`：附件与 Markdown 保存根目录，按 `group_id/YYYY-MM-DD/` 组织
- `download_attachments`：是否开启自动下载

也可通过环境变量覆盖附件根目录：

```bash
export ZSXQ_ATTACHMENT_DIR="~/.openclaw/workspace/zsxq"
```

优先级：`ZSXQ_ATTACHMENT_DIR` -> `ATTACHMENT_DIR` -> `config.json.attachment_dir`。

### `{baseDir}/groups.json`

```json
[
  {
    "group_id": "YOUR_GROUP_ID",
    "name": "星球名称",
    "scope": "digests",
    "max_topics": 20
  }
]
```

字段说明：
- `group_id`：星球 ID
- `name`：星球名称，展示用
- `scope`：`digests` 或 `all`
- `max_topics`：每个星球最多抓取的帖子数

---

## Prompt 使用说明

当用户请求知识星球内容获取、汇总、检索、导出或附件下载时使用本 Skill。默认假设用户希望通过官方 `zsxq-cli` 读取其已授权账号可访问的内容。

不要尝试绕过权限、伪造官方客户端、伪造 TLS/header 指纹、猜测 token、读取仓库中的凭证文件或输出完整认证信息。

### 意图识别

- “看看知识星球最新内容”“汇总星球更新”“最近有什么值得看”：读取 `groups.json`，按每个星球的 `scope` 和 `max_topics` 抓取并汇总。
- “只看精华”“精华帖”“高价值内容”：优先使用 `digests` 或 `topics <group_id> <count> digests`。
- “全部帖子”“不要只看精华”：使用 `topics <group_id> <count> all`。
- 用户要求“搜索某个关键词”“找包含某主题的帖子”“下载某关键词相关附件”：使用 `search <group_id> <keyword> [count] --markdown --download-attachments`；若缺少 `group_id`，先从 `groups.json` 查找，仍无法确定时询问用户。
- 用户给出 `wx.zsxq.com/topic/...` 链接或纯 topic_id：使用 `topic <group_id> <topic_id_or_url>`；若缺少 `group_id`，先从 `groups.json` 查找，仍无法确定时询问用户。
- 用户给出日期、时间范围或“本周/今天/昨天/某天”：换算成 `YYYY-MM-DD` 后使用 `topics-by-date`；相对日期按当前环境日期解释。
- 用户要求“保存”“导出 Markdown”“下载附件”“整理到本地”：在对应命令后追加 `--markdown`，并说明保存路径。
- 用户不确定星球 ID、想看“我加入了哪些星球”：使用 `groups` 子命令，并提醒该操作会暴露当前账号加入的星球列表。
- 用户明确要求旧 Cookie 方式或需要验证 legacy 行为：设置 `ZSXQ_BACKEND=http` 后再使用命令，并检查 `ZSXQ_TOKEN` 是否已设置。

### 推荐 Prompt 示例

```text
帮我汇总知识星球最近 20 条精华帖，按星球分组。
```

```text
抓取 YOUR_GROUP_ID 从 2026-06-01 到 2026-06-13 的帖子，导出 Markdown 并下载附件。
```

```text
搜索 YOUR_GROUP_ID 里和 SpaceX IPO 相关的帖子，导出 Markdown 并下载附件。
```

```text
查看这个帖子详情：https://wx.zsxq.com/topic/82811454228448260
```

```text
列出我当前账号加入的知识星球，帮我找到对应 group_id。
```

### Agent 输出要求

- 所有自然语言回复使用中文。
- 汇总多个帖子时优先输出要点，避免直接粘贴超长原文；必要时保留帖子链接和 topic_id 方便追溯。
- 明确标注抓取范围：星球名称或 group_id、`all`/`digests`、数量、日期范围、是否导出 Markdown。
- 若写入 Markdown 或下载附件，输出实际保存路径和失败附件数量。
- 不输出 `ZSXQ_TOKEN`、Cookie、Keychain token、临时下载签名 URL 或其他认证材料。
- 单个星球、单个帖子或附件失败时，继续处理其他结果，并在最后列出失败项和原因。
- 遇到 `digests_unavailable_from_cli` 时说明官方 CLI 输出缺少精华标记，不自动回退 legacy HTTP；只有用户明确要求 fallback 时才切换。

---

## 数据抓取脚本 `{baseDir}/fetch_topics.js`

### 1. 获取帖子列表

```bash
node {baseDir}/fetch_topics.js topics <group_id> [count] [scope] [--markdown]
```

- 默认后端命令：`zsxq-cli group +topics --group-id <group_id> --limit <1-30> --json`
- `scope`：`all` 或 `digests`，默认 `all`
- 文本截断上限 20000 字
- 若 `download_attachments` 为 `true`，自动整理图片和文件附件
- 加 `--markdown` 时导出 Markdown 到 `<attachment_dir>/<group_id>/<YYYY-MM-DD>.md`

### 2. 获取精华帖

```bash
node {baseDir}/fetch_topics.js digests <group_id> [count] [--markdown]
```

CLI 后端会按 `digested` / `is_digested` 字段过滤。如果官方 CLI 输出不包含精华标记，返回 `digests_unavailable_from_cli`。

### 3. 按关键词搜索并下载

```bash
node {baseDir}/fetch_topics.js search <group_id> <keyword> [count] [--markdown] [--download-attachments]
```

- 默认通过官方 MCP tool `search_topics` 搜索主题：

```bash
zsxq-cli api call search_topics --params '{"group_id":"123456","query":"SpaceX IPO"}' --format json
```

- 当前官方 CLI 未文档化 `search_topics` 的分页参数，`count` 只作为客户端截断
- 搜索命中后使用 `topic +detail` 补全正文、图片和文件字段
- `--download-attachments` 会强制下载匹配帖子的附件
- `--markdown` 会按日期写入 Markdown

### 4. 获取指定帖子详情

```bash
node {baseDir}/fetch_topics.js topic <group_id> <topic_id_or_url> [--markdown]
```

支持纯帖子 ID 或完整链接。保留 `group_id` 参数用于兼容旧接口；CLI 后端实际执行：

```bash
zsxq-cli topic +detail --topic-id <topic_id> --json
```

### 5. 按日期范围抓取帖子

```bash
node {baseDir}/fetch_topics.js topics-by-date <group_id> <start_date> [end_date] [count] [--markdown]
```

- 日期格式：`YYYY-MM-DD`
- 帖子按时间倒序，遇到早于 `start_date` 的帖子自动停止翻页
- 支持附件自动下载和 Markdown 导出

### 6. 列出已加入的星球

```bash
node {baseDir}/fetch_topics.js groups
```

默认执行：

```bash
zsxq-cli group +list --json --limit 200 --scope all
```

返回当前账号已加入的所有星球信息。

---

## 附件下载行为

- 图片和文件按 `attachment_dir/group_id/YYYY-MM-DD/` 目录结构存放
- 附件文件名会加 `topic_id` 前缀，例如 `789_image_1.jpg`、`789_report.pdf`
- 已存在文件自动跳过
- 下载失败记录到 `attachments_local.error`，不中断主流程
- CLI 返回可下载 URL 时直接下载；若只有 `file_id`，legacy HTTP 下载 URL 查询可能需要 `ZSXQ_TOKEN`

## 错误处理

| 错误场景 | 处理 |
| --- | --- |
| 未安装 `zsxq-cli` | 返回 `zsxq_cli_missing`，提示 `npm install -g zsxq-cli` |
| 官方 CLI 未登录 | 返回 `zsxq_cli_not_authenticated`，提示 `zsxq-cli auth login` |
| 官方 CLI 非 JSON 输出 | 返回 `zsxq_cli_non_json` |
| 官方 CLI 命令失败 | 返回 `zsxq_cli_failed` 并保留截断后的 stderr/stdout |
| 精华标记缺失 | 返回 `digests_unavailable_from_cli`，不自动切换 HTTP |
| 单帖详情补全失败 | 搜索命中仍保留，结果中记录 `detail_error` |
| legacy HTTP token 未设置 | 仅在 `ZSXQ_BACKEND=http` 时提示设置 `ZSXQ_TOKEN` |
| legacy HTTP 429 | 指数退避并加入随机抖动 |
| 附件下载失败 | 记录错误并继续 |

## 1059 说明

默认路径使用官方 `zsxq-cli`，避免继续与知识星球对非官方客户端访问的 1059 风控对抗。本 Skill 不实现伪造官方客户端或绕过风控的逻辑。

如显式启用 legacy HTTP fallback 并遇到 `code: 1059`，应回到默认 CLI 后端：

```bash
unset ZSXQ_BACKEND
zsxq-cli auth login
```

---

## 详细 API 参考

如需了解 CLI 命令、输出归一化、legacy HTTP fallback 和错误码，参阅 `{baseDir}/references/api-reference.md`。
