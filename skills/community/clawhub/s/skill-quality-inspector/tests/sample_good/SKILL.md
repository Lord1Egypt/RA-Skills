---
name: sample-good
description: >-
  测试用干净仓库，用于验证 quality_audit 不误报。触发词："测试"、"样例"、"干净"。
agent_created: true
metadata:
  version: 1.0.0
  category: 测试
  difficulty: 入门
  architecture: superpower
---

# 样例仓库

> 干净样本，供脚本冒烟测试。

本技能采用 superpower 架构：SKILL.md 只做路由。

## 何时使用

- 测试场景

## 能力索引（超级技能路由）

| 任务 | 读取·调用 | 关键词 |
|------|-----------|--------|
| 参考手册 | `references/good-ref.md` | 参考、手册、good |
| 子技能 | `skills/good-skill/SKILL.md` | 好技能、good |
| 脚本 | `scripts/good_script.py` | 好脚本 |
| 模板 | `assets/good-asset.md` | 好模板 |

## 内置脚本

- `scripts/good_script.py` — 示例脚本

运行示例：

```bash
python3 scripts/good_script.py --help
```

## 模板资源

- `assets/good-asset.md` — 示例模板

## 核心原则

1. 渐进式加载
2. 明确边界

## 与其他技能协作

- 无
