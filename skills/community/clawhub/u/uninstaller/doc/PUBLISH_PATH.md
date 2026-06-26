# Full Publish Path — Uninstaller Skill

Complete checklist for publishing the uninstaller skill across all distribution domains.

**Layout (SSOT)**: Root `SKILL.md` is the single source. `.github/skills/uninstaller/SKILL.md` and `skill-dist/openclaw-uninstall/SKILL.md` are symlinks to it. No sync script; edit root only.

---

## Overview

| Phase | Domains | Trigger | Token |
|-------|---------|---------|-------|
| **Automated (CI)** | ClawHub, ghcr.io | Push to main | CLAWHUB_TOKEN, GITHUB_TOKEN |
| **GitHub-based** | skills.sh | Repo is source | — |
| **Manual** | Sundial | After release | Interactive login |
| **Contribution** | OpenAI, Anthropic | PR when needed | — |

---

## 1. Automated (GitHub Actions)

**Trigger**: Push to `main`

| Job | Domain | Command | Secret |
|-----|--------|---------|--------|
| verify-copilot-skill | GitHub Copilot | diff SKILL.md ↔ .github/skills/ | — |
| publish-clawhub | ClawHub | `clawhub publish .` | CLAWHUB_TOKEN |
| publish-sundial | Sundial | `npx sundial-hub push .` | SUNDIAL_TOKEN (skip if unset) |
| publish-ghcr | ghcr.io (OCI) | `andrewhowdencom/skr` Action | GITHUB_TOKEN (auto) |
| publish-skillcreator | SkillCreator | TBD | SKILLCREATOR_TOKEN (skip if unset) |

**Setup**: Add `CLAWHUB_TOKEN` in repo Settings → Secrets. See [TOKEN_SETUP.md](TOKEN_SETUP.md).

---

## 2. GitHub-based (no action)

### skills.sh (Vercel)

**Publish**: Repo is the source. No manual publish. When users run:

```bash
npx skills add ERerGB/openclaw-uninstall
```

the skill is installed and telemetry drives leaderboard ranking.

**Verify**: Ensure `SKILL.md` at repo root with valid frontmatter (`name`, `description`).

**Link**: https://skills.sh/ERerGB/openclaw-uninstall (after first install)

---

## 3. Manual (after release)

### Sundial Hub

```bash
cd /path/to/openclaw-uninstall
npx sundial-hub auth login   # One-time, opens browser
npx sundial-hub push .       # Run after each release
```

**When**: After tagging a release or when you want to sync to Sundial.

---

## 4. Contribution (optional)

### OpenAI Codex

- Repo: https://github.com/openai/skills
- Action: Open PR to add uninstaller to curated or experimental skills
- When: If you want official Codex visibility

### Anthropic Claude

- Repo: https://github.com/anthropics/skills
- Action: Open PR to add uninstaller
- When: If you want official Claude skills directory

---

## 5. Install Commands (for users)

| Domain | Install command |
|--------|-----------------|
| ClawHub | `clawhub install uninstaller` |
| skills.sh | `npx skills add ERerGB/openclaw-uninstall` |
| GitHub Copilot | Clone repo — skill in `.github/skills/uninstaller/` (symlink) |
| Cursor (personal) | `./scripts/install-personal.sh` — symlink to repo |
| Sundial | `npx sundial-hub add uninstaller` (if published) |
| ghcr.io | `skr install ghcr.io/erergb/openclaw-uninstall:latest` |

---

## 6. Run Full Path Locally

```bash
./scripts/publish-all.sh
```

Runs automated steps (ClawHub if token set) and prompts for manual steps (Sundial).
