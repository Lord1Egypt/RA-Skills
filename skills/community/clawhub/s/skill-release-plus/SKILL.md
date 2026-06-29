---
name: skill-release-plus
description: >
  Multi-hub skill publisher. Sign → Audit (placeholder) → Pack (clean tar.gz with
  exclude rules) → Publish to clawhub.com, skillhub.cn (Tencent Cloud), or
  GitHub Releases, all in one command. Pluggable adapter framework — add your
  own hub via a user-hook script (subprocess + JSON envelope). Single source of
  truth: one exclude.json, one signing pass, one package, fan out to N targets.
  Default target: clawhub only. Use --target all for all three real hubs, or
  --target user-hook:./my-script.sh for custom destinations. Triggers on:
  publish skill, release skill, push to skill hub, ship skill to multiple hubs,
  发布 skill, 上传到 clawhub, 发布到 skillhub.cn.
---

# skill-release-plus

**Version**: 1.0.3  
**Author**: Evan Song <[github.com/Songhonglei](https://github.com/Songhonglei)>
**Repo**: <https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus>
**License**: MIT (this repo) — clawhub mirror auto-uses MIT-0 (platform-enforced)  
**Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

Sign → Pack → Publish to **multiple skill hubs in one command**. Supports
`clawhub.com`, `skillhub.cn` (Tencent Cloud), `GitHub Releases`, and any
custom hub via a user-hook script.

---

## Quick start

```bash
# Default: publish to clawhub only
python3 scripts/release.py --slug my-skill -m "first release" --version 1.0.0

# Publish to all three real hubs at once
python3 scripts/release.py --slug my-skill -m "ship it" --version 1.0.0 --target all

# Custom hub via user hook
python3 scripts/release.py --slug my-skill -m "v1" --version 1.0.0 \
    --target user-hook:/path/to/my-publish.sh

# Check token readiness before publishing
python3 scripts/release.py --check --target all

# Dry-run (sign + pack, skip publish)
python3 scripts/release.py --slug my-skill -m "test" --version 1.0.0 --dry-run

# Inspect current exclude rules
python3 scripts/release.py --show-exclude
```

---

## Supported targets

| Target | Status | Auth | Notes |
|---|---|---|---|
| `clawhub` | ✅ | `SRP_CLAWHUB_TOKEN` (env) or `clawhub login` | Wraps the [clawhub CLI](https://www.npmjs.com/package/clawhub) |
| `skillhub-cn` | ✅ | `SRP_SKILLHUB_CN_TOKEN` (env) | Tencent Cloud — POST `/api/v1/community/skills/publish` (multipart). Rate-limit 3 publish/min/token. **Auto-retries on 429.** |
| `github-release` | ✅ | `SRP_GITHUB_TOKEN` (env) | Pure `git` + GitHub REST API (no `gh` CLI required). Supports `owner/repo[/subdir]` for monorepo layouts. |
| `user-hook:<path>` | ✅ | Hook-defined | Your script receives metadata via env vars + JSON stdin, returns `{"ok": true, "url": "..."}` on stdout |

> **Not supported**: `cn.clawhub-mirror.com` (ByteDance Volcano) is a **read-only public mirror** of clawhub.com — publishing to clawhub automatically syncs there. There is no separate publish endpoint.

---

## Installation

```bash
# Install Python 3.8+ (standard library only, no pip install needed)
git clone https://github.com/Songhonglei/build-better-skills.git
cd build-better-skills/skills/skill-release-plus

# Or install via clawhub:
clawhub install skill-release-plus
```

**Dependencies**:
- Python 3.8+ (standard library only — `urllib`, `subprocess`, `tarfile`, `json`, `argparse`, `dataclasses`, `pathlib`)
- `git` 2.x (for `github-release` target only)
- `clawhub` CLI (for `clawhub` target only — auto-detected from `$PATH`)
- `skill-sign` (optional — for content signing; skipped if not installed)
- `PyYAML` (optional — improves SKILL.md frontmatter parsing for edge cases; stdlib fallback handles `description: "..."` single-line and `description: >` folded scalar without it)

---

## Configuration

Resolution priority (highest → lowest):

1. **CLI args** (`--slug`, `--target`, `--version`, etc.)
2. **Process env vars** (`SRP_*` private namespace)
3. **Project-local `./.env`**
4. **Global `~/.config/skill-release-plus/.env`**
5. **Missing required key → onboarding prompt** (interactive)

### Environment variables (all `SRP_*` prefixed)

| Variable | Required for | Description |
|---|---|---|
| `SRP_CLAWHUB_TOKEN` | clawhub target | clawhub API token (or run `clawhub login`) |
| `SRP_SKILLHUB_CN_TOKEN` | skillhub-cn target | Tencent skillhub.cn personal token (starts with `skh_`) |
| `SRP_GITHUB_TOKEN` | github-release target | GitHub PAT with `repo` scope |
| `SRP_GITHUB_OWNER` | github-release (optional) | Default repo owner (defaults to authenticated user) |
| `SRP_GITHUB_REPO` | github-release (optional) | Default repo name (defaults to slug) |
| `SRP_GITHUB_BRANCH` | github-release (optional) | Default branch (default: `main`) |
| `SRP_GITHUB_BASIC_AUTH_HEADER` | github-release (optional) | If `true`, use HTTP Basic Auth header instead of URL-embedded token |
| `SRP_DEFAULT_TARGETS` | optional | Comma-separated default target list (default: `clawhub`) |
| `SRP_OUTPUT_DIR` | optional | Package output directory (default: `<cwd>/output/skill-release`) |
| `SRP_SIGN_OPTIONAL` | optional | If `true`, skip signing when `skill-sign` not installed (default: `true`) |
| `SRP_SIGN_SCRIPT` | optional | Explicit path to `sign.py` (overrides auto-detection of `skill-sign`) |

---

## Architecture

```
release.py (dispatcher, 352 LOC)
  ├─ _lib_config.py         (4-layer config + parse_targets, 289 LOC)
  ├─ _lib_package.py        (sign / pack / exclude rules / multipart, 305 LOC)
  ├─ _lib_adapters_base.py  (BaseAdapter ABC, 98 LOC)
  └─ _adapter_*.py:
       ├─ clawhub          (CLI wrap, 185 LOC)
       ├─ github-release   (git + GitHub REST API, 392 LOC)
       ├─ skillhub-cn     (Tencent Cloud HTTP/multipart, 308 LOC)
       └─ user-hook       (subprocess + JSON envelope, 140 LOC)
```

**Design principles**:

- **Single source of truth**: One `config/exclude.json`, one signing pass, one tar.gz, fan out to N targets
- **Adapter independence**: Each adapter is a separate Python module subclassing `BaseAdapter`; no cross-adapter coupling
- **Fail-open by default**: One target failing does not block others (dispatcher reports per-target status)
- **Protocol-agnostic base**: BaseAdapter doesn't assume HTTP / multipart / git — adapters own their protocol

---

## Writing a custom adapter (user-hook)

Create an executable script:

```bash
#!/bin/bash
# my-publisher.sh
set -e

# Hook receives:
#   $SRP_HOOK_SLUG, $SRP_HOOK_VERSION, $SRP_HOOK_CHANGELOG,
#   $SRP_HOOK_TAR_PATH, $SRP_HOOK_SKILL_DIR, $SRP_HOOK_DISPLAY_NAME

curl -sf -F "package=@$SRP_HOOK_TAR_PATH" \
     -F "version=$SRP_HOOK_VERSION" \
     "https://my-private-hub.example.com/publish"

# Print JSON envelope on stdout for the dispatcher to parse
echo '{"ok": true, "url": "https://my-private-hub.example.com/skills/'"$SRP_HOOK_SLUG"'"}'
```

Then invoke:

```bash
chmod +x my-publisher.sh
python3 scripts/release.py --slug my-skill -m "v1" --version 1.0.0 \
    --target user-hook:./my-publisher.sh
```

---

## Exclude rules

Default `config/exclude.json` strips:

- VCS: `.git`, `.svn`, `.hg`
- IDE: `.idea`, `.vscode`, `.DS_Store`, `Thumbs.db`
- Build artifacts: `__pycache__`, `*.pyc`, `node_modules`, `dist`, `build`
- Secrets: `.env`, `.secrets`, `*.pem`, `*.key`, `.token`
- Test/dev: `tests/__pycache__`, `.pytest_cache`, `.tox`
- See full list: `python3 scripts/release.py --show-exclude`

---

## Command reference

```
usage: release.py [-h] [--slug SLUG] [--changelog CHANGELOG]
                  [--version VERSION] [--display-name DISPLAY_NAME]
                  [--skill-dir SKILL_DIR] [--target TARGET] [--dry-run]
                  [--show-exclude] [--check]

options:
  -h, --help            show this help message and exit
  --slug SLUG           skill slug (lowercase, digits, hyphens)
  --changelog, -m       release changelog
  --version VERSION     explicit version (semver); default: auto-bump patch
  --display-name        human-readable display name (default: slug)
  --skill-dir SKILL_DIR  path to skill source directory (default: ./<slug>)
  --target TARGET       comma-separated targets, or "all". Default: clawhub.
                        Special: user-hook:<path> for custom hooks.
  --dry-run             sign + pack but skip publish
  --show-exclude        print current exclude rules and exit
  --check               check token readiness for selected targets
```

Exit codes:
- `0` — all targets succeeded
- `1` — at least one target failed (others may have succeeded)
- `2` — invalid arguments or config error

---

## Triggers

This skill should be used when the user says:

- "publish skill X to clawhub / skillhub.cn / GitHub"
- "ship my skill to multiple hubs"
- "release X.Y.Z of my skill"
- "发布 skill 到 clawhub"
- "把 skill 推到 skillhub.cn"
- "skill 同时发到三个 hub"
- "用 user-hook 发到我自己的 hub"

---

## Limitations

- **`skillhub-cn` rate limit**: 3 publish/minute/token. Dispatcher waits and retries on 429.
- **`github-release` requires explicit `--version`**: No auto-tag-bump (would require parsing existing tags reliably across owner/repo combos).
- **`skillhub-cn` requires `description`** in SKILL.md frontmatter (≤1024 bytes). YAML folded (`>`) scalar is supported.
- **No rollback**: If 2/3 targets succeed and 1 fails, you must manually clean up the 2 successes or accept partial state.

---

## License

MIT (this repo). See `LICENSE`.

Note: when this skill is published to clawhub.com, the platform enforces MIT-0
license metadata on hub mirror — original repo MIT license is unchanged.
