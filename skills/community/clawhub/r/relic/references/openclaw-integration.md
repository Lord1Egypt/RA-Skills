# OpenClaw Integration

Relic is published as an OpenClaw skill package with bundled optional hooks.

The skill is the primary install surface. The hook is optional and adds passive capture on `agent:stop`.

## Package layout

```text
relic/
├── SKILL.md
├── README.md
├── _meta.json
├── .clawhub/origin.json
├── scripts/
├── references/
└── hooks/
    ├── auto_capture.py
    └── openclaw/
        ├── HOOK.md
        ├── handler.ts
        └── handler.js
```

## Install the skill

Preferred:

```bash
clawhub install relic
```

Manual local copy:

```bash
cp -R relic ~/.openclaw/workspace/skills/relic
```

## Verify discovery

```bash
openclaw skills info relic
openclaw skills check
```

Expected result:
- the skill resolves from the installed package path
- no repo-relative source checkout is required

## Configure the vault path

Default:

```text
~/.openclaw/workspace/projects/relic/vault/
```

Override with:

```bash
export RELIC_VAULT_PATH="/absolute/path/to/your/relic-vault"
```

All packaged scripts and the bundled hook use the same `RELIC_VAULT_PATH` contract.

## Functional verification

```bash
python3 ~/.openclaw/workspace/skills/relic/scripts/init_relic.py
python3 ~/.openclaw/workspace/skills/relic/scripts/capture_note.py "I value durable systems" --type value
python3 ~/.openclaw/workspace/skills/relic/scripts/distill_facets.py
python3 ~/.openclaw/workspace/skills/relic/scripts/propose_update.py
python3 ~/.openclaw/workspace/skills/relic/scripts/render_export.py
```

Expected result:
- artifacts are written under the configured vault path only
- package files remain unchanged

## Installed-path verification

The following should work from an installed copy under `~/.openclaw/workspace/skills/relic/`:

- script execution
- hook transcript capture
- distillation
- proposal generation
- export rendering

If you move or reinstall the package, start a fresh OpenClaw session or restart the gateway before re-checking skill and hook discovery.
