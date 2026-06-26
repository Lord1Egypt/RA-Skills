---
name: vercel-staging-workflow
description: Set up a staging/production workflow for Vercel projects using GitHub Actions and stable URL aliases. Use when asked to create a staging environment, set up preview URLs, configure Vercel deployment workflow, or establish a staging/production branch strategy. Creates a GitHub Action that automatically updates a stable staging alias after each push to main, giving you a permanent staging URL that always points to the latest deployment. Works with Vercel's Git integration (no vercel CLI needed in CI). NOT for non-Vercel hosting platforms.
---

# Vercel Staging Workflow

Stable staging URLs for Vercel projects via GitHub Actions + Vercel Alias API.

## The Problem

Vercel generates random URLs per deployment (`myproject-abc123.vercel.app`). You want a **stable** staging URL that always points to the latest `main` deploy.

## The Solution

A GitHub Action that:
1. Triggers on push to `main`
2. Waits for Vercel's Git-triggered deployment to finish
3. Sets a stable alias: `yourproject-staging.vercel.app`

**Result:** Two stable URLs per project:
- `yourproject-staging.vercel.app` → latest main (auto-updated)
- `yourproject.vercel.app` → production (manual promote or custom domain)

## Setup (per project)

### 1. Get Vercel Project ID

```bash
cd your-project
vercel link --yes
cat .vercel/project.json  # copy projectId
```

### 2. Create Permanent API Token

⚠️ **Important:** Use a permanent token from https://vercel.com/account/tokens — NOT the CLI token (those rotate automatically!).

### 3. Add GitHub Secrets

In your repo → Settings → Secrets:
- `VERCEL_TOKEN` — permanent API token
- `VERCEL_PROJECT_ID` — from step 1
- `VERCEL_TEAM_ID` — (optional, for team accounts)

### 4. Add the GitHub Action

Copy `references/github-action-template.yml` to `.github/workflows/staging-alias.yml`.

Edit the `STAGING_ALIAS` variable:
```yaml
STAGING_ALIAS: "yourproject-staging.vercel.app"
```

### 5. Push and verify

```bash
git add .github/workflows/staging-alias.yml
git commit -m "ci: add staging alias workflow"
git push
```

After the action runs, `https://yourproject-staging.vercel.app` will point to the latest deployment.

## Multi-Project Setup

For multiple projects sharing the same token, set `VERCEL_TOKEN` as an org-level secret and only vary `VERCEL_PROJECT_ID` per repo.

## Production Deploys

Production stays separate — either:
- Use Vercel's "Promote to Production" button
- Set up a `production` branch that triggers a production alias
- Use custom domains (always point to production)

## Key Gotchas

1. **CLI tokens rotate** — always use permanent API tokens from vercel.com/account/tokens
2. **Team accounts** need `VERCEL_TEAM_ID` — find it in Vercel dashboard URL or API
3. **Wait time** — the action polls for up to 3 minutes for deployment to reach READY
4. **Fallback** — if exact commit not found, falls back to latest READY deployment

## Full Action Template

See `references/github-action-template.yml` for the complete, commented GitHub Action file ready to copy into your project.
