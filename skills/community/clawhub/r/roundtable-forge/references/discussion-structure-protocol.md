# Discussion Structure Protocol

This protocol defines how to choose the **discussion structure** for a roundtable. The discussion structure controls *how* characters think and speak, independent of *what* the final output looks like.

## Why a separate dimension

`output_format` (minutes / podcast / brief) only controls the renderer. `discussion_structure` controls the thinking methodology that produces the content. They are orthogonal:

- `six_hats + minutes` = a structured analysis report with six thinking dimensions.
- `six_hats + podcast` = a podcast where guests walk through six hats together.
- `standard + podcast` = a free-flowing podcast.
- `delphi + minutes` = an anonymous multi-round divergence report.

Choosing a richer discussion structure is the primary lever for increasing content depth and length.

## Available structures

| Value | Name | Core mechanism | Best for | Status |
|-------|------|----------------|----------|--------|
| `standard` | Standard roundtable | Free-flowing turns; characters speak from their own domain. | Open-ended exploration, creative brainstorming. | Stable (default). |
| `six_hats` | Six Thinking Hats | All characters think from the same hat color at the same time, then switch. | Decision analysis, risk assessment, comprehensive coverage. | Stable. |
| `delphi` | Delphi method | Anonymous multi-round convergence; hides speaker identity to surface true disagreement. | Sensitive topics, consensus-building, surfacing minority views. | Stable. |
| `world_cafe` | World Café | Table hosts stay fixed while members rotate across tables to cross-pollinate ideas. | Large-scale ideation, cross-domain synthesis. | Stable. |
| `fishbone` | Fishbone grouping | Independent sub-groups each produce a full proposal, then cross-review. | Generating multiple alternative solutions. | Stable. |

All structures are currently `Stable`. If a structure cannot be executed (e.g., insufficient participants for `world_cafe` tables), fall back to `standard`, inform the user, and continue.

## Selection rules

1. **Default to `standard`** unless the user explicitly asks for a structured method or the topic clearly benefits from one.
2. **Match topic to structure**:
   - Decision under uncertainty → `six_hats` (forces risk + value + creativity).
   - Sensitive or politically charged topic → `delphi` (neutralizes ego by hiding identity) or `six_hats` (neutralizes ego by role-switching).
   - Need many alternative solutions → `fishbone` (when available).
   - Large, multi-stakeholder topic → `world_cafe` (when available).
3. **Respect explicit user choice**: if the user names a method ("用六顶思考帽", "德尔菲法", "世界咖啡"), use it directly.
4. **Record the choice**: write `metadata.discussion_structure` in Memory and explain why in the route output.

## Trigger cues

### six_hats
- "六顶思考帽", "six hats", "六帽", "de Bono", "德波诺"
- "全面分析", "从多个维度", "从不同维度", "结构化讨论"
- "风险和价值", "权衡", "trade-off", "决策分析"
- "six thinking hats"

### delphi
- "德尔菲", "delphi", "匿名讨论", "多轮收敛", "匿名.*讨论", "共识.*收敛"

### world_cafe
- "世界咖啡", "world cafe", "轮换讨论", "桌主", "跨桌"

### fishbone
- "鱼骨图", "fishbone", "多套方案", "分组讨论", "交叉评审"

## Interaction with other dimensions

- **output_format**: any structure can pair with any output format. The renderer reads `rounds`/`speeches` regardless of structure.
- **runtime_claim**: structured methods work in both `single_backend_multi_session` and `real_subagent_runtime`. In `real_subagent_runtime`, the Conductor dispatches all characters for the same hat before switching.
- **temporal_grounding**: still applies. Each hat pass must ground claims in `metadata.current_date`.
- **conductor_invitation**: the Conductor can still pause to invite the user, typically between hat switches or at a black-hat/red-hat fork.
- **continuation**: `next_steps` generated under a structured method should note which hat or phase surfaced them.

## Memory representation

Each round records which structure produced it:

```json
{
  "round_number": 1,
  "discussion_structure": "six_hats",
  "focus_question": "...",
  "structure_context": {
    "current_hat": "black",
    "hat_sequence": ["blue_open", "white", "red", "yellow", "black", "green", "blue_close"],
    "hat_index": 4
  },
  "speeches": []
}
```

For `standard`, omit `structure_context` or set it to `{}`.

For `delphi`, each round records the phase and anonymization metadata:

```json
{
  "round_number": 1,
  "discussion_structure": "delphi",
  "focus_question": "...",
  "structure_context": {
    "delphi_phase": "independent",
    "anonymized": true,
    "participant_count": 3
  },
  "speeches": [
    {
      "speech_id": "s1",
      "character_id": "expert_a",
      "content": "...",
      "structure_context": {
        "anonymous_label": "专家 #1"
      }
    }
  ]
}
```

The convergence round carries a `synthesis` with `consensus`, `divergence`, and `open_questions`.

For `world_cafe`, each round records the phase, table count, and rotation number:

```json
{
  "round_number": 1,
  "discussion_structure": "world_cafe",
  "focus_question": "...",
  "structure_context": {
    "world_cafe_phase": "rotation_1",
    "table_count": 3,
    "rotation_number": 1
  },
  "speeches": [
    {
      "speech_id": "s1",
      "character_id": "expert_a",
      "content": "...",
      "structure_context": {
        "table_id": "table_1",
        "is_host": true
      }
    }
  ]
}
```

For `fishbone`, each round records the phase and group count:

```json
{
  "round_number": 1,
  "discussion_structure": "fishbone",
  "focus_question": "...",
  "structure_context": {
    "fishbone_phase": "independent_proposal",
    "group_count": 3
  },
  "speeches": [
    {
      "speech_id": "s1",
      "character_id": "expert_a",
      "content": "...",
      "structure_context": {
        "group_id": "group_1"
      }
    }
  ]
}
```

## Fallback

If the chosen structure cannot be executed (e.g., insufficient participants for `world_cafe` tables), fall back to `standard`, inform the user, and continue. Do not block the discussion.
