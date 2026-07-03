# Cron Job 配置详解

所有字段都可以通过 `${VAR}` 引用变量（详见 `references/variables.md`）。

## Cron job 结构模板

```json
{
  "name": "daily-tech-news",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "${SCHEDULE_EXPR}",
    "staggerMs": ${STAGGER_MS},
    "tz": "${SCHEDULE_TZ}"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "<见 references/prompt.md，用 envsubst 渲染后填入>",
    "timeoutSeconds": ${TIMEOUT_SECONDS},
    "model": "${MODEL}"
  },
  "delivery": {
    "mode": "announce",
    "channel": "${DELIVERY_CHANNEL}",
    "to": "${RECIPIENT}",
    "accountId": "${DELIVERY_ACCOUNT_ID}"
  },
  "description": "每日AI/科技热点 ${ARTICLE_COUNT} 篇文字推送（每篇 ${WORDS_PER_ARTICLE} 字，仅文字无图）"
}
```

## 字段说明

### schedule

| 字段 | 变量 | 默认 | 说明 |
|---|---|---|---|
| `kind` | — | `cron` | 使用 cron 表达式 |
| `expr` | `SCHEDULE_EXPR` | `15 23 * * *` | cron 表达式（5字段）|
| `staggerMs` | `STAGGER_MS` | `2700000` | 在基础时间上随机加 0-N 毫秒抖动 |
| `tz` | `SCHEDULE_TZ` | `Asia/Shanghai` | IANA 时区名 |

### payload

| 字段 | 变量 | 默认 | 说明 |
|---|---|---|---|
| `kind` | — | `agentTurn` | 触发 agent 执行 |
| `message` | — | (prompt渲染结果) | 用 envsubst 渲染 `references/prompt.md` |
| `timeoutSeconds` | `TIMEOUT_SECONDS` | `300` | 5 分钟 |
| `model` | `MODEL` | `minimax/MiniMax-M2.7` | 强制指定模型避免 fallback |

### delivery

| 字段 | 变量 | 默认 | 说明 |
|---|---|---|---|
| `mode` | — | `announce` | 完成后主动推送 |
| `channel` | `DELIVERY_CHANNEL` | `openclaw-weixin` | 推送渠道 |
| `to` | `RECIPIENT` | `<依 channel 而定>` | 接收人 |
| `accountId` | `DELIVERY_ACCOUNT_ID` | `<已配对的 bot 实例>` | 已配对的 bot 实例 |

### sessionTarget

`isolated` — 每次运行独立 session，互不干扰。

## 创建新 cron job 的完整步骤

```bash
# 1. 设变量（按需修改）
export MODEL=minimax/MiniMax-M2.7
export SEARCH_PROVIDER=tavily
export WHITELIST="OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX"
export ARTICLE_COUNT=3
export WORDS_PER_ARTICLE=400
export SEND_IMAGE=false
export SCHEDULE_EXPR="15 23 * * *"
export STAGGER_MS=2700000
export SCHEDULE_TZ=Asia/Shanghai
export DELIVERY_CHANNEL=openclaw-weixin
export RECIPIENT="<your-openid>@im.wechat"
export DELIVERY_ACCOUNT_ID="<your-bot-id>"
export SENSITIVE_WORDS="武器/生物/政治/中国政策"
export TIMEOUT_SECONDS=300

# 2. 渲染 prompt
envsubst < references/prompt.md > /tmp/prompt-rendered.md

# 3. 创建 cron job
openclaw cron add \
  --name "daily-tech-news" \
  --schedule "${SCHEDULE_EXPR}" \
  --tz "${SCHEDULE_TZ}" \
  --stagger ${STAGGER_MS} \
  --model "${MODEL}" \
  --agent main \
  --target isolated \
  --timeout ${TIMEOUT_SECONDS} \
  --prompt-file /tmp/prompt-rendered.md \
  --delivery-mode announce \
  --delivery-channel "${DELIVERY_CHANNEL}" \
  --delivery-to "${RECIPIENT}" \
  --delivery-account "${DELIVERY_ACCOUNT_ID}"
```

## 触发与状态查询

```bash
# 手动触发
openclaw cron run --id <job-id>

# 查看状态
openclaw cron list

# 查看历史
openclaw cron runs --id <job-id>

# 查看完整 job 配置
openclaw cron get --id <job-id>
```

## 常用修改场景

### 改字数（只改 prompt）

```bash
export WORDS_PER_ARTICLE=500
envsubst < references/prompt.md > /tmp/prompt-500.md
openclaw cron update --id <job-id> --prompt-file /tmp/prompt-500.md
```

### 改模型（只改 cron 字段）

```bash
openclaw cron update --id <job-id> --patch '{
  "payload": {"model": "minimax/MiniMax-M3"}
}'
```

### 改触发时间

```bash
openclaw cron update --id <job-id> --patch '{
  "schedule": {"expr": "09 * * *", "staggerMs":0}
}'
```

### 加白名单企业

```bash
export WHITELIST="OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX·Meta"
envsubst < references/prompt.md > /tmp/prompt-meta.md
openclaw cron update --id <job-id> --prompt-file /tmp/prompt-meta.md
```

### 切换到其他 channel

```bash
# 微信 → Telegram 切换
export DELIVERY_CHANNEL=telegram
export RECIPIENT="<telegram-chat-id>"
export DELIVERY_ACCOUNT_ID="<telegram-bot-id>"
envsubst < references/prompt.md > /tmp/prompt-tg.md

openclaw cron update --id <job-id> --patch "{
  \"payload\": {\"message\": \$(jq -Rs . < /tmp/prompt-tg.md)},
  \"delivery\": {
    \"mode\": \"announce\",
    \"channel\": \"telegram\",
    \"to\": \"<telegram-chat-id>\",
    \"accountId\": \"<telegram-bot-id>\"
  }
}"
```

## 字数 vs 用时（实测）

| 字数 | 用时 (M2.7) | 用时 (M3) | 备注 |
|---|---|---|---|
| 300 | ~40s | ~150s | 太短，内容单薄 |
| **400** | **~67s** | ~270s | **推荐配置** |
| 500 | ~110s | ~350s | 偶尔触发内容过滤 |

## 模型选择（实测）

| Model | 用时（400字 ×3 条）| 备注 |
|---|---|---|
| `minimax/MiniMax-M2.7` | **~67s** | **推荐默认**，稳定 |
| `minimax/MiniMax-M3` | ~270s | 内容质量略好，但慢 4 倍 |
| `anthropic/claude-sonnet-4-6` | ~120s | 内容质量高，但有 prompt injection 风险 |
| `anthropic/claude-opus-4-8` | ~180s | 最优质量但慢且贵 |

## 切换 search provider

需要同时改 3 处：

```bash
# 1. 改 ~/.openclaw/openclaw.json 的 provider
# tools.web.search.provider = "brave" # 或 searxng

# 2. 配对应 API key
# ~/.openclaw/secrets/*.env:
# BRAVE_API_KEY=...

# 3. 改 prompt 里的 ${SEARCH_PROVIDER}
export SEARCH_PROVIDER=brave
envsubst < references/prompt.md > /tmp/prompt-brave.md
openclaw cron update --id <job-id> --prompt-file /tmp/prompt-brave.md
```