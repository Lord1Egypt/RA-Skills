# skill-hub-query

Query, install, update, and edit AI agent skills on any compatible Skill Hub —
self-hosted, or any Hub that implements the documented API contract — with a
single, predictable CLI. Plus a built-in adapter for the public
[skillhub.cn](https://skillhub.cn) hub.

- **License**: MIT
- **Author**: Evan Song (<https://github.com/Songhonglei>)
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite (Install stage)

> **Heads-up**: for the generic-contract mode this tool does NOT target
> [clawhub.ai](https://clawhub.ai) — that Hub has its own API surface and an
> official `clawhub` CLI. Use generic mode for a private/compatible Hub, or use
> the built-in `skillhub_cn` provider for skillhub.cn.

## Two ways to use it

### 1. Generic contract (self-hosted / compatible Hub)

Point it at any Hub implementing the [API contract](SKILL.md#self-hosted-hub-api-contract):

```bash
export SKILL_HUB_URL="https://hub.your-company.com"
export SKILL_HUB_TOKEN="<your-token>"   # optional; without it, public-only fallback

bash scripts/sync.sh                    # refresh local cache
bash scripts/query.sh keyword calendar  # search
bash scripts/query.sh slug some-skill   # detail
bash scripts/install.sh some-skill --yes
bash scripts/edit.sh some-skill --summary "New summary"   # if your Hub supports /edit
bash scripts/team.sh list 42 --json                          # team members (if your Hub has /team)
bash scripts/doctor.sh                  # diagnose configuration
```

Dual-channel: with a token it uses the authenticated API (full features incl.
private skills); without a token it falls back to the unauthenticated channel
(public skills only).

### 2. Built-in provider: skillhub.cn

[skillhub.cn](https://skillhub.cn) is a China-optimized public hub. Activate the
adapter — no token needed:

```bash
export SKILL_HUB_PROVIDER=skillhub_cn

bash scripts/query.sh keyword code            # search (live)
bash scripts/query.sh today                   # browse newest
bash scripts/query.sh slug skill-creator      # detail
bash scripts/query.sh versions skill-creator  # version history
bash scripts/install.sh skill-creator --yes   # install
bash scripts/doctor.sh                         # capability matrix
```

When `SKILL_HUB_PROVIDER` is set, `SKILL_HUB_URL` / token are ignored and the
adapter targets `https://api.skillhub.cn`.

#### skillhub.cn capability matrix

| Operation | Supported? |
|---|---|
| Search / browse / detail / versions / install | ✅ live, public, no token |
| `sync.sh` | ⚪ no-op (live search needs no cache) |
| `query.sh author <handle>` | ❌ no author filter (use `keyword`) |
| `edit.sh` (edit card metadata) | ❌ card metadata is a one-way mirror from upstream clawhub/GitHub; change the upstream source and re-publish instead |
| `team.sh` (team management) | ❌ no team endpoints on skillhub.cn |

## Security

- Skill slugs are validated (`validate_slug`) before use in URLs or filesystem
  paths — path-traversal (`..`), absolute paths, and illegal characters are
  rejected.
- Downloaded archives are checked for ZIP magic bytes and unsafe entry paths
  (`..`, absolute paths) before extraction, and every extraction target is
  re-resolved to confirm it stays inside the staging directory.
- Extraction runs through `scripts/_zip_safe.py` (Python `zipfile`) rather than
  `unzip`, so non-ASCII filenames survive intact — see
  [SKILL.md](SKILL.md#requirements).
- `install.sh` resolves the version from the Hub's version-history API (never
  from a possibly stale local cache) and verifies the downloaded package's own
  declared version before replacing anything on disk.
- `--yes` is a **user-authorization flag**; an agent must not add it on its own.
- Never commit tokens to git or echo full tokens.

## Configuration

See [`SKILL.md`](SKILL.md#configuration) for the full environment-variable table
and the [self-hosted Hub API contract](SKILL.md#self-hosted-hub-api-contract).
For the detailed endpoint/field reference, see
[`references/api.md`](references/api.md).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
