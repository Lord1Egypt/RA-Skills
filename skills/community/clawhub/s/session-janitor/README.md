# session-janitor

Automated transcript and session hygiene for [OpenClaw](https://github.com/openclaw/openclaw) gateways.

## What It Does

- **Trims oversized transcripts** — keeps recent exchanges + synthetic compaction summary, archives the rest
- **LLM memory extraction** — uses the gateway's chat completions API to extract structured memories from trimmed content
- **Prunes stale sessions** — removes old subagent/cron session entries from `sessions.json`
- **Archives orphan transcripts** — cleans up files with no active session
- **Sidecar offloader** — extracts large tool outputs (≥5KB) to `.toolcache/` files, replacing them with lightweight stubs
- **Multi-gateway** — auto-discovers all gateway installations (`~/.openclaw/`, `~/.openclaw-*/`)

## Install

```bash
git clone https://github.com/sam-ueckert/session-janitor
cd session-janitor
bash scripts/setup.sh
```

Setup auto-discovers your gateway(s), generates `config.json`, and installs a cron job.

## Configuration

Edit `config.json` after setup:

| Key | Default | Description |
|-----|---------|-------------|
| `trimMaxKB` | 250 | Trim transcripts larger than this |
| `keepPairs` | 10 | Recent user/assistant pairs to keep after trim |
| `archiveRetentionDays` | 7 | Delete old archives after N days |
| `orphanGraceMinutes` | 30 | Wait before archiving orphan transcripts |
| `staleSubagentHours` | 24 | Prune stuck subagent entries older than this |
| `sidecar.enabled` | true | Offload large toolResult entries to `.toolcache/` files |
| `sidecar.minEntryBytes` | 5120 | Minimum toolResult size (bytes) to trigger offload |
| `llmExtraction.enabled` | true | Extract memories from trimmed content via LLM |
| `llmExtraction.maxPerRun` | 1 | Max LLM extractions per cron cycle |
| `memCli.enabled` | false | Store memories via `mem` CLI (requires mem) |
| `cronSchedule` | `*/15 * * * *` | How often to run |

## Manual Run

```bash
bash scripts/janitor.sh
```

## Logs

```bash
tail -f /tmp/session-janitor.log
```

## Requirements

- OpenClaw gateway installed (`~/.openclaw/openclaw.json`)
- Python 3
- `mem` CLI optional (for structured memory storage)

## License

MIT
