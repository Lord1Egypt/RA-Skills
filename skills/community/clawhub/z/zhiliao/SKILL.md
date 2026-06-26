---
name: zhiliao
description: "知了 - AI 话题追踪与资讯聚合服务。通过自然语言创建追踪话题，自动从全网聚合相关文章并定时更新。适用场景：(1) 创建信息追踪话题（如追踪黄金价格、科技新闻、行业动态），(2) 获取和浏览话题下的聚合文章，(3) 设置定时任务定期抓取新文章，(4) 查看/管理话题列表，(5) 取消订阅不需要的话题。触发关键词：zhiliao、知了、话题追踪、资讯聚合、信息监控、追踪话题、创建话题、订阅话题、取消订阅、文章聚合。"
metadata: {"openclaw":{"emoji":"📰","primaryEnv":"ZHILIAO_API_KEY"}}
---

# 知了 - AI 话题追踪与资讯聚合

通过自然语言创建追踪话题，自动从全网聚合相关文章。使用 `command/` 目录下的 CLI 工具调用 API。

## 配置 API Key

用户需前往知了网站 (https://zhiliao.news/) 注册，并在 API Key 申请页面 (https://open.zhiliao.news/) 获取 API Key。

**方式一 — 环境变量（推荐）**：

```bash
export ZHILIAO_API_KEY="your-api-key-here"
```

**方式二 — 配置文件（永久保存）**：

```bash
mkdir -p ~/.zhiliao
echo '{"apiKey":"your-api-key-here","baseUrl":"http://api-public.zhiliao.news"}' > ~/.zhiliao/config.json
```

**额度说明**：每个 API Key 可免费创建 3 个话题，超出后需前往知了网站付费充值。

## 数据存储

所有数据保存在 `~/.zhiliao/` 目录（按需创建）：
- `config.json` — API Key 和服务地址
- `topics.json` — 已创建的话题列表
- `articles/<topic_id>.json` — 各话题的文章缓存
- `sessions/<scope>.json` — 创建话题的 session_id（幂等性）

## 工作流程

### 1. 创建话题（两步式：预览 + 确认）

采用「预览 → 用户选择 → 确认」的两步式流程创建话题：

1. **了解需求**：询问用户想追踪什么信息
2. **优化 prompt**：帮助用户细化描述，使话题更精准：
   - 模糊: "科技新闻" → 优化: "AI大模型技术进展，包括OpenAI、Google、Anthropic等公司的最新发布和研究突破"
   - 模糊: "股市" → 优化: "A股半导体板块行情分析，包括主要芯片公司股价走势和产业政策影响"
3. **调用预览命令**：获取待创建话题的预览和相关已有话题列表
4. **展示预览结果**：向用户展示：
   - 待创建的话题（名称、描述、封面图）
   - 相关的已有话题列表（可直接关注，无需重复创建）
5. **用户选择**：
   - 创建新话题 → 调用确认命令 `--action create`
   - 关注已有话题 → 调用确认命令 `--action subscribe --topic-id xxx`
   - 不满意 → 调整 prompt 重新预览

**会话隔离**：每次对话开始时生成一个独立的 `SCOPE`（6位随机字符串），在本次对话中所有创建话题操作复用同一个 `SCOPE`。

```bash
# 对话开始时生成 SCOPE（后续复用）
SCOPE=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 6)

# Step 1: 预览话题（返回 JSON，包含 session_id、created_topic、related_topics）
<skill-path>/command/create-topic.sh "优化后的PROMPT" "$SCOPE"

# Step 2a: 确认创建新话题
<skill-path>/command/create-topic.sh --confirm --session-id "SESSION_ID" --action create

# Step 2b: 或关注已有话题
<skill-path>/command/create-topic.sh --confirm --session-id "SESSION_ID" --action subscribe --topic-id "TOPIC_ID"
```

也可以使用 `--auto-create` 跳过预览直接创建：

```bash
<skill-path>/command/create-topic.sh "优化后的PROMPT" "$SCOPE" --auto-create
```

命令会自动处理：
- Session ID 的创建和管理
- `/generate` API 调用获取预览
- `/confirm` API 调用执行创建或关注
- 话题数据的本地保存

### 2. 获取话题文章

```bash
<skill-path>/command/fetch-articles.sh TOPIC_ID [LIMIT] [CURSOR]
```

参数说明：
- `TOPIC_ID` — 话题 ID（必填）
- `LIMIT` — 每页数量（可选，默认 20）
- `CURSOR` — 翻页游标（可选，用于获取下一页）

示例：
```bash
# 获取前 20 篇文章
<skill-path>/command/fetch-articles.sh 69afe54d037de4f01d67b756

# 获取前 10 篇
<skill-path>/command/fetch-articles.sh 69afe54d037de4f01d67b756 10

# 翻页（使用上次返回的 cursor）
<skill-path>/command/fetch-articles.sh 69afe54d037de4f01d67b756 20 "1773390505_2"
```

输出格式：Markdown，包含标题、原文链接、摘要、发布时间、核心观点。同时自动缓存到 `~/.zhiliao/articles/`。

### 3. 查看话题列表

```bash
# 列出所有话题
<skill-path>/command/list-topics.sh

# 查看单个话题详情及缓存文章
<skill-path>/command/list-topics.sh TOPIC_ID
```

输出格式：Markdown 表格，包含话题 ID、名称、描述、创建时间、缓存状态。

### 4. 取消订阅话题

当用户不再需要追踪某个话题时，引导用户先通过 `list-topics` 查看话题 ID，再执行取消订阅：

```bash
# 查看话题列表，获取 TOPIC_ID
<skill-path>/command/list-topics.sh

# 取消订阅
<skill-path>/command/unsubscribe-topic.sh TOPIC_ID
```

取消订阅成功后，命令会自动清理本地话题记录和文章缓存。

### 5. 检查所有话题更新

```bash
<skill-path>/command/check-articles.sh
```

遍历本地话题列表，对每个话题调用 API 获取最新文章（前 10 篇），汇总展示并更新缓存。

### 6. 定时任务（OpenClaw Cron）

**每天早上8点日报**：
```bash
openclaw cron add --cron "0 8 * * *" --isolated --prompt "运行知了文章检查: <skill-path>/command/check-articles.sh"
```

**每小时检查一次**：
```bash
openclaw cron add --cron "0 * * * *" --isolated --prompt "运行知了文章检查: <skill-path>/command/check-articles.sh"
```

**Cron 表达式格式**：`分钟 小时 日 月 星期`
- `0 8 * * *` — 每天8:00
- `0 */2 * * *` — 每2小时
- `*/15 * * * *` — 每15分钟
- `0 9-17 * * 1-5` — 工作日9:00-17:00每小时

**管理定时任务**：
```bash
openclaw cron list              # 查看所有任务
openclaw cron remove <jobId>    # 删除任务
```

## 错误处理

- **未配置 API Key**：命令会提示配置方法
- **API 返回错误**：展示错误信息；若提示额度不足，引导用户付费充值
- **网络错误**：命令会报错退出
- **话题文章为空**：话题刚创建需要时间聚合，建议稍后再查

## 技术实现

所有命令使用 **curl + jq + iconv** 实现：
- `iconv -c -t UTF-8` — 清理 API 响应中的控制字符
- `jq` — 解析 JSON 和格式化输出
- 临时文件 — 避免 bash 变量保留控制字符
- `select(.field == $value | not)` — 避免 zsh 的 `!=` 转义问题

## 命令列表

| 命令 | 功能 | 用法 |
|------|------|------|
| `create-topic` | 预览话题 | `./create-topic.sh "描述" [SCOPE]` |
| `create-topic` | 预览并自动创建 | `./create-topic.sh "描述" [SCOPE] --auto-create` |
| `create-topic` | 确认创建/关注 | `./create-topic.sh --confirm --session-id ID --action create\|subscribe [--topic-id ID]` |
| `fetch-articles` | 获取文章 | `./fetch-articles.sh TOPIC_ID [LIMIT] [CURSOR]` |
| `list-topics` | 查看话题列表 | `./list-topics.sh [TOPIC_ID]` |
| `unsubscribe-topic` | 取消订阅话题 | `./unsubscribe-topic.sh TOPIC_ID` |
| `check-articles` | 检查所有话题更新 | `./check-articles.sh` |

所有命令位于 `command/` 目录，已添加执行权限。
