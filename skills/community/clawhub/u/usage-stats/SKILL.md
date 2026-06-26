---
name: usage-stats
description: |
  OpenClaw 使用统计技能。自动分析会话记录，生成 token 消耗、费用、工具使用等完整报告。
  触发场景：用户提到"使用统计"、"token 消耗"、"费用分析"、"使用报告"、"使用情况"、
  "usage stats"、"token usage"、"消费记录"、"我用了多少"、"统计"等关键词时使用。
  关键词：usage, token, stats, 统计, 费用, cost, 消耗, report
---

# Usage Stats — OpenClaw 使用统计

## 概述

解析 `~/.qclaw/agents/main/sessions/` 下的所有会话记录，生成完整的 OpenClaw 使用统计报告，包含 Token 消耗、费用估算、模型分布、工具调用排行、错误分析、时段分布、日趋势等维度。

**使用方式：** 直接告诉我"跑一下使用统计"或"统计一下我的使用情况"，我调用脚本生成报告。

## 核心功能

- ✅ **Token 统计**：input / output / cacheRead / cacheWrite / 总计
- ✅ **费用估算**：基于 usage 数据计算总费用
- ✅ **模型分布**：各模型的调用次数和 token 消耗
- ✅ **缓存命中率**：cacheRead / (cacheRead + cacheWrite)
- ✅ **工具调用排行**：所有工具的调用频次（exec / browser / message 等）
- ✅ **错误分析**：归类常见错误 + 根因 + 解决方案
- ✅ **会话详情**：每个会话的开始时间、时长、token、轮次
- ✅ **日趋势**：每日 token/会话/错误量变化
- ✅ **时段分布**：24 小时活跃热力图
- ✅ **历史趋势对比**：与上次运行的对比

## 工作流程

### 步骤 1：运行脚本

执行 `scripts/analyze_usage.py`，报告输出到：
`~/.qclaw/workspace/memory/usage_stats_latest.md`

历史快照保存在：`~/.qclaw/workspace/memory/usage_stats_history.json`

### 步骤 2：解读报告

| 章节 | 含义 |
|------|------|
| Overall Stats | 整体汇总（总费用、总 token、活跃时长） |
| Model Distribution | 各模型的调用量和费用 |
| Error Analysis | 错误类型排行 + 自动根因分析 |
| Tool Usage | 工具调用频次排行 |
| Exec Performance | 命令执行耗时（P50/P95） |
| Conversation Activity | 消息角色分布 + 会话结束原因 |
| Text Volume | 平均消息长度 |
| Session Detail | 每个会话的详细数据 |
| Daily Trend | 每日 token / 会话量趋势 |
| Hourly Distribution | 24 小时活跃时段热力图 |
| Trend (vs Last Run) | 与上次运行的环比变化 |
| Troubleshooting Guide | 错误知识库（根因 + 修复方案） |

### 步骤 3：更新记忆

将重要发现写入 `memory/YYYY-MM-DD.md`（如：发现了某个高频错误、token 消耗异常等）。

## 数据来源

- **会话记录**：`~/.qclaw/agents/main/sessions/*.jsonl`
- **历史快照**：`~/.qclaw/workspace/memory/usage_stats_history.json`

> 数据来自会话消息中的 `usage` 字段，由 OpenClaw 自动记录，无需手动维护。

## 限制与注意事项

- **缓存命中**：仅统计 OpenClaw 明确记录的 `cacheRead`/`cacheWrite`，实际缓存效果可能更高
- **费用估算**：基于报告数据计算，可能与实际账单有差异，仅供参考
- **错误归类**：脚本按错误模式自动归类，部分罕见错误可能归到泛型类型（`exit_code` 等）
- **数据范围**：仅统计 `main` agent 的会话，子 agent 会话不包含在内
- **历史长度**：最多保留 90 条历史快照，超出自动清理旧记录

## 常见问题

| 问题 | 答案 |
|------|------|
| 报告在哪里？ | `~/.qclaw/workspace/memory/usage_stats_latest.md` |
| 历史记录在哪？ | `~/.qclaw/workspace/memory/usage_stats_history.json` |
| 如何查看趋势？ | 报告中 "Trend (vs Last Run)" 章节 |
| 发现高频错误怎么办？ | 参见 "Troubleshooting Guide" 章节，按提示修复 |
| 能统计指定时间段吗？ | 目前自动统计全部历史，可手动编辑脚本过滤日期 |
| 缓存命中率 100% 正常吗？ | 正常，说明 AI 回复大量复用上下文缓存 |

## 输出格式规范

详见 `references/output-format.md`
