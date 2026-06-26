---
name: vercel-cli
description: Vercel CLI skill for deploying and managing Vercel projects from the terminal.
metadata: { "openclaw": { "emoji": "▲", "requires": { "bins": ["nodejs"], "env":["VERCEL_TOKEN"]},"primaryEnv":"VERCEL_TOKEN" } }

---

# Vercel CLI

Vercel CLI skill for deploying and managing Vercel projects from the terminal. Use when the user wants to deploy, list, inspect, rollback, or manage Vercel deployments; configure domains, SSL certificates, environment variables; manage teams or view usage; or needs help with `vercel` CLI commands.

## Environment Setup

**Install Vercel CLI:**
```bash
pnpm i -g vercel
```

**Update:**
```bash
pnpm i -g vercel@latest
```

**Verify Version:**
```bash
vercel --version
```

## Authentication

**Interactive Login:**
```bash
vercel login
```

**CI/CD Environment (Recommended):**
1. Create an access token on the [Tokens page](https://vercel.com/account/tokens)
2. Set the `VERCEL_TOKEN` environment variable

> Prefer using the `VERCEL_TOKEN` environment variable over the `--token` flag to avoid exposing the token in process lists or logs.

## Core Workflows

### Deployment
```bash
vercel                      # Deploy to preview environment
vercel deploy --prod        # Deploy to production environment
vercel build                # Build locally
vercel dev                  # Develop locally simulating Vercel environment
```

### Project Linking
```bash
vercel init                 # Initialize from official template
vercel link                 # Link local directory to Vercel project
vercel pull                 # Pull remote environment variables to local
```

### Deployment Management
```bash
vercel list [project]       # List recent deployments
vercel inspect [url/id]     # View deployment details (add --logs for build logs)
vercel logs [url]           # View runtime logs (--follow for real-time tracking)
vercel promote [url/id]     # Promote specified deployment to production
vercel redeploy [url/id]    # Rebuild and redeploy
vercel rollback             # Rollback production environment
vercel remove [url]         # Remove deployment or project
vercel bisect               # Bisect to locate problematic deployment
```

### Domains and Certificates
```bash
vercel alias set [url] [domain]   # Set custom domain
vercel alias rm [domain]          # Remove domain alias
vercel domains ls                 # List domains
vercel domains add [domain]       # Add domain
vercel certs ls                   # List SSL certificates
vercel certs issue [domain]       # Issue certificate for domain
```

### Environment Variables
```bash
vercel env ls                     # List environment variables
vercel env add [name] [env]       # Add (env optional: production/preview/development)
vercel env rm [name] [env]        # Remove environment variable
vercel env pull [file]            # Pull to local file
```

### Account and Teams
```bash
vercel whoami                    # Current logged-in username
vercel teams list                # List teams
vercel switch [team]             # Switch team
vercel usage                     # View usage and billing
```

### Advanced Tools
```bash
vercel api [endpoint]           # Make authenticated API request (Beta)
vercel curl [path]              # HTTP request (Beta)
vercel cache purge              # Purge CDN cache
vercel blob                     # Vercel Blob storage operations
vercel integration              # Manage integrations
vercel mcp                      # MCP client configuration
```

## Key Notes

- Most commands support `--help` for detailed parameters: `vercel help [command]`
- `vercel` is equivalent to `vercel deploy`
- `--prod` / `--production` flag deploys to production environment
- `--follow` for `logs` command enables real-time log tracking
- Use `VERCEL_TOKEN` environment variable for automated authentication; do not expose token on the command line

## Reference Documentation

- See `references/commands.md` for detailed command parameter descriptions