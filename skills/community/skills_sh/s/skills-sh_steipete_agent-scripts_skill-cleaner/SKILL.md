---
name: skill-cleaner
description: "Codex/OpenClaw skill audit: live budget, usage, duplicates, compact descriptions."
---

# Skill Cleaner

Use this when trimming skill prompt budget, finding duplicate skills, auditing enabled/disabled skill roots, or deciding which skills/plugins to remove.

## Workflow

1. Run the analyzer from this skill directory or repo root:

```bash
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --months 3
```

Useful variants:

```bash
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --no-logs
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --no-live --no-logs
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --months 6 --max-log-mb 800 --deep-logs
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --context-tokens 272000 --budget-percent 2 --no-logs
node --experimental-strip-types skills/skill-cleaner/scripts/skill-cleaner.ts --root ~/Dropbox/boxd/skills --no-logs
```

2. Read the report in this order:
- `Skill Budget`: live Codex inventory, 2% budget, budgeted usage, and full-description pressure.
- `Description candidates`: long descriptions where relaxed grammar saves prompt budget.
- `Duplicates`: same skill name or near-identical description/body across Codex, plugin cache, repo siblings, and personal skill roots.
- `Unused candidates`: no recent user mention or actual `SKILL.md` read in recent Codex/OpenClaw logs.
- `Root summary`: where skills came from and whether config marks them disabled.

3. Before deleting or editing:
- Verify the kept copy exists and is loaded.
- Prefer deleting repo-local or `agent-scripts` duplicates when Codex built-ins cover them.
- Keep repo-local OpenClaw maintainer skills when they encode repo policy or live operations.
- Preserve trigger nouns in descriptions: product, tool, action, object.

## Analyzer Notes

- By default, `codex debug prompt-input` supplies the exact model-visible skill list, order, names, and aliased paths. `--no-live` forces the broader filesystem fallback.
- The broad filesystem scan remains for duplicate, disabled, and archived-cache diagnostics; it is not treated as the loaded inventory.
- The script mirrors Codex's model-visible line shape: `- name: description (file: path)`.
- It applies Codex-like frontmatter rules: YAML frontmatter only, default name from parent dir, single-line sanitized `name` and `description`.
- It follows Codex `core-skills/src/render.rs`: 2% of raw `context_window`, token cost `ceil(utf8_bytes / 4)`, then full descriptions -> equal description truncation -> omitted minimum lines. Alias-table line cost is included.
- It reads `~/.codex/models_cache.json` for GPT-5.5 `context_window`; fallback is 272,000 tokens and 2%.
- It scans only normal Codex/plugin/repo skill roots by default. Extra folders such as Dropbox archives are included only with `--root <path>`.
- It realpath-dedupes roots, so symlinked roots such as `~/.codex/skills/agent-scripts -> ~/Projects/agent-scripts/skills` do not create false duplicates.
- For duplicate names, it reports description/body similarity and suggests deletion candidates only when bodies are near copies. Keep priority defaults to direct Codex system skills, then direct Codex skills, then plugin skills, then personal/repo copies.
- It scans `~/.codex/history.jsonl` and recent `~/.codex/sessions/**/*.jsonl` by default. Add `--deep-logs` for archived sessions and common OpenClaw/Clawd log folders.
- Usage evidence is heuristic: user `$skill`/`use skill` mentions and paths observed in tool-call arguments.

## Output Policy

- Suggest first; edit only when the user asks.
- If asked to apply cleanup, make small grouped commits: descriptions, deletes, config disables.
- Do not delete ignored/untracked skill dirs without naming the destination or confirming they are disposable.
