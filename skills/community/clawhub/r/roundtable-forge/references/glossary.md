# Glossary

This file is the single source of truth for the vocabulary used across roundtable-forge. Every protocol, schema field, lint rule, and renderer must use the terms defined here. When adding a new enum value or concept, update this file first, then update [memory-schema.md](memory-schema.md) and [lint_memory.py](../scripts/lint_memory.py) in the same pass.

## Core roles

| Term | Definition |
|------|------------|
| **Conductor** | The coordinator agent that selects characters, poses focus questions, dispatches agents, writes to Memory, and synthesizes the outcome. The Conductor never appears as a speaking character in the transcript. |
| **Character** | A participant agent with its own `agent_profile`. Each character speaks from a distinct domain. Synonyms: participant, seat, guest (podcast mode). |
| **Host** | A special `archetype` character added only in podcast mode. Serves the listener, not the argument. See [podcast-output-protocol.md](podcast-output-protocol.md). |
| **User** | The human who initiated the roundtable. The Conductor invites the user at bounded decision points. |

## Core concepts

| Term | Definition |
|------|------------|
| **Memory** | The shared JSON file that is the single source of truth for a roundtable. All agents read from and write to this file. Schema defined in [memory-schema.md](memory-schema.md). |
| **Round** | A topic segment with a single `focus_question`. A roundtable contains one or more rounds. |
| **Speech** | A single character's utterance within a round. Each speech has a `speech_id`, `character_id`, `content`, and optional `action_type`. |
| **Exchange** | The intra-round record of speaking intents and interrupts. See [intra-round-speaking-protocol.md](intra-round-speaking-protocol.md). |
| **Synthesis** | The final convergence section: `consensus`, `divergence`, `open_questions`, and `next_steps`. Populated by the Conductor after the last round. |
| **Argument graph** | A compact, traceable projection of atomic viewpoints and their relations. Stored in `synthesis.argument_graph`; rendered as a separate artifact. See [argument-graph-protocol.md](argument-graph-protocol.md). |
| **Interjection** | A user or Conductor interruption recorded during the discussion. See [user-interjection-protocol.md](user-interjection-protocol.md). |

## Four orthogonal dimensions

| Dimension | Field | Purpose |
|-----------|-------|---------|
| **Discussion structure** | `metadata.discussion_structure` | Controls *how* characters think (methodology). See values below. |
| **Output format** | `metadata.output_format` | Controls *what* the final artifact looks like (renderer target). See values below. |
| **Output artifact** | `metadata.output_artifacts` | Declares additional projections produced beside the primary format, such as an argument graph. |
| **Runtime claim** | `runtime_claim` / `metadata.runtime_claim` | Controls *where* agents execute (execution tier). See values below. |

These four are independent: any structure can pair with any format, artifact set, and runtime.

## Enum vocabularies

The following enums are enforced by [lint_memory.py](../scripts/lint_memory.py). Using a value outside these sets triggers an error or warning.

### `characters[].type`

| Value | Meaning |
|-------|---------|
| `real_living` | A real person currently alive. Requires temporal grounding. |
| `real_historical` | A real person from history. |
| `fictional` | A character from fiction, literature, or media. |
| `archetype` | A generalized role (e.g., "产品经理", "系统架构师") rather than a specific person. |

### `runtime_claim`

| Value | Meaning |
|-------|---------|
| `single_backend_multi_session` | Default. All characters run as isolated prompts within one backend. |
| `real_subagent_runtime` | Each character is spawned as an independent subagent via the Task tool. |
| `soft_orchestration_only` | Fallback. The Conductor simulates characters without true agent isolation. |

### `metadata.output_format`

| Value | Renderer | Use when |
|-------|----------|----------|
| `minutes` | `render_memory_to_markdown.py` | Default. Structured, reader-facing report. |
| `podcast` | `render_memory_to_podcast_script.py` | Narrative, listenable dialogue transcript with a Host. |

### `metadata.output_formats` (v2.6.0+)

A plural form of `output_format` that declares multiple renderer targets in one go. When present, `output_formats` takes precedence over `output_format` and the Conductor renders each declared format separately.

| Value | Renderer | Use when |
|-------|----------|----------|
| `["minutes"]` | `render_memory_to_markdown.py` | Same as `output_format: minutes`. |
| `["podcast"]` | `render_memory_to_podcast_script.py` | Same as `output_format: podcast`. |
| `["minutes", "podcast"]` | Both renderers, in this order | Dual-output: a reader-facing report and a listenable dialogue transcript side by side. |
| `["podcast", "minutes"]` | Both renderers, reversed order | Same as above but emit podcast first. |

**Coexistence rules** (when both fields are present):

| `output_format` | `output_formats` | Effective |
|----------------|------------------|-----------|
| absent | `["minutes"]` | `["minutes"]` |
| `minutes` | absent | `["minutes"]` |
| `minutes` | `["podcast"]` | `["podcast"]` (the plural form wins) |
| `podcast` | `["minutes", "podcast"]` | `["minutes", "podcast"]` |

The legacy `output_format` field is preserved for backwards compatibility and existing instances. New instances should prefer `output_formats`.

### `metadata.output_artifacts` (v2.8.0+)

A list of secondary projections generated from the same Memory after synthesis.
Artifacts do not replace or extend `metadata.output_formats`.

| Value | Renderer | Use when |
|-------|----------|----------|
| `argument_graph` | `render_memory_to_argument_graph.py` | Show atomic viewpoints, support/opposition paths, assumptions, and open questions. |

New full and continued roundtables default to `["argument_graph"]`. An empty
array explicitly opts out. See
[argument-graph-protocol.md](argument-graph-protocol.md).

### `synthesis.argument_graph` vocabularies

#### Node types

| Value | Meaning |
|-------|---------|
| `question` | Root or open question. |
| `claim` | Substantive position or recommendation. |
| `evidence` | Fact, example, or observation used as support. |
| `assumption` | Premise another position depends on. |
| `decision` | Converged choice or explicit trade-off. |
| `next_step` | Proposed action after synthesis. |

#### Node status

| Value | Meaning |
|-------|---------|
| `neutral` | No convergence status assigned. |
| `consensus` | Broad agreement. |
| `divergent` | Material disagreement. |
| `open` | Unresolved. |

#### Edge relations

| Value | Meaning |
|-------|---------|
| `supports` | Supplies evidence or reasoning for the target. |
| `extends` | Adds a compatible dimension. |
| `contradicts` | Directly conflicts under the same conditions. |
| `challenges` | Questions a premise, evidence, or practicality. |
| `qualifies` | Adds a condition, exception, or boundary. |
| `depends_on` | Requires the target to hold. |
| `answers` | Directly answers the target question. |
| `raises` | Introduces the target question or issue. |

#### Edge confidence

| Value | Meaning |
|-------|---------|
| `high` | Explicitly stated in the transcript. |
| `medium` | Strongly implied by an explicit response path. |
| `low` | Plausible but should be treated cautiously. |

### `podcast_script` (v2.7.0+ production spec)

When `output_formats` includes `"podcast"`, Memory carries an authoritative `podcast_script` object. v2.7.0+ expands this object with 12 production-quality fields modeled on competitive analysis of Chinese-market reference podcasts (《无人知晓》《岩中花述》《天真不天真》). See [podcast-output-protocol.md](podcast-output-protocol.md#production-quality-spec-v270) for full spec.

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `show_title` | yes | string | Episode title with season/episode marker |
| `tagline` | yes | string | One-sentence show positioning |
| `host_id` | yes | string (char id) | Which character plays Host |
| `intro_narrative` | recommended | object | Three-segment Host intro: `context_entry` / `guest_intro` / `emotional_promise` |
| `structure_mode` | yes | `free\|parts\|hybrid` | Whether the episode uses Parts / free-flow / hybrid |
| `segments` | yes | array | Per-segment title, intro, dialogue, transition |
| `outro` | yes | string | Host closing monologue |
| `shownotes.cast` | yes | array of strings | Speaker roster with role annotations |
| `shownotes.team` | yes | object | `{host, editor, producer}` with handles |
| `shownotes.about_show` | recommended | string | 1–2 sentence show positioning |
| `shownotes.timestamps` | yes | array of `{time, topic}` | Min 5–25 depending on episode length, MM:SS format |
| `shownotes.resources` | yes | array of `{time, type, title, source}` | Min 1 per timestamp; min 20 for 90+ min episodes |
| `shownotes.theme_song` | recommended | `{title, artist, license}` | Brand asset |
| `shownotes.sponsor` | optional (can be `{}`) | `{name, description}` | Commercial backing |
| `shownotes.social` | recommended | `{website, xiaohongshu, wechat, weibo, other}` | Multi-platform distribution handles |
| `shownotes.mid_breaks` | conditional (episodes > 90 min) | array of `{time, label}` | Mid-episode break markers |
| `shownotes.cross_promotion` | optional | array of `{show, episode, topic}` | Internal show network effects |
| `shownotes.legal_disclaimer` | recommended | string | Topic-specific disclaimer (investment / medical / legal / AI-speculative / generic) |
| `shownotes.ai_generated_disclaimer` | yes | string | Standard AI-generation notice (mirrors Memory's top-level `disclaimer` field) |

**Backward compat**: Existing instances with only the v2.5.x fields (`show_title`, `tagline`, `host_id`, `segments`, `outro`, `shownotes` with just `cast`/`resources`/`timestamps`) continue to work. The renderer will emit fallback placeholders for any missing v2.7.0 field.

### `metadata.discussion_structure`

| Value | Protocol reference | Phases |
|-------|-------------------|--------|
| `standard` | — (free-flowing) | No phases. |
| `six_hats` | [six-hats-protocol.md](six-hats-protocol.md) | Hat sequence: `blue_open` → `white` → `red` → `yellow` → `black` → `green` → `blue_close`. |
| `delphi` | [delphi-protocol.md](delphi-protocol.md) | `independent` → `feedback` → `convergence`. |
| `world_cafe` | [world-cafe-protocol.md](world-cafe-protocol.md) | `setup` → `rotation_1` → `rotation_2` → `rotation_3` → `harvest`. |
| `fishbone` | [fishbone-protocol.md](fishbone-protocol.md) | `grouping` → `independent_proposal` → `cross_review` → `synthesis`. |

### `speeches[].action_type` and speaking intents

| Value | Meaning (action_type) | Meaning (intent) |
|-------|----------------------|-------------------|
| `independent` | A standalone opening statement. | — |
| `extend` | Build on a previous speech. | Wants to extend. |
| `rebut` | Challenge or disagree. | Wants to rebut. |
| `question` | Ask a probing question. | Wants to ask. |
| `interrupt` | A brief mid-speech clarification (recorded in `exchange`). | — |
| `pivot` | Shift to a new angle. | Wants to change direction. |
| `pass` | — | Declines to speak this turn. |

### Hat codes (six_hats)

| Code | Label |
|------|-------|
| `blue_open` | Blue hat · Opening (process control) |
| `white` | White hat · Facts and data |
| `red` | Red hat · Emotions and intuition |
| `yellow` | Yellow hat · Value and optimism |
| `black` | Black hat · Risks and caution |
| `green` | Green hat · Creativity and alternatives |
| `blue_close` | Blue hat · Closing (synthesis) |
| `blue` | Blue hat · Process control (generic) |

### Delphi phases

| Phase | Description |
|-------|-------------|
| `independent` | Experts answer independently without seeing each other's responses. |
| `feedback` | Anonymized summary circulated; experts revise. |
| `convergence` | Final consensus, divergence, and open questions recorded. |

### World Café phases

| Phase | Description |
|-------|-------------|
| `setup` | Table hosts introduce focus questions; members seated. |
| `rotation_1` | First rotation: members move to new tables. |
| `rotation_2` | Second rotation. |
| `rotation_3` | Third rotation. |
| `harvest` | Table hosts present cross-round insights to the plenary. |

### Fishbone phases

| Phase | Description |
|-------|-------------|
| `grouping` | Divide participants into independent sub-groups. |
| `independent_proposal` | Each group produces a complete proposal. |
| `cross_review` | Groups review each other's proposals. |
| `synthesis` | Merge reviewed proposals into a final output. |

### Interjection types

| Value | Description |
|-------|-------------|
| `question` | User asks a clarifying question. |
| `seat_expansion` | User adds a new character. |
| `topic_pivot` | User redirects the discussion. |
| `pause` | User pauses the discussion. |
| `end` | User ends the discussion early. |
| `conductor_invitation` | Conductor pauses to ask the user a bounded question. |
| `continuation` | User selects a `next_step` to continue. |

### Conductor invitation triggers

| Value | When to use |
|-------|-------------|
| `value_fork` | The discussion reaches a value judgment split. |
| `experience_gap` | The agents lack real-world context the user can provide. |
| `abstraction_escalation` | The discussion is getting too abstract; needs grounding. |
| `character_question` | The user might want to add or clarify a character. |
| `key_decision` | A key decision point that the user should own. |

### `next_steps[].scope`

| Value | Meaning |
|-------|---------|
| `micro` | An individual task one person can complete. |
| `meso` | A team or process-level change. |
| `macro` | A strategy or culture-level shift. |

### `next_steps[].effort`

| Value | Meaning |
|-------|---------|
| `low` | Hours to one day. |
| `medium` | Days to a week. |
| `high` | Weeks or more. |

### Roundtable state (top-level `state` field)

| Value | Meaning |
|-------|---------|
| `init` | Memory is initialized, no round dispatched yet. |
| `round_open` | A round is in progress; characters may speak. |
| `handoff_pending` | Current round's speeches are complete; handoff card is being generated. |
| `handoff_consumed` | Next round's first speech has consumed the previous handoff card. |
| `paused` | User paused the discussion via an interjection. |
| `resumed` | User unpaused; about to enter `round_open` for the next round. |
| `synthesizing` | All rounds are done; Conductor is populating `synthesis`. |
| `completed` | Memory is finalized; output is rendered. |

See [state-machine.md](state-machine.md) for transition rules.

### Handoff card fields (rounds[].handoff_card)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `card_id` | string | yes | Stable id, pattern `hc-` + 3-digit zero-padded index. |
| `from_round` | integer | yes | The round that produced this card. |
| `to_round` | integer | recommended | The round expected to consume this card. |
| `generated_at` | string (ISO 8601) | yes | When the card was generated. |
| `summary` | string | yes | One-sentence summary, 20–80 字. |
| `key_takeaways` | array | yes | 1–5 actionable points, each 10–60 字. |
| `unresolved_questions` | array | recommended | 0–5 answerable questions. |
| `consumed_by` | array | recommended | `speech_id` values that cited this card. |

See [handoff-card-protocol.md](handoff-card-protocol.md).

## Field naming conventions

- Use `snake_case` for all JSON field names.
- Use stable `id` fields (`speech_id`, `character_id`, `intent_id`) for cross-references.
- Prefix structure-specific context with the structure name: `world_cafe_phase`, `delphi_phase`, `fishbone_phase`, `current_hat`.
- Temporal fields use ISO 8601 (`created_at`, `updated_at`, `current_date`).
- The disclaimer text is fixed and defined in [disclaimer-template.md](disclaimer-template.md).
