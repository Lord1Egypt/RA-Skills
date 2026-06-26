# Vercel CLI Command Reference

## Project Initialization and Deployment

### vercel init

Initialize a sample project from the official template library.
```bash
vercel init [template-name]
```

### vercel / vercel deploy

Deploy the current project. Deploys to preview environment by default.
```bash
vercel [path] [options]
vercel deploy [path] [options]
```
Common options:
- `--prod` / `--production`: Deploy to production environment
- `--token <token>`: Specify authentication token (not recommended; prefer `VERCEL_TOKEN` environment variable)
- `--yes`: Skip all confirmation prompts
- `--force`: Force rebuild

### vercel build

Build the project locally (simulates Vercel build environment).
```bash
vercel build [options]
```
Common options:
- `--prod`: Build production environment version
- `--token <token>`: Authentication token

### vercel dev

Simulate Vercel deployment environment locally for development and testing.
```bash
vercel dev [port]
```
Default port is 3000.

### vercel link

Link the local directory to a Vercel project.
```bash
vercel link [options]
```

### vercel pull

Pull remote environment variables and project settings to local.
```bash
vercel pull [options]
```
Common options:
- `--environment production|preview|development`: Specify environment
- `--yes`: Automatically overwrite local variables with same name

---

## Deployment and Version Management

### vercel list

List deployment records for the current account/team.
```bash
vercel list [project] [options]
```
Common options:
- `--limit <number>`: Limit number of results returned (default 20)

### vercel inspect

View detailed information for a specified deployment.
```bash
vercel inspect <url|id> [options]
```
Common options:
- `--logs`: Display build and runtime logs
- `--wait`: Wait for deployment to complete before output

### vercel logs

View runtime logs for a deployment.
```bash
vercel logs <url> [options]
```
Common options:
- `--follow` / `-f`: Real-time tracking of new logs
- `--limit <number>`: Limit number of entries returned

### vercel promote

Promote a specified preview deployment to the current production deployment.
```bash
vercel promote <url|id> [options]
```

### vercel redeploy

Rebuild and redeploy based on an existing deployment.
```bash
vercel redeploy <url|id> [options]
```
Common options:
- `--prod`: Also deploy to production environment

### vercel rollback

Roll back the production environment to the previous stable deployment.
```bash
vercel rollback [options]
```

### vercel remove

Remove a specified deployment or project.
```bash
vercel remove <url|id|project> [options]
```
Note: Deleting a project is permanent.

### vercel bisect

Quickly locate the problematic deployment using binary search.
```bash
vercel bisect [options]
```
Requires specifying "good" and "bad" deployment versions.

---

## Domain and Certificate Management

### vercel alias set

Set a custom domain alias for a deployment.
```bash
vercel alias set <url> <domain> [options]
```

### vercel alias rm

Remove a domain alias.
```bash
vercel alias rm <domain> [options]
```

### vercel domains ls

List all domains under the account.
```bash
vercel domains ls [options]
```

### vercel domains add

Add a domain to a specified project.
```bash
vercel domains add <domain> [project] [options]
```
Common options:
- `--delegated`: Delegate DNS management to Vercel
- `--renew`: Auto-renew

### vercel domains buy

Purchase a domain directly through the CLI.
```bash
vercel domains buy <domain> [options]
```

### vercel dns ls

View DNS records for a domain.
```bash
vercel dns ls [domain] [options]
```

### vercel certs ls

List all SSL certificates under the account.
```bash
vercel certs ls [options]
```

### vercel certs issue

Issue a new SSL certificate for a domain.
```bash
vercel certs issue <domain> [options]
```

---

## Environment Variable Management

### vercel env ls

List environment variables for the project.
```bash
vercel env ls [options]
```

### vercel env add

Add an environment variable.
```bash
vercel env add <name> [env] [options]
```
Parameters:
- `name`: Variable name
- `env`: Optional `production`, `preview`, or `development` (adds to all three environments if not specified)

Common options:
- `-e <value>` / `--environment <env>`: Specify target environment
- `--encrypt`: Encrypted storage (default)

### vercel env rm

Remove an environment variable.
```bash
vercel env rm <name> [env] [options]
```

### vercel env pull

Pull environment variables to a local `.env` file.
```bash
vercel env pull [file] [options]
```
Generates `.env.local` by default.

### vercel env update

Update the value of an existing environment variable.
```bash
vercel env update <name> [env] [options]
```

### vercel target list

Manage custom deployment targets.
```bash
vercel target list [options]
```

---

## Team and Account Management

### vercel whoami

Display the username of the currently logged-in account.
```bash
vercel whoami
```

### vercel teams list

List all teams the current user belongs to.
```bash
vercel teams list [options]
```

### vercel switch

Switch the team context for current operations.
```bash
vercel switch [team] [options]
```

### vercel usage

View usage and billing statistics for the current account.
```bash
vercel usage [options]
```
Common options:
- `--month <YYYY-MM>`: View specified month

### vercel contract

View contract commitment information.
```bash
vercel contract
```

---

## Cache and Storage

### vercel cache purge

Purge CDN or data cache.
```bash
vercel cache purge [options]
```
Common options:
- `--team <team>`: Specify team
- `--token <token>`: Authentication token

### vercel blob

Interact with Vercel Blob storage.
```bash
vercel blob [subcommand]
```
Subcommands:
- `vercel blob ls`: List blobs
- `vercel blob rm <url>`: Remove blob
- `vercel blob url <key>`: Get blob URL

---

## Other Utilities

### vercel api

Make authenticated Vercel API requests (Beta).
```bash
vercel api <endpoint> [options]
```
Common options:
- `--method GET|POST|PATCH|DELETE`: HTTP method
- `--body <json>`: Request body

### vercel curl

Make HTTP requests to deployments bypassing protection mechanisms (Beta).
```bash
vercel curl <path> [options]
```

### vercel integration

Manage marketplace integrations and resource configurations.
```bash
vercel integration [subcommand]
```

### vercel mcp

Set up MCP (Model Context Protocol) client configuration.
```bash
vercel mcp [options]
```

### vercel webhooks

Manage webhooks (Beta).
```bash
vercel webhooks [subcommand]
```

### vercel project ls

Manage projects.
```bash
vercel project ls [options]
```

### vercel redirects list

List redirect rules for the project.
```bash
vercel redirects list [options]
```

### vercel telemetry

Enable or disable telemetry data collection.
```bash
vercel telemetry [enable|disable]
```

### vercel buy

Purchase credits, plugins, subscriptions, or domains via CLI.
```bash
vercel buy [item] [options]
```

### vercel help

Get command help.
```bash
vercel help [command]
```