# OpenClaw Integration

Skill Vetter v2 works as a normal packaged skill in OpenClaw.

## Install

```bash
clawdhub install skill-vetter-v2
```

Or copy manually:

```bash
cp -r skill-vetter-v2 ~/.openclaw/skills/
```

## Optional hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/skill-vetter-v2
openclaw hooks enable skill-vetter-v2
```

## Suggested workflow

1. Open the target skill folder
2. Read `SKILL.md`, `README.md`, scripts, hooks, references, and metadata
3. Run the local helper:
   ```bash
   bash scripts/scan-skill.sh /path/to/target-skill
   ```
4. Write the structured report
5. Optionally verify the final report

## Design intent

The hook is advisory. It does not install, execute, or approve the target skill.
The verdict remains local.
