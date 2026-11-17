---
name: skill-validator-omni
description: Validates skills against seven authoring standards across all agents. Use to audit/certify.
version: 2.5.1
author: Adel Ben Yahia (adelpro)
license: MIT
platforms: [linux, macos, windows]
compatibility: Requires Node.js 18+ (yaml package installed via npm).
metadata:
  author: Adel Ben Yahia (adelpro)
  version: 2.5.0
  hermes:
    tags: [skills, validation, standards, audit, cli]
    related_skills: [skill-engineer, hermes-agent-skill-authoring, publishing-skills]
---

# Skill Validator

The compliance gate for agent skills: validates a skill, a plugin, or a whole repo against seven standards in one command. Flagship: **Agent Plugins 1.0.0** (agent-plugins.org) — the open, vendor-neutral spec for packaging Agent Skills and MCP servers into portable plugins, published by a TSC of Core Maintainers from **Amazon, Cursor, Microsoft, OpenAI, and Vercel**. Also enforces the agentskills.io spec, Anthropic best practices, Hermes in-repo standard, OpenAgent skills.sh discoverability, Claude Code marketplace installability, and the OpenAI Codex skill format. Ships as `npx skill-validator-omni` (Node, zero Python deps) and as `scripts/validate.js` for local use.

This is a validation/audit tool. Creation/scaffolding is a secondary workflow — the differentiator is certifying that a skill will install and work across agents, not generating SKILL.md files.

## When to Use

- User asks to "validate", "audit", "check", "lint", or "certify" a skill
- User wants to know if a skill/repo is installable via `npx skills add` or Claude Code
- Before publishing a skill repo to skills.sh or a Claude marketplace
- As a CI gate on a skills repo (exit codes: 0 pass, 1 failed checks, 2 usage error)
- Creating a new skill that must be standards-compliant from day one (scaffold, then validate)

## Don't Use For

- Subjective quality review / multi-agent QA — use skill-engineer (quality gates, Designer/Reviewer/Tester)
- Skill authoring inside the hermes-agent repo itself — use hermes-agent-skill-authoring (repo tests + docs regen)
- Pure creation with no standards concern — `skill-creator` (anthropics/skills) does that

## Prerequisites

- Node.js >= 18 (runs `scripts/validate.js` or the npm CLI)
- Published CLI: `npx skill-validator-omni <dir> [--json]` (fetched from npm; needs only Node)
- Local script: `node scripts/validate.js <dir>` (needs the `yaml` package — the repo's `npm install` covers it)

## What Gets Validated

| Standard | Checks |
|---|---|
| Agent Plugins 1.0.0 | `plugin.json` manifest: canonical `$schema` (`agent-plugins.org/schemas/1.0.0/plugin.schema.json`), name format (1-64, lowercase alnum/hyphen/dot, no `--`/`..`), closed field set (unknown fields flagged), keywords/author typing, `skills/` layout (immediate children), optional `mcp.json` parses |
| agentskills.io spec | name == dir, name format (`[a-z0-9]+(-[a-z0-9]+)*`, <=64, no `--`), description 1-1024, compatibility <=500, allowed-tools typing, body non-empty |
| Anthropic best practices | third-person description, body < 500 lines, progressive disclosure (supporting dirs required above 200 lines) |
| Hermes in-repo | description <=60 + ends with `.`, version/author/license/platforms, metadata.hermes.{tags, related_skills}, required sections |
| OpenAgent skills.sh | discoverable layout (root `SKILL.md`, `skills/` up to 3 levels, agent dirs), every dir name == frontmatter name, well-known index `$schema` |
| Claude Code | `marketplace.json` (JSON + name + plugins), `plugin.json` + `<plugin>/skills/` per plugin, `.claude/skills/` project layout |
| OpenAI Codex | frontmatter limited to `name`/`description`/`license`/`allowed-tools`/`metadata` (mirrors `openai/skills` `quick_validate.py`), hyphen-case name == dir (<=64, no edge/consecutive hyphens), name/desc present, description no angle brackets <=1024 + trigger words (docs guidance), body < 500 lines, no ancillary docs (README/INSTALLATION_GUIDE/QUICK_REFERENCE/CHANGELOG), `agents/openai.yaml` keys (interface/policy/dependencies), repo `.agents/skills`/`.codex/skills`/plugin.json layout |

Every skill discovered in a repo (nested `skills/<category>/<skill>/`) gets the full suite — a broken skill can't hide inside a big repo.

## Installability (what "installable" means)

A skill project passes install checks when it satisfies at least one discoverable layout:

- **Agent Plugins 1.0.0** — portable plugin package: `plugin.json` at the plugin root with `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`; skills in `skills/<name>/SKILL.md` (immediate children, agentskills.io format); optional `mcp.json` for MCP servers. Loadable by compatible clients from Amazon, Cursor, Microsoft, OpenAI, and Vercel ecosystems.
- **`npx skills add <owner/repo>`** (skills.sh CLI) discovers from:
  - `SKILL.md` at repo root (single-skill repo)
  - `skills/<name>/SKILL.md` (container dirs walked up to 3 levels)
  - agent dirs: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.codex/skills/`, `.gemini/skills/`, `.config/opencode/skills/`
  - HTTP publishers: `.well-known/agent-skills/index.json` with `$schema: https://schemas.agentskills.io/discovery/0.2.0/schema.json` (legacy: `.well-known/skills/`)
- **Claude Code** — plugin marketplace: `.claude-plugin/marketplace.json` (name + plugins) at root, added with `/plugin marketplace add <owner>/<repo>` (CLI `claude plugin marketplace add github.com/<owner>/<repo>`), then `/plugin install <plugin>@<marketplace>`; each plugin needs `.claude-plugin/plugin.json` (name) + `<plugin>/skills/<name>/SKILL.md`. Repos with only `.claude/skills/<name>/SKILL.md` auto-discover when Claude Code runs there.
- **OpenAI Codex** — Codex CLI auto-scans `.agents/skills` from the working directory up to the repo root (legacy: `.codex/skills`); distro beyond a local repo goes through Agent Plugins (`plugin.json`, covered above) or `npx skills add <owner>/<repo> -a codex`. Skill frontmatter must match `openai/skills` `quick_validate.py`: only `name`/`description`/`license`/`allowed-tools`/`metadata` allowed.

## Procedure

1. **Validate** — `npx skill-validator-omni <dir>` (or `node scripts/validate.js <dir>`). Read the PASS/FAIL report. Add `-s <standard>` to run one standard (repeatable; `--list-standards` shows names; `--all` is the default).
2. **Fix failures** — each check prints the offending detail; fix frontmatter/structure and re-run until exit 0.
3. **CI gate** — `npx skill-validator-omni <dir> --json | jq -e '.ok'` (JSON report, exit 1 on failure).
4. **Verify installability for publish** — `npx skills add <owner>/<repo> --list -y` must list your skills; for Claude, confirm the marketplace/plugin layouts above.
5. **Scaffold (secondary)** — copy `references/frontmatter-template.md` into a new `SKILL.md`, fill fields, then validate from step 1.

## Common Edge Cases

- **Validating a repo vs a single skill** — point at either; the tool discovers `skills/`, agent dirs, and plugin dirs automatically
- **Skill with no `metadata.hermes`** — Hermes checks fail; that's correct if you publish outside Hermes, but the repo-level skill still gets spec + Anthropic + OpenAgent checks
- **`yaml` package missing** — install deps: `npm install` in the skill-validator-omni repo, or use the published CLI which bundles it
- **Windows** — the npm CLI needs only Node (no python3 requirement)

## Pitfalls

- Treating open-agent.io (the AFK-surf product site) as a standards source — it publishes NO skill spec. The real "open agent" standards are **agent-plugins.org** (Agent Plugins 1.0.0, vendor-neutral, Amazon/Cursor/Microsoft/OpenAI/Vercel) and **skills.sh** (schema at `schemas.agentskills.io`), both enforced by this validator
- Confusing the Agent Plugins manifest with a Claude plugin manifest — Agent Plugins uses root `plugin.json` + `$schema: agent-plugins.org/schemas/1.0.0/plugin.schema.json` (closed field set); Claude uses `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`. Both get checked
- Claiming "installable" without the layout: `npx skills add` discovers root `SKILL.md`, `skills/`, or agent dirs — a skill buried in `examples/` is NOT discoverable; a Claude marketplace needs `.claude-plugin/marketplace.json`, not just plugin code
- Letting the repo copy of `scripts/validate.js` drift from `github.com/adelpro/skill-validator-omni/src/validate.js` — sync after changing either side
- Adding the progressive-disclosure requirement to tiny skills — it only applies above 200 lines
- Expecting one SKILL.md to satisfy both Hermes and Codex frontmatter — Hermes requires `version`/`author`/`platforms`; Codex's closed field set (name/description/license/allowed-tools/metadata) rejects them. The standards conflict by design; the per-standard report shows which side a skill meets, so don't "fix" a Codex flag by deleting Hermes fields (and vice-versa)

## Verification

- `npx skill-validator-omni <dir>` exits 0 with no failures on a compliant skill; report ends with per-standard scores (`[PASS] Agent Plugins 1.0.0: 7/7` etc.)
- JSON mode carries a `standards` array (one object per standard: passed/failed/total/ok) for per-standard CI gating: `jq -e '.standards["Agent Plugins 1.0.0"].ok'`
- `node scripts/validate.js <dir>` on this skill directory passes all checks except the Codex frontmatter restriction — expected: this is a Hermes-flavoured skill, and Hermes requires `version`/`author`/`platforms` fields that Codex's closed field set rejects. The conflict is per-standard by design; run `-s codex` vs `-s hermes` to see each side
- Repo test suite green: `node --test` in `~/projects/skill-validator-omni` (25 tests: spec, OpenAgent, well-known, Claude, Agent Plugins, Codex, fallback parser)
- Broken cases proven: name mismatch → exit 1, invalid marketplace.json → FAIL, missing well-known `$schema` → FAIL, Agent Plugins bad name/missing `$schema`/unknown field → FAIL, Codex unexpected frontmatter field/angle-bracket description/ancillary docs → FAIL
- `scripts/validate.js` matches `github.com/adelpro/skill-validator-omni/src/validate.js`
