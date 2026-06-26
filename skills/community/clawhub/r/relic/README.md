# relic

Relic is a local-first OpenClaw skill package for preserving and evolving a person's durable self-model over time.

It is packaged for ClawHub/OpenClaw as a **skill package** with bundled optional hooks. The skill is the primary published artifact. Optional hooks provide passive capture so the overall installation behaves like a richer plugin experience without storing private user state inside the package.

Source repository context lives at the repo root `README.md`. This package README is for the publishable skill artifact itself.

- **Skill entrypoint** — `SKILL.md`
- **Runtime scripts** — deterministic local commands in `scripts/`
- **Reference docs** — setup, data model, examples, and evolution policy in `references/`
- **Optional bundled hook** — `hooks/openclaw/` for passive capture on `agent:stop`
- **Package metadata** — `_meta.json` and `.clawhub/origin.json`

## Install

Preferred ClawHub flow:

```bash
clawhub install relic
```

Manual local install:

```bash
cp -R relic ~/.openclaw/workspace/skills/relic
```

## Verify the skill

```bash
openclaw skills info relic
openclaw skills check
```

## Private vault location

Relic keeps mutable runtime state outside the published package.

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

1. Initialize the vault:

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/init_relic.py
```

2. Capture an observation manually:

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "I value clarity" --type value
```

3. Distill and export:

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py
python3 ~/.openclaw/workspace/skills/relic/scripts/render_export.py
```

4. Inspect the exported prompt:

```bash
cat "${RELIC_VAULT_PATH:-$HOME/.openclaw/workspace/projects/relic/vault}/exports/agent-prompt.md"
```

## Optional passive capture hook

Relic includes a bundled optional OpenClaw hook named `relic-capture`.

Verify and enable it with:

```bash
openclaw hooks info relic-capture
openclaw hooks check
openclaw hooks enable relic-capture
```

If you just installed or moved the package or hook, start a fresh OpenClaw session or restart the gateway before verifying discovery.

## Verification checklist

- `openclaw skills info relic` resolves the installed skill.
- `openclaw skills check` reports the skill as ready.
- `openclaw hooks info relic-capture` resolves the bundled hook.
- A real OpenClaw session appends observations to `inbox.ndjson`.
- Distill and export write only into the configured vault path.

## References

- `references/openclaw-integration.md`
- `references/hooks-setup.md`
- `references/data-model.md`
- `references/examples.md`
- `references/evolution-policy.md`

## License

MIT
