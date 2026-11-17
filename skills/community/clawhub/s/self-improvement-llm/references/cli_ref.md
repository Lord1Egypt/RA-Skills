# CLI Reference & Detailed Structures

## Structured Log Format

Every entry uses this format (inspired by pskoett standard):

### Learning Entry

```
## [LRN-YYYYMMDD-XXX] category:brief_title

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | wont_fix | promoted
**Area**: frontend | backend | infra | tests | docs | config | behavior | tooling

### Summary
One-line description

### Details
What happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement

### Metadata
- Source: conversation | error | user_feedback | self_discovery
- Related Files: path/to/file
- Tags: tag1, tag2
- Pattern-Key: unique_key_for_dedup (optional, for recurring patterns)
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD
```

### Error Entry

```
## [ERR-YYYYMMDD-XXX] tool_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: infra | tooling | config

### Summary
Brief description of what failed

### Error
Actual error message or output

### Context
- Command/operation attempted
- Input or parameters used

### Suggested Fix
What might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
- See Also: ERR-YYYYMMDD-XXX (if recurring)
```

### Feature Request Entry

```
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: as appropriate

### Summary
What the user wanted to do

### User Context
Why they needed it

### Complexity Estimate
simple | medium | complex

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
```

### ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: LRN (learning), ERR (error), FEAT (feature)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., 001, A7B)

## Auto-Generated Skill Format

```markdown
---
name: skill-slug-name
description: 一句话描述这个技能做什么
created: 2026-05-27
updated: 2026-05-27
source: auto
triggers: ["触发关键词或场景"]
tools: [web_fetch, exec, read]
---

## Procedure

1. 步骤一：做了什么
2. 步骤二：怎么做的
3. 步骤三：验证结果

## Pitfalls

- 已知问题或陷阱
- 容易出错的地方
- 环境依赖

## Verification

- 如何验证结果正确
- 预期输出是什么
```

## Verification Loop — JSON Entry

```json
{
  "id": "change-20260505-001",
  "source": "LRN-20260505-003",
  "target": "TOOLS.md",
  "change": "Added 'prefer read over exec for files'",
  "hypothesis": "This will reduce file-viewing errors",
  "verified": false,
  "next_check": "2026-05-12",
  "evidence": []
}
```

### Verification Outcomes

| Result | Action |
|--------|--------|
| ✅ Confirmed effective | Mark verified, reduce monitoring to monthly |
| ❌ Ineffective | Revert change, log why it failed |
| ❌ Made worse | Revert immediately, escalate |
| ❓ Inconclusive | Extend monitoring, add more data points |

## Conflict Resolution — Priority Score

```
Score = BasePriority(100/60/30/10) + RecurrenceBonus(×10 each) + RecencyBonus(up to 30) + AreaWeight(up to 50)
Highest score wins.
```

## Forgetting Mechanism

| Time without reinforcement | Action |
|---------------------------|--------|
| 30 days | Priority demoted one level (high→medium, etc.) |
| 60 days | Priority → low, flagged as stale |
| 90 days | Auto-resolved as `wont_fix` |

## Auto-Revert

| Overdue | Action |
|---------|--------|
| 7 days | Grace period — reminder only |
| 14 days | First extension + evidence request |
| 21+ days | Auto-revert: change undone, logged as `auto_reverted` |

## Conversation Scoring — Trend Example

```
📈 Score Trends (last 7 days, 12 scores):

  Date         Avg  Acc  Use  Eff  Ton  Pro
  ──────────────────────────────────────────
  2026-05-01   7.2    8    8    7    7    6
  2026-05-02   7.8    8    9    7    8    7
  2026-05-03   8.0    8    9    8    8    7

  Trend: ↑ (7.2 → 8.0)
```

## CLI --log Parameters

| Param | Values | Default |
|-------|--------|--------|
| `--source` | `conversation`, `error`, `user_feedback`, `self_discovery` | `self_discovery` |
| `--priority` | `critical`, `high`, `medium`, `low` | `medium` |
| `--area` | any string | `tooling` |
| `--pattern-key` | any string | none |

## Dynamic Memory Topics

| Topic | Keywords |
|-------|----------|
| weather | 天气, 温度, wind, rain, 预报 |
| code | 代码, script, python, bug, fix |
| finance | 金融, 股票, stock, 交易 |
| skill | skill, clawhub, 技能 |
| learning | improve, learn, reflect, 学习 |
| memory | memory, remember, recall, 记忆 |
| browser | browser, playwright, 自动化 |
| config | config, 配置, setup, API, key |

## Knowledge Graph

### Node Types

| Type | Icon | Description |
|------|------|-------------|
| **event** | 📌 | 具体事件 |
| **lesson** | 💡 | 从事件中学到的教训 |
| **principle** | 📜 | 通用原则 |
| **knowledge** | 📖 | 事实知识 |
| **pattern** | 🔍 | 重复出现的模式 |

### Edge Types

| Type | Direction | Meaning |
|------|-----------|---------|
| **caused_by** | A → B | A 是由 B 引起的 |
| **led_to** | A → B | A 导致了 B |
| **supports** | A → B | A 支持 B |
| **contradicts** | A → B | A 与 B 矛盾 |
| **related_to** | A → B | A 与 B 相关 |
| **derived_from** | A → B | A 是从 B 推导出来的 |

### Auto-Link Rules

- **Keyword overlap ≥ 2** → `related_to`
- **Error words** (error, fail, wrong) → `caused_by`
- **Support words** (should, prefer, use) → `supports`
- **Contradiction words** (not, instead, rather) → `contradicts`
