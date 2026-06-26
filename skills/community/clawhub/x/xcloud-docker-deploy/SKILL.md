---
name: xcloud-docker-deploy
description: "xCloud Docker Deploy v1.4.1 — a confirmation-gated skill for preparing projects for xCloud. It inspects or changes files only after user consent, generates Docker/GHCR deployment files, fixes xCloud port rules, and routes live API work only after a separate explicit token-consent step."
license: Apache-2.0
version: "1.4.1"
author: "M Asif Rahman"
homepage: "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill"
source: "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill"
repository: "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐳",
        "requires": { "bins": ["git", "docker"] },
        "install":
          [
            {
              "id": "github",
              "kind": "link",
              "label": "GitHub",
              "url": "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill",
            },
            {
              "id": "release",
              "kind": "link",
              "label": "Latest Release",
              "url": "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1",
            },
            {
              "id": "xcloud-agent-skills",
              "kind": "link",
              "label": "xCloud Agent Skills",
              "url": "https://app.xcloud.host/agent/skills",
            },
            {
              "id": "xcloud-api",
              "kind": "link",
              "label": "xCloud API Docs",
              "url": "https://app.xcloud.host/api/v1/docs",
            },
            {
              "id": "security",
              "kind": "link",
              "label": "Security Notes",
              "url": "https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/blob/main/SECURITY.md",
            },
          ],
      },
  }
tags:
  - docker
  - deployment
  - devops
  - xcloud
  - docker-compose
  - github-actions
  - wordpress
  - laravel
  - nextjs
  - nodejs
  - python
  - ci-cd
  - hosting
  - infrastructure
category: "DevOps & Deployment"
platforms:
  - claude-code
  - openClaw
  - claude-ai
  - cursor
  - windsurf
  - codex
  - any
security:
  verified: true
  package_no_runtime_network_calls: true
  no_executables: true
  templates_only: true
  requires_explicit_user_confirmation: true
  live_api_requires_separate_consent: true
---

# xCloud Docker Deploy v1.4.1

[![Version](https://img.shields.io/badge/version-1.4.1-brightgreen.svg)](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1)
[![ClawHub](https://img.shields.io/badge/ClawHub-xcloud--docker--deploy-blue)](https://clawhub.ai/asif2bd/skills/xcloud-docker-deploy)
[![xCloud API](https://img.shields.io/badge/xCloud-API%20Skills-purple)](https://app.xcloud.host/agent/skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)

Built for xCloud Custom Docker deployments by [Asif2BD](https://github.com/Asif2BD) · [GitHub](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill) · [Latest Release](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1) · [xCloud Agent Skills](https://app.xcloud.host/agent/skills)

## Start Here

This is a deployment-preparation skill. Before it inspects a project, edits files, recommends production changes, asks for API tokens, or routes to live xCloud API skills, the agent must confirm the exact action with the user.

Use this safe opening:

> I can do read-only analysis first, or I can generate deployment files after your confirmation. I will not push, deploy, collect tokens, or call live xCloud APIs unless you explicitly approve that exact step.

Use normal human language. Ask:

> This is my project. I want to deploy it on xCloud. Please inspect it, decide whether it should use xCloud native deployment or Docker, generate the proper Dockerfile, Docker image workflow, docker-compose.yml, `.env.example`, and give me the exact xCloud deployment steps.

If you already have a compose file, ask:

> Please make this `docker-compose.yml` work on xCloud. Fix anything xCloud does not support, especially Docker build steps, proxy services, and host ports 80/443.

The agent should then:
1. Ask whether to perform read-only analysis or generate files.
2. Detect the stack after the user confirms project inspection.
3. Choose native xCloud deployment or Custom Docker.
4. Generate or fix Docker files only after explicit confirmation.
5. Explain the exact xCloud UI/API steps in simple language.
6. Before any production-impacting step, recommend a branch, backup, and staging/test deployment.

> **xCloud port-safety notice:** final compose output must never bind host port `80` or `443`. If an app listens on container port `80`, use `3080:80` and set xCloud's exposed/primary port to `3080`.

Adapt any `docker-compose.yml` to work with [xCloud](https://xcloud.host) — a git-push Docker deployment platform.

## How xCloud Works

```
git push → xCloud runs: docker-compose pull && docker-compose up -d
```

**xCloud never runs `docker build`.** Images must be pre-built in a public registry. SSL, reverse proxy, and domain routing are handled by xCloud — your stack must not duplicate them.

Read `references/xcloud-constraints.md` for the full ruleset before making changes.

## Current xCloud API + Agent Skills Context

xCloud now publishes API-backed agent skills for operational work:

| Official skill | Owns |
|---|---|
| `xcloud:servers` | Servers, PHP, databases, cron, firewall/fail2ban, sudo users, WordPress provisioning |
| `xcloud:sites` | Site lifecycle, status, backups, domains, cache, SSH, site cron, git |
| `xcloud:wordpress` | WordPress plugins, themes, updates, debug, magic login, vulnerabilities, PageSpeed |
| `xcloud:ssl` | SSL certificates: view, install, renew, status, delete |
| `xcloud:account` | Current user, API tokens, Cloudflare integrations, blueprints, health |

Use this skill for project detection, Dockerfile/compose generation, GHCR CI, and xCloud Custom Docker readiness. Use the official API skills when the user asks to inspect or mutate live xCloud resources.

### API Token Flow

This Docker deploy skill can work alongside the official xCloud API skills when those skills/tools are available. If a task needs live xCloud data or live actions:

1. Ask whether the user wants live xCloud API help.
2. State the exact live operation before requesting a token, such as "list servers" or "read deployment logs".
3. Ask for a least-privilege, short-lived token where possible.
4. If no token is available, ask the user to provide or configure a private `XCLOUD_API_TOKEN`.
5. Never print, store, log, reuse, or commit the token. Use it only for the approved action.
6. Use the official xCloud API skills for live operations:
   - `xcloud:servers` for server capacity, PHP, databases, cron, firewall, sudo users, WordPress provisioning
   - `xcloud:sites` for site status, domains, backups, cache, SSH, git, deployment logs
   - `xcloud:wordpress` for WordPress plugins, themes, updates, debug, magic login, vulnerabilities, PageSpeed
   - `xcloud:ssl` for certificates
   - `xcloud:account` for current user, API tokens, Cloudflare integrations, blueprints, health
7. Keep Docker generation local and deterministic; use the API only for live xCloud account/server/site actions.

### Production Safety Gate

Before recommending `git push`, deployment webhooks, migration commands, cache clears, DNS changes, SSL changes, or live API actions:

1. Confirm the target environment: staging or production.
2. Ask whether a backup exists for production sites/databases.
3. Prefer a feature branch or pull request for generated files.
4. Show the generated Dockerfile, compose file, workflow, and environment variable list before the user applies them.
5. Do not trigger deployment webhooks or live API mutations without a separate final confirmation.

---

## Phase 0 — Detect Project Type First

**Before anything else, scan the project directory for these files:**

Read `DETECT.md` for full detection rules. Quick routing:

| Found in project | Stack | Action |
|---|---|---|
| `wp-config.php` or `wp-content/` | WordPress | Read `references/xcloud-native-wordpress.md` |
| `composer.json` + `artisan` | Laravel | Read `references/xcloud-native-laravel.md` |
| `package.json` + `next.config.*` | Next.js | Docker path → use `dockerfiles/nextjs.Dockerfile` + `compose-templates/nextjs-postgres.yml` |
| `package.json` (no framework config) | Node.js | Read `references/xcloud-native-nodejs.md` |
| `composer.json` (no artisan) | PHP | Read `references/xcloud-native-php.md` |
| `requirements.txt` or `pyproject.toml` | Python | Docker path → use `dockerfiles/python-fastapi.Dockerfile` |
| `go.mod` | Go | Docker path — generate Dockerfile manually |
| `docker-compose.yml` exists | Existing Docker | Proceed to Step 1 below |
| `Dockerfile` (no compose) | Build-from-source | Generate compose → Scenario A below |

See `references/xcloud-deploy-paths.md` for the Native vs Docker decision guide.

---

## Step 1 — Detect Which Scenarios Apply

Inspect the provided `docker-compose.yml`:

| Signal | Scenario |
|--------|----------|
| `build:` or `build: context: .` | **A** — Build-from-source |
| Caddy / Traefik / nginx-proxy service | **B** — Proxy conflict |
| Multiple `ports:` across services | **B** — Multi-port |
| Host port `80` or `443` in any `ports:` mapping | **B** — xCloud reserved port conflict |
| `./nginx.conf:/etc/nginx/...` volume mount | **B** — External config |
| Multiple services each with `build:` | **C** — Multi-service build |
| `image: some-public-image`, single port | Already compatible — verify port + env vars |

A compose file can trigger **multiple scenarios** simultaneously (handle A first, then B).

---

## Scenario A — Build-from-Source

> Read `references/scenario-build-source.md` for full details.

**What to do:**
1. Remove `build:` directive from compose
2. Replace `image:` with `ghcr.io/OWNER/REPO:latest`
3. Generate `.github/workflows/docker-build.yml` using `assets/github-actions-build.yml` template
4. Generate `.env.example` from all `${VAR}` references

**Deliverables:**
- Modified `docker-compose.yml`
- `.github/workflows/docker-build.yml`
- `.env.example`
- xCloud Deploy Steps (see Output Format)

---

## Scenario B — Proxy Conflict / Multi-Port / External Config

> Read `references/scenario-proxy-conflict.md` for full details.

**What to do:**
1. Remove Caddy/Traefik/nginx-proxy service entirely
2. Remove SSL labels and multi-port `ports:` from app services (replace with `expose:`)
3. Add `nginx-router` service with inline config via `configs:` block
4. Expose single port (default: `3080`) for xCloud to proxy

**Deliverables:**
- Modified `docker-compose.yml` with `nginx-router` + `configs:` block
- `.env.example`
- xCloud Deploy Steps

---

## Scenario C — Multi-Service Build

> Read `references/scenario-multi-service-build.md` for full details.

When multiple services have `build:` directives (separate frontend + backend + worker):

**What to do:**
1. For each service with `build:`, create a separate GHCR image path
2. Generate a matrix GitHub Actions workflow that builds all images in parallel
3. Update compose to use all GHCR image references

**Deliverables:**
- Modified `docker-compose.yml` (all `build:` removed)
- `.github/workflows/docker-build.yml` (matrix strategy)
- `.env.example`

---

## Output Format

Always produce complete, copy-paste-ready output:

```
## Modified docker-compose.yml
[full file]

## .github/workflows/docker-build.yml  (Scenario A/C only)
[full file]

## .env.example
[full file]

## xCloud Deploy Steps
1. Push repo to GitHub
2. (Scenario A/C) Wait for GitHub Actions to build image — check Actions tab
3. Server → New Site → Custom Docker → connect repo
4. Exposed port: [PORT]
5. Env vars to add: [list from .env.example]
6. Deploy
```

---

## Rules

- **Never** include `build:` in the final compose — xCloud silently ignores it
- **Never** bind host port `80` or `443` in final compose — xCloud's Nginx/SSL layer already owns them
- **If the app listens on container port `80`, output `3080:80` and tell xCloud to use exposed/primary port `3080`**
- **If you see `80:80`, treat it as invalid for xCloud and rewrite it to `3080:80`**
- **Never** expose database ports to host (remove `"5432:5432"` — use `expose:` internally)
- **Never** include Caddy, Traefik, nginx-proxy, or Let's Encrypt config
- **Always** preserve `environment:`, `volumes:`, `healthcheck:`, worker/sidecar services
- **Always** use `expose:` (internal) not `ports:` (host) for services behind nginx-router
- **Always** report the xCloud exposed/primary port as the host-side port from the single allowed web mapping
- **WebSockets?** Add upgrade headers to nginx config (see proxy-conflict reference)
- `configs.content:` inline syntax requires Docker Compose v2.23+ — use heredoc `command:` alternative if uncertain

## Port Normalization

xCloud receives public traffic on `80`/`443` through its own Nginx and SSL layer. Docker compose should expose one high host port for xCloud to proxy into:

```
User → xCloud Nginx 80/443 → Docker host port >=1024 → container port
```

Normalize ports before final output:

| Original mapping | Final xCloud mapping | xCloud exposed/primary port |
|---|---|---|
| `80:80` | `3080:80` | `3080` |
| `443:443` | remove | n/a |
| `8080:80` | prefer `3080:80` unless user explicitly requires `8080` | `3080` |
| `3000:3000` | allowed | `3000` |
| `8000:8000` | allowed | `8000` |

Final validation: no `ports:` mapping may start with `80:` or `443:`.

---

## Examples

See `examples/` for ready-made transformations:
- `examples/rybbit-analytics.md` — Caddy + multi-port app (Scenario B)
- `examples/custom-app-dockerfile.md` — build-from-source (Scenario A)
- `examples/fullstack-monorepo.md` — multi-service build (Scenario C)
