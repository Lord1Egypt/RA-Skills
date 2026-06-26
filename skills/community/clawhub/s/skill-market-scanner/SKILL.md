---
name: clawhub-guard
version: 1.0.0
description: ClawHub 技能市场安全守卫 — 自动浏览/搜索/审查技能，帮你发现好用的、过滤危险的。集成 skill-vetter 自动安全审查。
---

# ClawHub Guard

> ClawHub 技能市场的安检员。不让危险技能溜进来，不让好技能被忽略。

## 解决的问题

| 无此技能 | 有此技能 |
|---------|---------|
| 手动 `clawhub explore` 翻页 | `scan` 自动浏览 + 审查 top N |
| 不知道技能是否安全 | 自动调用 skill-vetter 审查 |
| 好技能沉在市场里找不到 | `hunt "关键词"` 持续监控 |
| 装了的技能不知是否过时 | `audit` 检查已装技能更新 |

## 命令

```bash
python clawhub_guard.py scan              # 浏览市场最新 50 个技能，审查推荐 top 5
python clawhub_guard.py hunt "关键词"      # 搜索市场，审查后推荐
python clawhub_guard.py audit             # 检查已装技能是否有更新
python clawhub_guard.py install <slug>    # 安全安装（先审查再装）
```

## 审查流程（自动）

```
scan/hunt → 拿技能列表 → 每个技能 → skill-vetter 审查 → 风险分级 → 推荐清单
```

## 依赖

- `clawhub` CLI（已全局安装）
- Python 3.11+

## 典型工作流

```bash
# 逛逛市场
clawhub-guard scan
# → Top 5 推荐 + 风险评级

# 找特定技能
clawhub-guard hunt "中医"
# → 搜索 + 审查 + 推荐

# 更新已装技能
clawhub-guard audit
# → 列出可更新的 + skill-vetter 复核
```
