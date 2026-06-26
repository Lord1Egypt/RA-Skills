---
name: deploy-kit
description: >
  Deploy projects to Vercel, Netlify, or Fly.io with one command.
  Auto-detects framework (Next.js, React, Python, Node.js, static HTML).
  Shows deploy URL when done. Supports rollback. Use when the user asks to
  deploy, ship, publish, or push to production.
  Triggers on: "deploy this", "ship it", "push to production", "deploy to vercel",
  "deploy to netlify", "deploy to fly", "go live".
tags:
  - deploy
  - vercel
  - netlify
  - flyio
  - hosting
  - production
  - ship
  - devops
---

# Deploy Kit

You deploy projects to Vercel, Netlify, or Fly.io. One command, auto-detection, done.

## Core Behavior

When the user says "deploy" or "ship", detect what kind of project it is and deploy to the best platform. If the user specifies a platform, use that one.

## Auto-Detection

Check the project root for these files to determine the framework:

| File | Framework | Best Platform |
|------|-----------|--------------|
| `next.config.*` | Next.js | Vercel |
| `package.json` with `react-scripts` | Create React App | Vercel or Netlify |
| `index.html` (no package.json) | Static site | Netlify |
| `fly.toml` | Already configured for Fly.io | Fly.io |
| `Dockerfile` | Container | Fly.io |
| `requirements.txt` or `pyproject.toml` | Python | Fly.io |
| `Procfile` | Heroku-style | Fly.io |
| `astro.config.*` | Astro | Vercel or Netlify |
| `svelte.config.*` | SvelteKit | Vercel |
| `nuxt.config.*` | Nuxt | Vercel |

## Deploy Commands

### Vercel
```bash
# Check if vercel CLI is installed
which vercel || npm install -g vercel

# Deploy (auto-detects framework)
vercel --yes

# Deploy to production
vercel --prod --yes
```

### Netlify
```bash
# Check if netlify CLI is installed
which netlify || npm install -g netlify-cli

# Deploy preview
netlify deploy --dir=.

# Deploy to production
netlify deploy --prod --dir=.

# For static sites, detect the build output directory:
# Next.js: out/ or .next/
# React: build/
# Plain HTML: . (current directory)
```

### Fly.io
```bash
# Check if fly CLI is installed
which fly || curl -L https://fly.io/install.sh | sh

# If no fly.toml, launch new app
fly launch --yes --no-deploy

# Deploy
fly deploy
```

## Workflow

### Step 1: Detect
```
Detected: Next.js project (found next.config.js)
Recommended platform: Vercel
```

### Step 2: Check CLI
```
Vercel CLI: installed (v37.2.0)
```

### Step 3: Deploy
Run the deploy command and show the output URL.

### Step 4: Report
```
Deployed to Vercel
URL: https://my-project-abc123.vercel.app
Production: https://my-project.vercel.app
Time: 34s
Framework: Next.js
Region: iad1 (US East)
```

## Other Commands

### "Status" / "Is it live?"
Check the current deployment status:
```bash
vercel ls --limit 1
# or
netlify status
# or
fly status
```

### "Rollback"
```bash
vercel rollback
# or
netlify rollback
# or
fly releases --image
```

### "Logs"
```bash
vercel logs [url]
# or
netlify logs
# or
fly logs
```

### "Add domain"
```bash
vercel domains add mydomain.com
# or
netlify domains:add mydomain.com
```

## Rules
- Always ask before deploying to production: "Deploy to production? (y/n)"
- Show the URL immediately after deploy completes
- If deploy fails, show the error and suggest a fix
- Never store or expose API tokens — use the CLI's built-in auth
- Default to preview/staging deploy, not production
- If no platform preference, recommend based on auto-detection table
