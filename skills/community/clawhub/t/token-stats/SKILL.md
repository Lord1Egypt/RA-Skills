---
name: token-stats
description: "统计 OpenClaw 的 token 用量。扫描所有 session JSONL 文件，输出 prompt/cache/output token 明细。Use when: user asks about token usage, cost, consumption, how many tokens were used, or token statistics."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
---

# Token Stats

统计 OpenClaw 全部会话的 token 用量，基于 session JSONL 文件的原始数据。

## When to Use

✅ **USE this skill when:**

- "用了多少 token？"
- "统计一下 token 消耗"
- "看看用量" / "token 用量"
- "每天消耗多少？"
- "哪个会话最费 token？"
- "缓存命中率怎么样？"

## Quick Start

```bash
# 基础统计（仅全局汇总）
python3 {baseDir}/scripts/token_stats.py

# 包含已删除会话（完整历史）
python3 {baseDir}/scripts/token_stats.py --include-deleted

# 每日明细
python3 {baseDir}/scripts/token_stats.py --daily

# 每日明细 + 会话排名
python3 {baseDir}/scripts/token_stats.py --daily --sessions

# 指定日期范围
python3 {baseDir}/scripts/token_stats.py --since 2026-03-01 --until 2026-03-16

# Top 20 会话
python3 {baseDir}/scripts/token_stats.py --sessions --top 20

# JSON 输出（可供其他工具消费）
python3 {baseDir}/scripts/token_stats.py --format json --daily

# 完整报告
python3 {baseDir}/scripts/token_stats.py --include-deleted --daily --sessions --top 20
```

## Token 计算方法

### 数据来源

唯一可靠的数据源是 session JSONL 文件（`~/.openclaw/agents/<agent>/sessions/*.jsonl`）。
`sessions.json` 只存最后一次 API 调用的快照，不适合做累计统计。

### 数据位置

Token 数据在 JSONL 条目中的路径：
```
entry.message.usage  (仅 role=assistant 的条目)
```

注意：usage 在 `message` 子对象里面，不在顶层。

### 字段说明

| 字段 | 含义 | 可靠性 |
|------|------|--------|
| `input` | API prompt_tokens - cacheRead - cacheWrite | ❌ 经常为负数 |
| `output` | 输出 token（含 thinking） | ✅ 可靠 |
| `cacheRead` | 缓存命中的 prompt token | ✅ 可靠 |
| `cacheWrite` | 新写入缓存的 token | ⚠️ 通过 New-API 永远为 0 |
| `totalTokens` | input + output + cacheRead + cacheWrite | ❌ 受 input 负值影响 |
| `cost` | 费用 | ⚠️ 通过 New-API 永远为 0 |

### 为什么 input 为负数

```
Provider 返回: prompt_tokens = 3 (仅未缓存部分)
Provider 返回: cached_tokens = 19531
OpenClaw 计算: input = prompt_tokens - cacheRead = 3 - 19531 = -19528
```

某些 provider (如 Kimi/Moonshot) 的 `prompt_tokens` 已排除缓存部分，
但 OpenClaw 又减了一次，导致双重扣除。

### 正确公式

```python
# 每次调用的真实 prompt token 数
fresh_input = max(input, 0)       # 新增未缓存 token
prompt = cacheRead + fresh_input  # 总 prompt (含缓存)

# 总 token = prompt + output
total = prompt + output
```

### 不可靠的统计方式

- ❌ 直接累加 `input` → 总和会是负数
- ❌ 用 `totalTokens - output` 算 prompt → totalTokens 已被负 input 压低
- ❌ 看 `sessions.json` → 只是最后一次调用的快照，compaction 后重置

## Compaction 的影响

OpenClaw 会在上下文接近窗口上限时触发 compaction（压缩）。
JSONL 中的历史 usage 记录不受 compaction 影响（追加写入），所以统计是完整的。
但 `sessions.json` 的值会在 compaction 后被新调用覆盖。

## Notes

- 扫描大量文件可能需要几秒钟
- `--include-deleted` 会包含 `.deleted` 和 `.bak` 后缀的历史文件
- 缓存命中率超过 100% 的显示说明用了旧的错误公式，本脚本已修正
