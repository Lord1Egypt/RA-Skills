---
name: sigmaflow-deploy
description: Deploy the SigmaFlow SvelteKit trading frontend to the Git repository. Use when building and deploying changes to the SigmaFlow application, including after feature implementation, bug fixes, or any code changes. This skill handles cloning the repo, installing dependencies, building the SvelteKit app, and pushing to the GitLab instance at git.homelab:3000.
---

# SigmaFlow Deploy

## Overview

Automates deployment of the SigmaFlow trading frontend to the GitLab repository at `http://git.homelab:3000/vitali/SigmaFlow-Svelte`. This skill handles the full deployment workflow: repository management, dependency installation, SvelteKit production build, and pushing to the remote repository.

## Quick Start

### Basic Deployment

```bash
# Deploy to main branch (default)
scripts/deploy.sh

# Deploy to specific branch
scripts/deploy.sh ./SigmaFlow-Svelte main

# Use custom repo directory
scripts/deploy.sh /path/to/repo dev
```

### When to Run

- After completing a feature implementation (charts, orders, portfolio)
- After bug fixes or code changes
- Before testing in production environment
- As part of CI/CD pipeline integration

## Deployment Workflow

The deployment script performs these steps:

1. **Clone/Update Repository**: Clones from GitLab if needed, or updates existing clone
2. **Install Dependencies**: Runs `npm install` if node_modules doesn't exist
3. **Build Application**: Runs `npm run build` to create production bundle
4. **Commit Changes**: Stages all changes with timestamped commit message
5. **Push to Remote**: Pushes to specified branch (default: main)

## Repository Credentials

The script uses embedded credentials:
- **URL**: `http://git.homelab:3000/vitali/SigmaFlow-Svelte.git`
- **Token**: `c865b793f09a3b79b65ebdfbd75c5b17395188d2`

**Security Note**: These credentials are stored in the script. For production environments, consider environment variables or secret management.

## Parameters

The deploy script accepts optional parameters:

- `$1` (optional): Repository directory path (default: `./SigmaFlow-Svelte`)
- `$2` (optional): Branch name to push (default: `main`)

## Output

On success, the script displays:
- `[INFO]` messages for each step
- Final success message with deployment confirmation
- Application URL (configure based on hosting setup)

On no changes:
- `[WARN]` indicating no changes to commit
- Graceful exit (no git push)

## Troubleshooting

**Build fails**: Check SvelteKit configuration and fix errors, then re-run deploy
**Authentication error**: Verify token is valid and has write access to repository
**Push rejected**: Pull latest changes, resolve conflicts, then deploy again
