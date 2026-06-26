# Data Contracts

The runtime now focuses on trade journaling plus long-term memory.

## Runtime Layout

- `data/finance_journal.db`: main SQLite database
- `artifacts/daily/YYYYMMDD/`: daily artifacts, reference notes, reports, memory compaction outputs
- `memory/`: long-term memory snapshots and markdown mirrors
- `status/`: scheduler state
- `obsidian-vault/`: user-facing markdown vault

## Core Tables

### `plans`

Required keys:
- `plan_id`
- `ts_code`
- `direction`
- `thesis`
- `logic_tags_json`
- `valid_from`
- `valid_to`
- `status`

### `trades`

Required keys:
- `trade_id`
- `ts_code`
- `buy_date`
- `buy_price`
- `status`

### `reviews`

Required keys:
- `review_id`
- `trade_id`
- `ts_code`
- `sell_date`
- `review_due_date`
- `status`

### `session_threads`

Required keys:
- `session_key`
- `status`
- `memory_json`
- `last_route`
- `updated_at`

`memory_json` is short-term conversational memory only.
Long-term recall lives in the memory tables below.

## Long-Term Memory Tables

### `memory_cells`

Required keys:
- `memory_id`
- `memory_kind`
- `source_entity_kind`
- `source_entity_id`
- `title`
- `text_body`
- `summary_json`
- `tags_json`
- `quality_json`
- `provenance_json`

### `memory_scenes`

Required keys:
- `scene_id`
- `scene_key`
- `scene_type`
- `title`
- `memory_ids_json`
- `stats_json`

### `memory_hyperedges`

Required keys:
- `edge_id`
- `edge_key`
- `edge_type`
- `label`

### `memory_skill_cards`

Required keys:
- `skill_id`
- `source_kind`
- `source_id`
- `title`
- `intent`
- `trigger_conditions_json`
- `do_not_use_when_json`
- `evidence_trade_ids_json`
- `sample_size`
- `bandit_snapshot_json`

## Session / Evolution Payload Additions

### `session turn`

Optional keys:
- `memory_retrieval`
- `memory_checklist`

### `evolution remind`

Optional keys:
- `memory_candidates`
- `linked_skill_cards`

### `plan reference`

Optional keys:
- `memory_candidates`
- `linked_skill_cards`
