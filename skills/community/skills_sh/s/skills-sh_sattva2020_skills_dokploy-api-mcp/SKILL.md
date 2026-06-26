---
name: dokploy-api-mcp
description: >-
  Deploy and manage applications on Dokploy (self-hosted PaaS).
  Use when deploying apps, managing Docker Compose services,
  databases (PostgreSQL, MySQL, MariaDB, MongoDB, Redis),
  configuring domains, SSL, backups, notifications, rollbacks,
  scheduled tasks, environments, organizations, SSO,
  preview deployments, patches, Docker Swarm clusters,
  running migrations, or troubleshooting Dokploy deployments.
  Covers tRPC API (449 endpoints), CLI, MCP server (449 tools),
  and common pitfalls with Next.js, Docker, and Traefik.
argument-hint: "[action] <details>"
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash(curl *) Bash(npx *) Bash(docker *) Bash(ssh *) Bash(git *) Read Write WebFetch
metadata:
  author: ai-ads-agent
  version: "2.0"
  category: deployment
---

# Dokploy Deployment

Deploy and manage applications on a self-hosted Dokploy instance (v0.28.4+).
Dokploy is an open-source PaaS (alternative to Vercel/Heroku) using Docker + Traefik v3.

## Quick Reference

| Item | Value |
|------|-------|
| Dashboard | `https://<DOKPLOY_HOST>/` |
| API base | `https://<DOKPLOY_HOST>/api/` |
| Swagger UI | `https://<DOKPLOY_HOST>/swagger` (browser login required) |
| Auth header | `x-api-key: <TOKEN>` |
| CLI install | `npm install -g @dokploy/cli` |
| MCP server | `@sattva/dokploy-mcp` (449 tools — full API coverage) |
| API version | OpenAPI 3.1.0, 449 endpoints |
| Docs | https://docs.dokploy.com |

## First Run — Setup

**On first use**, check if the Dokploy MCP server is configured. If not, run the interactive setup:

```
1. Check: does ~/.claude/mcp.json contain a "dokploy" server entry?
2. If NO → run: python3 skills/dokploy-api-mcp/scripts/setup.py
   (or the full path in the user's skill installation directory)
3. The script will:
   - Ask for Dokploy URL (e.g., https://dokploy.example.com)
   - Ask for API key (generated in Dashboard → Settings → Profile → API/CLI)
   - Validate the connection
   - Auto-configure ~/.claude/mcp.json with the MCP server
4. Tell the user: "Restart Claude Code to activate the Dokploy MCP server."
```

**With CLI arguments** (non-interactive):

```bash
python3 skills/dokploy-api-mcp/scripts/setup.py --url https://dokploy.example.com --key YOUR_API_KEY
```

**After setup**, the MCP server (`@sattva/dokploy-mcp`, 449 tools) will be available on next Claude Code restart. Prefer MCP tools over curl for all operations.

## Environment Variables

Before using this skill, ensure these are available:

```
DOKPLOY_URL=https://dokploy.example.com
DOKPLOY_API_KEY=<generated-api-token>
```

Generate API token: Dashboard → Settings → Profile → API/CLI → Generate.

## Deployment Workflow

### Step 1: Check Current State

```bash
# Get application status
curl -s -X GET "${DOKPLOY_URL}/api/trpc/application.one?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'APP_ID'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}"
```

### Step 2: Trigger Deploy

```bash
# Deploy application (POST — mutation)
curl -s -X POST "${DOKPLOY_URL}/api/application.deploy" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"json":{"applicationId":"APP_ID"}}'
```

### Step 3: Monitor Deploy Status

```bash
# Poll deployment status
curl -s -X GET "${DOKPLOY_URL}/api/trpc/deployment.all?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'APP_ID'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}"
```

### Step 4: Verify Health

```bash
curl -sk "https://<app-domain>/api/health"
```

## API Reference

Dokploy uses **tRPC** internally. Two request formats:

### Queries (read) — GET with encoded input

```
GET /api/trpc/<router>.<procedure>?input=URL_ENCODED({"json":{...}})
Header: x-api-key: <token>
```

### Mutations (write) — POST with JSON body

```
POST /api/<router>.<procedure>
Header: x-api-key: <token>
Header: Content-Type: application/json
Body: {"json":{...}}
```

### Key Endpoints

See [references/API-REFERENCE.md](references/API-REFERENCE.md) for the full list (449 endpoints).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `project.all` | GET | List all projects |
| `project.one` | GET | Get project by ID |
| `application.one` | GET | Get app details + status |
| `application.deploy` | POST | Trigger deployment |
| `application.stop` | POST | Stop application |
| `application.start` | POST | Start application |
| `application.update` | POST | Update app settings |
| `application.saveBuildType` | POST | Change build type |
| `application.saveEnvironment` | POST | Set environment variables |
| `compose.one` | GET | Get compose service |
| `compose.deploy` | POST | Deploy compose service |
| `deployment.all` | GET | List deployments for app |
| `domain.byApplicationId` | GET | Get domains for app |
| `domain.create` | POST | Add custom domain |
| `postgres.one` | GET | Get PostgreSQL service |
| `redis.one` | GET | Get Redis service |
| `mariadb.one` | GET | Get MariaDB service |
| `mongo.one` | GET | Get MongoDB service |
| `environment.byProjectId` | GET | List environments |
| `rollback.rollback` | POST | Rollback deployment |
| `schedule.create` | POST | Create scheduled task |
| `backup.create` | POST | Create backup config |
| `notification.createTelegram` | POST | Setup Telegram notifications |
| `docker.getContainersByAppNameMatch` | GET | List Docker containers |
| `application.readTraefikConfig` | GET | Read Traefik config |

## CLI Usage

```bash
# Install
npm install -g @dokploy/cli

# Authenticate (creates ~/.config/dokploy/config.json)
dokploy authenticate

# Verify token
dokploy verify

# Application management
dokploy app create   # Create new application
dokploy app deploy   # Deploy application
dokploy app stop     # Stop application
dokploy app delete   # Delete application

# Database management
dokploy db create    # Create database service
dokploy db delete    # Delete database service

# Environment variables
dokploy env set      # Set env vars
dokploy env list     # List env vars

# Project management
dokploy project create
dokploy project list
```

## MCP Server (449 tools — full API coverage)

**When MCP is available, ALWAYS prefer MCP tools over curl.** MCP handles tRPC URL encoding and response parsing automatically.

See [references/MCP-TOOLS.md](references/MCP-TOOLS.md) for the full 449-tool reference.

### Setup

**Automatic** (recommended): Run the setup script from the "First Run" section above — it configures MCP automatically.

**Manual** (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "dokploy": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@sattva/dokploy-mcp"],
      "env": {
        "DOKPLOY_URL": "https://dokploy.example.com/api",
        "DOKPLOY_API_KEY": "<your-api-token>"
      }
    }
  }
}
```

**Note:** On macOS/Linux use `"command": "npx"` directly instead of `cmd /c`.
**Local dev:** use `"command": "node", "args": ["e:/My/MCP/dokploy-mcp/dist/index.js"]`.

### MCP Tools by Category (449 total)

| Category | Tools | Description |
|----------|-------|-------------|
| `application_*` | 29 | App lifecycle, deploy, config, git providers |
| `compose_*` | 28 | Docker Compose services |
| `settings_*` | 49 | Server settings, Traefik, cleanup, monitoring |
| `notification_*` | 38 | Slack/Telegram/Discord/Email/Webhook/Gotify/Ntfy/Pushover/Lark/Teams |
| `user_*` | 18 | User management, API keys, permissions |
| `server_*` | 16 | Remote server management |
| `postgres_*` | 14 | PostgreSQL management |
| `redis_*` | 14 | Redis management |
| `mysql_*` | 14 | MySQL management |
| `mariadb_*` | 14 | MariaDB management |
| `mongo_*` | 14 | MongoDB management |
| `patch_*` | 12 | File patches |
| `backup_*` | 11 | Database backups |
| `organization_*` | 10 | Organizations, invitations |
| `sso_*` | 10 | SSO/SAML enterprise auth |
| `domain_*` | 9 | Domain/SSL management |
| `ai_*` | 9 | AI-powered compose generator |
| `deployment_*` | 8 | Deployment history, queue |
| `project_*` | 8 | Project management |
| `gitea_*` | 8 | Gitea provider |
| `docker_*` | 7 | Container operations |
| `bitbucket_*` | 7 | Bitbucket provider |
| `registry_*` | 7 | Docker registries |
| `gitlab_*` | 7 | GitLab provider |
| `stripe_*` | 7 | Billing (cloud) |
| `environment_*` | 7 | Environments per project |
| `github_*` | 6 | GitHub provider |
| `licenseKey_*` | 6 | Enterprise licensing |
| `sshKey_*` | 6 | SSH key management |
| `mounts_*` | 6 | Volume mounts |
| `destination_*` | 6 | S3 backup destinations |
| `schedule_*` | 6 | Scheduled tasks/cron |
| `volumeBackups_*` | 6 | Volume backups |
| `certificates_*` | 4 | SSL certificates |
| `cluster_*` | 4 | Docker Swarm cluster |
| `port_*` | 4 | Port management |
| `redirects_*` | 4 | URL redirects |
| `security_*` | 4 | Security settings |
| `previewDeployment_*` | 4 | Preview deployments |
| `swarm_*` | 3 | Swarm node info |
| `gitProvider_*` | 2 | Git provider generic |
| `rollback_*` | 2 | Deployment rollbacks |
| `admin_*` | 1 | Admin setup |

### MCP Deployment Workflow

```
1. application_one                → check current status
2. application_saveEnvironment    → set/update env vars if needed
3. application_saveBuildType      → ensure Dockerfile build configured
4. application_deploy             → trigger deployment
5. application_one                → poll until applicationStatus = "done"
6. curl health endpoint           → verify app is working
```

### MCP Limitations (use Dashboard only)

- **Build/container logs** — WebSocket only, no MCP or REST endpoint
- **Docker exec into container** — No API endpoint, use SSH to VPS

**Everything else is available through MCP tools**, including: Redis, MariaDB, MongoDB, Compose, Backups, Notifications, Schedules, Rollbacks, SSO, Patches, Organizations, and more.

## Common Pitfalls

See [references/PITFALLS.md](references/PITFALLS.md) for detailed solutions.

| Problem | Cause | Fix |
|---------|-------|-----|
| `COPY /app/public` fails | Git ignores empty dirs | `RUN mkdir -p public` in Dockerfile |
| DB connection error | Neon HTTP driver vs standard PG | Use `postgres` (postgres.js) package |
| Clerk `publishableKey` missing | SSG validates env at build | `export const dynamic = "force-dynamic"` + skip provider in build phase |
| Container crash with migrate.mjs | standalone output lacks modules | Run migrations via in-app API endpoint |
| Build logs unavailable via API | WebSocket only, no REST | Check Dashboard UI or poll `deployment.all` for status |
| Container logs unavailable via API | WebSocket only | Use Dashboard UI |
| External DB port unreachable | VPS firewall blocks port | Use internal Docker network names |
| SSL certificate error from curl | Self-signed or Let's Encrypt delay | Use `curl -sk` or wait for cert provisioning |
| 404 on API routes after deploy | Route not in standalone output | Verify route exists in `.next/standalone` |
| Traefik middleware broken after upgrade | Dokploy v0.25+ uses Traefik v3 | Update middleware config syntax |

## Build Types

Dokploy supports:

| Type | When to use |
|------|-------------|
| **Dockerfile** | Custom builds, multi-stage, full control |
| **Nixpacks** | Auto-detect language, zero config |
| **Buildpack** | Heroku/Paketo compatible apps |
| **Docker Image** | Pre-built images from registry |

## Services (Databases)

Create via Dashboard → Project → Add Service:

- **PostgreSQL** — internal hostname: `<appName>:5432`
- **MySQL/MariaDB** — internal hostname: `<appName>:3306`
- **MongoDB** — internal hostname: `<appName>:27017`
- **Redis** — internal hostname: `<appName>:6379`

Internal hostnames use Docker network. External ports optional (may need firewall rules).

## Domain & SSL

1. Add domain via Dashboard or API (`domain.create`)
2. Point DNS A-record to VPS IP
3. Dokploy auto-provisions Let's Encrypt certificate via Traefik v3
4. HTTPS works automatically after DNS propagation

## Next.js Specific Guide

See [references/NEXTJS-GUIDE.md](references/NEXTJS-GUIDE.md) for full details on deploying Next.js 14/15 to Dokploy.
