---
name: vemem
description: Visual entity memory — remember faces, objects, and places across sessions with persistent identity. Use when the user asks who is in an image, when you need to resolve an image to a specific known person/thing, when identifying someone from a photo, when labeling a new face for future recognition, or when maintaining knowledge (facts, events, relationships) keyed by appearance rather than by text. Bridges vision models and text LLMs by turning raw images into named entity references with attached context the text side can reason about.
license: MIT
compatibility: Requires Python 3.12+ and the vemem package (pip install vemem). InsightFace model weights (~200MB) download on first use.
metadata:
  homepage: https://github.com/linville-charlie/vemem
  version: "0.1"
---

# vemem — visual entity memory

## Before you install — what this skill touches on your system

Read this first. This skill handles biometric data, so transparency up front beats surprises later.

### What this skill is, exactly

**The skill itself is instruction-only.** It's the markdown you're reading — no scripts, no executables, no automatic installation of anything. Adding this skill to your ClawHub / Claude Code / Hermes / OpenClaw install does not by itself run code on your machine.

The skill *instructs the agent* to install and use the `vemem` Python package separately. That package is the component that actually reads images and writes to disk.

### If you install the vemem package, here is everything it does

**Local state it creates or reads:**
- `~/.vemem/` (override with `VEMEM_HOME`) — the LanceDB store holding face embeddings, entity bindings, facts, and the event log. This is where biometric vectors live.
- `~/.insightface/models/buffalo_l/` — InsightFace model weights (~200MB), downloaded from InsightFace's official distribution on the first face observation.
- **Images you explicitly pass** to `observe_image` / `identify_image` — either as base64 or as a filesystem path the library reads. **vemem does not scan your disk for images on its own.** It only sees bytes you hand it.

**Network activity vemem itself produces:**
- **First-use only**: downloads InsightFace `buffalo_l` weights. After that, zero network activity from the library.
- The MCP server (`vemem-mcp-server`) uses **stdio only** — no network ports opened.
- The optional OpenClaw sidecar (`vemem-openclaw-sidecar`) binds to **localhost only**.

**What vemem does NOT do on its own:**
- Does not call remote LLM APIs. Example recipes in `references/examples.md` show how to *compose* vemem with OpenAI / Anthropic APIs if you choose to. Those are your calls, with your API keys. If you stay local (Ollama etc.), nothing leaves your machine.
- Does not process images automatically. Every `observe_image` is an explicit invocation by the agent or you.
- Does not train on your data, phone home, or send embeddings anywhere.

### The OpenClaw automatic-processing concern is a separate opt-in

The ClawHub review correctly flagged that vemem has a first-party OpenClaw integration that can auto-process every image attachment. **That integration is a separate install** (`vemem-openclaw-sidecar` + registering a specific OpenClaw plugin) and is NOT enabled by adding this skill or by installing the base `vemem` package.

Enable it only if you understand you're granting an always-on face-recognition layer over every image your agent sees. Disable at any time by stopping the sidecar process.

### Verification & provenance

- Source: [github.com/linville-charlie/vemem](https://github.com/linville-charlie/vemem) · MIT license
- Release tags are signed commits on `main`; pin a version in production (e.g. `vemem==0.1.0`) rather than tracking `latest`
- `pip show -f vemem` lists every file the install adds to your environment
- To audit what the MCP server or sidecar actually touches at runtime:
  - Linux/macOS: `lsof -p <pid>` (open files + sockets) or `strace -e trace=file,network -p <pid>`
  - macOS Instruments File Activity trace for a GUI view
- The GDPR-style `forget()` is [test-verified](https://github.com/linville-charlie/vemem/blob/main/tests/storage/test_lancedb_specific.py) to physically remove embeddings from LanceDB version history. Reproduce locally before trusting for regulated data.

### Compliance context

vemem stores biometric identifiers. **If you deploy it to users other than yourself, YOU are the data controller under GDPR / BIPA / CCPA.** The library provides primitives (`forget` / `restrict` / `export`) but does not enforce consent capture — that's your app's responsibility. Full deployer checklist: [COMPLIANCE.md](https://github.com/linville-charlie/vemem/blob/main/COMPLIANCE.md).

### Recommended first-run posture

1. Install into a dedicated venv, not your system Python.
2. Use a test `VEMEM_HOME` path (e.g. `/tmp/vemem-test`) for your first session so you can inspect + delete the store wholesale.
3. Use a local VLM/LLM (Ollama) for the first integration test, not remote APIs, to confirm no images leave your machine.
4. Enable the OpenClaw sidecar integration only after you've seen vemem behave as a manually-invoked tool.

---

## What this skill does

vemem is the identity layer that sits between a vision model (face/object detector) and a text LLM. It turns "an image of a person" into a **named, stable entity ID** — same person across sessions, same face across angles, same object across lighting.

It keeps track of facts, events, and relationships **per entity** — like Mem0 or mem0-style stores, but keyed on visual identity rather than on a `user_id` you have to know in advance.

## When to activate

Activate this skill when the user:
- asks "who is this?" / "who is in this picture?" / "do you recognize them?"
- wants to remember someone or something for later ("that's Charlie, he runs marathons")
- tells you to correct an identity ("no, that's Dana not Charlie")
- wants to forget an entity for privacy ("remove all data about X")
- asks about entities they've previously introduced ("what do you know about Charlie?")
- wires you into a camera/photo pipeline that needs persistent visual identity

Do NOT activate for:
- general text memory (use the standard memory skill / mem0 / etc.)
- image generation or editing (vemem doesn't touch pixels)
- OCR, captioning, scene description (those are VLM jobs — vemem consumes their output)

## Setup

### Quick check — is vemem available?

Run `python -c "import vemem; print(vemem.__version__)"`. If that fails, install:

```bash
pip install vemem
# or with uv:
uv pip install vemem
```

First-time face encoding triggers a ~200MB InsightFace model download into `~/.insightface/`. Warn the user if their network is constrained.

### Run the MCP server (preferred for agents)

```bash
python -m vemem.mcp_server
```

This exposes 14 tools over stdio. Wire it into your host's MCP config. For Claude Desktop, the ready-to-paste config lives at `docs/examples/claude_desktop_config.json` in the vemem repo.

### Use directly (preferred for scripting in Python)

```python
from vemem import Vemem
vem = Vemem()  # LanceDB store at ~/.vemem, InsightFace encoder
```

Store path is overridable via `VEMEM_HOME` env var or `Vemem(home="/path/to/store")`.

## Core operations — the mental model

There are 13 operations. The ones you'll use most:

### Writing identity into the store

| Op | When |
|---|---|
| `observe(image_bytes)` | A new image came in. Detect faces/objects, embed, persist. Returns a list of Observations, each with a stable content-hash id. |
| `label(observation_ids, name)` | The user just told you who someone is. Creates the entity if new, binds those observations to it. This is the moment identity becomes permanent. |
| `remember(entity_id, fact)` | Attach a fact to a known entity — "Charlie runs marathons", "the red mug lives in the kitchen". |

### Reading identity out

| Op | When |
|---|---|
| `identify(image_bytes, k=5)` | Return candidate entities matching the image, ranked by similarity. Each candidate already includes attached facts — you don't need a separate recall call. |
| `recall(entity_id)` | All known facts, events, and relationships for an entity. Use when the user references someone by name. |

### Correcting mistakes

| Op | When |
|---|---|
| `relabel(observation_id, new_name)` | "That's not Charlie, that's Dana" — reassigns the observation and emits a negative binding so the clusterer won't re-attach it. |
| `merge(entity_ids)` | Two entities turn out to be the same person. Folds them together, preserving facts with provenance. |
| `split(entity_id, groups)` | One entity turns out to be two people. Separates them with cross-wise negative bindings. |
| `forget(entity_id)` | Privacy delete — hard-removes observations, embeddings, bindings, facts. Physically prunes from storage version history (GDPR Art. 17 compliant). **Not reversible.** |
| `undo(event_id=None)` | Undoes the most recent reversible op by you (within a 30-day window). Does not work on `forget`. |

## Common patterns

### Pattern A: camera frame comes in

```python
observations = vem.observe(image_bytes)
candidates = vem.identify(image_bytes, k=3, min_confidence=0.4)

if candidates:
    names = [f"{c.entity.name} (conf {c.confidence:.2f})" for c in candidates]
    print(f"Visible: {', '.join(names)}")
else:
    print(f"Unknown face(s) detected: {len(observations)}. Label with vem.label(obs_ids, name=...).")
```

### Pattern B: user says "that's Charlie"

```python
observations = vem.observe(image_bytes)
charlie = vem.label([o.id for o in observations], name="Charlie")
vem.remember(charlie.id, "we met at the coffee shop on 2026-04-17")
```

### Pattern C: agent needs context for a reply

```python
candidates = vem.identify(image_bytes, k=3)
context_parts = []
for c in candidates:
    fact_strs = "; ".join(f.content for f in c.facts)
    context_parts.append(f"{c.entity.name} (conf {c.confidence:.2f}): {fact_strs}")
context = "People visible: " + " | ".join(context_parts) if context_parts else "No known faces."

# Feed `context` into your LLM's system message or context block.
```

### Pattern D: correction

```python
# identify() said "Charlie" at 0.71 confidence, but user says it's Dana
candidates = vem.identify(image_bytes)
wrong_obs_id = candidates[0].matched_observation_ids[0]
vem.relabel(wrong_obs_id, "Dana")
# A negative binding against Charlie is now recorded — the clusterer won't re-assign.
```

### Pattern E: privacy request

```python
# User says "forget everything about Sarah"
sarah = vem.store.find_entity_by_name("Sarah")
if sarah is not None:
    counts = vem.forget(sarah.id)
    print(f"Deleted: {counts}")
    # Pruned from LanceDB version history — actually gone, GDPR-compliant.
    # This is NOT reversible. Warn the user before calling.
```

## Important constraints

- **Identity is the entity ID, not the name.** `label(..., name="Charlie")` re-uses an existing Charlie entity by name — but renaming an entity doesn't merge it with another same-named one. If the user has two "Charlie"s, use `merge()` explicitly.
- **`forget()` is irreversible.** Ask for confirmation before calling. 30-day `undo` does not cover it.
- **Encoder version is part of identity-of-evidence.** If you try `identify()` with a different encoder than the one used when building the gallery, you get an empty result — not a false match. This is by design.
- **Facts are free-form text.** vemem does not LLM-extract facts from conversations. That's the caller's job (or use Mem0 in parallel, keyed by `entity_id` as the `user_id`).
- **Composable with text memory systems.** The `entity_id` vemem returns is a perfect `user_id` for Mem0 / Letta / Supermemory. They own text conversational memory; vemem owns visual identity.

## Compliance note

vemem stores biometric identifiers. If the host app is deployed to users, the **deployer is the data controller** under GDPR / BIPA / CCPA. Key primitives:
- `forget(entity_id)` = Art. 17 erasure (with prune)
- `restrict(entity_id)` = Art. 18 restriction
- `export(entity_id)` = Art. 20 portability

Full checklist: `COMPLIANCE.md` in the vemem repo.

## Not this skill's job

- **No general chat memory** — use Mem0 / Letta / Supermemory in parallel for text conversational memory.
- **No image generation / editing** — this is a read-and-remember layer.
- **No autonomous clustering commits** in v0 — auto-suggestions exist but require explicit `label()` to commit. This keeps the hot path deterministic.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `identify()` returns `[]` on a face you labeled earlier | Different encoder version, or the face isn't being detected | Check `encoder.id` hasn't changed; try `min_confidence=0.2` to see raw scores |
| `RuntimeError: image pipeline unavailable` | InsightFace weights not installed | First call downloads ~200MB from InsightFace to `~/.insightface/`; ensure network access on first use |
| `ModalityMismatchError` on merge | Trying to merge a face entity with an object entity | v0 keeps modalities separate; create an `instance_of` relationship instead |
| `OperationNotReversibleError` on undo | Past 30 days, or op was `forget` | Not fixable — `forget` is deliberately irreversible; window is configurable via `DEFAULT_UNDO_WINDOW` |

## Deeper references (bundled with this skill)

Loaded on demand when the agent needs the detail — keep them out of the
hot context path.

- [`references/mcp-tools.md`](references/mcp-tools.md) — every MCP tool's
  exact input/output shape. Read when deciding parameter names for a
  specific tool call.
- [`references/examples.md`](references/examples.md) — copy-paste code
  recipes for Ollama, OpenAI, and Claude; correction flows; privacy
  flows; composition with Mem0 / Letta.
- [`references/troubleshooting.md`](references/troubleshooting.md) —
  expanded error matrix with diagnostic commands. Read when a tool
  raises something unexpected.

## Upstream references (in the vemem repo)

- Full spec (load-bearing): `docs/spec/identity-semantics.md`
- Architecture: `docs/ARCHITECTURE.md`
- Real-world VLM+LLM recipes: `docs/examples/real_bridge.md`
- MCP tool reference: `docs/examples/mcp_usage.md`
- Compliance checklist: `COMPLIANCE.md`

Repo: https://github.com/linville-charlie/vemem
