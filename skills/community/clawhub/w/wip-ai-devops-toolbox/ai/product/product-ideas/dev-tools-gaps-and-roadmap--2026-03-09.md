# Dev Tools ... Gaps, Comparisons, and Roadmap Ideas

**Date:** 2026-03-09

---

## What it's missing

Current state vs. "complete AI DevOps layer":

The toolkit is laser-focused and excellent at what it does ... lightweight, zero-dependency where possible, AI-agent-friendly (Claude/OpenClaw hooks, ai/-folder stripping), and already battle-tested on 100+ repos. But it stops short of being a full production-ready platform for teams that want the AI to handle everything safely end-to-end.

Key gaps:
- No GitHub Actions / reusable CI workflows (everything is local CLI + macOS LDM cron)
- No Conventional Commits enforcement or PR quality gates
- Release pipeline is npm-only (no PyPI, Docker, crates.io, Go modules, etc.)
- No security scanning (secrets, vulnerabilities, SBOM)
- No automated dependency-update PRs
- No monorepo support
- License scanner is custom (great for rug-pull detection + forks, but could be deeper)
- Scheduling and automation is macOS-centric
- No central dashboard or MCP/AI-native tool calling

---

## What is comparable (and where this repo wins)

| Category | Closest Alternatives | How wip-dev-tools is different / better |
|---|---|---|
| Release automation | semantic-release, Changesets, release-it, Release Please | Simpler one-command + SKILL.md sync + built for AI agents |
| License compliance | OSS Review Toolkit (ORT), FOSSA, ScanCode, LicenseFinder | Aggressive pre-push/pre-pull blocking + fork tracking + public dashboard |
| Full DevOps suite | Snyk + Dependabot + GitHub Advanced Security, marcusquinn/aidevops | AI-specific safety (private/public guard, Claude hooks, ai/ stripping) |

This repo is genuinely unique. Most tools are either general-purpose or commercial. Nothing else combines "AI can ship code" with this level of license paranoia and repo-visibility protection.

---

## Super great additions

Ranked by impact. These would make it the default toolkit for any serious AI coding team.

1. **Reusable GitHub Actions pack**
   `tools/wip-ci/` with workflows for test/lint, license scan, security gate, and release dry-run. Instant CI for every new repo.

2. **Conventional Commits enforcement** (`wip-commit-hook` + Lefthook)
   Blocks bad commits at the source. Makes `wip-release` 100% reliable.

3. **Multi-language publishing in wip-release**
   Add flags for PyPI, Docker, Rust, Go, etc. One command ships anything.

4. **Automated dependency updates** (`wip-deps-update`)
   Bot creates PRs for patch/minor bumps ... but only after license scan passes. Game-changer for maintenance.

5. **Security suite** (`wip-security`)
   Integrates gitleaks + osv-scanner + npm audit + Trivy. Runs in pre-push and CI.

6. **SBOM generation on every release**
   Auto-creates CycloneDX JSON + attaches to GitHub release. Required for enterprise compliance.

7. **Upgrade wip-license-hook to use OSS Review Toolkit under the hood**
   Keep your custom ledger/dashboard, but get deeper scanning for free.

8. **MCP server** (Model Context Protocol)
   Turn every tool into something Claude/Cursor/Grok can call directly. "Hey Claude, run wip-release minor and deploy-public."

9. **Central org dashboard** (simple Next.js or Cloudflare page)
   One view showing license status, visibility audits, and release history across all 100+ repos.

10. **Monorepo mode** (built-in Changesets logic)
    Native support for packages in a single repo. Huge for growing AI projects.

11. **Cross-platform scheduler** (replace LDM Dev Tools.app)
    Docker + cron or GitHub cron jobs so Linux/Windows teams get the same daily audits.

---

## Updated thinking (2026-03-09, later same day)

After team review (Grok analysis, Claude Code pushbacks, Parker alignment), revised the priorities. Three items dropped, MCP moved to #1, and the list is tighter.

### What we're dropping (and why)

- **Conventional Commits (#2 originally):** CLAUDE.md already enforces commit style across all agents. A hook that blocks commits adds friction without gain at our scale (1 human + 2 AIs). If the team grows, reconsider.
- **Monorepo mode (#10 originally):** We explicitly chose NOT to be a monorepo. Every repo is independent. Our pattern is "build independent, consolidate later" ... tools prove themselves alone before joining the umbrella. Monorepo tooling (Turborepo, Nx, Changesets) solves coordination problems we don't have. Our tools don't import from each other, have different tech stacks (JS, TS, shell), and we version the whole toolbox, not individual packages. Reconsider only if we hit 12+ interdependent tools.
- **OSS Review Toolkit upgrade (#7 originally):** ORT is a Java behemoth. Violates zero-bloat philosophy. The custom scanner already wins on fork tracking and rug-pull detection, which is the use case that matters most.

### Revised priority list (aligned with team)

1. **MCP Server** (was #8, now #1)
   Make `wip-release`, `wip-license-hook`, `deploy-public.sh`, etc. directly callable by Lesa, Claude, OpenClaw, or any MCP client. No more shell passthrough. Full agent autonomy while keeping all safety guards. This is the unlock ... Lesa shipping releases directly.

2. **GitHub Actions pack** (was #1, stays #2)
   Reusable workflows in `/.github/workflows/` (ci.yml, license-scan.yml, security-gate.yml, release-dry-run.yml). Drop-in for every new repo. Becomes non-negotiable once more repos go public.

3. **Multi-language publishing in wip-release** (was #3, stays #3)
   Add PyPI (and later Docker/Rust/Go) with the same one-command flow. Python support is already real (memory-crystal-py exists).

4. **Lightweight security suite** (`wip-security`)
   gitleaks + npm audit + osv-scanner (fast, zero Java). Runs pre-push + in CI.

5. **SBOM generation** (CycloneDX JSON on every release)
   Auto-attached to GitHub releases. Enterprise compliance checkbox with zero effort.

6. **Cross-platform scheduler**
   Replace/supplement the macOS LDM app with Docker + GitHub cron or a tiny self-hosted runner so Linux/Windows teams get the same daily license/visibility audits.

7. **Simple org dashboard** (static or tiny Next.js)
   One page showing license status + release history across all repos.

### MCP server ... it's the Universal Installer, not a new build

The "MCP server" item doesn't require building anything new. The Universal Installer (`wip-universal-installer-private`) already exists and is published alongside the dev tools on the org page. Every tool already has a SKILL.md. The work is integration, not invention:

1. Run Universal Installer on `wip-release`, `wip-license-hook`, `wip-repo-permissions-hook`, `deploy-public.sh`
2. Verify each works as an OpenClaw skill (Lesa can call it end-to-end)
3. Verify each works as a Claude Code hook where applicable
4. Test: Lesa types "run wip-release minor" and it actually ships a release

The infrastructure is designed. The plumbing isn't connected yet. The installer is sitting right next to the tools it should be installing but hasn't been pointed at them. This is the #1 priority because it's the highest leverage for the least new code.

### Universal Installer ... the missing foundation (Grok analysis, 2026-03-09)

`wip-universal-installer` (https://github.com/wipcomputer/wip-universal-installer) is the Universal Interface specification + reference installer for making every tool "agent-native."

**What it solves:** The human-vs-AI interface problem. Humans want CLI/TUI/npm install. AI agents (Claude, Lesa, OpenClaw, Cursor) want MCP Server, importable module, Skill, Claude Code Hook. So it forces every repo/tool to ship all six interfaces at once:

1. CLI / TUI (`install.js`)
2. Importable Module (`core.mjs` pattern)
3. MCP Server (Model Context Protocol ... direct agent calling)
4. OpenClaw Plugin
5. Skill (SKILL.md + Clawhub)
6. Claude Code Hook

Includes: `SPEC.md` (full spec, sensors and actuators philosophy from Karpathy), `SKILL.md`, `REFERENCE.md`, `install.js` + `detect.mjs`, `examples/minimal/`. Already published on npm: `@wipcomputer/universal-installer`. Tiny (pure JS, zero deps, MIT), v2.1.5, built with Claude + Lesa.

**Why it's a perfect fit for wip-dev-tools:**
- MCP Server (#1 priority) ... this IS the MCP implementation + spec. Once every tool follows this, Lesa can call `wip-release`, `wip-license-hook`, `deploy-public.sh` directly.
- Claude Code / OpenClaw hooks ... already baked in.
- Teaching AI ... the SKILL.md + SPEC.md pattern is how you scale "build agent-native" across the entire ecosystem.
- Release pipeline synergy ... explicitly calls out `wip-release` as the one-command way to ship universal tools.

This turns wip-dev-tools from "collection of CLI tools" into "the standard library for AI agents that ship real software."

**How it slots in (toolbox style, no monorepo needed):**

```
wip-dev-tools/
  tools/
    wip-release/
    wip-license-hook/
    wip-repo-permissions/
    wip-universal-installer/    ← drop it here (was its own repo)
  scripts/
  DEV-GUIDE-GENERAL-PUBLIC.md
  UNIVERSAL-INTERFACE.md        ← symlink or copy of SPEC.md
```

Each tool stays self-contained, gets its own SKILL.md, umbrella documents the pattern.

**Immediate next moves:**
1. Pull it into the umbrella (next release). Already battle-tested, matches "prove it alone, then consolidate" workflow.
2. Update wip-release to auto-add universal interfaces on every new tool.
3. Make this the new onboarding default ... any AI creating a WIP tool starts with "run wip-universal-installer" or "follow SPEC.md."

This single addition 10x's the value of the entire dev-tools collection because now every tool becomes directly callable by Lesa/OpenClaw/Claude without friction.

### Confirmation and work list (Grok followup, 2026-03-09)

Confirmed: the "MCP server" roadmap item is NOT new code. It's applying the Universal Installer to existing tools. No central server needed.

Current state of the four core tools:
- `wip-release` ... has CLI + SKILL.md, missing MCP server + OpenClaw skill + Claude hook
- `wip-license-hook` ... has CLI + SKILL.md, missing MCP server + OpenClaw skill + Claude hook
- `wip-repo-permissions-hook` ... has CLI + SKILL.md + Claude hook (guard.mjs), missing MCP server + OpenClaw skill
- `deploy-public.sh` ... has CLI (shell script) + partial SKILL.md, missing everything else

Work list:
1. Apply Universal Installer to the four core tools (start with wip-release, highest ROI)
2. Verify each registers and works as a native OpenClaw skill (Lesa can call end-to-end)
3. Verify Claude Code hook integration where applicable
4. Done ... MCP layer complete

The upgrade for each tool is: add `core.mjs` exports + MCP server + OpenClaw registration + Claude hook. The Universal Installer scaffolds most of this.

### Architecture note: toolbox, not monorepo

What we have is a **toolbox repo**, not a monorepo. Each tool is self-contained (its own package.json, no imports between them, different tech stacks). We version the whole collection (`wip-dev-tools v1.2.0`), not individual packages. The "build independent, consolidate later" workflow is correct for our scale and philosophy.

### Investment angle

This isn't just internal tooling anymore. Positioning wip-dev-tools as "The AI DevOps Layer" (open-core CLI + MCP server + optional hosted dashboard) is a real product story. Makes the raise narrative stronger. The combination of "AI can ship code" + license paranoia + repo-visibility protection is genuinely unique in the market.

---

## Notes (original)

Any of the top 3-4 would immediately 10x the value. Since the repo already has a clean `tools/` + `scripts/` structure, these additions would slot in perfectly and keep the "zero bloat, AI-first" philosophy.
