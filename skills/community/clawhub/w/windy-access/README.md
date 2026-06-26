# Windy Access — ClawHub skill

The ClawHub-distributable skill that wires an OpenClaw install into the
Windy ecosystem in one command.

## Schema (verified 2026-05-20 against ClawHub `https://clawhub.ai`)

The previous version of this folder shipped a hand-rolled `skill.json` with
invented fields (`hooks`, `requirements.binaries`, `writes.files`,
`providers`, `providerBaseUrls`). **None of those are valid ClawHub
fields.** Verified by inspecting the OpenClaw runtime in
`~/.local/lib/node_modules/openclaw/dist/` and downloading a real
published skill (`golang-cli@1.2.0`) from ClawHub's API.

ClawHub skills are **markdown files with YAML frontmatter**, packaged
as a ZIP archive with `SKILL.md` at the root. The canonical schema:

```yaml
---
name: <slug>                                # kebab-case, ^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$
description: <one-line summary>             # used for ClawHub's vector search
user-invocable: true | false                # whether `claw skill <slug>` invokes it
license: MIT | Apache-2.0 | ...
compatibility: <free-text>                  # describes target runtime + project
metadata:
  author: <handle>                          # publisher's handle
  version: "<semver>"                       # string, must be quoted in YAML
  openclaw:                                 # openclaw-specific sub-namespace
    emoji: <emoji>
    homepage: <url>
    requires:
      bins:                                 # binary deps the agent must have
        - <bin-name>
    install: []                             # post-install hooks (array)
allowed-tools: <space-separated Claude tools the skill may use>
---

<skill body in markdown — this is what the agent reads at invocation>
```

Plus an optional `_meta.json` at the archive root, but ClawHub manages
that server-side (it stores `ownerId`, `slug`, `version`, `publishedAt`).
Don't ship `_meta.json` in the source repo.

## Archive layout (what gets uploaded)

```
windy-access-0.1.0.zip
├── SKILL.md          # required, root level, must contain YAML frontmatter
├── README.md         # optional, used as the skill's hub page on clawhub.ai
├── assets/           # optional, auxiliary files the skill references
└── evals/            # optional, eval cases (evals/evals.json)
```

ClawHub's archive root marker is `SKILL.md` (or `skill.md`, `skills.md`,
`SKILL.MD` — case-tolerant). The skill installer fails with "archive is
missing SKILL.md" if it's not at the archive root.

## ClawHub API reference (from runtime inspection)

| Endpoint | Method | Purpose |
|---|---|---|
| `https://clawhub.ai/api/v1/skills` | GET | List/search skills (supports `?q=`, `?limit=`) |
| `https://clawhub.ai/api/v1/skills/<slug>` | GET | Skill detail (returns `{skill, latestVersion, metadata, owner}`) |
| `https://clawhub.ai/api/v1/download?slug=<slug>&version=<version>` | GET | Download archive as ZIP (returns `application/zip`) |

The publish API endpoint is not exposed in OpenClaw's bundled client
(the runtime only consumes, doesn't publish). Publishing is done via
the ClawHub web UI at https://clawhub.ai or via a `clawhub` CLI (not
shipped with OpenClaw, distributed separately).

Auth: `Authorization: Bearer <token>` from `CLAWHUB_TOKEN` env or
`~/.config/clawhub/config.json` (`auth.token` / `accessToken` / etc.).

## Publish flow

```bash
# 1. Validate SKILL.md locally
#    (validator exists in OpenClaw runtime; expose via `claw skill validate` once available)
test -f SKILL.md
head -1 SKILL.md | grep -q "^---$"   # frontmatter check

# 2. Build the archive
zip -r windy-access-0.1.0.zip SKILL.md README.md  # add assets/ + evals/ if present

# 3. Publish (web UI today; CLI when available)
open https://clawhub.ai
# → drag the zip into the publisher UI
# → set slug=windy-access, version=0.1.0, license=MIT
# → submit
```

Once live, users see it at https://clawhub.ai/skills/windy-access and
install with `claw skill add windy-access` (or via the OpenClaw UI).

## Schema delta (what changed from the pre-verification draft)

| Old `skill.json` field | Verified replacement |
|---|---|
| `name` | `name` in YAML frontmatter (top-level) |
| `displayName` | derived from `name` by ClawHub; not in the skill itself |
| `version` | `metadata.version` (must be quoted in YAML — string, not number) |
| `description` | `description` in YAML frontmatter |
| `author` (object) | `metadata.author` (string handle) |
| `homepage` | `metadata.openclaw.homepage` |
| `license` | `license` in YAML frontmatter |
| `keywords`, `categories` | **not used** — ClawHub uses vector search over `description` |
| `providers`, `providerBaseUrls`, `providerAuthEnvVars`, `api` | **not a skill concern.** Providers live in OpenClaw plugin manifests (`openclaw.plugin.json`), which is a different shape entirely. If we ever want Windy Mind to appear as a built-in OpenClaw provider, that's a separate `openclaw-plugin-windy-mind` package, not part of this skill. |
| `hooks` (install/uninstall/status) | `metadata.openclaw.install` array. Note: ClawHub skills don't have uninstall hooks — the agent is expected to undo work via runtime knowledge. We rely on `windy disconnect` being callable from the skill body. |
| `requirements.binaries` | `metadata.openclaw.requires.bins` |
| `writes.files`, `writes.marker-blocks-in` | **not a schema field.** Documented in the skill body markdown instead — agents read it to know what files they'll touch. |

## What's still verifiable later

- **`allowed-tools` syntax** — confirmed against `golang-cli` example
  (space-separated tool names, parameterized via `Bash(go:*)` etc.). The
  exact grammar isn't documented in OpenClaw's bundle; conservatively
  list every tool the skill might invoke.
- **`install: []` array semantics** — empty in every published example I
  inspected; the field exists but its element shape isn't documented.
  For now we drive install via `windy connect` from the skill body, not
  via this array.
- **Eval cases (`evals/evals.json`)** — present in golang-cli's archive
  but the schema isn't documented. Defer until ClawHub publishes a
  schema; meanwhile, ship without evals/.

## Companions

- The CLI itself: `pipx install windy-connect` (PyPI publishing flow per
  [docs/pypi-setup.md](../../docs/pypi-setup.md)) or
  `curl get.windyconnect.com | sh`
- Bundle spec: [docs/bundle-spec-v1.md](../../docs/bundle-spec-v1.md)
- ADR-052 (two-tier access): [docs/adr/](../../docs/adr/)
