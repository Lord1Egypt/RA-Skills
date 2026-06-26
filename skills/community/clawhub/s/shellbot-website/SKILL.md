---
name: shellbot-website
version: 1.1.0
description: Build, deploy, and design micro apps and websites on Cloudflare Workers. Scaffolds from templates (React Router + Hono, Next.js, Astro, Remix), deploys, sets up custom domains, provisions resources (D1, KV, R2, Queues), manages secrets, and applies production-grade frontend design. Use when creating websites, web apps, landing pages, or any project on Cloudflare Workers.
allowed-tools: Bash(wrangler *), Bash(npx wrangler *), Bash(npm create cloudflare*), Bash(bash scripts/*), Bash(curl *api.cloudflare.com*), Bash(npm run *), Bash(npm install *), Bash(npx create-cloudflare*), Bash(mkdir *), Bash(jq *), Read, Write
argument-hint: "<command> [options]"
metadata:
  openclaw:
    emoji: "🌐"
    primaryEnv: "CLOUDFLARE_API_TOKEN"
    optionalEnv: ["CLOUDFLARE_ACCOUNT_ID"]
    homepage: "https://getshell.ai"
---

# ShellBot Website

Build and deploy micro apps and websites on Cloudflare Workers with production-grade design.

## Arguments

- **Command:** `$0` (`create` | `deploy` | `domain` | `provision` | `secrets` | `status` | `teardown`)
- **Arg 1:** `$1` (template name, resource type, domain, etc.)
- **Arg 2+:** `$2`, `$3`, etc.
- **All args:** `$ARGUMENTS`

| Command | Script | Example |
|---------|--------|---------|
| `create` | `scripts/create-project.sh` | `/shellbot-website create my-app --template react-hono` |
| `deploy` | `scripts/deploy.sh` | `/shellbot-website deploy --env production` |
| `domain` | `scripts/setup-domain.sh` | `/shellbot-website domain my-worker example.com` |
| `provision` | `scripts/provision-*.sh` | `/shellbot-website provision d1 my-db` |
| `secrets` | `scripts/manage-secrets.sh` | `/shellbot-website secrets put API_KEY` |
| `status` | `scripts/status.sh` | `/shellbot-website status --resources` |
| `teardown` | `scripts/teardown.sh` | `/shellbot-website teardown my-worker` |

## Authentication

Two authentication methods, checked in this order:

### Method 1: API Token (recommended, required for agents/CI)

Set `CLOUDFLARE_API_TOKEN` environment variable. This is the primary method — it takes precedence over OAuth if both are present.

If any command fails with authentication errors, tell user:
```
Get an API token from https://dash.cloudflare.com/profile/api-tokens
Use the "Edit Cloudflare Workers" template, or create a custom token with:
  Workers Scripts: Edit
  D1: Edit
  Workers KV Storage: Edit
  Workers R2 Storage: Edit
  Zone DNS: Edit (for custom domains)
Then: export CLOUDFLARE_API_TOKEN="your-token-here"
```

### Method 2: OAuth via `wrangler login` (fallback for local use)

If `CLOUDFLARE_API_TOKEN` is not set, attempt OAuth login:

```bash
wrangler login
```

This opens a browser for Cloudflare OAuth. When running in an agent context:

1. Run `wrangler login` — it will print an authorization URL to stdout
2. Show the URL to the user and ask them to open it in their browser
3. The user authorizes in the browser, which redirects to `localhost:8976`
4. Wrangler receives the callback and stores OAuth tokens in `~/.wrangler/config/default.toml`

**Limitation**: This only works when the agent runs on the user's local machine (the OAuth callback must reach `localhost:8976`). It will NOT work in remote/CI environments — use API token there.

After login, verify with:
```bash
wrangler whoami
```

### Auth check order in scripts

All scripts check `CLOUDFLARE_API_TOKEN` first. If not set, they check if `wrangler whoami` succeeds (meaning OAuth tokens exist in `~/.wrangler/config/default.toml`). If neither works, they error with instructions for both methods.

### Optional: Account ID

`CLOUDFLARE_ACCOUNT_ID` — auto-detected by wrangler. Set it to skip the account selection prompt when multiple accounts exist.
```
Find at: Dashboard → Overview → right sidebar → Account ID
Then: export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

### Prerequisites

- **Node.js v20+**
- **Wrangler**: `npm install -g wrangler` or use `npx wrangler`

Verify setup:
```bash
wrangler whoami
```

## Non-Interactive Design

All scripts run fully non-interactively — no prompts, no user input required. This makes them safe for agent invocation. Destructive operations require explicit `--force` flags instead of confirmation prompts.

## Quick Start

```bash
# 1. Scaffold from template (fully non-interactive, no deploy, no git init)
bash scripts/create-project.sh my-app

# 2. Local development
cd my-app && npm run dev

# 3. Deploy to Cloudflare
bash scripts/deploy.sh

# 4. Add custom domain
bash scripts/setup-domain.sh my-app example.com

# 5. Provision resources as needed
bash scripts/provision-d1.sh my-db --binding DB
bash scripts/provision-kv.sh my-cache --binding CACHE
bash scripts/provision-r2.sh my-assets --binding ASSETS
```

## Project Scaffolding

### Default Templates

| Short Name | Template | Best For |
|------------|----------|----------|
| `react-hono` (default) | `react-router-hono-fullstack-template` | Fullstack apps with React Router 7 + Hono API |
| `next` | `next-starter-template` | Next.js apps on CF Workers |

```bash
# Primary default (React Router + Hono)
bash scripts/create-project.sh my-app

# Use Next.js instead
bash scripts/create-project.sh my-app --template next

# Use any CF template by short name or full name
bash scripts/create-project.sh my-app --template astro-blog
bash scripts/create-project.sh my-app --template remix
bash scripts/create-project.sh my-app --template vite-react
```

See [references/cf-templates.md](references/cf-templates.md) for the full catalog of 36+ templates.

### Custom Template URL

```bash
bash scripts/create-project.sh my-app --template-url https://github.com/user/repo
```

## Deployment

```bash
# Deploy to production
bash scripts/deploy.sh

# Deploy to specific environment
bash scripts/deploy.sh --env staging
bash scripts/deploy.sh --env production

# Dry run (shows what would deploy)
bash scripts/deploy.sh --dry-run

# View deployments
wrangler deployments list

# Rollback to previous version
wrangler rollback [version-id]
```

The `deploy.sh` script pre-checks that wrangler config exists and `CLOUDFLARE_API_TOKEN` is set before deploying.

## Custom Domains

Three approaches to connect a custom domain to a CF Worker. See [references/custom-domains.md](references/custom-domains.md) for the full guide.

### 1. Automated Setup (Recommended)

```bash
# Domain must already be in your CF account
bash scripts/setup-domain.sh my-worker example.com

# With specific zone ID (skips lookup)
bash scripts/setup-domain.sh my-worker example.com --zone-id abc123

# Subdomain
bash scripts/setup-domain.sh my-worker app.example.com
```

### 2. Via wrangler.toml Routes

```toml
[[routes]]
pattern = "example.com/*"
zone_id = "your-zone-id"
```

### 3. Via Cloudflare Dashboard

Workers & Pages → your worker → Settings → Domains & Routes → Add Custom Domain.

### DNS Requirements

- Domain must be in your Cloudflare account (orange-cloud proxied)
- SSL is automatic — no certificate management needed
- DNS propagation takes 1-5 minutes for proxied domains

## Resource Provisioning

### D1 (SQL Database)

```bash
bash scripts/provision-d1.sh my-db --binding DB
# Creates database, outputs binding snippet for wrangler.toml
# Optional: --migration-file schema.sql (applies initial migration)
```

Common D1 operations:
```bash
wrangler d1 execute my-db --command "SELECT * FROM users"
wrangler d1 execute my-db --file schema.sql
wrangler d1 execute my-db --local --command "..."  # Local dev
wrangler d1 migrations create my-db add-users
wrangler d1 migrations apply my-db
```

### KV (Key-Value Store)

```bash
bash scripts/provision-kv.sh my-cache --binding CACHE
# Creates namespace, outputs binding snippet
```

### R2 (Object Storage)

```bash
bash scripts/provision-r2.sh my-assets --binding ASSETS
# Creates bucket, outputs binding snippet
```

### Queues

```bash
bash scripts/provision-queue.sh my-queue --binding QUEUE --type producer
# Creates queue, outputs producer/consumer binding snippets
```

## Secrets Management

```bash
# Add a secret (non-interactive)
bash scripts/manage-secrets.sh put API_KEY "sk-..."

# List secrets
bash scripts/manage-secrets.sh list

# Delete a secret
bash scripts/manage-secrets.sh delete API_KEY

# Bulk upload from JSON
bash scripts/manage-secrets.sh bulk secrets.json

# Environment-specific
bash scripts/manage-secrets.sh put API_KEY "sk-..." --env production
```

## Configuration

Wrangler supports TOML and JSON/JSONC. **If both exist, JSON takes precedence.** Pick one.

### Quick Reference (wrangler.toml)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-30"
compatibility_flags = ["nodejs_compat"]

[vars]
API_URL = "https://api.example.com"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

[[kv_namespaces]]
binding = "CACHE"
id = "xxx"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "my-assets"

[env.production]
vars = { API_URL = "https://api.example.com" }

[env.staging]
vars = { API_URL = "https://staging-api.example.com" }
```

See [references/wrangler-config.md](references/wrangler-config.md) for the full reference including JSONC format, static assets, and all binding types.

## Frontend Design

When building the frontend, apply these principles. Each links to a deep reference guide.

### Typography
→ *See [references/typography.md](references/typography.md)*

Choose distinctive fonts (not Inter/Roboto). Use a modular type scale with `clamp()` for headings. Pair a display font with a body font. Use `font-display: swap` and fallback metric matching to prevent layout shift.

### Color & Theme
→ *See [references/color-and-contrast.md](references/color-and-contrast.md)*

Use OKLCH for perceptually uniform palettes. Tint neutrals toward your brand hue. Follow the 60-30-10 rule (neutrals / secondary / accent). Avoid pure black/white. Avoid the AI palette (cyan-on-dark, purple-blue gradients).

### Layout & Space
→ *See [references/spatial-design.md](references/spatial-design.md)*

Use a 4pt spacing system. Create rhythm through varied spacing. Use `auto-fit` grids. Avoid wrapping everything in cards. Embrace asymmetry.

### Motion
→ *See [references/motion-design.md](references/motion-design.md)*

Only animate `transform` and `opacity`. Use exponential easing (quart/quint/expo). 100-150ms for feedback, 200-300ms for state changes, 300-500ms for layout. Always support `prefers-reduced-motion`.

### Interaction
→ *See [references/interaction-design.md](references/interaction-design.md)*

Design all 8 states (default, hover, focus, active, disabled, loading, error, success). Use `:focus-visible` for keyboard-only focus rings. Prefer optimistic UI and undo over confirmation dialogs.

### Responsive
→ *See [references/responsive-design.md](references/responsive-design.md)*

Mobile-first with `min-width` queries. Use container queries for components. Detect input method (`pointer: fine/coarse`), not just screen size. Handle safe areas.

### UX Writing
→ *See [references/ux-writing.md](references/ux-writing.md)*

Specific verb + object for buttons. Every error message answers what/why/how-to-fix. Empty states are onboarding moments. Pick one term and stick with it.

### The AI Slop Test

If someone sees this interface and immediately thinks "AI made this" — that's the problem. Avoid: cyan-on-dark, purple gradients, glassmorphism everywhere, identical card grids, gradient text, dark mode with glowing accents. Make unexpected, intentional design choices.

### Context Gathering

Before doing design work, you MUST have confirmed design context:
1. Check loaded instructions for a **Design Context** section
2. Check `.impeccable.md` in project root
3. If neither exists, ask the user for: target audience, use cases, brand personality/tone

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not authenticated" | Set `CLOUDFLARE_API_TOKEN` env var or run `wrangler login` |
| Node version error | Requires Node.js v20+ |
| No config found | Run from project root with `wrangler.toml` or `wrangler.jsonc` |
| Config changes ignored | JSON takes precedence over TOML if both exist |
| Binding not found | Check wrangler config bindings match code references |
| Custom domain not working | Domain must be proxied (orange cloud) in CF DNS |
| SSL pending | Wait 1-5 min for automatic certificate provisioning |

## Scripts & References

### Scripts
| Script | Purpose |
|--------|---------|
| `scripts/create-project.sh` | Scaffold project from CF templates |
| `scripts/deploy.sh` | Deploy worker with pre-checks |
| `scripts/setup-domain.sh` | Configure custom domain via CF API |
| `scripts/provision-d1.sh` | Create D1 database + binding snippet |
| `scripts/provision-kv.sh` | Create KV namespace + binding snippet |
| `scripts/provision-r2.sh` | Create R2 bucket + binding snippet |
| `scripts/provision-queue.sh` | Create queue + binding snippet |
| `scripts/manage-secrets.sh` | Add/list/delete/bulk secrets |
| `scripts/status.sh` | Deployment status, resources, logs |
| `scripts/teardown.sh` | Delete worker + resources |

### References
| File | Topic |
|------|-------|
| [references/cf-templates.md](references/cf-templates.md) | All 36+ CF quickstart templates |
| [references/custom-domains.md](references/custom-domains.md) | Domain setup, DNS, routes, SSL |
| [references/wrangler-config.md](references/wrangler-config.md) | Full wrangler.toml/jsonc reference |
| [references/typography.md](references/typography.md) | Font selection, scales, loading |
| [references/color-and-contrast.md](references/color-and-contrast.md) | OKLCH, palettes, dark mode |
| [references/spatial-design.md](references/spatial-design.md) | Grids, spacing, hierarchy |
| [references/motion-design.md](references/motion-design.md) | Animation timing, easing |
| [references/interaction-design.md](references/interaction-design.md) | States, forms, focus, loading |
| [references/responsive-design.md](references/responsive-design.md) | Mobile-first, fluid, container queries |
| [references/ux-writing.md](references/ux-writing.md) | Labels, errors, empty states |

## External Resources

- [Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)
- [Workers Templates](https://developers.cloudflare.com/workers/get-started/quickstarts/)
