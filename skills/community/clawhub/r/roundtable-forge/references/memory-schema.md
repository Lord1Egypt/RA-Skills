# Memory Schema

The shared Memory file is the single source of truth for a roundtable. Every agent reads from and writes to this file.

> **Authoritative vocabulary:** all enum values used in Memory fields (`characters[].type`, `runtime_claim`, `metadata.output_format`, `metadata.discussion_structure`, `speeches[].action_type`, hat codes, structure phase codes, interjection types, `next_steps[].scope` / `next_steps[].effort`) are defined in [glossary.md](glossary.md). This file documents the **field shape**; the glossary is the **vocabulary source of truth**. When the two disagree, the glossary wins.

## File format

Use JSON. File name convention: `roundtable-<topic-slug>-<timestamp>.json`.

## Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version, currently `2.8.0`. |
| `sources` | array | v2.7.0+ 顶层真实资料清单，cross_promotion 必须引用这里；空数组允许。详见 [sources-and-citations.md](sources-and-citations.md)。 |
| `topic` | string | The user's core question or theme. |
| `user_question` | string | The user's original, full question as entered. Preserved verbatim to ground the report. |
| `owner` | string | The user who initiated the roundtable. |
| `created_at` | string | ISO 8601 timestamp. |
| `updated_at` | string | ISO 8601 timestamp. |
| `disclaimer` | string | The fixed disclaimer text. |
| `runtime_claim` | string | `single_backend_multi_session`, `real_subagent_runtime`, or `soft_orchestration_only`. |
| `state` | string | Current state in the state machine. See [state-machine.md](state-machine.md). One of `init` / `round_open` / `handoff_pending` / `handoff_consumed` / `paused` / `resumed` / `synthesizing` / `completed`. |
| `state_log` | array | Ordered log of state transitions. Each entry: `{from, to, trigger, at, round_number}`. |
| `contract_version` | string | The versioned contract this Memory conforms to. Usually equals `version` but may diverge for forward-compat. |
| `contract_compat` | object | Compatibility window for downstream consumers. `{min_compatible, max_compatible, deprecated_since}`. See [state-machine.md § Lint enforcement](state-machine.md). |
| `characters` | array | List of seated characters, each with an `agent_profile`. |
| `rounds` | array | List of discussion rounds. |
| `interjections` | array | User interjections recorded during the discussion. |
| `synthesis` | object | Consensus, divergence, open questions, next steps, and the optional argument graph. |
| `podcast_script` | object | Populated when `output_formats` (or legacy `output_format`) declares `podcast`. v2.7.0+ has 12 production-quality fields; see [podcast-output-protocol.md](podcast-output-protocol.md). `shownotes.cross_promotion[*].source` 字段必须引用顶层 `sources` 中的 key。 |
| `metadata` | object | Configuration such as max_rounds, expansion_count, runtime_claim, output_format, discussion_structure, current_date, temporal_notes, enforce_handoff_cards. |

## Character object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Short unique identifier. |
| `name` | string | Character name or descriptive label. |
| `type` | string | `real_living`, `real_historical`, `fictional`, or `archetype`. |
| `source_domain` | string | Domain or work the character comes from. |
| `expertise` | array | Areas of knowledge relevant to the topic. |
| `invited_reason` | string | Why this character was selected. |
| `added_round` | integer | Round number when the character joined. |
| `agent_profile` | object | Profile used to instantiate the character agent. See [multi-agent-runtime-protocol.md](multi-agent-runtime-protocol.md). |

## Agent profile object

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Same as `characters[].id`. |
| `role_name` | string | Display name. |
| `persona` | string | System prompt describing the character. |
| `voice_and_tone` | string | Speaking style. |
| `must_protect` | string | Non-negotiable stance. |
| `evidence_type` | string | Allowed claim types. |
| `activation_condition` | string | When the agent should speak. |

## Round object

| Field | Type | Description |
|-------|------|-------------|
| `round_number` | integer | 1-based index. |
| `focus_question` | string | The sub-question for this round. |
| `discussion_structure` | string | Optional. `standard`, `six_hats`, `delphi`, `world_cafe`, or `fishbone`. If omitted, read from `metadata.discussion_structure`. |
| `structure_context` | object | Optional. Structure-specific metadata. For `six_hats`: `{"current_hat": "white", "hat_sequence": [...], "hat_index": 1}`. For `delphi`: `{"delphi_phase": "independent", "anonymized": true, "participant_count": 3}`. For `world_cafe`: `{"world_cafe_phase": "rotation_1", "table_count": 3, "rotation_number": 1}`. For `fishbone`: `{"fishbone_phase": "independent_proposal", "group_count": 3}`. |
| `speaking_order` | array | Ordered list of `character_id` for this round. |
| `speeches` | array | List of speeches, in chronological order. |
| `exchange` | array | Optional exchange replies within the round. |
| `handoff_card` | object | Optional. The handoff card written at the end of this round. Required for non-last rounds when `metadata.enforce_handoff_cards` is `true`. See [handoff-card-protocol.md](handoff-card-protocol.md). |

## Speech object

| Field | Type | Description |
|-------|------|-------------|
| `speech_id` | string | Stable unique identifier. |
| `timestamp` | string | ISO 8601 timestamp. |
| `character_id` | string | Reference to characters[].id. |
| `content` | string | The speech text. |
| `key_points` | array | Bullet summary of claims. |
| `action_type` | string | `independent`, `extend`, `rebut`, `question`, `interrupt`, or `pivot`. See `intra-round-speaking-protocol.md`. |
| `responds_to` | string | Optional `speech_id` this speech responds to. |
| `structure_context` | object | Optional. For `delphi`: `{"anonymous_label": "专家 #1"}`. For `world_cafe`: `{"table_id": "table_1", "is_host": true}`. For `fishbone`: `{"group_id": "group_1", "reviewing_group_id": "group_2"}`. Used by renderers to group and label speeches. |

## Speaking intent object

Recorded in `rounds[].exchange` after each speech to show who wanted to speak next and how.

| Field | Type | Description |
|-------|------|-------------|
| `intent_id` | string | Stable identifier. |
| `timestamp` | string | ISO 8601 timestamp. |
| `character_id` | string | Character who submitted the intent. |
| `trigger_speech_id` | string | The speech that triggered this intent. |
| `intent_type` | string | `extend`, `rebut`, `question`, `pivot`, or `pass`. Submitted after each speech to let the Conductor choose the next speaker. |
| `one_line_reason` | string | Brief reason for the intent. |

## Interrupt object

Recorded in `rounds[].exchange` when a character briefly interrupts another speech.

| Field | Type | Description |
|-------|------|-------------|
| `interrupt_id` | string | Stable identifier. |
| `timestamp` | string | ISO 8601 timestamp. |
| `character_id` | string | Character who interrupts. |
| `interrupted_speech_id` | string | The speech being interrupted. |
| `content` | string | Short challenge or clarification (1-2 sentences). |

## Interjection object

| Field | Type | Description |
|-------|------|-------------|
| `interjection_id` | string | Stable identifier. |
| `round_number` | integer | Round where the interjection happened. |
| `type` | string | `question`, `seat_expansion`, `topic_pivot`, `pause`, `end`, `conductor_invitation`, or `continuation`. |
| `raw_text` | string | The user's original message, or the Conductor's invitation text when `type` is `conductor_invitation`. |
| `resolved_into` | string | The resulting action. |
| `trigger` | string | Required for `conductor_invitation` and `continuation`. Indicates why the interjection was recorded. |
| `selection_mode` | string | Optional for `conductor_invitation`. `single` or `multiple`. Defaults to `single`. |
| `options` | array | Required for `conductor_invitation`. The bounded options presented to the user. |
| `user_response` | string | Required for `conductor_invitation` once the user replies. The user's original reply. |
| `added_seats` | array | Required for `continuation` when new characters are added. List of `character_id`s. |

### `conductor_invitation` records

See [conductor-invitation-protocol.md](conductor-invitation-protocol.md).

- `trigger` values: `value_fork`, `experience_gap`, `abstraction_escalation`, `character_question`, `key_decision`.
- `options` should contain 2–4 bounded choices, but may be empty if the invitation is open-ended.
- `selection_mode` examples: `single`, `multiple`.
- `resolved_into` examples: `awaiting-user-response`, `user-chose-option-B`, `user-chose-options-B-C`, `user-answered-openly:{summary}`, `user-declined`, `topic-pivot`.

### `continuation` records

See [continuation-protocol.md](continuation-protocol.md).

- `trigger` value: `next_step_selection`.
- `resolved_into` format: `new-focus-question:{focus_question}` or `declined`.
- `added_seats` is optional and only populated when the continuation adds new characters.

## Metadata object

| Field | Type | Description |
|-------|------|-------------|
| `max_rounds` | integer | Deprecated. Use `round_budget` instead. Kept for backward compat. |
| `round_budget` | object | `{min, max}` 轮次预算范围。Conductor 根据问题复杂度评估，在每轮 handoff_pending 时检查是否继续。 |
| `complexity_tier` | string | `simple` / `medium` / `complex` / `open_exploration`。问题复杂度分级，决定 round_budget 初始值。 |
| `expansion_count` | integer | How many seats have been added mid-discussion. |
| `protocol_version` | string | Memory schema version. |
| `runtime_claim` | string | Same top-level `runtime_claim`. |
| `output_format` | string | `minutes` (default) or `podcast`. Controls the renderer. |
| `output_formats` | array<string> | v2.6.0+. Plural form of `output_format`. When present, takes precedence over the singular field. |
| `output_artifacts` | array<string> | v2.8.0+. Secondary projections rendered beside the primary formats. Currently supports `argument_graph`; an empty array opts out. |
| `discussion_structure` | string | `standard` (default), `six_hats`, `delphi`, `world_cafe`, or `fishbone`. Controls the thinking methodology. |
| `current_date` | string | ISO 8601 date anchoring the discussion in the present. |
| `temporal_notes` | string | Optional notes on time-sensitive assumptions or verification limits. |
| `enforce_handoff_cards` | boolean | When `true` (default for new roundtables), lint requires `rounds[].handoff_card` for every non-last round. When `false`, handoff cards are recommended but only emit warnings. |

## State log entry object

Stored in top-level `state_log[]`. See [state-machine.md](state-machine.md).

| Field | Type | Description |
|-------|------|-------------|
| `from` | string | Previous state. Empty string for the first log entry. |
| `to` | string | New state. Must be one of the valid states. |
| `trigger` | string | Human-readable trigger. Stable tokens listed in [state-machine.md](state-machine.md#stable-trigger-tokens). |
| `at` | string | ISO 8601 timestamp. |
| `round_number` | integer | The round that owns this transition. Omit for non-round transitions. |

## Contract compat object

Stored in top-level `contract_compat`. Describes the versioned contract window for downstream consumers.

| Field | Type | Description |
|-------|------|-------------|
| `min_compatible` | string | The minimum contract version that can read this Memory. |
| `max_compatible` | string | The maximum contract version tested against this Memory. |
| `deprecated_since` | string | Optional. The contract version since when this contract was deprecated. |

## Handoff card object

Stored in `rounds[].handoff_card`. See [handoff-card-protocol.md](handoff-card-protocol.md).

| Field | Type | Description |
|-------|------|-------------|
| `card_id` | string | Stable id, pattern `hc-NNN`. |
| `from_round` | integer | The round that produced this card. |
| `to_round` | integer | The round expected to consume this card. Omit for the last round. |
| `generated_at` | string | ISO 8601 timestamp. |
| `summary` | string | One-sentence summary, 20–80 字. |
| `key_takeaways` | array | 1–5 actionable points. |
| `unresolved_questions` | array | 0–5 answerable questions. |
| `consumed_by` | array | `speech_id` values that cited this card. |

## Synthesis object

| Field | Type | Description |
|-------|------|-------------|
| `consensus` | array | Points most characters agree on. |
| `divergence` | array | Disagreements with the positions held. |
| `open_questions` | array | Questions worth follow-up. |
| `next_steps` | array | Suggested continuations. Each item is a `Next step` object. |
| `argument_graph` | object | Optional traceable viewpoint graph. Required when `metadata.output_artifacts` contains `argument_graph`. See [argument-graph-protocol.md](argument-graph-protocol.md). |

## Argument graph object

Stored in `synthesis.argument_graph`.

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Argument graph contract version. Currently `1.0.0`. |
| `title` | string | Human-readable graph title. |
| `root_node_id` | string | Existing node id for the graph's central question. |
| `nodes` | array | Atomic viewpoint nodes. |
| `edges` | array | Directed, evidence-backed relationships between nodes. |

### Argument graph node

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable unique id, recommended pattern `ag-nNNN`. |
| `type` | string | `question`, `claim`, `evidence`, `assumption`, `decision`, or `next_step`. |
| `label` | string | Concise atomic idea shown in the graph. |
| `summary` | string | Optional explanation without adding a second claim. |
| `status` | string | `neutral`, `consensus`, `divergent`, or `open`. |
| `character_ids` | array | Characters whose positions the node represents. Empty in Delphi mode. |
| `source_speech_ids` | array | Speech ids that support this extraction. Required for every non-root node. |

### Argument graph edge

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable unique id, recommended pattern `ag-eNNN`. |
| `source` | string | Existing source node id. |
| `target` | string | Existing target node id. |
| `relation` | string | `supports`, `extends`, `contradicts`, `challenges`, `qualifies`, `depends_on`, `answers`, or `raises`. |
| `rationale` | string | Concise transcript-grounded reason for the relation. |
| `source_speech_ids` | array | Speech ids that substantiate the relation. |
| `confidence` | string | `high`, `medium`, or `low`. |

## Next step object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Short identifier, e.g. `ns-001`. |
| `title` | string | One-line description of the continuation. |
| `scope` | string | `micro` (individual task), `meso` (team/process), or `macro` (strategy/culture). |
| `effort` | string | `low`, `medium`, or `high`. |
| `rationale` | string | Why this step is suggested, based on the discussion. |
