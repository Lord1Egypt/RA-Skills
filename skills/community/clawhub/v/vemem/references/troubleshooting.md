# Troubleshooting

Symptoms → likely cause → fix. Scan this when something isn't working; the short version is in the main `SKILL.md` under "Troubleshooting."

---

## Install / startup

### `ModuleNotFoundError: No module named 'vemem'`

vemem isn't installed in the current environment. Fix:

```bash
pip install vemem
# or in a uv-managed project:
uv add vemem
```

### `RuntimeError: vemem image pipeline unavailable — InsightFace failed to initialize`

The InsightFace `buffalo_l` weights (~200MB) haven't been downloaded to `~/.insightface/models/buffalo_l/`, or the download was interrupted. InsightFace downloads on first construction, so the fix is to let it run with network access:

```bash
python -c "from insightface.app import FaceAnalysis; FaceAnalysis(name='buffalo_l').prepare(ctx_id=0)"
```

If you're on an offline host, pre-download on a connected machine and copy the `~/.insightface/` folder across.

Text-only operations (`label`, `recall`, `remember`, `merge`, etc.) still work with the pipeline unavailable — only image-taking tools (`observe_image`, `identify_image`) will raise.

### `lancedb.connect()` segfaults — process crashes before any Python error

Known issue: `lancedb<0.20` segfaults on CPython 3.14. The project pins local dev to Python 3.13 via `.python-version`. Fix:

```bash
# If using uv:
echo "3.13" > .python-version
uv sync

# If using pyenv:
pyenv install 3.13
pyenv local 3.13
pip install vemem
```

The CI matrix runs 3.12 and 3.13 so published releases are covered; it's purely a local-dev bump-Python issue.

### MCP server won't start

Check that the console script is installed:

```bash
which vemem-mcp-server
# /Users/.../venv/bin/vemem-mcp-server
```

If missing, the install didn't register `[project.scripts]` — reinstall with `pip install --force-reinstall vemem` or run `python -m vemem.mcp_server` as a fallback.

If the server starts but the client can't reach it, check `VEMEM_HOME` is writable:

```bash
ls -la "$VEMEM_HOME"  # default: ~/.vemem
```

---

## Identity resolution

### `identify()` returns `[]` on a face I just labeled

Three possible causes, ordered by likelihood:

1. **Different encoder between write and read.** Encoder version is part of identity-of-evidence. If the write side used `insightface/arcface@0.7.3` and the read side uses `insightface/arcface@0.8.0`, the gallery is empty for the new encoder. Check `encoder.id` on both sides. Fix: pin the insightface version or accept that an encoder bump means rebuilding the gallery (v0 limitation; re-embed path is a v0.1 item).

2. **Confidence threshold too strict.** Default is 0.5. For face verification on real images, 0.35 is often a better floor. Retry with `min_confidence=0.2` to see raw scores:

   ```python
   results = vem.identify(image, min_confidence=0.2, k=10)
   for c in results:
       print(c.entity.name, c.confidence)
   ```

3. **Detector didn't find the face.** If the image has no face (or the detector missed it — small, occluded, or extreme angle), there's nothing to match. Check:

   ```python
   observations = vem.observe(image)
   print(len(observations), "detections")
   ```

### Identify returns the wrong person

The clusterer matched based on embedding similarity alone. Correct it:

```python
candidates = vem.identify(image)
wrong_obs_id = candidates[0].matched_observation_ids[0]
vem.relabel(wrong_obs_id, "CorrectName")
# A negative binding is recorded — can't happen again for this observation.
```

If the wrong match is *systematic* across many observations, the two people may have been auto-clustered together. Split them:

```python
wrong_entity = vem.store.find_entity_by_name("WrongName")
correct_obs = [...]
incorrect_obs = [...]
vem.split(wrong_entity.id, [correct_obs, incorrect_obs])
```

---

## Errors from ops

### `ModalityMismatchError`

You tried to label/merge across `face` and `object` observations in one call. vemem keeps modalities separate in v0.

Fix: make two separate calls, one per modality. Or if you genuinely want to relate a face to an object, create a `Relationship` (e.g. `owner_of`) between their entities.

### `KindMismatchError`

You tried to `merge` an `instance` entity with a `type` entity. This is meaningless — they represent different things ("my red mug" vs. "red mugs in general").

Fix: create an `instance_of` relationship instead:

```python
# Wrong:
vem.merge([my_mug_id, red_mugs_id])

# Right:
vem.store.put_relationship(Relationship(
    from_entity_id=my_mug_id,
    to_entity_id=red_mugs_id,
    relation_type="instance_of",
    ...
))
```

### `EntityUnavailableError`

The entity is `forgotten`, `merged_into` another, or not found. For `forgotten`: it's gone, data can't be recovered. For `merged_into`: use the new (winner) entity id.

```python
entity = vem.store.get_entity(old_id)
if entity and entity.status.value == "merged_into":
    new_id = entity.merged_into_id
    snapshot = vem.recall(new_id)
```

### `OperationNotReversibleError`

Three sub-cases:

1. Event is past the 30-day undo window — not fixable, it expired on purpose.
2. Event is a `forget` — never reversible by design. If the user wants restoration, they need to re-introduce the person (and re-enter consent/labels).
3. Event has already been undone — call `identify_by_name` on the affected entity to inspect current state; you may be chasing a ghost.

### `NoCompatibleEncoderError`

You passed a vector to `identify()` with an `encoder_id` that has no gallery rows. This happens when:
- An encoder-version mismatch (see "identify returns []" above)
- You're querying a fresh store that hasn't had any observations ingested
- You're mixing encoders — the gallery for CLIP is disjoint from the gallery for InsightFace

vemem refuses to silently translate across encoders. Ingest some observations with the same encoder_id first.

---

## Storage / persistence

### "My store is corrupted" / LanceDB errors on read

If LanceDB's lock is stuck or the directory got partially written:

```bash
# As a last resort — move the dir aside and start fresh
mv ~/.vemem ~/.vemem.broken
# Re-label your people; your EventLog in .broken has the history if you need to diff
```

A proper `repair()` CLI is planned for v0.1.

### Disk usage growing

Every write creates a new LanceDB version. Automatic pruning runs on `forget(...)`, but accumulated history grows without explicit cleanup. To compact manually:

```python
from vemem import Vemem
from datetime import datetime, UTC, timedelta

vem = Vemem()
vem.store.prune_versions(datetime.now(UTC) - timedelta(days=7))
```

EventLog rows are retained by default (1 year non-forget, 5 years forget). For stores with heavy write volume, trim:

```python
# NOT implemented as a first-class method yet; use LanceDB's table access
# if you really need to truncate the log. Losing the log means losing undo.
```

---

## Performance

### `observe()` is slow

Expected on the first call — InsightFace's ONNX runtime warms up the model. Subsequent calls on the same Python process should be ~50-200ms for a 1080p image on a modern CPU, faster with GPU.

Bulk ingest patterns:

```python
# Don't do this in a tight loop — each call reloads the encoder state
for path in paths:
    vem.observe(open(path, "rb").read())

# Do batch in a single process / worker:
vem = Vemem()  # loads encoder once
for path in paths:
    vem.observe(open(path, "rb").read())
```

### `identify()` returns stale results after writes

LanceDB's ANN index doesn't update automatically after every write. v0 uses brute-force cosine search so this isn't an issue at personal scale, but if you've called `create_index()` manually:

```python
vem.store._db.open_table("embeddings_insightface__arcface_0_7_3").optimize()
# Rebuild the index after bulk writes
```

### Queries against LanceDB suddenly crashing

You probably upgraded Python to 3.14 on a machine with an older `lancedb`. Pin to 3.13 (see "install / startup" above).

---

## Diagnostics

Quick sanity check:

```python
import vemem
from vemem import Vemem

print(vemem.__version__)

with Vemem() as vem:
    print("store:", type(vem.store).__name__)
    print("encoder:", vem._encoder.id if vem._encoder else "(none — weights missing)")
    print("detector:", vem._detector.id if vem._detector else "(none)")
```

Listing the schema version + table counts:

```python
from vemem.storage.lancedb_store import LanceDBStore

store = LanceDBStore()
print("schema version:", store.schema_version())
print("tables:", store._db.table_names())
```

If you're debugging a production install, `uv run vm inspect <entity_id>` shows the entity's current binding count, active facts, and recent events without having to drop into Python.

---

## When to file an issue

Real bugs worth reporting to https://github.com/linville-charlie/vemem/issues:

- `forget()` didn't prune vectors (verify by calling `table.checkout(pre_forget_version)` and seeing the row still there)
- Schema mismatch after upgrade (`SchemaVersionError`)
- Crash with a clean reproducer, not just "my store is weird"
- Thread-safety issue — v0 is single-writer by design, but if single-writer loses data, that's a bug

Not bugs:
- "identify() returned a different confidence than last time" — encoder behavior
- "I want behavior X" — open a discussion, not an issue
- "Python 3.14 segfaults on lancedb 0.19" — known; upgrade lancedb or pin Python
