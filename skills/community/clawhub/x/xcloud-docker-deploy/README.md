# xCloud Docker Deploy Skill

> **For AI Agents:** Let users say, "This is my project. I want to deploy it on xCloud." Then confirm the intended scope, inspect the project only with consent, choose native or Docker deployment, generate the right files, and guide the xCloud deploy in plain language.

[![Version](https://img.shields.io/badge/version-1.4.1-blue)](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![SkillsMP](https://img.shields.io/badge/SkillsMP-listed-purple)](https://skillsmp.com)
[![ClawHub](https://img.shields.io/badge/ClawHub-published-orange)](https://clawhub.ai/Asif2BD/xcloud-docker-deploy)
[![Platforms](https://img.shields.io/badge/platforms-Claude%20Code%20%7C%20Codex%20%7C%20OpenClaw%20%7C%20Cursor-lightgrey)](#install)

---

## Start Here

Use normal human language:

```text
This is my project. I want to deploy it on xCloud.
Please inspect it, decide whether it should use xCloud native deployment or Docker,
generate the proper Dockerfile, Docker image workflow, docker-compose.yml,
.env.example, and give me the exact xCloud deployment steps.
```

For an existing compose file:

```text
Please make this docker-compose.yml work on xCloud.
Fix anything xCloud does not support, especially Docker build steps,
proxy services, and host ports 80/443.
```

The skill should respond with simple, copy-paste-ready output:
- What kind of project it detected
- Whether xCloud native deployment or Custom Docker is the better path
- The Dockerfile, compose file, GHCR GitHub Actions workflow, and `.env.example` when needed
- The exact xCloud exposed/primary port
- The exact xCloud UI or API steps

Before the agent inspects files, edits a repository, requests tokens, triggers webhooks, or routes to live xCloud API skills, it must ask for explicit confirmation of that exact step. Start with read-only analysis when possible.

Safe agent opening:

```text
I can do read-only analysis first, or I can generate deployment files after your confirmation.
I will not push, deploy, collect tokens, or call live xCloud APIs unless you explicitly approve that exact step.
```

## What It Does

### What's New in v1.4.1

- Adds explicit confirmation gates before inspection, file generation, credential collection, deployment recommendations, webhooks, or live API routing.
- Rewrites the security attestation so it accurately describes templates, generated workflows, and user-approved live operations.
- Adds least-privilege token guidance plus production backup/staging guidance.

### What's New in v1.4.0

- Starts with human-friendly usage prompts instead of platform internals.
- Explains how this Docker deploy skill can hand live xCloud operations to official xCloud API skills.
- Keeps the `80:80` → `3080:80` rule visible in the first screen of the skill body.

Paste a project structure or `docker-compose.yml` and ask the AI to deploy it on xCloud. The skill:

1. **Detects your stack** — WordPress, Laravel, PHP, Node.js, Next.js, NestJS, Nuxt, Python, Go, Rust, or existing Docker
2. **Picks the right path** — xCloud Native deploy vs Docker
3. **Generates all files** — Dockerfile, docker-compose.yml, GitHub Actions CI/CD, .env.example
4. **Gives exact xCloud UI steps** — copy-paste ready

### What It Handles

| Scenario | Signal | Fix |
|----------|--------|-----|
| **Stack detection** | Any project files | Auto-routes to native or Docker path |
| **Build-from-source** | `build: context: .` in compose | GitHub Actions → GHCR; replaces `build:` with `image:` |
| **Proxy conflict** | Caddy/Traefik/nginx-proxy service | Removes it, adds embedded nginx-router |
| **Multi-port** | Multiple `ports:` on different services | Routes through nginx-router, single exposed port |
| **Reserved ports** | `80:80` or `443:443` host bindings | Rewrites/removes them; uses `3080:80` when container listens on 80 |
| **External config** | `./nginx.conf:/etc/nginx/...` | Embeds config inline via `configs:` block |
| **No Docker at all** | WordPress/Laravel/Node.js project | Native xCloud deploy guide |

---

## Install

### Claude Code (CLI)
```bash
# From ClawHub
clawhub install xcloud-docker-deploy

# Or manually
git clone https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill.git
cp -r xCloud-Docker-Deploy-Skill ~/.claude/skills/xcloud-docker-deploy
```

### OpenAI Codex CLI
```bash
git clone https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill.git
cp -r xCloud-Docker-Deploy-Skill ~/.codex/skills/xcloud-docker-deploy
```

### OpenClaw Agent
Drop the skill folder into your agent's `skills/` workspace directory.

### Claude.ai (Projects)
Upload `SKILL.md` to your Project files. The AI will use it as context automatically.

### Cursor / Windsurf / Any AI IDE
Add `SKILL.md` contents to your system prompt or project rules file.

---

## Usage

Once installed, just describe what you want:

```
"Make this docker-compose.yml work on xCloud"
"Deploy my Laravel app to xCloud"
"My Next.js app needs to run on xCloud, help me set it up"
"Convert this Caddy + React + API stack for xCloud"
```

The agent reads DETECT.md first, identifies your stack, then follows the appropriate guide.

### Critical xCloud Port Rule

xCloud already owns host ports `80` and `443` for its Nginx and SSL layer. Final Docker compose output must never bind those host ports.

Use this routing model:

```
User -> xCloud Nginx 80/443 -> Docker host port >=1024 -> container port
```

Examples:

| App listens on | Final compose mapping | xCloud exposed/primary port |
|---|---|---|
| container `80` | `3080:80` | `3080` |
| container `3000` | `3000:3000` | `3000` |
| container `8000` | `8000:8000` | `8000` |

If a source compose has `80:80`, treat it as invalid for xCloud and rewrite it to `3080:80`.

---

## Works With xCloud API Skills

xCloud now publishes API-backed agent skills for live operations:

- `xcloud:servers` — servers, PHP, databases, cron, firewall/fail2ban, sudo users, WordPress provisioning
- `xcloud:sites` — site lifecycle, status, backups, domains, cache, SSH, site cron, git
- `xcloud:wordpress` — WordPress updates, debug, magic login, vulnerabilities, PageSpeed
- `xcloud:ssl` — SSL certificates
- `xcloud:account` — current user, API tokens, Cloudflare integrations, blueprints, health

Use this skill for project detection, Dockerfile/compose generation, GHCR CI, and Custom Docker readiness. Use the official xCloud API skills for live account/server/site actions.

### Private API Token Flow

If the user wants live xCloud account/server/site actions, the agent should ask for or help configure `XCLOUD_API_TOKEN`.

Keep it simple:
- Ask for the token only when live xCloud API access is needed.
- State the exact live operation before asking for a token.
- Prefer least-privilege and short-lived tokens where possible.
- Never print, store, log, reuse, or commit the token.
- Use this Docker skill for local project analysis and file generation.
- Use official xCloud API skills for live operations like checking servers, creating sites, reading deployment logs, renewing SSL, or verifying status.

### Production Safety Gate

Before recommending `git push`, deployment webhooks, production migrations, cache clears, DNS changes, SSL changes, or live xCloud API mutations:

- Confirm the target environment: staging or production.
- Ask whether a backup exists for production sites/databases.
- Prefer a feature branch or pull request for generated files.
- Show generated Dockerfile, compose file, workflow, and environment variable list before applying.
- Do not trigger deployment webhooks or live API mutations without a separate final confirmation.

---

## Supported Stacks

| Stack | Deploy Path | Files Provided |
|-------|-------------|----------------|
| WordPress | xCloud Native | Step-by-step UI guide |
| Laravel | xCloud Native | Deploy hooks, queue worker config |
| PHP (generic) | xCloud Native | Web root config, Composer hooks |
| Node.js / Express | xCloud Native | PORT env setup |
| Next.js | Docker | `dockerfiles/nextjs.Dockerfile` + `compose-templates/nextjs-postgres.yml` |
| NestJS | Docker | Generated Dockerfile + compose |
| Python / FastAPI | Docker | `dockerfiles/python-fastapi.Dockerfile` + compose with Celery |
| Go | Docker | Generated Dockerfile + compose |
| Existing Docker | Adapt | Scenario A/B/C transformation |

---

## Skill Structure

```
xcloud-docker-deploy/
├── SKILL.md                          ← Main skill instructions (load this)
├── DETECT.md                         ← Stack fingerprinting rules
├── references/
│   ├── xcloud-constraints.md         ← Platform rules (must-read)
│   ├── xcloud-deploy-paths.md        ← Native vs Docker decision matrix
│   ├── xcloud-native-wordpress.md    ← WordPress deploy guide
│   ├── xcloud-native-laravel.md      ← Laravel deploy guide
│   ├── xcloud-native-nodejs.md       ← Node.js deploy guide
│   ├── xcloud-native-php.md          ← PHP deploy guide
│   ├── scenario-build-source.md      ← Scenario A deep-dive
│   ├── scenario-proxy-conflict.md    ← Scenario B deep-dive
│   └── scenario-multi-service-build.md ← Scenario C deep-dive
├── dockerfiles/
│   ├── laravel.Dockerfile            ← PHP 8.3-fpm-alpine, multi-stage
│   ├── nextjs.Dockerfile             ← 3-stage standalone build
│   ├── node-app.Dockerfile           ← Node 20-alpine, non-root
│   ├── php-generic.Dockerfile        ← PHP 8.3-apache + mod_rewrite
│   └── python-fastapi.Dockerfile     ← Python 3.12-slim + uvicorn
├── compose-templates/
│   ├── laravel-mysql.yml             ← PHP-FPM + nginx + MySQL + Redis
│   ├── nextjs-postgres.yml           ← Next.js + PostgreSQL
│   ├── nodejs-api-postgres.yml       ← Node API + PostgreSQL
│   └── python-fastapi-postgres.yml   ← FastAPI + PostgreSQL + Celery
├── assets/
│   └── github-actions-build.yml      ← GitHub Actions GHCR build workflow
└── examples/
    ├── rybbit-analytics.md           ← Caddy + multi-port (Scenario B)
    ├── custom-app-dockerfile.md      ← Build-from-source (Scenario A)
    ├── fullstack-monorepo.md         ← Multi-service (Scenario C)
    ├── laravel-app.md                ← Laravel native deploy
    └── nextjs-app.md                 ← Next.js Docker deploy
```

---

## About xCloud

[xCloud](https://xcloud.host) is a git-push Docker deployment platform. Push your repo, xCloud runs `docker-compose pull && docker-compose up -d`. It handles SSL, reverse proxy, and domain routing automatically — your stack must not duplicate those.

References:
- xCloud Agent Skills docs: https://app.xcloud.host/agent/skills
- xCloud Public API docs: https://app.xcloud.host/api/v1/docs

---

## Author

**M Asif Rahman** — [@Asif2BD](https://github.com/Asif2BD)

- ClawHub: [clawhub.ai/Asif2BD/xcloud-docker-deploy](https://clawhub.ai/Asif2BD/xcloud-docker-deploy)
- SkillsMP: [skillsmp.com](https://skillsmp.com)

---

## License

Apache 2.0 — free to use, modify, and distribute.
