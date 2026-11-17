# Recordings, the archive and ingestion

The core rules in [SKILL.md](../SKILL.md) apply.

## Cloud recordings

`zm personal recordings list --json` and `recordings show` inspect cloud assets. Prefer occurrence UUIDs for
recurring meetings. Attending a meeting does not grant recording API access.

## Download

`zm personal recordings download --since-time <date> --until-time <date> --output-dir <dir> --jsonl` archives
bounded history. With a meeting ID instead of the date bounds, `download` handles one occurrence.

- Use `--json` for a bounded receipt list or `--jsonl` to retain completed receipts after a later failure.
- Existing files are never overwritten. Repeated runs skip verified manifest entries; completed files survive later
  failures.
- Interrupted transfers resume a verified prefix only when a strong validator and the returned byte range agree;
  changed representations restart safely. `--no-resume` uses ephemeral partials.
- Keep the account, the profile and the archive destination consistent.

## The local archive

- `recordings archive check <dir> --offline` verifies local checksums.
- Inspect `recordings archive locks` before `recordings archive recover`; recovery previews stale local dead-process
  locks, and `--yes` removes only authorized ones.
- `zm personal search recordings <dir> 'budget'` and `recordings archive transcript <dir>` verify VTT before
  reading and need no login or store. Archive search is literal and case-insensitive and returns shared search
  hits. `page.has_more` requires a larger limit or a narrower query; there is no cursor. Transcript reads support
  `--uuid`/`--file-ids`.
- Archive reads do not import.

## Import

- `recordings archive import <dir> --offline --jsonl` validates the entire selection before atomic per-occurrence
  appends. Byte limits bound both files and total input.
- Unknown start times require an existing occurrence; corrected revisions and pull cursors are preserved.
- Receipts acknowledge completed appends; optional exact counts distinguish creation, replay and correction.
- Legacy folder imports use `meetings import`; cloud archive assets use `recordings archive import`.

## Profiles and the store

- A profile is one Zoom login and its stored meetings; an import or sync naming an unknown profile beside others is
  refused, so never invent a profile name. Reads require existing profile data and do not register profiles.
- `MESSAGING_STORE` selects an explicit database. Store opens preserve legacy `messages.db` files and sidecars; manage
  their retention separately.
- Serialize ingestion for an account. `meetings sync --lookback-days` revisits late transcripts.

## Export

`meetings export <id> --format markdown|vtt` needs `--output` to write and never overwrites; VTT needs an unambiguous
current transcript or an explicit transcript id.

## Watch

`zm personal watch api` or `watch files <folder>` runs in the foreground with `--jsonl`; each cycle closes its store.
Restart to change captured profile or source settings. `--since-time` is the initial API bound until a cursor write
succeeds; overlap applies to that bound and later cursors. Stop with Ctrl-C. `--timeout` bounds finite commands;
`watch` and MCP serving are foreground lifetimes.
