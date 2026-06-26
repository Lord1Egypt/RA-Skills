# Skill Hub Token Configuration Guide

Step-by-step instructions for configuring tokens used by the auto-publish pipeline.

---

## 1. ClawHub (CLAWHUB_TOKEN)

**Required for**: OpenClaw skill publishing

### Get the token

1. Open https://clawhub.ai
2. Log in with GitHub
3. Go to **Settings** → **API Tokens**
4. Click **Generate** / **Create CLI token**
5. Copy the token (format: `clh_xxxx...`)

### Configure locally (optional)

```bash
# One-time login (stores token in config)
clawhub login --token "clh_xxxx" --no-browser

# Verify
clawhub whoami
```

Config path: `~/Library/Application Support/clawhub/config.json` (macOS) or `~/.config/clawhub/config.json` (Linux)

### Configure GitHub Actions

1. Repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Name: `CLAWHUB_TOKEN`
4. Value: paste your `clh_xxxx` token

---

## 2. Sundial Hub (SUNDIAL_TOKEN)

**Target**: Claude Code, Cursor, Gemini, Codex CLI, ChatGPT, Copilot, Windsurf

### Verified: No token support (2026-03)

```bash
$ npx sundial-hub auth --help
Commands: login, logout, status

$ npx sundial-hub auth login --help
# No --token, --no-browser, or env var options
```

**Conclusion**: Sundial only supports interactive browser login. **CI auto-publish not possible** with current CLI.

### Workaround: Local publish only

```bash
cd /path/to/openclaw-uninstall
npx sundial-hub auth login   # Opens browser, one-time
npx sundial-hub push .       # Publish manually after releases
```

---

## 3. skr / OCI Registry (GITHUB_TOKEN)

**Target**: ghcr.io, any OCI-compatible agent

### Configuration

**No extra secret needed.** The default `GITHUB_TOKEN` is automatically provided to workflows. To publish to ghcr.io:

1. Use the `andrewhowdencom/skr` GitHub Action
2. Set `registry: ghcr.io`, `username: ${{ github.actor }}`, `password: ${{ secrets.GITHUB_TOKEN }}`
3. Ensure the workflow has `contents: write` if pushing packages

---

## 4. SkillCreator.ai

**Target**: Claude, Copilot, Cursor, Codex, Gemini CLI, 10+ runtimes

### Current status

- Creator program: https://www.skillcreator.ai/creators/apply
- Apply with name, email, GitHub username
- No public token/CI docs found

### Next steps

1. Apply as a creator
2. After approval, check their dashboard/docs for API token or CLI auth
3. Add a `SKILLCREATOR_TOKEN` secret when available

---

## Domains that need no token

| Domain | Why |
|--------|-----|
| **skills.sh (Vercel)** | GitHub-based. Install: `npx skills add ERerGB/openclaw-uninstall`. Repo is auto-indexed when users install. |
| **OpenAI Codex** | Contribute via PR to github.com/openai/skills |
| **Anthropic** | Contribute via PR to github.com/anthropics/skills |
| **GitHub Copilot** | Skills in `.github/skills/` or `.agents/skills/` — repo structure |

## Quick reference (token-required)

| Domain      | Secret name     | Where to get it                          |
|-------------|-----------------|------------------------------------------|
| ClawHub     | `CLAWHUB_TOKEN` | clawhub.ai → Settings → API Tokens       |
| Sundial     | —               | No token; interactive login only          |
| skr/ghcr.io | `GITHUB_TOKEN`  | Auto-provided by GitHub Actions          |
| SkillCreator| TBD             | After creator approval                   |

---

## Verify pipeline

After adding secrets:

1. Push to `main` (or manually trigger the workflow)
2. Check **Actions** → **Publish Skills**
3. `publish-clawhub` should succeed if `CLAWHUB_TOKEN` is set
4. `publish-sundial` skips if `SUNDIAL_TOKEN` is empty; runs if set
