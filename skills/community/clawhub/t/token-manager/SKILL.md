---
name: token-manager
description: Universal LLM Token Manager - Monitor usage and provide cost-saving recommendations for Kimi/Moonshot, DeepSeek, OpenAI, Anthropic, Gemini, and local models. Features scheduled balance monitoring, cross-session tracking, and proactive alerts.
---

# Token Manager

通用 LLM Token 管家：费用估算、余额查询、跨会话用量统计、余额告警。所有命令输出 JSON，任何能执行 shell 命令的 agent 都可直接使用。

## 功能

- 费用估算：按各 provider 官方牌价计算输入/输出费用
- 余额查询：Kimi/Moonshot、DeepSeek 官方余额 API（其余 provider 需登录控制台）
- Token 估算：Kimi 官方 estimate-token-count API，失败自动回落本地近似估算
- 跨会话统计：daily/weekly 报告，按币种分组（不混算 CNY/USD）
- 余额告警：可配阈值 + 冷却期，低余额时双语提醒

## 环境变量

API Key 优先从环境变量读取：

| Provider | 环境变量 |
|----------|----------|
| Kimi/Moonshot | `MOONSHOT_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Gemini | `GEMINI_API_KEY`（或 `GOOGLE_API_KEY`） |
| Ollama | 无需 |

所有命令均支持 `--api-key` 临时传参，仅供调试——注意 shell 历史与进程列表会留痕，日常请用环境变量。

## 命令参考

脚本位于 `scripts/`，所有输出为 JSON。

### manager.js

```bash
# 完整报告（会话上下文 → 费用 + 余额 + 建议）
node scripts/manager.js report \
  --tokens-in 11000 --tokens-out 146 \
  --context-used 42000 --context-max 200000 \
  --thinking off \
  --provider moonshot --model kimi-k3.1-pro

# 查询余额
node scripts/manager.js balance deepseek

# Token 数估算（Kimi 官方 API 优先；无 key 或失败时本地近似）
node scripts/manager.js tokens moonshot "要估算的文本"
node scripts/manager.js tokens moonshot '[{"role":"user","content":"..."}]' --model kimi-k3.1-pro

# 费用估算（不外联）
node scripts/manager.js estimate deepseek 1000000 300000 deepseek-flash

# 其他
node scripts/manager.js providers          # 列出支持的 provider
node scripts/manager.js set-provider deepseek
node scripts/manager.js history            # 查看使用历史
```

`report` 全部为命名参数：`--tokens-in --tokens-out --context-used --context-max --thinking --balance --provider --model --api-key`。`--context-max` 缺省取 provider 上下文窗口（未配置时 200000）；`--balance` 可手动传入余额跳过 API 查询。

价格按模型精确匹配：模型不在价格表内时返回错误并列出已知模型，**绝不猜价**。

### scheduler.js（余额监控）

```bash
node scripts/scheduler.js check moonshot 5   # 余额低于 ¥5 时告警（默认阈值 5）
node scripts/scheduler.js stats              # 告警历史统计
```

告警冷却：余额 < ¥1 冷却 30 分钟，否则 1 小时。历史保留 30 天。输出 `exit 1` + 双语告警文案，方便 cron/hook 捕获。

### session-tracker.js（跨会话统计）

```bash
node scripts/session-tracker.js record moonshot kimi-k3.1-pro 11000 146 0.15 CNY
node scripts/session-tracker.js daily          # 今日报告
node scripts/session-tracker.js weekly         # 近 7 天报告 + 趋势
node scripts/session-tracker.js recommend      # 省钱建议
```

sessions 日志保留 90 天；费用按币种分组聚合，趋势按币种分别计算。

## 各 Agent 平台接入

### OpenClaw

```bash
# 定时余额监控（每 30 分钟）
openclaw cron add "token-check" "node /path/to/token-manager/scripts/scheduler.js check moonshot 5" --cron "*/30 * * * *"

# 会话结束时记录用量（可选）
node scripts/session-tracker.js record "$PROVIDER" "$MODEL" "$TOKENS_IN" "$TOKENS_OUT" "$COST" "$CURRENCY"
```

### Claude Code / Codex / pi / 其他 agent

本 skill 无平台依赖，核心是三个零依赖 Node 脚本。接入方式：

1. **Stop hook / 会话结束钩子**：解析本次会话 token 用量后调用 `session-tracker.js record ...`
2. **定时任务**：cron 调用 `scheduler.js check <provider> <threshold>`，非零退出码即告警
3. **按需调用**：任务前用 `manager.js estimate` 预估费用，任务后用 `manager.js report` 生成报告

省钱建议（脚本也会在报告中输出）：
- 大批量任务优先 `--thinking off` 或子代理
- 非关键任务用低价模型：DeepSeek Flash、GPT-6 Luna、Claude Haiku、Gemini Flash、kimi-*-highspeed
- Kimi K3 系支持上下文缓存，重复前缀自动省钱

## 价格维护

内置价格为 **2026-11-09** 快照（每百万 tokens）：

| Provider | 模型 | 输入 | 输出 | 币种 |
|----------|------|------|------|------|
| moonshot | kimi-k3.1-pro（默认） | 13 | 26 | CNY |
| moonshot | kimi-k3.1-pro-highspeed | 26 | 52 | CNY |
| moonshot | kimi-k3 | 20 | 40 | CNY |
| moonshot | kimi-k2.7-code / kimi-k2.6 | 6.5 | 27 | CNY（2026-12 下线） |
| deepseek | deepseek-flash（默认，峰值价） | 2 | 8 | CNY |
| deepseek | deepseek-v4-pro（峰值价） | 9 | 27 | CNY |
| openai | gpt-6.1-terra（默认） | $1 | $5 | USD |
| openai | gpt-6.1-sol | $2 | $10 | USD |
| openai | gpt-6-luna-pro | $0.10 | $0.50 | USD |
| anthropic | claude-sonnet-5.5（默认） | $2 | $10 | USD |
| anthropic | claude-haiku-5.5 | $0.10 | $0.50 | USD |
| anthropic | claude-opus-5.5 | $4 | $20 | USD |
| gemini | gemini-4-argon（默认） | $2 | $10 | USD |
| gemini | gemini-3.8-flash | $0.75 | $3.75 | USD |
| ollama | 本地模型 | FREE | FREE | — |

DeepSeek 峰值时段为北京时间工作日 9-12/14-18 点，其余时段约半价，上表按峰值计。价格会过时，更新方式：编辑 `scripts/manager.js` 中 `DEFAULT_CONFIG.providers.<id>.pricing`，或改本地覆盖文件 `.data/config.json`（不改默认源码）。

## 数据文件

均在 `scripts/../.data/`（可用环境变量 `TOKEN_MANAGER_DATA_DIR` 重定向）：

- `config.json` — 用户配置（provider、价格覆盖）
- `token-usage.json` — manager 使用历史
- `sessions.json` — 跨会话用量日志（90 天）
- `alert-state.json` — 告警状态与历史（30 天）

## 安全说明

- API Key 优先从环境变量读取；`--api-key` 仅供临时调试
- 所有数据仅存本地 `.data/`，无遥测、不上传
- 网络请求仅访问官方 LLM API（余额/Token 估算）
