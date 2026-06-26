# sync-notes

> End-to-end encrypted, bidirectional sync between a local notes vault (Obsidian, plain Markdown, anything really) and a **Cloudflare R2** bucket — powered by [`rclone`](https://rclone.org/) `bisync` over an `rclone crypt` remote.

This is an [OpenClaw](https://openclaw.ai) skill, but the heavy lifting is just a pair of bash scripts. You can use them outside of OpenClaw without modification.

[简体中文](./README.zh-CN.md)

---

## Why?

- 🔒 **Zero-trust storage.** Your notes are encrypted client-side via `rclone crypt`. Cloudflare only ever sees ciphertext blobs with encrypted filenames.
- 🔁 **Real bidirectional sync.** `rclone bisync` propagates additions, modifications and deletions in both directions, with conflict markers when both sides changed.
- 📱 **Mobile-friendly.** The crypt format is compatible with the [Remotely Save](https://github.com/remotely-save/remotely-save) Obsidian plugin, so your phone can sync the same bucket without holding the rclone config.
- 🧰 **Self-contained.** All paths derive from the script location. No daemons, no extra services — just `bash` + `rclone`.
- 🛟 **Backups before writes.** Every write-side run mirrors the local vault to `backups/latest/` first.

---

## Layout

```
sync-notes/
├── SKILL.md                      # OpenClaw skill manifest (also the design doc)
├── README.md / README.zh-CN.md   # this file
├── config/
│   ├── rclone.conf.example       # template for the rclone remotes
│   ├── rclone.conf               # your real config (gitignored, chmod 600)
│   ├── .env.example              # template for non-rclone settings
│   ├── .env                      # your real settings  (gitignored, chmod 600)
│   └── filter.txt                # rclone filter rules (excludes .obsidian/, .DS_Store, etc.)
├── scripts/
│   ├── setup.sh                  # interactive configuration wizard
│   └── sync.sh                   # main entry point / dispatcher
├── state/                        # rclone bisync workdir (gitignored)
├── logs/                         # per-run + master logs   (gitignored)
└── backups/                      # rolling local snapshots (gitignored)
```

---

## Requirements

- `bash` 4+
- [`rclone`](https://rclone.org/install/) **v1.65+** (older builds lack some `bisync` flags used here)
- A [Cloudflare R2](https://developers.cloudflare.com/r2/) bucket and an S3-compatible API token scoped to it
- A passphrase (and optional salt) for the `crypt` remote — **lose this and the data is unrecoverable**

---

## Quick start

```bash
# 1. Clone the repo somewhere
git clone https://github.com/jiangsier-xyz/jiangsier-skill-sync-notes.git
cd jiangsier-skill-sync-notes

# 2. Tell the script where your notes live
export CLOUD_NOTES_PATH=/absolute/path/to/your/vault

# 3. Run the wizard — fills in rclone.conf and .env (chmod 600)
./scripts/setup.sh

# 4. Sanity check
./scripts/sync.sh status

# 5. First-time baseline (must do this once before bisync will run)
./scripts/sync.sh init

# 6. Routine bidirectional sync from now on
./scripts/sync.sh
```

> 💡 **Putting `CLOUD_NOTES_PATH` in your shell rc (`.zshrc` / `.bashrc`) is the most painless option.**

---

## Subcommands

| Command | Behaviour |
|---|---|
| `sync.sh setup` | Run the wizard. Idempotent — confirms before overwriting existing config. |
| `sync.sh init [--force]` | First-run baseline (`rclone bisync --resync`). Refuses to run if a baseline already exists. |
| `sync.sh bisync` (default) | Bidirectional sync with conflict reporting. Backs up locally first. |
| `sync.sh download <glob> [--dry-run]` | Pull files matching `<glob>` from the remote into the local vault. Backs up first. |
| `sync.sh upload <glob> [--dry-run]` | Push files matching `<glob>` to the remote. |
| `sync.sh status` | Show config validity, last-sync info, conflicts, backup state. |

`<glob>` is passed to `rclone --include` and applies to **plaintext** paths (after decryption). A bare keyword like `welcome` is broadened to `**welcome**` automatically; pre-wildcarded globs (`ideas/**`, `*.md`) pass through unchanged.

---

## Conflict handling

`bisync` runs with `--conflict-suffix conflict1,conflict2`. After every run, the script scans the vault for `*.conflict1*` / `*.conflict2*` files. **If any are found, the script exits non-zero and prints the list — the LLM/human is expected to resolve them manually before the next sync.** No silent automatic merging.

---

## Configuration files

### `config/rclone.conf`

Two remotes:

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
filename_encoding = base64        # match Remotely Save (rclone default is base32)
directory_name_encryption = true
password = <OBSCURED via `rclone obscure`>
password2 = <OBSCURED via `rclone obscure`>   # optional
```

### `config/.env`

```sh
RCLONE_REMOTE=notes                       # crypt remote name
BACKUP_KEEP=1                             # rolling local backup count
RCLONE_EXTRA_FLAGS="--transfers=4 --checkers=8"
```

### `config/filter.txt`

`rclone` filter rules. The shipped defaults exclude `.obsidian/`, `.DS_Store`, `Thumbs.db`, swap files and Office lock files — adjust to taste.

---

## Required environment

| Variable | Purpose | Required |
|---|---|---|
| `CLOUD_NOTES_PATH` | Absolute path of the local notes directory | ✅ |

The script aborts immediately with a clear message if `CLOUD_NOTES_PATH` is unset, missing, or not a directory.

---

## Remotely Save interop

The `crypt` settings above are deliberately tuned to match Remotely Save's defaults:

- `filename_encryption = standard`
- `filename_encoding = base64`
- `directory_name_encryption = true`
- Same passphrase (and salt, if you set one)

With those aligned, your phone (Remotely Save) and your desktop (this skill) can safely sync to the same R2 bucket.

---

## OpenClaw integration

When dropped into an OpenClaw workspace, this skill is triggered by:

```
/sync-notes              → bisync
/sync-notes setup        → wizard
/sync-notes init         → baseline
/sync-notes status       → status
/sync-notes 下载 welcome  → download '**welcome**'
/sync-notes upload daily/*.md
```

See [`SKILL.md`](./SKILL.md) for the full natural-language → subcommand mapping that the LLM is expected to follow.

---

## Safety notes

- **Never commit `config/rclone.conf` or `config/.env`** — they're in `.gitignore`, but double-check before pushing.
- **Never commit `backups/`** — it contains a verbatim copy of your vault. Also gitignored.
- The `crypt` passphrase is the only thing standing between Cloudflare and your plaintext notes. Back it up offline.
- `bisync` is powerful and can delete on both sides. Use `--dry-run` and `status` liberally on the first few runs.

---

## License

MIT. See [`LICENSE`](./LICENSE) if present.
