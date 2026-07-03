---
name: 热点检索输出报文
description: "定时从白名单企业（默认 OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX）抓取24小时内热点，用搜索工具 content摘要直接撰写中文短文（默认400 字），发送纯文字（默认3 条、无图）到推送渠道。模型、搜索、白名单、字数、推送渠道、触发时间全部可配置，含反幻觉+敏感词回避规则。"
---

# 热点检索输出报文

定时向推送渠道发送多条科技/AI热点纯文字短文。所有关键参数可配置。

## 适用场景

- 用户希望定时收到 AI / 科技 / 互联网行业资讯
- 推送渠道任意（支持微信 iLink AI、Telegram、Slack、Email 等）
- 内容限定在白名单企业内
- 要求事实可查、来源可溯、不发图、不幻觉

## 配置变量（全部可改）

修改这些变量即可改变任务行为，无需改 prompt / cron job 主体。

| 变量 | 默认值 | 说明 |
|---|---|---|
| `MODEL` | `minimax/MiniMax-M2.7` | 生成模型。也可选 M3、Claude Sonnet/Opus 等 |
| `SEARCH_PROVIDER` | `tavily` | 搜索后端。也可选 `brave` / `searxng` |
| `WHITELIST` | `OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX` | 话题来源限定（用 `·` 分隔）|
| `ARTICLE_COUNT` | `3` | 每次推送条数（1-5 推荐）|
| `WORDS_PER_ARTICLE` | `400` | 每条字数（推荐 300-600）|
| `SEND_IMAGE` | `false` | 是否发图。本机抓图不可靠，强烈建议保持 false |
| `SCHEDULE_EXPR` | `15 23 * * *` | cron 表达式（默认每天 23:15）|
| `STAGGER_MS` | `2700000` | 抖动毫秒数（45min）。设为 0 则固定时间触发 |
| `SCHEDULE_TZ` | `Asia/Shanghai` | 时区 |
| `DELIVERY_CHANNEL` | `openclaw-weixin` | 推送渠道（如 openclaw-weixin / telegram / email）|
| `RECIPIENT` | `收到人 ID，格式依 channel 而定` | 接收人 ID |
| `DELIVERY_ACCOUNT_ID` | `已配对的 bot 实例 ID` | 推送渠道对应的已配对账号 |
| `SENSITIVE_WORDS` | `武器/生物/政治/中国政策` | 触发内容过滤的话题关键词，遇到则换话题 |
| `TIMEOUT_SECONDS` | `300` | 任务超时 |

> **完整变量定义**见 `references/variables.md`。修改后用 `envsubst` 或手动替换 `${VAR}` 即可重新生成 prompt。

## 反幻觉 / 反内容过滤硬约束

```
- 只准用 ${SEARCH_PROVIDER} content 摘要里写明的事实，禁止脑补数字、人名、日期
- 不发图、不调用 image_generate（SEND_IMAGE=false 时强制）
- 避免触发内容过滤：不写 "${SENSITIVE_WORDS}" 等敏感词；
  如选中的话题包含敏感词，换个白名单企业的话题
- 话题必须来源于白名单（${WHITELIST}），其他公司一律不发
- 每篇必须有可验证的来源 URL（${SEARCH_PROVIDER} 返回的 source URL 字段）
- 如果凑不到 ${ARTICLE_COUNT} 条真实热点，宁可少发也不要凑数或编造
```

## 不需要做的事

- **不要调用 web_fetch** —— 本机抓 Bloomberg / Reuters / Yahoo 全部超时或 403
- **不要下载图片** —— ${SEARCH_PROVIDER} 不返回稳定 image_url，且 SEND_IMAGE=false
- **不要使用 Unsplash / 通用图库**
- **不要用 image_generate 编造配图**（除非 SEND_IMAGE=true 且明确需要占位图）

## 操作步骤（agent 视角）

1. `web_search` 搜索白名单（${WHITELIST}）过去 24h 内的最新动态（中英文各一次，并行）
2. 筛选出最有爆点的 ${ARTICLE_COUNT} 条热点（最好来自不同公司）
3. 仅用 ${SEARCH_PROVIDER} 返回的 `content` 字段（200-500 字摘要）作为正文基础
4. 每条撰写 ${WORDS_PER_ARTICLE} 字左右中文短文，文末标注「来源：[媒体名] [URL]」
5. 用 `message` 工具依次发到 ${RECIPIENT}
6. 任务结束简短报告：发了 X 条、每条的企业归属、每条来源 URL、字数

## 重建 / 复用本任务（按变量配置）

### 1. 确认基础设施

```bash
# 推送 channel 已配对
openclaw channels list

# 搜索工具已配（${SEARCH_PROVIDER} 对应的 API key 已设置）
grep -E "TAVILY_API_KEY|BRAVE_API_KEY" ~/.openclaw/openclaw.json ~/.openclaw/secrets/*.env

# 模型已在 agents.defaults.models 列出
grep "models" ~/.openclaw/openclaw.json
```

### 2. 渲染 prompt 模板

```bash
# 用 envsubst 把 ${VAR} 替换为环境变量或默认值
envsubst < references/prompt.md > /tmp/prompt-rendered.md
```

### 3. 创建 cron job

```bash
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

### 4. 验证

```bash
openclaw cron run --id <job-id>  # 手动触发
openclaw cron list               # 看状态
openclaw cron runs --id <job-id>  # 看历史
```

## 配置切换示例

### 换模型为 M3

```bash
MODEL=minimax/MiniMax-M3 openclaw cron update --id <job-id> \
  --patch '{"payload": {"model": "minimax/MiniMax-M3"}}'
```

### 换搜索工具为 Brave

```bash
# 1. 配 Brave API key
# 2. 改 openclaw.json: tools.web.search.provider = "brave"
# 3. 改 prompt 里的 "tavily" → "brave"
SEARCH_PROVIDER=brave openclaw cron update --id <job-id> \
  --patch "$(cat <(sed 's/tavily/brave/g' prompt.md))"
```

### 换字数

```bash
WORDS_PER_ARTICLE=500 envsubst < references/prompt.md > prompt-500.md
openclaw cron update --id <job-id> --prompt-file prompt-500.md
```

### 加新白名单企业

```bash
WHITELIST="OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX·Meta"
envsubst < references/prompt.md > prompt-meta.md
openclaw cron update --id <job-id> --prompt-file prompt-meta.md
```

### 切到 Telegram

```bash
DELIVERY_CHANNEL=telegram \
RECIPIENT=<telegram-chat-id> \
DELIVERY_ACCOUNT_ID=<telegram-bot-id> \
  envsubst < references/prompt.md > prompt-tg.md
openclaw cron update --id <job-id> --prompt-file prompt-tg.md
# 同时改 delivery 段
```

## 已知坑

### 1. iLink AI 沙盒化 / 14 分钟配额窗口

**症状**：cron 报 `delivered:true`，plugin 返回 `messageId`，**用户实际收不到任何消息**。

**根因**：iLink AI 后端对 sandbox/test bot 限制严格，配对后约 14 分钟内可正常投递，之后 sendMessage 端点进入"兼容式 stub"模式。

**诊断命令**（直接 curl 打 iLink AI）：

```bash
# 获取 token
TOKEN=$(cat ~/.openclaw/openclaw-weixin/accounts/<bot-id>.json | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")

# Test: sendMessage
curl -s -w "\n[HTTP %{http_code}]" -X POST \
  -H "Content-Type: application/json" \
  -H "AuthorizationType: ilink_bot_token" \
  -H "X-WECHAT-UIN: dGVzdA==" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"msg":{"to_user_id":"<openid>@im.wechat","client_id":"cli_test","message_type":1,"message_state":2,"item_list":[{"type":1,"text_item":{"text":"test"}}]},"base_info":{"channel_version":"0.6.0","bot_agent":"openclaw/0.6.0"}}' \
  https://ilinkai.weixin.qq.com/ilink/bot/sendmessage
# 正常: {"errcode":0, ...}
# 沙盒化: {} + HTTP200

# Test: getConfig
curl -s -w "\n[HTTP %{http_code}]" -X POST \
  -H "Content-Type: application/json" \
  -H "AuthorizationType: ilink_bot_token" \
  -H "X-WECHAT-UIN: dGVzdA==" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"ilink_user_id":"<bot-id>@im.bot:<token-suffix>","base_info":{"channel_version":"0.6.0","bot_agent":"openclaw/0.6.0"}}' \
  https://ilinkai.weixin.qq.com/ilink/bot/getconfig
# 正常: {"ret":0, ...}
# 沙盒化: {"ret":-4,"errmsg":"GetTypingTicket rpc failed"} + HTTP200
```

**临时缓解**：重新配对拿新 token。
**长期方案**：登录 iLink AI 后台查看 bot 健康/配额，或换 channel（ Telegram / Slack / Email）。

### 2. Cron delivery.accountId 指向已失效 bot

**症状**：cron 跑完报 `delivered:true`，但消息丢失。
**原因**：bot token 过期或被吊销，但 cron job 的 `delivery.accountId` 没同步更新。
**修复**：重配对后立即同步更新 cron job。

### 3. Web fetch 全失败

**症状**：Bloomberg / Reuters / Yahoo 等返回 30s 超时或 403。
**修复**：不再调用 web_fetch，只用 ${SEARCH_PROVIDER} content 字段。

### 4. 内容过滤 `output new_sensitive`

**症状**：模型输出截断，`stopReason: error`，message tool 调用被吞掉。
**修复**：SENSITIVE_WORDS 列表触发后主动换话题，不要写"AI"以外的元话题（行业政策/监管/中美关系）。

### 5. 旧 bot token 过期

**症状**：savedAt 超过 8 天的 token 在 iLink AI 后端被静默吊销。
**修复**：定期重配对。

## 重新配对微信 bot

```bash
# 1. 停 gateway（用 nohup 脱钩避免杀掉 exec session）
nohup systemctl --user stop openclaw-gateway > /dev/null 2>&1 &

# 2. 删旧 token 文件
rm ~/.openclaw/openclaw-weixin/accounts/<old-bot-id>.json
rm ~/.openclaw/openclaw-weixin/accounts/<old-bot-id>.sync.json
rm ~/.openclaw/openclaw-weixin/accounts/<old-bot-id>.context-tokens.json
echo '[]' > ~/.openclaw/openclaw-weixin/accounts.json

# 3. 启 gateway
systemctl --user start openclaw-gateway

# 4. PTY 模式跑 login 拿 QR
script -qfc "openclaw channels login --channel openclaw-weixin" /tmp/weixin-login.log

# 5. 手机微信扫 QR → 同意授权
# 6. 新 bot id 自动写入

# 7. 同步更新所有相关 cron job 的 delivery.accountId
# 8. 用 curl 验证新 bot 是否被沙盒化（见上文）
```

## 相关文件

- `references/variables.md` — 完整变量定义与默认值
- `references/prompt.md` — 完整 prompt 模板（含 `${VAR}` 占位符）
- `references/cron-config.md` — cron job 字段定义与默认值