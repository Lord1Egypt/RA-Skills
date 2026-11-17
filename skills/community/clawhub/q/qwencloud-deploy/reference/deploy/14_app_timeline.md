# Application dossier app_timeline (step 14)

`app_timeline.jsonl` is the application's continuous dossier, kept next to `.qwencloud-deploy`. All
three skills — deploy, observe, operate — append one JSON line to it, stringing together the full
life of an application: deploy, hot updates, each checkup, each recovery action. observe reads it for
recent changes when summarizing; operate reads it to line up with what most recently happened.

---

## Usage

The deploy skill uses this script to write `event=deploy` / `event=hotfix`:

```bash
python3 scripts/append_timeline.py \
  --skill qwencloud-deploy \
  --event deploy \
  --summary "Full-stack deploy done: systemd + Nginx, public 47.x.x.x" \
  --data-json '{"stack_id":"stk-xxx","region":"ap-southeast-1","app_type":"systemd"}'
```

observe / operate are separate skills; each appends one line directly to the same file in the format
below (`event=observe` / `event=operate`), with its own name in the `skill` field.

---

## Record format

One JSON object per line. Common fields:

| Field | Value |
|-------|-------|
| `ts` | Event timestamp (UTC, ISO 8601) |
| `skill` | Writer: `qwencloud-deploy` / `qwencloud-observe` / `qwencloud-operate` |
| `event` | `deploy` / `hotfix` / `observe` / `operate` |
| `summary` | One-line human-readable summary |

Event-specific fields (deploy passes them via `--data-json`; observe / operate write them straight
into the line):

| event | Suggested fields |
|-------|------------------|
| `deploy` | `stack_id`, `region`, `app_type` |
| `hotfix` | `artifact` (updated artifact), `verification` (probe result) |
| `observe` | `score`, `grade`, `fault_layer` (when a fault exists) |
| `operate` | `target`, `action`, `confirmation`, `request_id`, `verification` |

---

## Security

Write redacted read-only information only. **Never** write a password, token, connection string, or
signed URL. The appended file lands at 0600. `record_state.py` already adds `.qwencloud-deploy` /
`.qwencloud-deploy.local` to `.gitignore`; `app_timeline.jsonl` holds no secrets and may be committed
with the project, or ignored at the user's discretion.
