# Output Template Contract

This file defines the **structural contract** that every roundtable output must satisfy. It is the agreement between the Memory (single source of truth) and any downstream consumer — human readers, other skills, or automated pipelines.

> **Relationship to other files:**
> - [assets/roundtable-template.md](../assets/roundtable-template.md) is the **visual layout** reference for the Markdown renderer.
> - [podcast-output-protocol.md](podcast-output-protocol.md) defines the **podcast script structure** stored in Memory.
> - [argument-graph-protocol.md](argument-graph-protocol.md) defines the **argument graph artifact** stored in synthesis.
> - This file defines the **contract** that all renderers must fulfill: what sections are mandatory, how they map to Memory fields, and what a consumer can rely on.

## Design principle

The output contract follows one rule: **the Memory JSON is the source of truth; the rendered file is a projection**. Every section in the rendered output must trace back to a Memory field. If a Memory field is missing, the renderer omits the section gracefully rather than inventing content.

## Mandatory top-level fields

A Memory file must contain these fields for any output to be renderable. [lint_memory.py](../scripts/lint_memory.py) checks them in `lint_output_contract()`.

| Field | Required | Used by |
|-------|----------|---------|
| `version` | yes | Schema compatibility check. |
| `topic` | yes | Title of the output. |
| `user_question` | yes | Quoted verbatim in the background section. |
| `runtime_claim` | yes | Reported in the route summary. |
| `characters` | yes (non-empty) | Roster display. |
| `rounds` | yes (non-empty) | Discussion body. |
| `disclaimer` | yes | Appended to every output. |
| `metadata` | yes | Configuration block. |
| `metadata.output_formats` or `metadata.output_format` | yes | Selects one or more renderers; plural takes precedence. |
| `metadata.output_artifacts` | recommended | Selects secondary projections; new roundtables default to `argument_graph`. |
| `metadata.discussion_structure` | yes | Selects the phase vocabulary. |
| `metadata.current_date` | yes | Temporal anchor. |
| `synthesis` | recommended | Consensus / divergence / next steps / optional argument graph. |

## Minutes output contract (`minutes` in effective formats)

The Markdown renderer (`render_memory_to_markdown.py`) produces a structured report with these sections, in order:

| Section | Source in Memory | Required |
|---------|-----------------|----------|
| **Title** | `topic` | yes |
| **Disclaimer** | `disclaimer` | yes |
| **Table of contents** | derived from `rounds[].round_number` + `focus_question` | yes |
| **议题背景** (Background) | `user_question`, `metadata.current_date`, `metadata.temporal_notes` | yes |
| **与会角色** (Roster) | `characters[]` with `name`, `type`, `source_domain`, `expertise`, `invited_reason` | yes |
| **讨论过程** (Discussion body) | `rounds[]` with `focus_question`, `speeches[]`, optional `exchange[]` | yes |
| **合成** (Synthesis) | `synthesis.consensus`, `synthesis.divergence`, `synthesis.open_questions`, `synthesis.next_steps` | recommended |
| **如何继续** (Continuation) | fixed text + Memory file path reference | yes |
| **Disclaimer (footer)** | `disclaimer` | yes |

### Round rendering by discussion structure

The renderer adapts the discussion body section based on `metadata.discussion_structure`:

| Structure | Grouping | Phase label | Special behavior |
|-----------|----------|-------------|------------------|
| `standard` | chronological | none | Free-flowing speeches. |
| `six_hats` | by `current_hat` | hat label per group | All speeches in a hat phase grouped together. |
| `delphi` | chronological | `delphi_phase` label | `anonymous_label` replaces character name; convergence round shows synthesis block. |
| `world_cafe` | by `table_id` | `world_cafe_phase` label | Table groups; `is_host` marked; harvest speeches in plenary. |
| `fishbone` | by `group_id` | `fishbone_phase` label | Group groups; `reviewing_group_id` shown in cross-review. |

### Next step rendering

Each `synthesis.next_steps[]` item renders as:

```markdown
- **ns-001** [meso/medium] 固化输出模板与公共语言清单
  - 理由：{rationale}
```

Legacy string-format items render as plain bullets. The lint warns when `id` or `title` is missing.

## Podcast output contract (`podcast` in effective formats)

The podcast renderer (`render_memory_to_podcast_script.py`) produces a narrative transcript. See [podcast-output-protocol.md](podcast-output-protocol.md) for the full `podcast_script` object structure.

| Section | Source in Memory | Required |
|---------|-----------------|----------|
| **Show title** | `podcast_script.show_title` | yes |
| **Tagline** | `podcast_script.tagline` | recommended |
| **Segments** | `podcast_script.segments[]` | yes |
| **Segment dialogue** | `segments[].dialogue[]` with `speaker_id`, `line` | yes |
| **Outro** | `podcast_script.outro` | yes |
| **Show notes** | `podcast_script.shownotes` with `cast`, `resources`, `timestamps` | recommended |

When `podcast_script` is empty, the renderer falls back to transforming `rounds` and `synthesis` into a podcast transcript automatically.

## Argument graph artifact contract (`argument_graph` in `metadata.output_artifacts`)

The argument graph renderer (`render_memory_to_argument_graph.py`) produces a
separate `*.argument-graph.md` file. It does not change the effective
`minutes` / `podcast` formats.

| Section | Source in Memory | Required |
|---------|-----------------|----------|
| **Title** | `synthesis.argument_graph.title` or `topic` | yes |
| **Disclaimer** | `disclaimer` | yes |
| **Mermaid graph** | `argument_graph.nodes[]` + `argument_graph.edges[]` | yes |
| **Legend** | controlled relation vocabulary | yes |
| **Node traceability** | `nodes[].character_ids` + `nodes[].source_speech_ids` | yes |
| **Edge rationale** | `edges[].rationale` + `edges[].source_speech_ids` | yes |
| **Disclaimer (footer)** | `disclaimer` | yes |

The renderer must not infer or repair missing relations. If the graph is
declared but missing or fails lint, the artifact is incomplete and must not be
claimed as delivered.

## Downstream consumer guarantees

Any skill or pipeline that reads a roundtable output can rely on these invariants:

1. **The Memory JSON is always valid** — `lint_memory.py` must pass with zero errors before rendering.
2. **Every speech is traceable** — `character_id` references a real character; `responds_to` references a real speech (or is omitted).
3. **Structure context is consistent** — if `metadata.discussion_structure` is `world_cafe`, every round carries `structure_context.world_cafe_phase`; the lint enforces this.
4. **The disclaimer is always present** — in both the header and footer of minutes, and in the outro of podcast.
5. **Temporal anchor is set** — `metadata.current_date` grounds all time-sensitive claims.
6. **Synthesis follows the standard shape** — `consensus`, `divergence`, and `open_questions` are arrays; `next_steps` items use the structured object form with `id`, `title`, `scope`, `effort`.
7. **Graph relations are traceable** — every non-root graph node and every graph edge cites existing `speech_id` values; all node and edge references resolve.
8. **Delphi anonymity survives graph rendering** — Delphi argument graph nodes do not expose `character_ids`.

## Validation checklist

Before declaring a roundtable complete, verify:

- [ ] `lint_memory.py` reports 0 errors.
- [ ] All mandatory top-level fields are present and non-empty.
- [ ] `metadata.output_format` matches the renderer used.
- [ ] Every `metadata.output_artifacts` entry has a matching synthesis payload and rendered file.
- [ ] `metadata.discussion_structure` matches the phase vocabulary in `rounds[].structure_context`.
- [ ] Every `character_id` in `speeches[]` resolves to a character in `characters[]`.
- [ ] `synthesis.next_steps[]` items all have `id` and `title`.
- [ ] Argument graph node/edge references and speech citations all resolve.
- [ ] Every rendered file opens with the disclaimer and ends with it.

## Change protocol

When modifying the output contract:

1. Update this file.
2. Update [glossary.md](glossary.md) if new terms are introduced.
3. Update [memory-schema.md](memory-schema.md) if new fields are added.
4. Add or update lint rules in [lint_memory.py](../scripts/lint_memory.py).
5. Bump `VERSION`; bump `CURRENT_SCHEMA_VERSION` only when the Memory schema itself changes.
6. Run the full validation gate: `quick_validate` → `validate.py --changed` → benchmark.
