# SharpInput Self-Learning System (v2.3+)

## Overview

After each interaction, analyze the user's choices and update preference data.
On next invocation, read preferences to personalize the flow.

**Storage**: `references/user-preferences.json` (JSON format, schema-defined, NOT workspace memory)
**Migration note**: If `references/user-preferences.md` exists with data, one-time migrate to JSON on first read, then delete the .md file.

---

## JSON Schema

用户偏好文件使用严格的 JSON 格式，终结 Markdown 格式漂移问题。

### 文件结构

```json
{
  "schema_version": "1.0",
  "last_updated": "2026-05-07",
  "history": [ ... ],
  "summary": { ... }
}
```

### history 条目字段

#### All Levels (0/1/2/3)

| Field | Type | Example | Required |
|-------|------|---------|----------|
| timestamp | string | "2026-05-02" | yes |
| level_used | int | 3 | yes |
| level_assigned | int | 2 | yes |
| level_upgraded | bool | true | no |
| intent_primary | string | "决策" | yes |
| intent_secondary | string | "分析" | no |
| language | string | "zh" | yes |

#### Level 2+ Additional

| Field | Type | Example |
|-------|------|---------|
| pressure_strategy | string | "regret pre-mortem" |
| strategy_skipped | string \| null | null |

#### Level 3 Additional

| Field | Type | Example |
|-------|------|---------|
| angle_selected | string | "risk-first" |
| paths_presented | string[] | ["risk-first", "counter-intuitive", "minimalist"] |
| user_choice | string | "single" / "combination" |
| choice_detail | string | "B: counter-intuitive" |
| feedback | string \| null | "great" / "off track" / null |

#### Outcome Tracking (v2.4+)

| Field | Type | Example |
|-------|------|---------|
| outcome_score | int \| null | null (未追踪), 1-5 (见输出效果追踪) |
| outcome_note | string \| null | "AI回答质量明显提升" |

#### Confirmed Context

| Field | Type | Example |
|-------|------|---------|
| context_role | string \| null | "产品经理" |
| context_tech_stack | string \| null | "React + Python" |
| context_budget | string \| null | "~6000" |
| context_team_size | int \| null | 8 |
| context_domain | string \| null | "互联网/Web开发" |
| context_constraints | string \| null | "预算有限、短期出成果" |

### summary 字段

| Field | Type | Example |
|-------|------|---------|
| level_bias | object | {"total_sessions": 9, "level_distribution": {"0":0,...,"3":9}, "top_level_pct": 100} |
| angle_preference | string[] | ["risk-first", "adversarial", "counter-intuitive"] |
| intent_history | object | {"决策": 5, "分析": 3} |
| correction_map | object | {"模式A": "正确意图A"} |
| intent_priming | object\|null | {"primary_intent_top3": ["决策","分析","验证"], "corrections": {}} |
| context_autofill | object | {"role": "产品经理", "tech_stack": "React + Python"} |
| outcome_stats | object\|null | {"avg_score": 4.2, "positive_ratio": 0.8, "tracked_count": 5} |

### outcome_stats 字段（v2.4+）

| 子字段 | 类型 | 说明 |
|--------|------|------|
| avg_score | float | 所有已追踪的效果评分平均值（1.0-5.0） |
| positive_ratio | float | 评分 ≥ 4 的条目占比 |
| tracked_count | int | 有 outcome_score 的条目数 |
| best_intent | string | 评分最高的意图类型 |
| worst_intent | string | 评分最低的意图类型 |

完整 JSON 示例见 `user-preferences.json`。

---

## When to Write — 包含效果追踪（v2.4+）

After Stage 3 Step 2 outputs the final question:
1. Extract all applicable fields from this session into JSON format
2. Read `references/user-preferences.json`
3. Append this session's data to the `history` array (keep last 10 entries only)
4. Recalculate the `summary` section from the last 10 entries
5. Update `last_updated` to current date
6. Write back as valid JSON

### Post-Interaction 效果追踪（可选扩展）

不在输出阶段执行。而是在用户后续回来说"上次你帮我优化的那个问题……"时追踪效果：

| 触发模式 | 提取字段 | 更新方式 |
|---------|---------|---------|
| 用户主动反馈（"上次那个问题好/不好"） | outcome_score (1-5), outcome_note | 查找最后一次同意图的历史条目，更新 |
| 用户用优化后的问题获得AI回答后回来说结果 | outcome_score (从用户语气推断：积极=4-5，中性=3，负面=1-2) | 同上 |
| 跨会话效果对比（"比上次更好了"） | 无需更新，已记录在 timestamp | 用于 summary 效果趋势分析 |

效果追踪触发后即时更新 history 中对应条目。

### 写入规则

- **直接操作 JSON 对象**，不要手动拼接字符串。使用 JSON.parse + JSON.stringify 逻辑。
- `schema_version` 保持不变（仅在架构升级时更新）。
- `history` 是数组，新条目 append，最旧条目自动弹出（窗口限10）。
- 每次写入后验证 JSON 结构完整性。

---

## When to Read

After Gate, before Intent Recognition (the Memory Load step):
1. Read `references/user-preferences.json`
2. If `summary` exists, apply preferences silently (see Memory Load in SKILL.md)
3. If file doesn't exist or is empty, skip

### 读取规则

- 如果文件读取失败（格式错误），降级为无偏好的正常流程
- 如果 `schema_version` 不支持，忽略 `history`，只读取 `summary`
- 始终检查字段存在性再使用

---

## Preference Application Rules

### Default Level Bias
- If ≥70% of last 10 sessions used Level 3 → when Gate assigns Level 1/2, suggest upgrade
- If ≥70% used Level 2 → default hint is Level 2
- Otherwise → no bias, follow Gate's assignment

### Angle Preference
- In Stage 3, generate at least 1 path with the user's top-2 angle tags
- The other paths should explore different angles for diversity

### Forcing Strategy Adjustment
- If a strategy was skipped in ≥50% of sessions where it was applied → lower its priority
- Never remove a strategy entirely; only reduce emphasis

### Recommendation Bias
- In Stage 5 selection prompt, recommend the path whose angle tag matches user's top preference
- If credibility conflicts with preference, show both: "根据偏好推荐 Path A，但 Path B 可信度更高"

### Feedback Integration
- "great" feedback → boost the selected angle tag + intent combination as a strong positive signal
- "off track" → record as negative signal; in next session with similar intent, avoid that angle tag

### Negative Pattern Detection (v2.4+)
- If an angle tag gets "off track" feedback ≥2 times → add to `avoided_angles` in summary
- When generating paths, skip avoided angles unless explicitly requested
- Reset avoided angles on "重置偏好"

### Intent Priming（v2.3）

从历史记录中提取意图偏好，用于偏置当前轮次的意图识别：

- 如果最近 10 次中 ≥60% 共享同一个主意图，该意图置信度 +0.1
- 如果当前输入信号模糊（关键词匹配得分 0.3-0.7），优先选择用户历史 top-3 意图
- 记录意图修正：当用户通过 AskUserQuestion 纠正意图时，将该输入模式→正确意图的映射记录到 `correction_map` 字段

### Context Auto-Fill（v2.3）

当意图专属上下文规则要求询问某一字段，而该字段的值已存在于用户偏好记录中时：

1. **自动填充**该字段，不在交互中重复提问
2. 在最终输出中标注：`根据你的记录，[value]（可调整）`
3. 如果用户在本次交互中调整了该值，更新偏好记录
4. 可自动填充的字段：role, tech stack, budget, team size, domain, common constraints

在打开输出时同步执行：扫描最终优化问题中的 `[xxx]` 占位符，如果用户偏好中有匹配的字段值，自动替换。

---

## Sliding Window

- Keep only the last 10 interaction records
- When adding the 11th, remove the oldest (index 0)
- All statistics (percentages, top preferences) are calculated from the window
- `summary.level_bias.level_distribution` sums to exactly the window size

---

## Preference Reset

If user says "重置偏好" / "reset preferences":
- Clear the `history` array
- Clear `summary` to defaults
- Confirm: "偏好已重置。" / "Preferences reset."
