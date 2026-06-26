---
name: weread-to-flomo
description: Sync WeRead (微信读书) highlights and notes into flomo with incremental deduplication and configurable sync scope. Use when the user wants to export or sync WeRead annotations to flomo, including (1) only today's new highlights, (2) a specified date, or (3) a full migration of all exported notes. Supports configurable tag templates, local state tracking, and Markdown-based intermediate storage.
---

# weread-to-flomo

Use this skill to move WeRead highlights/notes into flomo safely.

## Default workflow

1. Export WeRead notes into local Markdown files first.
2. Set `FLOMO_WEBHOOK` and `WEREAD_COOKIE` via environment variables or config files outside the skill package.
3. Choose one sync scope:
   - `today`: only today's new entries
   - `date`: entries from a specified day
   - `all`: full migration
4. Use local state tracking to avoid duplicate pushes.
5. Run `--dry-run` before the first real sync or before a bulk migration.
6. Prefer `today` or `date` mode when the user already has historical reading notes in flomo.

## Modes

### 1. Sync today's new entries

```bash
python3 ./scripts/weread_to_flomo.py --weread-dir /path/to/weread --mode today --flomo-webhook "$FLOMO_WEBHOOK" --dry-run
python3 ./scripts/weread_to_flomo.py --weread-dir /path/to/weread --mode today --flomo-webhook "$FLOMO_WEBHOOK"
```

### 2. Sync a specified date

```bash
python3 ./scripts/weread_to_flomo.py --weread-dir /path/to/weread --mode date --date 2026-03-26 --flomo-webhook "$FLOMO_WEBHOOK"
```

### 3. Full migration

```bash
python3 ./scripts/weread_to_flomo.py --weread-dir /path/to/weread --mode all --flomo-webhook "$FLOMO_WEBHOOK"
```

## Sync scopes

- `today`: sync only entries whose WeRead timestamp falls on the current Asia/Shanghai day.
- `date`: sync only entries from `--date YYYY-MM-DD`.
- `all`: migrate all exported entries.

## Tag template

Default output:

```text
内容正文

#02_读书 #02_读书/「书名」
```

Override with:

```bash
--tag-prefix "02_读书"
```

## State and dedup

- State file defaults to `.weread-flomo-state.json` under the WeRead export directory.
- Dedup uses `bookmark:<id>` / `review:<id>`.
- Re-running the same scope only sends unsent entries.

## Notes

- Keep webhook/cookie outside the skill directory.
- Dry-run on first use.
- If the user already manually copied many old notes into flomo, prefer `today` or `date` mode before `all`.

## References

- Read `references/formatting.md` when adjusting output structure or tag conventions.
- Read `references/publishing.md` when preparing the skill for ClawHub publication.
