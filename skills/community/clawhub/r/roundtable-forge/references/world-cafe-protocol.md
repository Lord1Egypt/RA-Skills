# World Café Protocol

Use this protocol when `metadata.discussion_structure` is `world_cafe`. It implements the World Café method inside a roundtable-forge discussion.

## Core principle

In standard roundtable mode, all characters speak in a single group. In World Café mode, **participants are split across multiple tables**. Each table has a fixed **host** who stays put across rotations, while **members rotate** to new tables between rounds. This cross-pollinates ideas across tables and prevents groupthink.

The host is the continuity anchor: they summarize the previous rotation's key points for new arrivals, ensuring insights carry forward without being lost in rotation.

## Phases

| Phase | Value | What happens | Speeches? |
|-------|-------|-------------|-----------|
| Setup | `setup` | Tables formed, hosts assigned, focus question set for all tables. Conductor explains the rotation rules. | No (Conductor framing only) |
| Rotation 1 | `rotation_1` | First discussion round. Each table discusses the focus question independently. Every participant speaks. | Yes |
| Rotation 2 | `rotation_2` | Members rotate to new tables. Hosts stay and deliver a **host summary** of rotation 1's key points. New members build on those insights. | Yes |
| Rotation 3 (optional) | `rotation_3` | A third rotation for larger groups. Same mechanism: hosts summarize, new members build. | Yes |
| Harvest | `harvest` | All tables reconvene in plenary. Each host presents their table's accumulated insights. Conductor synthesizes cross-table patterns. | Yes (host presentations + Conductor synthesis) |

A standard World Café uses 2 rotations. Use 3 only for large groups (6+ participants).

## Table mechanics

- **Table count**: typically 3 tables for 6–9 participants (2–3 members per table + 1 host).
- **Host assignment**: the Conductor designates one host per table. Hosts are chosen for their ability to synthesize and listen, not for domain authority.
- **Rotation order**: members rotate `table_1 → table_2 → table_3 → table_1`. Hosts never rotate.
- **Host summary**: at the start of rotation 2+, each host delivers a 100–150 word summary of the previous rotation's key points. This is recorded as a speech with `is_host: true` and `host_summary` in `structure_context`.

## Conductor behavior

Under World Café mode, the Conductor:

1. **Forms tables** in the setup phase, balancing domain diversity across tables.
2. **Announces each rotation** explicitly: "现在进入第二轮轮换，新成员加入各桌，桌主会先总结上一轮的要点。"
3. **Ensures host summaries** are delivered before new members speak in rotation 2+.
4. **Facilitates the harvest** by inviting each host to present, then synthesizing cross-table patterns.
5. **Writes `structure_context.world_cafe_phase`** to Memory for every round.
6. **Writes `structure_context.table_id` and `structure_context.is_host`** for every speech.

## Character speaking constraints

- **Stay at your table**: speeches are tagged with `table_id`. A character speaks only at their current table for that rotation.
- **Build on previous insights**: in rotation 2+, non-host speeches should reference the host summary or ideas from other tables (carried by the rotating member).
- **Length**: 120–250 words per speech. Host summaries: 100–150 words.
- **Harvest phase**: host presentations are 200–300 words. Conductor synthesis: 200–280 words.

### Example (rotation 1, table 2)

> **组织设计师林薇**：在我们这桌，大家关注的是"激励传导链条在哪里断裂"。一个关键观察是：中层管理者往往是传导链的瓶颈——他们既不被股权激励覆盖，又承担执行压力。如果中层动力流失，高管的激励设计再精巧也传导不到基层。

### Example (rotation 2, host summary)

> **桌主·战略顾问陈昊**（桌主总结）：上一轮我们桌讨论的核心是"薪酬透明度与公平感知的关系"。三个要点：第一，透明度不是公开数字，而是让员工理解差距的逻辑；第二，当透明度缺失时，员工会用自己的假设填补信息真空，而这些假设往往比现实更极端；第三，渐进式透明化比一次性公开更有效。现在请新加入的同事在这个基础上展开。

## Memory representation

### Round-level structure_context

```json
{
  "world_cafe_phase": "rotation_1",
  "table_count": 3,
  "rotation_number": 1
}
```

### Speech-level structure_context

```json
{
  "table_id": "table_1",
  "is_host": false
}
```

For rotation 2+ host speeches, add `host_summary`:

```json
{
  "table_id": "table_1",
  "is_host": true,
  "host_summary": "上一轮讨论的三个要点：1) ... 2) ... 3) ..."
}
```

For harvest phase, `table_id` is omitted (plenary session):

```json
{
  "table_id": null,
  "is_host": true,
  "host_presentation": true
}
```

## Output considerations

- World Café rounds produce **cross-pollinated content**: ideas from one table appear in another table's next rotation, creating a rich web of connections.
- The renderer groups speeches by `table_id` within each rotation, and labels host summaries distinctly.
- A full World Café with 2 rotations × 3 tables × 3 participants typically produces 18–24 speeches = 2,500–6,000 words.
- `world_cafe + podcast` produces a dynamic show where guests describe their table experiences and the host synthesizes.

## Interaction with other features

- **Fusion thinker**: shines in the harvest phase, where cross-table synthesis is most valued.
- **Temporal grounding**: still applies. Each table's claims must be grounded in `metadata.current_date`.
- **Conductor invitation**: best placed between rotations (to check if the focus question needs adjustment) or before harvest (to decide which themes to prioritize).
- **Continuation**: `next_steps` from a World Café are richer because they carry cross-table perspective.
