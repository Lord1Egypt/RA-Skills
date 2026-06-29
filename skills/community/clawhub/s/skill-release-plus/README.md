# skill-release-plus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Multi-hub skill publisher** for the OpenClaw / skill-creator ecosystem.
Sign → Pack → Publish to `clawhub.com`, `skillhub.cn` (Tencent Cloud), and
GitHub Releases — all in one command. Pluggable adapter framework lets you
target any custom hub via a user-hook script.

```bash
# One command, three hubs:
python3 scripts/release.py --slug my-skill -m "ship it" --version 1.0.0 --target all
```

---

## Why this exists

The skill ecosystem now has multiple registries:

- **[clawhub.com](https://clawhub.com)** — community-driven, npm CLI
- **[skillhub.cn](https://skillhub.cn)** — Tencent Cloud, multipart HTTP API
- **GitHub Releases** — open-source / monorepo native distribution
- **Your own hub** — internal corporate skill hub, private mirror, etc.

Each has its own auth, protocol, packaging rules, and rate limits. Publishing
the same skill to all of them by hand means: sign once → pack manually for
each → upload via 3 different CLIs → forget which version went where → drift.

This skill does **single source of truth** packaging + **fan-out** publishing,
with adapter independence (each hub adapter is a separate Python module).

---

## Features

- ✅ **Multi-hub fan-out**: `--target clawhub,skillhub-cn,github-release` (or `all`)
- ✅ **Single packaging pass**: one signing, one `exclude.json`, one tar.gz, N targets
- ✅ **Pluggable user hooks**: bring your own hub via `--target user-hook:./my-script.sh`
- ✅ **Rate-limit aware**: skillhub-cn 429 auto-retry with backoff
- ✅ **Per-target token validation**: `--check` flag previews readiness without publishing
- ✅ **Dry-run mode**: sign + pack, skip upload (no API calls, no state changes)
- ✅ **Stdlib-only (PyYAML optional)**: no `pip install` needed for the happy path
- ✅ **GitHub monorepo support**: `owner/repo/subdir` for `skills/` subfolder layouts
- ✅ **4-layer config**: CLI > env > project `.env` > global `~/.config/.env`
- ✅ **Fail-open dispatch**: one target's failure does not block others
- ✅ **Owner self-service cleanup helpers**: `unlist`+`delete` for accidental publishes (skillhub-cn)

---

## Quick start

```bash
# 1. Clone or install
git clone https://github.com/Songhonglei/build-better-skills.git
cd build-better-skills/skills/skill-release-plus

# Or via clawhub:
clawhub install skill-release-plus

# 2. Set tokens (any subset is fine — only checked for selected targets)
export SRP_CLAWHUB_TOKEN=clh_xxx       # for clawhub
export SRP_SKILLHUB_CN_TOKEN=skh_xxx   # for skillhub.cn
export SRP_GITHUB_TOKEN=ghp_xxx        # for GitHub Releases

# 3. Verify readiness
python3 scripts/release.py --check --target all

# 4. Dry-run first (no API calls)
python3 scripts/release.py \
    --slug my-skill \
    --version 1.0.0 \
    -m "first release" \
    --target all \
    --dry-run

# 5. Publish for real
python3 scripts/release.py \
    --slug my-skill \
    --version 1.0.0 \
    -m "first release" \
    --target all
```

---

## Configuration

See [SKILL.md](./SKILL.md#configuration) for the full env var table.

The most common setup is to drop a `~/.config/skill-release-plus/.env` file:

```bash
SRP_CLAWHUB_TOKEN=clh_xxx
SRP_SKILLHUB_CN_TOKEN=skh_xxx
SRP_GITHUB_TOKEN=ghp_xxx
SRP_DEFAULT_TARGETS=clawhub,github-release
SRP_GITHUB_OWNER=YourName
```

---

## Architecture

```
release.py (dispatcher)
  ├─ _lib_config.py         (4-layer config + parse_targets)
  ├─ _lib_package.py        (sign / pack / exclude / multipart)
  ├─ _lib_adapters_base.py  (BaseAdapter ABC)
  └─ _adapter_*.py:
       ├─ clawhub          (CLI wrap)
       ├─ github-release   (git + GitHub REST API)
       ├─ skillhub-cn      (Tencent Cloud HTTP/multipart)
       └─ user-hook        (subprocess + JSON envelope)
```

Adapter pattern: each adapter subclasses `BaseAdapter` and implements
`publish()`, `check_slug_available()`, `inspect()`. The dispatcher iterates
over selected targets and aggregates per-target results into a JSON report.

---

## Writing a custom adapter

For a new hub, create `_adapter_my_hub.py`:

```python
from _lib_adapters_base import BaseAdapter, PublishResult

class MyHubAdapter(BaseAdapter):
    target_name = "my-hub"

    def publish(self, slug, version, changelog, tar_path, skill_dir, extra=None):
        # ... your HTTP / CLI / git logic ...
        return self._ok(slug=slug, version=version, url="https://my-hub/skills/...")
```

Or for a one-off, use `--target user-hook:./script.sh` (see [SKILL.md](./SKILL.md#writing-a-custom-adapter-user-hook)).

---

## Supported targets

| Target | Protocol | Auth |
|---|---|---|
| `clawhub` | CLI (`clawhub publish`) | `SRP_CLAWHUB_TOKEN` or `clawhub login` |
| `skillhub-cn` | HTTP multipart POST | `SRP_SKILLHUB_CN_TOKEN` (Bearer) |
| `github-release` | Git + REST API | `SRP_GITHUB_TOKEN` (PAT, `repo` scope) |
| `user-hook:<path>` | Subprocess + JSON envelope | Your script defines it |

> **Note**: `cn.clawhub-mirror.com` (ByteDance Volcano) is a **read-only mirror** of clawhub.com and is not a separate target. Publishing to clawhub auto-syncs to the mirror.

---

## Contributing

Issues and PRs welcome at <https://github.com/Songhonglei/build-better-skills>.

When adding a new adapter:

1. Create `scripts/_adapter_<hub>.py` subclassing `BaseAdapter`
2. Add the target name to `VALID_TARGETS` in `_lib_config.py`
3. Register it in `release.py`'s `ADAPTER_REGISTRY`
4. Add token env var to the table in SKILL.md
5. Add an end-to-end test (real network OK; use cheap throwaway slugs)

---

## License

MIT — see [LICENSE](./LICENSE). When published to clawhub.com, the platform
enforces MIT-0 license metadata on the hub mirror (`PLATFORM_SKILL_LICENSE`
constant); your original repo license is unchanged.

---

## Author

Evan Song — <https://github.com/Songhonglei>
