# 配置变量完整定义

所有变量都可以通过 `envsubst` 替换或手动修改来调整任务行为。

## 完整变量表

| 变量名 | 默认值 | 必填 | 说明 |
|---|---|---|---|
| `MODEL` | `minimax/MiniMax-M2.7` | 是 | 生成模型 ID |
| `SEARCH_PROVIDER` | `tavily` | 是 | 搜索后端（`tavily` / `brave` / `searxng`）|
| `SEARCH_API_KEY_ENV` | `TAVILY_API_KEY` | 是 | 对应 API key 的环境变量名 |
| `WHITELIST` | `OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX` | 是 | 话题来源限定（用 `·` 分隔）|
| `ARTICLE_COUNT` | `3` | 是 | 每次推送条数（1-5 推荐）|
| `WORDS_PER_ARTICLE` | `400` | 是 | 每条字数（推荐 300-600）|
| `SEND_IMAGE` | `false` | 是 | 是否发图（true / false）|
| `SCHEDULE_EXPR` | `15 23 * * *` | 是 | cron 表达式（5 字段）|
| `STAGGER_MS` | `2700000` | 否 | 抖动毫秒（0 = 固定时间触发）|
| `SCHEDULE_TZ` | `Asia/Shanghai` | 是 | 时区（IANA 名）|
| `DELIVERY_CHANNEL` | `openclaw-weixin` | 是 | 推送渠道 ID |
| `RECIPIENT` | `<收到人 ID，依 channel 而定>` | 是 | 接收人 ID（按 channel 格式）|
| `DELIVERY_ACCOUNT_ID` | `<已配对的 bot 实例 ID>` | 是 | 已配对的 bot / account 实例 |
| `SENSITIVE_WORDS` | `武器/生物/政治/中国政策` | 是 | 触发内容过滤的关键词，遇到则换话题 |
| `TIMEOUT_SECONDS` | `300` | 是 | 任务超时（秒）|

## 衍生配置（非变量，但跟变量关联）

| 项 | 默认 | 说明 |
|---|---|---|
| cron job 名 | `daily-tech-news` | 可改，但跟 schedule 关联 |
| cron job 描述 | `每日AI/科技热点 ${ARTICLE_COUNT} 篇文字推送（每篇 ${WORDS_PER_ARTICLE} 字，仅文字无图）` | 自由文本 |
| agent ID | `main` | 通常不变 |
| session target | `isolated` | 每次独立 session |

## 变量修改方法

### 方法1：envsubst 渲染

```bash
# 1. 设变量
export MODEL=minimax/MiniMax-M2.7
export SEARCH_PROVIDER=tavily
export WHITELIST="OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX"
# ... 其他变量

# 2. 渲染 prompt
envsubst < references/prompt.md > /tmp/prompt-rendered.md

# 3. 更新 cron job
openclaw cron update --id <job-id> --prompt-file /tmp/prompt-rendered.md
```

### 方法2：手动 sed 替换

```bash
# 改模型为 M3
sed -i 's/${MODEL}/minimax\/MiniMax-M3/g' references/prompt.md
# 改字数为500
sed -i 's/${WORDS_PER_ARTICLE}/500/g' references/prompt.md
# 渲染
cp references/prompt.md /tmp/prompt-rendered.md
```

### 方法3：OpenClaw cron update --patch（仅 cron 字段，不改 prompt）

```bash
# 改 schedule
openclaw cron update --id <job-id> --patch '{
  "schedule": {"expr": "09 * * *", "staggerMs":0, "tz": "Asia/Shanghai"}
}'

# 改 model
openclaw cron update --id <job-id> --patch '{
  "payload": {"model": "minimax/MiniMax-M3"}
}'
```

## 切换不同 channel 时的变量对照

| Channel | DELIVERY_CHANNEL | RECIPIENT 格式 | DELIVERY_ACCOUNT_ID |
|---|---|---|---|
| 微信 iLink AI | `openclaw-weixin` | `<openid>@im.wechat` | `<bot-id>-im-bot` |
| Telegram | `telegram` | `<chat-id>`（数字）| `<bot-username>` |
| Slack | `slack` | `#channel` 或 `<user-id>` | `<workspace>-bot` |
| Email | `email` | `<email-address>` | N/A |

切换 channel 时只需要改这 3 个变量 + cron job 的 delivery 段。

## 切换不同 search provider 时的变量对照

| Provider | SEARCH_PROVIDER | SEARCH_API_KEY_ENV | 配置位置 |
|---|---|---|---|
| Tavily | `tavily` | `TAVILY_API_KEY` | `~/.openclaw/openclaw.json` + `~/.openclaw/secrets/*.env` |
| Brave | `brave` | `BRAVE_API_KEY` | 同上 |
| SearXNG | `searxng` | N/A（自托管 URL）| `tools.web.search.searxng.baseUrl` |

切换时改 `~/.openclaw/openclaw.json` 的 `tools.web.search.provider`，并更新对应 API key。

## 切换不同 model 时的变量对照

| Model | 速度 (400字 ×3条) | 内容质量 | 内容过滤严格度 |
|---|---|---|---|
| `minimax/MiniMax-M2.7` | ~67s | 良好 | 中 |
| `minimax/MiniMax-M3` | ~270s | 较好 | 中 |
| `anthropic/claude-sonnet-4-6` | ~120s | 优秀 | 低（但有 prompt injection 风险）|
| `anthropic/claude-opus-4-8` | ~180s | 最优 | 低 |

## 推荐的变量组合

### 配置1：快速稳定（默认）
```
MODEL=minimax/MiniMax-M2.7
WORDS_PER_ARTICLE=400
SEARCH_PROVIDER=tavily
```
**适用**：日常推送，稳定 67 秒完成。

### 配置2：内容优先
```
MODEL=minimax/MiniMax-M3
WORDS_PER_ARTICLE=500
SEARCH_PROVIDER=tavily
```
**适用**：希望文章质量高、不在意用时（270s）。

### 配置3：多频次
```
SCHEDULE_EXPR="09,12,18 * * *"
STAGGER_MS=0
ARTICLE_COUNT=2
WORDS_PER_ARTICLE=300
```
**适用**：早中晚各推一次，每次 2 条短文。