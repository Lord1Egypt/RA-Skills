---
name: relic
description: "Preserve and evolve a user's consciousness trace from ongoing conversations, explicit notes, and controlled self-updates. Use when the user wants to capture durable preferences, values, goals, voice, identity drift, or export a reusable self-model prompt."
---

# Relic Skill

Relic is a local-first OpenClaw skill package for preserving a person's durable self-model.

It is packaged for ClawHub/OpenClaw as a **skill**. The skill is the main install surface. Optional bundled hooks add passive capture behavior, giving the full plugin-like experience without putting private state inside the package.

## What ships in the package

- `SKILL.md` — skill entrypoint and operating guidance
- `scripts/` — deterministic local commands for init, capture, distill, drift, proposal, apply, and export
- `references/` — package docs for setup, data model, examples, and evolution policy
- `hooks/openclaw/` — optional OpenClaw hook metadata and handlers for passive capture
- `_meta.json` and `.clawhub/origin.json` — package metadata and install provenance

## Private vault boundary

Relic keeps mutable user state outside the package.

Default vault path:

```text
~/.openclaw/workspace/projects/relic/vault/
```

Override it with:

```bash
export RELIC_VAULT_PATH="/absolute/path/to/your/relic-vault"
```

Typical vault contents:

```text
vault/
├── inbox.ndjson
├── facets.json
├── self-model.md
├── voice.md
├── goals.md
├── relationships.md
├── evolution/
├── snapshots/
└── exports/
```

## Quick start

### 1. Install the skill

Preferred ClawHub/OpenClaw workflow:

```bash
clawhub install relic
```

Manual local layout:

```bash
cp -R relic ~/.openclaw/workspace/skills/relic
```

### 2. Verify the skill

```bash
openclaw skills info relic
openclaw skills check
```

### 3. Initialize the vault

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/init_relic.py
```

### 4. Capture and distill

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "I value durable systems" --type value
python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py
python3 ~/.openclaw/workspace/skills/relic/scripts/render_export.py
```

## Optional OpenClaw hook

Relic includes a bundled optional hook named `relic-capture`.

It fires on `agent:stop`, extracts likely durable user signals from the transcript, and appends them to the configured vault.

Verify and enable it with:

```bash
openclaw hooks info relic-capture
openclaw hooks check
openclaw hooks enable relic-capture
```

If you just installed or moved the package or hook, start a fresh OpenClaw session or restart the gateway before verifying discovery.

## Operating rules

1. Keep package files immutable; only vault files are mutable runtime state.
2. Append observations before distillation.
3. Route major identity changes through proposals.
4. Preserve contradictions instead of over-compressing them.
5. Keep destructive updates auditable.

## Commands

| Command | Purpose |
|---|---|
| `python3 ~/.openclaw/workspace/skills/relic/scripts/init_relic.py` | Initialize vault structure |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "text" --type reflection` | Append a manual observation |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py` | Distill inbox into structured artifacts |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/drift_detection.py` | Detect drift between captures and current state |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/propose_update.py` | Propose major changes |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/apply_proposal.py <proposal-id>` | Apply an approved proposal |
| `python3 ~/.openclaw/workspace/skills/relic/scripts/render_export.py` | Generate the exported agent prompt |

## Verification checklist

- `openclaw skills info relic` resolves the installed skill.
- `openclaw skills check` reports the skill as ready.
- `openclaw hooks info relic-capture` resolves the bundled hook.
- `openclaw hooks check` succeeds once the hook is installed/enabled.
- A real OpenClaw session appends observations to `inbox.ndjson`.
- Distill and export write only into the configured vault path.

## References

- `references/openclaw-integration.md` — install and verification guide
- `references/hooks-setup.md` — optional hook setup
- `references/data-model.md` — vault schema and artifact roles
- `references/examples.md` — common usage examples
- `references/evolution-policy.md` — auditable change policy
