# MCP tool reference

Every tool the vemem MCP server exposes, with the exact input/output shape. Use this when the agent has decided which op to call and needs the precise argument names.

All tools accept an optional `actor` string (default `mcp:unknown`, overridable via the `VEMEM_MCP_ACTOR` env var). Writes record the actor in the EventLog for audit.

---

## Image ingestion

### `observe_image`

Detect + embed + persist every region in an image. Idempotent — re-observing the same bytes at the same bbox returns existing ids.

**Input** (provide exactly one of `image_base64` or `image_path`):
- `image_base64` (string, optional) — base64-encoded image bytes
- `image_path` (string, optional) — local filesystem path the MCP server can read
- `source_uri` (string, default `"mcp://inline"`) — opaque reference vemem stores but never fetches
- `modality` (string, default `"face"`) — `face` / `object` / `scene` / `audio`

**Output:**
```json
{
  "observations": [
    {"id": "obs_abc123", "bbox": [120, 80, 180, 240], "detector_id": "insightface/buffalo_l@0.7.3"}
  ],
  "source_hash": "sha256:..."
}
```

**When to call:** A new image came in and you want to remember it. Call before `label` or `identify_image` if you want the observation ids back.

---

### `identify_image`

Read-only. Run detector + encoder on an image, query the gallery, return ranked candidate entities per detected region.

**Input** (same image inputs as `observe_image`):
- `image_base64` OR `image_path`
- `k` (int, default 5) — max candidates per detection
- `min_confidence` (float, default 0.5) — filter threshold on cosine similarity
- `prefer` (string, default `"instance"`) — `instance` | `type` | `both` — ranking preference when both kinds match

**Output:**
```json
{
  "encoder_id": "insightface/arcface@0.7.3",
  "detections": [
    {
      "bbox": [120, 80, 180, 240],
      "candidates": [
        {
          "entity": {"id": "ent_charlie", "name": "Charlie", "kind": "instance", "modality": "face", "status": "active"},
          "confidence": 0.94,
          "matched_observation_ids": ["obs_..."],
          "method": "user_label",
          "facts": [{"content": "runs marathons", "source": "user"}]
        }
      ]
    }
  ]
}
```

**When to call:** You want to know who is in an image. The `facts` array is already populated — no follow-up `recall` needed.

---

### `identify_by_name`

Resolve an entity by name or id and return its full knowledge snapshot.

**Input:**
- `entity_name_or_id` (string, required) — display name or entity uuid

**Output:** same shape as `recall` (see below).

**When to call:** The user mentioned someone by name. You want their facts without having an image.

---

## Writes

### `label`

Bind one or more observations to a named entity. Creates the entity if new.

**Input:**
- `observation_ids` (list of strings, required)
- `entity_name_or_id` (string, required) — creates new if not found
- `actor` (string, optional)

**Output:**
```json
{"entity": {"id": "ent_charlie", "name": "Charlie", ...}, "entity_was_created": true}
```

**When to call:** User told you who someone is. "That's Charlie." Always call this, not `observe_image` + some other binding op.

---

### `relabel`

Move a single observation to a different entity. Emits a negative binding against the old entity so the auto-clusterer can't re-attach.

**Input:**
- `observation_id` (string, required)
- `new_entity_name_or_id` (string, required)
- `actor` (string, optional)

**Output:** `{"entity": {...}}`

**When to call:** Correction. "No, that's not Charlie, that's Dana." Use instead of calling `label` again — `relabel` records the negative signal.

---

### `merge`

Fold multiple entities into one. Migrates bindings + facts with provenance.

**Input:**
- `entity_ids` (list of strings, required) — 2+ entities
- `keep` (string, default `"oldest"`) — entity id or literal `"oldest"`
- `actor` (string, optional)

**Output:** `{"winner": {...}, "loser_ids": [...]}`

**When to call:** Two "unknown" entities turn out to be the same person. Rejects across modalities or across instance/type.

---

### `split`

Break one entity into N. `groups[0]` stays on the original id; subsequent groups become new entities. Cross-wise negative bindings emitted.

**Input:**
- `entity_id` (string, required) — the entity to split
- `groups` (list of list of observation ids) — how to partition
- `fact_policy` (string, default `"keep_original"`) — `keep_original` | `copy_to_all` | `manual`
- `actor` (string, optional)

**Output:** `{"entities": [{...}, {...}]}`

**When to call:** One entity was actually two people. Ungrouped observations stay on the original.

---

### `forget`

**Irreversible.** Hard-delete all observations, embeddings, bindings, facts, events, relationships. Prunes storage version history so biometric data is physically gone (GDPR Art. 17 compliant).

**Input:**
- `entity_id` (string, required)
- `grace_days` (int, default 0) — reserved for future grace-window support; 0 means delete now
- `actor` (string, optional)

**Output:** `{"counts": {"observations": N, "embeddings": N, "bindings": N, "facts": N, "events": N, "relationships": N}}`

**When to call:** User explicitly asks to delete someone's data. ALWAYS confirm first. Not recoverable via `undo`.

---

### `restrict` / `unrestrict`

Flip status between `active` and `restricted`. Restricted entities are excluded from `identify_image` / `identify_by_name` but their data is retained.

**Input:** `entity_id` (string), `actor` (string, optional)

**Output:** `{"entity": {..., "status": "restricted"}}`

**When to call:** GDPR Art. 18 — user wants to stop inference without deletion. Reversible via `unrestrict`.

---

## Knowledge

### `remember`

Attach a free-form text fact to an entity. Bi-temporal; retract later with `retract_fact` (via CLI) if needed.

**Input:**
- `entity_id` (string, required)
- `content` (string, required) — the fact text
- `source` (string, default `"user"`) — `user` / `vlm` / `llm` / `import`
- `actor` (string, optional)

**Output:** `{"fact": {"id": "fact_...", "content": "...", "source": "user", ...}}`

**When to call:** User told you something about someone. "Charlie runs marathons." Always tie to a resolved entity_id.

---

### `recall`

Full knowledge snapshot for an entity — facts, events, relationships.

**Input:**
- `entity_id` (string, required)
- `active_only` (bool, default true) — include retracted items when false

**Output:**
```json
{
  "entity": {"id": "ent_charlie", "name": "Charlie", ...},
  "facts": [{"content": "runs marathons", "valid_from": "...", "source": "user"}],
  "events": [{"content": "met at coffee shop", "occurred_at": "2026-04-03T10:00:00Z"}],
  "relationships": [{"from_entity_id": "...", "to_entity_id": "...", "relation_type": "cofounder_of"}]
}
```

**When to call:** User asked about someone you know. Feed the returned facts into the LLM's context block.

---

## Audit / reversal

### `undo`

Reverse the most recent reversible op by this actor (or a specific event). 30-day window. Does NOT work on `forget`.

**Input:**
- `event_id` (int, optional) — specific event to reverse; omit for most-recent-by-actor
- `actor` (string, optional)

**Output:** `{"undo_event": {"id": N, "undone_event_id": M, ...}}`

**When to call:** User says "undo that" or you want to roll back a mistaken label/merge/split. If it's forget, warn — forget is irreversible.

---

### `export`

GDPR Art. 20 data portability. Dump every row tied to an entity as JSON.

**Input:**
- `entity_id` (string, required)
- `include_embeddings` (bool, default false) — raw biometric vectors are usually not what the user wants

**Output:**
```json
{
  "entity": {...},
  "observations": [...],
  "embeddings": [],
  "bindings": [...],
  "facts": [...],
  "events": [...],
  "relationships": [...],
  "event_log": [...]
}
```

**When to call:** User asks "what do you have on me?" or wants a portable copy of their data before `forget`.

---

## Errors and what they mean

All domain errors bubble up as MCP tool errors with the exception message:

- `ModalityMismatchError` — trying to mix face + object observations in one label/merge call
- `KindMismatchError` — trying to merge an `instance` with a `type`; use `instance_of` relationship instead
- `EntityUnavailableError` — target entity is forgotten, merged, or not found
- `OperationNotReversibleError` — undoing past the 30-day window, undoing a `forget`, or undoing an already-undone event
- `NoCompatibleEncoderError` — querying a vector with an `encoder_id` that has no gallery rows
- `RuntimeError: vemem image pipeline unavailable` — InsightFace weights not installed; run the install once manually with network access

Always echo the error to the user when you can't silently recover.
