---
name: self-iteration-engine
description: >
  Self-iteration and feedback learning engine for AI agent skills.
  Tracks usage logs, detects performance patterns, triggers skill updates,
  and proposes new skill creation based on repeated request patterns.
  Use when: any skill needs to improve over time, detect failure patterns,
  learn from user corrections, or decide when to create new skills.
  Triggers: "learn from this", "improve yourself", periodic review cycles,
  or any skill declaring dependency for self-improvement.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔄"
    homepage: https://clawhub.ai/BusTes01/self-iteration-engine
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
      - claude-4-opus
---

# 🔄 Self-Iteration Engine

Self-iteration and feedback learning engine for AI agent skills. Tracks usage logs, detects performance patterns, triggers skill updates, and proposes new skill creation based on repeated request patterns.

This is a **shared component skill** — other skills reference it for self-improvement. When updating, ensure backward compatibility with all dependent skills. Users may install this skill standalone for its capabilities.

## Usage Log Format

Maintain a usage log file for each skill that declares dependency:

```markdown
# Usage Log: <skill-name>
## [YYYY-MM-DD]
- Request: <brief description>
- Outcome: success | partial | fail
- User corrected: yes | no
- Correction detail: <if yes, what was corrected>
- Lesson: <what to do differently next time>
```

File location: `memory/usage-logs/<skill-name>.md`

## Self-Iteration Triggers

Evaluate these conditions during each **periodic review** (default daily, configurable):

| Condition | Action |
|-----------|--------|
| 3+ consecutive successful invocations | Mark skill as "stable" — reduce context allocation |
| 2+ failures for the same scenario | Flag for SKILL.md reassessment |
| Same request type appears 3+ times | Evaluate creating a new dedicated skill |
| User corrected output | Log correction, adjust future behavior for that scenario |
| Skill hasn't been reviewed in 30+ days | Trigger review: check if dependencies changed, update examples |
| External tech change detected | Compare against skill's core technology stack, update if needed |

## Feedback Loop Implementation

```yaml
# memory/feedback-loop/<skill-name>.yaml
feedback_loop:
  last_review: "2026-05-19"
  next_review: "2026-05-26"
  status: "stable" | "needs-attention" | "monitoring"
  patterns_observed:
    - pattern: "user asks for financial data on weekends"
      current_response: "check if markets are open"
      improvement: "pre-fill with last trading day data"
      status: "resolved" | "pending" | "in-progress"
  skill_performance:
    total_calls: 47
    success_rate: 0.96
    issues:
      - "data freshness on weekends"
```

## Review Cycle

### Daily (lightweight)
- Scan today's usage log entries
- Check for failure patterns
- Log any user corrections

### Weekly (moderate) 
- Aggregate performance stats
- Check iteration triggers (listed above)
- If any trigger fires → update SKILL.md or create new skill
- Archive usage logs older than 7 days

### Monthly (deep)
- Full performance review across all skills
- Compare success rates, identify declining trends
- Check if any external technology replaced the skill's core stack
- Propose new skill ideas based on accumulated pattern data
- Run memory cleanup (delegate to complex-memory-manager)

## Update Decision Matrix

| Signal | Decision |
|--------|----------|
| 80%+ success rate, no user corrections | No update needed |
| 60-80% success rate | Minor update: clarify instructions, add edge cases |
| <60% success rate | Major update: redesign workflow, check data sources |
| User corrects same thing 3+ times | Fix that specific guidance in SKILL.md |
| External API / tool changed | Update immediately |
| New competing technology available | Evaluate migration; update if 2x+ better |

## New Skill Creation Criteria

Create a new skill when:
- Same request pattern appears 3+ times across different users
- The pattern cannot be handled well by existing skills
- The pattern has a clear, bounded scope
- A distinct tool/API would improve the result

Document in `memory/skill-ideas/`:
```yaml
proposal:
  name: <suggested-slug>
  rationale: "Pattern X appeared N times. Existing skill Y handles it poorly because..."
  scope: "<bounded description>"
  priority: high | medium | low
  created: <date>
```

## Cross-Skill Usage

Other skills declare dependency:
```yaml
metadata:
  openclaw:
    requires:
      skills:
        - self-iteration-engine
```

Usage logs are prefixed with the source skill name:
- `memory/usage-logs/skill-a.md`
- `memory/feedback-loop/skill-a.yaml`

When this skill updates log format, check ALL dependent skills' parsing logic.

---

# 🔄 自迭代引擎

面向AI Agent技能的自迭代与反馈学习引擎。追踪使用日志、检测性能模式、触发技能更新，并基于重复请求模式提出新技能创建建议。

这是一个**共享组件技能**——其他技能通过它实现自我改进。更新时需保证向后兼容。用户也可能独立安装此技能使用其能力。

## 使用日志格式

每个声明依赖的技能维护一份使用日志：

```markdown
# 使用日志：<skill名称>
## [YYYY-MM-DD]
- 请求：<简述>
- 结果：成功 | 部分成功 | 失败
- 用户修正：是 | 否
- 修正详情：<如果是，修正了什么>
- 经验：<下次应该怎么做>
```

文件位置：`memory/usage-logs/<skill名称>.md`

## 自迭代触发条件

**定期审查**时评估以下条件（默认每天，可配置）：

| 条件 | 行动 |
|------|------|
| 连续成功3次以上 | 标记为"稳定"——减少上下文分配 |
| 同一场景失败2次以上 | 标记SKILL.md需重新评估 |
| 同类请求出现3次以上 | 评估创建新专用skill |
| 用户修正了输出 | 记录修正，调整后续该场景的行为 |
| 技能超过30天未审查 | 触发审查：检查依赖是否变更、更新示例 |
| 检测到外部技术变化 | 与技能核心技术栈对比，需要时更新 |

## 反馈循环实现

```yaml
# memory/feedback-loop/<skill名称>.yaml
feedback_loop:
  last_review: "2026-05-19"
  next_review: "2026-05-26"
  status: "stable" | "needs-attention" | "monitoring"
  patterns_observed:
    - pattern: "用户在周末查询金融数据"
      current_response: "检查市场是否开盘"
      improvement: "自动填充最近交易日数据"
      status: "resolved" | "pending" | "in-progress"
  skill_performance:
    total_calls: 47
    success_rate: 0.96
    issues:
      - "周末数据新鲜度"
```

## 审查周期

### 每日（轻量）
- 扫描今天的日志条目
- 检查失败模式
- 记录用户修正

### 每周（中等）
- 汇总性能统计
- 检查触发条件
- 触发更新或创建新技能
- 归档超过7天的日志

### 每月（深度）
- 全技能性能审查
- 对比成功率，识别下降趋势
- 检查外部技术是否取代了技能核心
- 基于积累的模式数据提出新技能想法
- 执行记忆清理（委托给complex-memory-manager）

## 更新决策矩阵

| 信号 | 决策 |
|------|------|
| 成功率>80%，无用户修正 | 无需更新 |
| 成功率60-80% | 小幅更新：澄清说明、补充边界情况 |
| 成功率<60% | 重大更新：重新设计工作流、检查数据源 |
| 用户修正同一内容3次以上 | 在SKILL.md中修复该指导 |
| 外部API/工具变更 | 立即更新 |
| 出现新的竞争技术 | 评估迁移；若2倍以上优于现有则更新 |

## 新技能创建标准

以下情况创建新技能：
- 相同请求模式在不同用户出现3次以上
- 现有技能无法良好处理该模式
- 该模式有清晰、有边界的范围
- 有独特工具/API可提升结果

记录在 `memory/skill-ideas/`：
```yaml
proposal:
  name: <建议的slug>
  rationale: "模式X出现了N次。现有技能Y处理不佳因为..."
  scope: "<有边界的描述>"
  priority: high | medium | low
  created: <日期>
```

## 跨技能使用

其他技能声明依赖的方式：
```yaml
metadata:
  openclaw:
    requires:
      skills:
        - self-iteration-engine
```

使用日志以源技能名称为前缀：
- `memory/usage-logs/skill-a.md`
- `memory/feedback-loop/skill-a.yaml`

本技能更新日志格式时，需检查所有依赖技能的解析逻辑。
