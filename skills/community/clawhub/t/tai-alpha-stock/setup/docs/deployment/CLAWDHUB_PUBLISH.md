# Publish to ClawdHub / ClawHub

This repository is a **skill-shaped** layout: root `SKILL.md` is the marketplace entry; the Python package lives in `tai_alpha/`. Publishing uploads the **repository root folder** (the path you pass to `clawdhub publish`).

## What gets uploaded

The ClawdHub CLI (`clawdhub` ≥ 0.3.0) does **not** zip the entire tree blindly. It:

1. **Skips** `.git/`, `node_modules/`, `.clawdhub/`, and anything matched by **`.gitignore`** plus **`.clawdhubignore`** (repo root has both).
2. **Skips** hidden files and directories whose name starts with `.` when walking the tree (so `.cursor/`, `.venv/`, `.env` are not picked up from the walk).
3. **Only includes files** whose extension is on the publisher’s allowlist (e.g. `.md`, `.py`, `.yaml`, `.json`, `.toml`, `.sql`, `.sh` — not `.db`, `.whl`, `.png`, `.pyc`).

So **binaries** under ignored paths (e.g. `dist/`, `build/`, `tai_alpha_output/`, wheels, SQLite DBs) are **not** sent. What *does* go up by default is essentially **source + docs**: `tai_alpha/`, `scripts/`, `setup/`, root `SKILL.md`, `pyproject.toml`, etc.

**Tests:** the `tests/` tree is normal Python and *would* be included unless excluded. This repo’s **`.clawdhubignore`** omits `tests/` so the marketplace bundle stays focused on the runnable skill, not the calibration suite. Remove or edit that line if you intentionally want tests on ClawdHub.

## Prerequisites

- [Node.js](https://nodejs.org/) 20+ (`node -v`).
- A ClawdHub account and a publish token (browser login stores one locally).

**Command name:** the CLI binary is **`clawdhub`** (with a **d**), from the npm package [`clawdhub`](https://www.npmjs.com/package/clawdhub). There is no `clawhub` command — if you see `bash: clawhub: command not found`, use `clawdhub` instead (or install globally: `npm i -g clawdhub undici` — `undici` avoids a common startup error on recent Node).

## One-time authentication

```bash
# Installs CLI + undici into a temp dir (clawdhub 0.3.0 may omit undici; required at runtime)
# Or: npm i -g clawdhub && npm i -g undici   # if your global clawdhub fails to start

clawdhub login
# Headless / CI:
# clawdhub login --no-browser --token 'clh_...'
clawdhub whoami
```

Token file (macOS): `~/Library/Application Support/clawdhub/config.json` (override with `CLAWDHUB_CONFIG_PATH`).

## Publish this repo

From the repository root:

```bash
./setup/tools/clawdhub_publish.sh
```

Optional overrides:

```bash
CHANGELOG="Persona ecosystem, market router, zh-CN/zh-HK reports, SQLite persona_json" \
  ./setup/tools/clawdhub_publish.sh
```

Pass extra `clawdhub publish` flags after `--` if needed:

```bash
./setup/tools/clawdhub_publish.sh -- --no-input
```

The script reads `version` from `pyproject.toml` and sets `--slug tai-alpha-stock` and display name **Tai Alpha Stock**.

## Manual equivalent

```bash
VERSION=$(python3 -c "import pathlib,tomllib; print(tomllib.load(open(pathlib.Path('pyproject.toml'),'rb'))['project']['version'])")
# from a temp npm project with clawdhub + undici installed:
clawdhub publish . \
  --slug tai-alpha-stock \
  --name "Tai Alpha Stock" \
  --version "$VERSION" \
  --changelog "Your release notes"
```

Run the last command with cwd = this repo root (`.`).

## Before every release

See [../../README.md](../../README.md) (section **Pre-publish (ClawHub)**): tests, `check_structure`, wheel build, and keep root `SKILL.md` in sync with [../core/SKILL.md](../core/SKILL.md) frontmatter when you change the skill card.

## Registry URLs

Defaults follow the CLI (`https://clawdhub.com`). Override with `CLAWDHUB_SITE` / `CLAWDHUB_REGISTRY` if your org uses a different registry.

## Troubleshooting

### `Version already exists` (Convex / registry)

ClawdHub stores one immutable release per **`slug` + semver `version`**. If **`1.33.0`** (or whatever is in `pyproject.toml`) is already published for **`tai-alpha-stock`**, republishing the same version is rejected.

**Fix:** bump **`version`** in **`pyproject.toml`** and **`tai_alpha/__init__.py`** together (e.g. patch `1.33.0` → `1.33.1`), then run the publish script again with a new **`CHANGELOG`** describing the delta.

### `Non-error was thrown: "Timeout"` (during `publish`)

The upstream `clawdhub` CLI uses a **15 second** HTTP deadline for API calls, including the **multipart skill upload**. Repositories with many `.py` / `.md` / `.yaml` files often need longer, especially on slower or long‑RTT links.

**`./setup/tools/clawdhub_publish.sh`** patches that deadline to **180 seconds** (and sets Undici `allowH2: false`) inside its **temporary** `node_modules` only — your global `clawdhub` install is unchanged. If you publish manually with `clawdhub publish`, either use the script or apply an equivalent timeout bump in your local `node_modules/clawdhub/dist/http.js` before publishing.

### `[UNDICI-H2] Warning: H2 support is experimental`

Harmless noise on some Node versions. The publish script turns **`allowH2: false`** in the same patched `http.js` to avoid the experimental HTTP/2 path.

### Still timing out

- Try again (transient registry or network).
- Trim the bundle via **`.clawdhubignore`** (already excludes `tests/`).
- As a last resort, temporarily ignore heavier doc trees (e.g. parts of `setup/docs/`) — only if you accept that those files will not appear in the installed skill folder.
