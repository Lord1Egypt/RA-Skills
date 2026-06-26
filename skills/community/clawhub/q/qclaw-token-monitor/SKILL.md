---
name: qclaw-token-monitor
description: |
  AI Token消耗监控优化工具。读取会话日志，统计Token消耗，检测异常模式（短时激增、重复失败等），提供优化建议，生成消耗趋势报告。
  中文优先，面向QClaw/OpenClaw用户。
  当用户说"Token消耗"、"费用多少"、"Token统计"、"超支"、"优化建议"时触发。
  Keywords: Token, 消耗, 费用, 监控, 优化, 趋势, 统计, 异常检测.
metadata: {"openclaw": {"emoji": "📊"}}
---

# Token消耗监控优化

监控 AI Token 消耗，检测异常，提供优化建议。

## 功能

- 📊 读取 session 日志统计 Token 消耗
- 🚨 检测异常消耗（短时激增、重复失败等）
- 💡 给出优化建议
- 📈 生成消耗趋势报告

## 使用

### 检查今日消耗
```bash
python3 ~/.qclaw/skills/token-monitor/scripts/token_stats.py --today
```

### 检查指定日期
```bash
python3 ~/.qclaw/skills/token-monitor/scripts/token_stats.py --date 2026-04-14
```

### 检查异常模式
```bash
python3 ~/.qclaw/skills/token-monitor/scripts/token_stats.py --check-anomaly
```

### 生成优化报告
```bash
python3 ~/.qclaw/skills/token-monitor/scripts/token_stats.py --report
```

## 异常检测规则

| 规则 | 阈值 | 说明 |
|------|------|------|
| 单日总量 | >1000万 | 严重超标 |
| 单小时 | >200万 | 需要检查 |
| 重复失败 | >3次 | 死循环风险 |
| 浏览器快照 | 单次>5000字 | 未压缩 |

## 历史数据参考

| 日期 | Input | Output | Total | 状态 |
|------|-------|--------|-------|------|
| 4/11 | 3.46M | 117K | 28.8M | 🚨 超标 |
| 4/12 | 5.57M | 127K | 37.0M | 🚨 严重超标 |
| 4/13 | 1.80M | 22K | 9.5M | ⚠️ 偏高 |
| 4/14 | 430K | 20K | 3.7M | ✅ 正常 |

**4/12是Token浪费最严重的一天**：3700万token，根因是Chrome CDP崩溃重试+ClawHub限速重试

## 优化建议库

- 浏览器快照用 `compact=true`
- 同一操作失败3次立即换方案
- 限速不硬等，跳转做其他事
- 后台进程不轮询
- Context超过150K时触发LCM压缩

## 数据存储

- 日志：`~/.qclaw/agents/main/sessions/*.jsonl`
- 统计：`memory/token-usage-YYYY-MM-DD.json`

## 依赖

- Python 3（系统自带）
- 无第三方依赖
