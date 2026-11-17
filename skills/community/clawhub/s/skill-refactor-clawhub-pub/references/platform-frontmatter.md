# Platform frontmatter field matrix

The same skill is consumed by different hosts, and the frontmatter schema differs.
Do **not** invent fields a host does not recognize. Use this matrix to pick the
fields for the target platform, then keep the published skill in the host-neutral
core (`name`, `description`, `when_to_use`) plus that platform's additions.

## Verified conclusion (online, 2026-10-11)

SKILL.md is the **"Agent Skills" open standard** published by Anthropic; one
SKILL.md is read by 20+ agents. Two format families actually coexist:

1. **OpenClaw-native (the common format)** — `metadata.openclaw.*` (requires /
   primaryEnv / os / install / …). Used by OpenClaw, Hermes, WorkBuddy,
   CodeBuddy, Trae, Kimi Code, Z-code, Agnes Code, Qoder, Cursor, 千问办公,
   百度搭子 (all Agent-Skills-standard implementors that adopt OpenClaw's
   packaging + scanner). "Most use the OpenClaw format" — **confirmed**.
2. **Claude extensions (a separate, host-specific set)** — `allowed-tools`,
   `context: fork`, `hooks`, `disable-model-invocation`, `user-invocable`,
   `argument-hint`, `agent`, `model`, `effort`. Claude Code adds these on top of
   the standard core; they are **safely ignored** by hosts that don't support
   them. "Claude uses another format" — **confirmed, as an extension layer, not
   a competing standard.**

Cross-agent portability rule (agensi.io): for max portability, publish only
`name` / `description` / `when_to_use` + plain markdown body; agent-specific fields
are ignored, not errors.

## Core fields (every platform)

| Field | Required | Notes |
|---|---|---|
| `name` | yes | lowercase hyphen slug; ≤64 chars; the stable trigger key |
| `description` | yes | what it does + when to use + NOT-for; primary trigger surface; ≤1024 chars |
| `when_to_use` | recommended | explicit triggers + explicit non-triggers |
| `tags` | recommended | discovery keywords |
| `summary` | recommended | one-line plain-English abstract for UI |

## Per-platform field matrix (14+ agents)

Legend: **core** = core-fields set; **OpenClaw** = `metadata.openclaw.*` package
fields; **Claude-ext** = Claude extension fields; **CN-review** = domestic content
red lines apply (千问办公 / 百度搭子 / SkillHub).

| # | Platform | Format family | Extra fields to add | Notes |
|---|---|---|---|---|
| 1 | Claude Code | core + Claude-ext | `allowed-tools`, `context: fork`, `hooks`, `disable-model-invocation`, `user-invocable`, `argument-hint`, `agent`, `model`, `effort` | the reference implementation of the standard |
| 2 | Codex CLI | core | `when_to_use`, `tags` | Agent-Skills standard reader; no OpenClaw metadata |
| 3 | OpenClaw | core + OpenClaw | `metadata.openclaw.*` (see Host B) | scanner-clean packaging; `license: MIT-0` default |
| 4 | Hermes | core + OpenClaw | `metadata.openclaw.*` | OpenClaw-ecosystem host |
| 5 | WorkBuddy | core + OpenClaw | `metadata.openclaw.*` | also honors Claude-ext when run via Claude runtime |
| 6 | CodeBuddy | core + OpenClaw | `metadata.openclaw.*` | OpenClaw-ecosystem host |
| 7 | Trae | core (full Agent-Skills impl) | `.trae/skills/` dir; `when_to_use` | implements the open standard end-to-end |
| 8 | Kimi Code | core + OpenClaw | `metadata.openclaw.*` | CN host |
| 9 | Z-code | core + OpenClaw | `metadata.openclaw.*` | CN host |
| 10 | Agnes Code | core + OpenClaw | `metadata.openclaw.*` | CN host |
| 11 | Qoder | core + OpenClaw | `metadata.openclaw.*` | CN host |
| 12 | Cursor | core | partial `when_to_use`; ignores OpenClaw metadata | uses `.cursor/skills` or AGENTS.md bridge |
| 13 | 千问办公 (Qwen Office) | core + CN-review | CN content red lines; no VPN/"科学上网" wording | domestic review gate |
| 14 | 百度搭子 (Baidu Dazi) | core + CN-review | CN content red lines | domestic review gate |

> If a host is not in this table, default to **core fields only** — that set is the
> portability floor that every Agent-Skills reader honors.

## Host A - Claude / WorkBuddy (host-side, extension layer)

These fields are honored by the Claude/WorkBuddy runtime, **not** by the ClawHub
OpenClaw scanner. They are optional and host-specific; document them per host, do
not force them into a ClawHub-published package.

| Field | Meaning |
|---|---|
| `allowed-tools` | whitelist of tools the skill may use |
| `context: fork` | run the skill in a forked context, keeping the main conversation clean |
| `disable-model-invocation` | forbid auto-triggering; user may still invoke by name |
| `user-invocable` | allow the user to invoke by name |
| `environment` / `network` | self-declared scope, for human trust |

## Host B - ClawHub / OpenClaw (published, scanner-visible)

The scanner reads `metadata.openclaw`. Declaration must match behavior; a code
reference that is not declared is flagged as a mismatch.

| Field | Meaning |
|---|---|
| `metadata.openclaw.requires.bins` | binaries that must all exist |
| `metadata.openclaw.requires.env` | required environment variables |
| `metadata.openclaw.requires.anyBins` | at least one of these must exist |
| `metadata.openclaw.requires.config` | config files the skill reads |
| `metadata.openclaw.primaryEnv` | the main credential variable |
| `metadata.openclaw.os` | supported OS list |
| `metadata.openclaw.install` | how to install deps (brew / node / go / uv) |
| `metadata.openclaw.always` | always-active skill |
| `metadata.openclaw.homepage` / `emoji` / `skillKey` / `nix` | metadata |
| `license: MIT-0` | default license; use only if there is no proprietary content |

> For a skill that ships an offline Python linter (this skill): declare
> `requires.bins: [python3]`, leave `env: []` and `config: []` empty, and set
> `license: MIT-0`. That is the minimal, accurate, scanner-clean declaration.

## Host C - SkillHub (Chinese domestic registry)

| Field | Meaning |
|---|---|
| `license` | keep `MIT` / `MIT-0` for GitHub-synchronized distribution |
| `displayName` | human-facing name |
| content red lines | domestic content review; avoid VPN / "scientific上网"-style wording (see the publish gate) |

## Decision rule

1. Identify the **publish target** (ClawHub / SkillHub / Claude-WorkBuddy / GitHub).
2. Start from the core fields (Host A section's "Core fields" table).
3. Add only that target's additions (Host B / Host C rows).
4. Never merge host-specific fields into a platform's published schema; if a field
   is needed by one host only, keep it in that host's copy, not the neutral package.
