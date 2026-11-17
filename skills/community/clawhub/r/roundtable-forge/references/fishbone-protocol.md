# Fishbone Grouping Protocol

Use this protocol when `metadata.discussion_structure` is `fishbone`. It implements the Fishbone grouping method inside a roundtable-forge discussion.

## Core principle

In standard roundtable mode, all characters work toward a single answer. In Fishbone mode, **participants are split into independent sub-groups**, each producing a **complete proposal** for the same problem. After independent proposals are formed, groups **cross-review** each other's work, then synthesize the best elements into a unified recommendation.

The name "fishbone" comes from the visual metaphor: multiple bones (proposals) branch from a central spine (the problem statement), and the cross-review weaves them together.

## Phases

| Phase | Value | What happens | Speeches? |
|-------|-------|-------------|-----------|
| Grouping | `grouping` | Conductor divides participants into sub-groups (typically 2–3 groups of 2–3 members). Same problem statement for all groups. | No (Conductor framing only) |
| Independent proposal | `independent_proposal` | Each group produces a complete proposal independently. No cross-group communication. Every member contributes. | Yes |
| Cross review | `cross_review` | Each group reviews at least one other group's proposal. Reviews cover strengths, gaps, and risks. Proposing groups may respond. | Yes |
| Synthesis | `synthesis` | Conductor synthesizes the best elements from all proposals into a unified recommendation. Groups may provide final input. | Yes (Conductor synthesis + optional group input) |

A standard Fishbone uses 2–3 groups. Use 3 groups for complex problems requiring diverse approaches.

## Group mechanics

- **Group count**: typically 2 groups for 4–6 participants, 3 groups for 6–9 participants.
- **Group composition**: the Conductor balances groups so each has complementary skills. Groups should be roughly equal in size.
- **Independence constraint**: during `independent_proposal`, groups cannot see or hear each other's work. In `real_subagent_runtime`, this means each group's subagents receive no context from other groups.
- **Cross-review assignment**: each group reviews the next group's proposal (group_1 → group_2 → group_3 → group_1). In 2-group mode, they review each other.
- **Proposal structure**: each proposal should address: (1) core approach, (2) key assumptions, (3) risks, (4) success criteria.

## Conductor behavior

Under Fishbone mode, the Conductor:

1. **Forms groups** in the grouping phase, ensuring domain diversity across groups.
2. **Dispatches independent proposals** in parallel (in `real_subagent_runtime`, each group is a separate subagent cluster with no cross-group context).
3. **Distributes proposals for cross-review** after all proposals are complete. Each group receives exactly one other group's proposal.
4. **Facilitates the synthesis** by identifying the strongest elements from each proposal and weaving them together.
5. **Writes `structure_context.fishbone_phase`** to Memory for every round.
6. **Writes `structure_context.group_id`** for every speech. In cross_review, also writes `reviewing_group_id`.

## Character speaking constraints

- **Stay in your group**: during `independent_proposal`, speeches are tagged with `group_id`. A character speaks only within their group.
- **Complete proposal**: each group's combined speeches should form a coherent, complete proposal — not fragmented opinions.
- **Constructive cross-review**: during `cross_review`, reviews must be specific and actionable. "This won't work" is not enough; "This assumption is untested because X" is acceptable.
- **Length**: 150–300 words per speech in `independent_proposal`. 120–200 words in `cross_review`. Conductor synthesis: 200–280 words.

### Example (independent_proposal, group 1)

> **产品架构师周明**：我们组的方案核心是"渐进式薪酬透明化"。第一步，公开薪酬带（band）而非具体数字，让员工理解层级结构。第二步，公布绩效指标的权重分配，让员工知道"什么被奖励"。第三步，引入同行 benchmark 对标，每年公布一次与同行的差距分析。关键假设：员工能理解带状结构；风险：如果带太宽，透明化反而增加不满。成功标准：一年内敬业度"我的努力会得到回报"项提升 10 分。

### Example (cross_review, group 2 reviewing group 1)

> **组织发展顾问赵雪**：渐进式透明化方案的优点是降低了冲击风险，但有一个关键缺口：它假设员工会理性理解薪酬带，但实际中"带"的概念对非 HR 背景的员工很抽象。建议在第一步之前增加"薪酬逻辑教育"环节——用具体案例解释为什么不同岗位的薪酬结构不同。另外，同行 benchmark 的对标对象选择容易被操纵，需要预设透明的选样规则。

## Memory representation

### Round-level structure_context

```json
{
  "fishbone_phase": "independent_proposal",
  "group_count": 3
}
```

### Speech-level structure_context

```json
{
  "group_id": "group_1"
}
```

For cross_review phase, add `reviewing_group_id`:

```json
{
  "group_id": "group_2",
  "reviewing_group_id": "group_1"
}
```

For synthesis phase, `group_id` is omitted (plenary session):

```json
{
  "group_id": null,
  "is_synthesis": true
}
```

## Output considerations

- Fishbone rounds produce **multiple complete proposals** followed by cross-review, creating a rich comparative analysis.
- The renderer groups speeches by `group_id` within each phase, and labels cross-reviews with both `group_id` and `reviewing_group_id`.
- A full Fishbone with 3 groups × 3 members × 2 phases (proposal + cross-review) typically produces 18–24 speeches = 3,000–7,000 words.
- `fishbone + podcast` produces a debate-style show where groups present and then challenge each other's proposals.

## Interaction with other features

- **Fusion thinker**: shines in the synthesis phase, where weaving together elements from multiple proposals is the core task.
- **Temporal grounding**: still applies. Each proposal's assumptions must be grounded in `metadata.current_date`.
- **Conductor invitation**: best placed after `independent_proposal` (to check if groups are on track) or before `synthesis` (to decide which elements to prioritize).
- **Continuation**: `next_steps` from a Fishbone are richer because they carry multi-proposal perspective and cross-review insights.
- **real_subagent_runtime**: in the `independent_proposal` phase, the Conductor must ensure each group's subagents receive no context from other groups — this is the independence guarantee.
