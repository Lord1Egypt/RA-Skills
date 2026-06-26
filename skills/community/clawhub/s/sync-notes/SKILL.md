---
name: sync-notes
description: Sync the local Obsidian vault with a Cloudflare R2 bucket using rclone (S3 + crypt). Triggered by `/sync-notes`. Defaults to bidirectional sync; understands natural-language flags for partial download/upload by glob.
version: 1.0.1
metadata:
  {"openclaw":{"emoji":"☁️","requires":{"bins":["rclone","bash"],"env":["CLOUD_NOTES_PATH"]}}}
---

# sync-notes Skill

Sync the local notes directory (`$CLOUD_NOTES_PATH`) with a **Cloudflare R2** bucket through an
end-to-end encrypted **rclone crypt** remote. The skill is a thin orchestrator over a single bash
entry point at `scripts/sync.sh`; the LLM's job is to translate the user's natural-language intent
into the right subcommand.

## Trigger

Activate **only** when the user message starts with `/sync-notes` (with or without trailing
arguments). Examples:

| User message | Intent | Action |
|---|---|---|
| `/sync-notes` | full bidirectional sync | `sync.sh bisync` |
| `/sync-notes setup` | run the configuration wizard | `sync.sh setup` |
| `/sync-notes init` | establish the bisync baseline (first run only) | `sync.sh init` |
| `/sync-notes status` | show config + last-sync info | `sync.sh status` |
| `/sync-notes 下载 welcome` | download files matching `welcome` | `sync.sh download '**welcome**'` |
| `/sync-notes upload daily/*.md` | upload glob | `sync.sh upload 'daily/*.md'` |
| `/sync-notes 把 ideas 目录拉下来` | download a directory | `sync.sh download 'ideas/**'` |

## How to interpret natural language

After stripping the `/sync-notes` prefix, classify the remainder:

1. **Empty** → run `bisync` (default bidirectional sync).
2. Contains a recognised keyword:
   - `setup`, `配置`, `wizard` → `setup`
   - `init`, `初始化`, `baseline` → `init`
   - `status`, `状态`, `信息` → `status`
3. Mentions **download** intent (`下载`, `拉`, `pull`, `download`, `get`, `取回`):
   - Extract the target token(s) and convert to a glob (see "Glob rules" below).
   - Run `sync.sh download '<glob>'`.
4. Mentions **upload** intent (`上传`, `推`, `push`, `upload`, `send`):
   - Same as above with `sync.sh upload '<glob>'`.
5. Otherwise: ask the user to clarify; do not guess.

### Glob rules

Globs are passed verbatim to rclone as `--include` filters and apply to *plain* (decrypted) paths.

- A bare keyword such as `welcome` becomes `**welcome**` (matches anywhere in path).
- A directory name like `ideas` becomes `ideas/**`.
- Paths already containing wildcards (`*`, `?`, `[`) are passed through unchanged.
- Filenames without extension default to matching `<name>` and `<name>.md`; combine with `**` if
  unsure. When in doubt, run `sync.sh download '<glob>' --dry-run` first.

## Workflow contract

1. **First run ever:** the script refuses `bisync` until a baseline exists. Tell the user to run
   `/sync-notes init` after confirming both sides are in the desired starting state.
2. **Backups:** before any write-side operation (`bisync`, `download`, `init`), the local notes
   directory is mirrored to `backups/latest/` (single rolling copy, previous one is replaced).
3. **Conflicts:** bisync runs with conflict markers. After every run the script scans for
   `*.conflict*` files; if any are found the script exits non-zero and lists them. **Surface this
   list to the user verbatim and ask which side to keep**—do not auto-resolve.
4. **Logs:** every invocation appends to `logs/sync.log` and emits a per-run file
   `logs/<UTC-timestamp>.log` for the rclone output.

## Filesystem layout

```
skills/sync-notes/
├── SKILL.md                  # this file
├── README.md                 # short user-facing notes (optional)
├── config/
│   ├── rclone.conf           # active rclone config (created by setup, gitignored)
│   ├── rclone.conf.example   # template
│   ├── .env                  # non-rclone settings (created by setup, gitignored)
│   └── .env.example          # template
├── scripts/
│   ├── sync.sh               # main entry point (dispatcher)
│   └── setup.sh              # interactive configuration wizard
├── state/
│   └── bisync/               # rclone bisync workdir (listings + lockfiles)
├── logs/                     # rolling logs
├── backups/
│   └── latest/               # most recent local snapshot (single copy)
└── .gitignore
```

`scripts/sync.sh` derives every path from its own location (`$(dirname "$0")/..`); no absolute
paths are hard-coded.

## Required environment

| Variable | Purpose | Required |
|---|---|---|
| `CLOUD_NOTES_PATH` | absolute path of the local notes directory | ✅ |

The script aborts early with a clear message if `CLOUD_NOTES_PATH` is unset, missing, or not a
directory.

## Configuration files

### `config/rclone.conf`

Native rclone format with **two remotes**:

```ini
[r2-raw]
type = s3
provider = Cloudflare
access_key_id = <ACCESS_KEY_ID>
secret_access_key = <SECRET_ACCESS_KEY>
endpoint = https://<ACCOUNT_ID>.r2.cloudflarestorage.com
acl = private

[notes]
type = crypt
remote = r2-raw:<BUCKET>/<OPTIONAL_PREFIX>
filename_encryption = standard
directory_name_encryption = true
password = <OBSCURED>
password2 = <OBSCURED>
```

### `config/.env`

Non-rclone settings consumed by `sync.sh`:

```sh
# Name of the crypt remote in rclone.conf
RCLONE_REMOTE=notes
# Number of local backup snapshots to retain
BACKUP_KEEP=1
# Extra rclone flags (optional)
RCLONE_EXTRA_FLAGS="--transfers=4 --checkers=8"
```

`.example` versions ship with the skill; the wizard fills in the real values.

## Subcommands implemented by `sync.sh`

| Subcommand | Behaviour |
|---|---|
| `setup` | Run `setup.sh`; collects R2 creds + crypt password(s); writes `rclone.conf` and `.env` with `chmod 600`. Idempotent: confirms before overwriting. |
| `init` | First-time baseline: `rclone bisync --resync`. Refuses to run if a baseline already exists unless `--force` is passed. |
| `bisync` (default) | `rclone bisync $LOCAL notes:` with conflict reporting. Backs up first. |
| `download <glob>` | `rclone copy notes: $LOCAL --include '<glob>'`. Backs up first. Defaults to `--dry-run` only when the user said "试" / "dry"; otherwise runs for real. |
| `upload <glob>` | `rclone copy $LOCAL notes: --include '<glob>'`. No local backup needed; remote is authoritative. |
| `status` | Prints config validity, last-sync timestamp, conflict files (if any), backup state. |

## Safety rules for the LLM

- **Never** write secrets into chat. If the user pastes secrets, immediately move them into
  `config/rclone.conf` / `config/.env` and remove from any visible context.
- **Never** invoke `rclone` with `--config` pointing somewhere outside this skill.
- **Never** run `bisync` if `status` reports unresolved conflicts; ask first.
- When `download`/`upload` glob match count is ambiguous, run with `--dry-run` first and show the
  list of matches.
- Backups are single-copy; if you are about to do something risky (large delete, schema change),
  copy `backups/latest/` to `backups/manual-<UTC>/` manually before proceeding and tell the user.

## First-time onboarding (what to tell the user)

```
1. /sync-notes setup           # fill in R2 + crypt creds
2. export CLOUD_NOTES_PATH=...  # point at the local notes dir
3. /sync-notes init             # establish the bisync baseline
4. /sync-notes                  # routine bidirectional sync
```
