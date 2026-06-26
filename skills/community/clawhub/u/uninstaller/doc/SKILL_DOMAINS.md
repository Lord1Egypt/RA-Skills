# Skill Distribution Domains — Pipeline Registry

High-weight domains for skill distribution. Includes big ecosystems (Vercel, OpenAI, Anthropic, Google, Microsoft) and OpenClaw-specific hubs.

## Domain Registry

### Big Ecosystems (no token / GitHub-based)

| Domain | Weight | Publish Method | CI Secret | Status |
|--------|--------|----------------|-----------|--------|
| **skills.sh (Vercel)** | P0 | GitHub repo — auto-indexed when installed | — | ✅ GitHub = publish |
| **OpenAI Codex** | P0 | PR to openai/skills or $skill-installer | — | Manual PR |
| **Anthropic Claude** | P0 | PR to anthropics/skills, Claude Plugin | — | Manual PR |
| **Google Antigravity** | P0 | Sundial / gemini skills install | — | Via Sundial |
| **GitHub Copilot** | P0 | .github/skills/, .agents/skills/ in repo | — | Repo structure |

### Direct Publish (token required)

| Domain | Weight | Publish Method | CI Secret | Status |
|--------|--------|----------------|-----------|--------|
| **ClawHub** | P0 | `clawhub publish .` | `CLAWHUB_TOKEN` | ✅ Active |
| **Sundial Hub** | P1 | `npx sundial-hub push .` | ❌ No token (interactive only) | 🔲 Local only |
| **SkillCreator.ai** | P1 | Registry (creator approval) | TBD | 🔲 Pending |
| **skr (OCI)** | P1 | `skr push` to ghcr.io | `GITHUB_TOKEN` | 🔲 Pending |

### Discovery / Aggregators (no direct publish)

| Domain | Weight | Notes |
|--------|--------|-------|
| **SkillsMP** | P2 | 425k+ skills, indexes from other sources |
| **AllSkills** | P2 | Anthropic skills directory |
| **UbiTools** | P2 | Anthropic skills hub |

## Details

### skills.sh (Vercel) — 62k+ skills, 205k+ repos
- **Target**: Claude Code, Copilot, Cursor, Cline, 18+ agents
- **Publish**: Public GitHub repo with SKILL.md. No manual publish — `npx skills add owner/repo` installs; installs drive leaderboard ranking
- **Install**: `npx skills add ERerGB/openclaw-uninstall`
- **Docs**: https://skills.sh/docs, https://vercel.com/docs/agent-resources/skills

### ClawHub (clawhub.ai)
- **Target**: OpenClaw users
- **CLI**: `clawhub publish . --slug uninstaller --name "Uninstaller"`
- **Auth**: `clawhub login --token $CLAWHUB_TOKEN --no-browser`
- **Docs**: https://docs.openclaw.ai/clawhub

### Sundial Hub (sundialhub.com)
- **Target**: Claude Code, Cursor, Gemini, Codex CLI, ChatGPT, Copilot, Windsurf
- **Format**: SKILL.md (open standard, compatible)
- **CLI**: `npx sundial-hub auth login && npx sundial-hub push .`
- **Auth**: `sun auth login` — **no --token option** (verified 2026-03). Interactive browser only; CI publish not supported
- **Docs**: https://sundialhub.com/docs

### SkillCreator.ai
- **Target**: Claude, Copilot, Cursor, Codex, Gemini CLI, 10+ runtimes
- **Format**: Agent Skills standard (SKILL.md)
- **CLI**: `npx ai-agent-skills` or `skr` (OCI)
- **Docs**: https://www.skillcreator.ai/

### skr (OCI Registry)
- **Target**: Any agent using OCI registries (ghcr.io, Docker Hub)
- **Action**: `andrewhowdencom/skr@main`
- **Auth**: `GITHUB_TOKEN` for ghcr.io
- **Docs**: https://github.com/andrewhowdencom/skr

### SkillsMP (skillsmp.com)
- **Target**: Discovery/search; aggregates from other sources
- **Publish**: No direct publish; skills may be indexed from GitHub/Sundial
- **Use**: Ensure skill is on ClawHub/Sundial for discoverability

## Token setup

See [TOKEN_SETUP.md](TOKEN_SETUP.md) for step-by-step configuration of each domain's token.

## Pipeline Checklist

- [x] ClawHub: workflow job, CLAWHUB_TOKEN
- [x] skr/OCI: ghcr.io publish (GITHUB_TOKEN auto)
- [x] GitHub Copilot: .github/skills/uninstaller/ + verify job
- [x] Sundial: job skips when SUNDIAL_TOKEN unset
- [x] SkillCreator: job skips when SKILLCREATOR_TOKEN unset (add CLI when docs available)

## Changelog

| Date | Change |
|------|--------|
| 2026-03-11 | Initial registry: ClawHub, Sundial, SkillCreator, skr, SkillsMP |
| 2026-03-11 | Added big ecosystems: skills.sh, OpenAI, Anthropic, Google, Microsoft. Sundial: no token (interactive only) |
