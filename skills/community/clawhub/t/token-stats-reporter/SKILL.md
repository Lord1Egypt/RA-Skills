---
name: token-stats-reporter
description: |
  生成 Token 使用统计和参考费用报告。支持 Anthropic Claude Opus 4.7 和 OpenAI GPT-5.5 两种参考费率，默认 Opus 4.7，输出"省了多少"的满足感。
  适用场景：用户要求查看 Token 使用统计、需要展示"本应多少费用"、生成每条消息末尾的 Token 统计行。
  触发词：token统计、费用多少、省了多少钱、Token统计。
version: 1.5.0
updated: 2026-05-10
author: 妮小虾 🦐
---

# Token 使用统计报告技能

生成 Token 使用统计和参考费用报告。

## 输出格式（v1.5.0，唯一标准）

```
📊 Token: {in} in / {out} out | cacheRead: {cache} | 本次总消耗: {total} | 本次计费token: {billing} | 本月: {count} 次 | 月累计总消耗: {monthly} | 💰 本次({model}参考){cost} | 💰 本月({model}参考){cost} | 模型: {model}
```

字段说明：
- `{in}` 本次 input tokens（整数）
- `{out}` 本次 output tokens（整数）
- `{cache}` 本次缓存读取 tokens（整数）
- `{total}` 本次总消耗（紧凑 k/M 格式）
- `{billing}` 本次计费 token = in + out + cache（整数）
- `{count}` 本月 assistant 消息数（整数）
- `{monthly}` 当月总 tokens（紧凑 k/M 格式）
- `{cost}` 按所选参考费率计算的费用
- `{model}` 当前模型名称

## 费率标准

| 模型 | Input | Output | Cache Read |
|------|-------|--------|------------|
| Anthropic **Opus 4.7**（默认） | $15.00/M | $75.00/M | $1.125/M |
| OpenAI **GPT-5.5** | $5.00/M | $30.00/M | $1.25/M |

汇率固定：USD → CNY = 7.20

**计算公式：**
```
费用(¥) = (in/1M × input_rate + out/1M × output_rate + cache/1M × cache_rate) × 7.20
```

## 使用方式

### 默认（Opus 4.7）
```bash
python3 scripts/token-show.py
```

### 指定费率模型
```bash
python3 scripts/token-show.py --model opus    # Opus 4.7
python3 scripts/token-show.py --model gpt5.5 # GPT-5.5
```

### 自定义费率（Input Output Cache 单位：$/MTok）
```bash
python3 scripts/token-show.py --rates 10 50 0.8
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| in | 本次 input tokens |
| out | 本次 output tokens |
| cacheRead | 本次缓存读取 tokens |
| 本次总消耗 | in + out + cacheRead（紧凑格式） |
| 本次计费token | in + out + cache（整数） |
| 本月次数 | 当月 assistant 消息数 |
| 月累计 | 当月总 tokens（in+out+cache） |
| 💰 本次(xxx参考) | 本次消息的参考费用 |
| 💰 本月(xxx参考) | 当月累计参考费用 |

## 费用格式规则

| 费用范围 | 格式 |
|---------|------|
| < ¥0.01 | ¥0.0000（四位小数） |
| ≥ ¥0.01 | ¥0.00（两位小数） |

## 数据来源

所有数据来自 `~/.openclaw/agents/main/sessions/*.jsonl`，每次实时扫描，按消息 timestamp 过滤当月数据。

## 常见问题

**Q: sessions目录为空时怎么办？**
A: 脚本正常返回全0值：`📊 Token: 0 in / 0 out | cacheRead: 0 | 本次总消耗: 0 | 本次计费token: 0 | 本月: 0 次 | 月累计总消耗: 0 | 💰 本次(Opus4.7参考)¥0.0000 | 💰 本月(Opus4.7参考)¥0.0000 | 模型: unknown`

**Q: 默认费率是哪个？**
A: 默认 Opus 4.7。不带参数运行脚本即为 Opus 4.7。

**Q: 为什么有两个参考费率？**
A: Opus 4.7 用于展示"本应花多少"的参考上限，GPT-5.5 作为对比参考。

**Q: 月份数据不对怎么办？**
A: 检查系统时间。脚本按当前月份过滤，sessions 文件中 timestamp 是历史月份会被过滤。

## 维护记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-10 | 1.5.0 | 支持 --model 参数选择 Opus 4.7 / GPT-5.5 / 自定义费率；增加本次计费token字段 |
| 2026-05-08 | 1.4.0 | 完善文档（费率表、FAQ、维护记录） |
| 2026-05-07 | 1.3.x | 升级为 Opus 4.7 参考费率 |
| 2026-04-06 | 1.0.0 | 初始版本 |