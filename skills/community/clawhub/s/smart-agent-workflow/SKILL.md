---
name: smart-agent-workflow
description: AI Agent 工作方法论 Skill — 专注 3高（高质量+高效率+高节省）。提供任务类型判断、WBS 拆分、P0/P1 分级汇报、安全检查、Context 管理。渠道无关，适用于 Claude Code、Cursor、Codex、OpenClaw 等任何 AI agent。唯一提供完整工作方法论的 Skill。
---

# Smart Agent Workflow

**专注 3高：高质量 + 高效率 + 高节省**

## 核心价值

| 原则 | 解决的问题 | 实现方式 |
|------|-----------|---------|
| 🎯 高质量 | agent 容易失控、偏离目标 | WBS 拆分 + P0/P1 汇报规范 |
| ⚡ 高效率 | 任务执行混乱、缺少规范 | 任务类型判断 + 批次执行 |
| 💰 高节省 | Context 超限、Token 浪费 | Context 管理 + 分层记忆 |

## 核心规范

### 任务类型判断

```
收到任务 → 新任务 or 连续任务？
         → 简单 or 复杂？（文件≥3 / 步骤≥5 / 耗时>15分钟，满足2条）
         → 简单任务用 P0，复杂任务用 P0+P1
```

### P0 规范（所有任务必须，3条）

1. 复杂任务必须拆分
2. 卡住必须上报（失败≥2次 / 等待>30秒）
3. 完成必须汇报（目标 + 结果 + 产出）

### P1 规范（复杂任务建议，3条）

4. 批次完成汇报
5. 危险操作确认
6. 连续任务插断点

## 推荐组合

```bash
# 最小配置
clawhub install smart-agent-workflow

# 标准配置（推荐）
clawhub install smart-agent-workflow
clawhub install self-improving

# 完整配置
clawhub install smart-agent-workflow
clawhub install self-improving
clawhub install proactivity
```

## 适用范围

渠道无关，适用于任何 AI agent：
- Claude Code（推荐）
- Cursor / Windsurf
- Codex
- OpenClaw

## 快速开始

```markdown
# 在 CLAUDE.md 或 Rules for AI 中添加：
读取 ~/smart-agent/AGENTS.md 并遵守所有规范
```

详细文档：https://github.com/whhaijun/agent-workflow
