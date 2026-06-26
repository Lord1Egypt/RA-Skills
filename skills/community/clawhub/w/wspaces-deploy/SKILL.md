---
name: wspaces-deploy
description: Deploy static websites to W-Spaces. Use when deploying HTML/CSS/JS sites, landing pages, or single-page apps to wspaces.app. Supports project creation, code push, and deployment via API key authentication.
---

# W-Spaces Deployment

Deploy static websites to W-Spaces (wspaces.app). Create projects, push HTML, and deploy to a live URL — all via API.

## Configuration

### Get your API key

1. Register: `scripts/wspaces_auth.sh --register --email you@example.com --password yourpass --name "Your Name"`
2. Verify your email (check inbox)
3. Login: `scripts/wspaces_auth.sh --login --email you@example.com --password yourpass`
4. Copy the API key from the response

### Set the API key

```bash
export WSPACES_API_KEY="wsk_live_xxxx..."
```

Or store in `.env`:
```
WSPACES_API_KEY=wsk_live_xxxx...
```

## Operations

### Create a project

```bash
scripts/wspaces_project.sh --create --name "My Landing Page"
```

Response includes project ID and slug.

### Push HTML code

```bash
# From a file
scripts/wspaces_push.sh --project <project-id> --file ./index.html

# From inline HTML
scripts/wspaces_push.sh --project <project-id> --html "<html><body><h1>Hello</h1></body></html>"
```

### Deploy to live URL

```bash
scripts/wspaces_deploy.sh --project <project-id>
```

Result: `https://<slug>.wspaces.app`

### List projects

```bash
scripts/wspaces_project.sh --list
```

### Check project details

```bash
scripts/wspaces_project.sh --get --id <project-id>
```

### View deployments

```bash
scripts/wspaces_deploy.sh --list --project <project-id>
```

## Common Workflows

### Deploy a landing page

```bash
# 1. Create project
scripts/wspaces_project.sh --create --name "Startup Landing"
# → project ID: abc-123

# 2. Push code
scripts/wspaces_push.sh --project abc-123 --file ./index.html

# 3. Deploy
scripts/wspaces_deploy.sh --project abc-123
# → https://startup-landing-xyz.wspaces.app
```

### Update existing site

```bash
# Push new code (creates new version)
scripts/wspaces_push.sh --project abc-123 --file ./index.html

# Redeploy
scripts/wspaces_deploy.sh --project abc-123
```

### Full flow from scratch

Tell your agent:
- **"Create a W-Spaces project called My Portfolio"**
- **"Push this HTML to my W-Spaces project"**
- **"Deploy my project to wspaces.app"**

## API Key Management

```bash
# Create additional API key
scripts/wspaces_auth.sh --create-key --name "CI/CD Key"

# List all keys
scripts/wspaces_auth.sh --list-keys

# Revoke a key
scripts/wspaces_auth.sh --revoke-key --id <key-id>
```

## API Reference

See [wspaces-api.md](references/wspaces-api.md) for complete API documentation.

## Troubleshooting

**"WSPACES_API_KEY not set"**
```bash
export WSPACES_API_KEY="wsk_live_xxx..."
```

**"Invalid API key"**
- Key may be revoked — generate a new one via login
- Check for extra spaces when copying

**"Please verify your email"**
- Check your inbox for verification email
- Verify before logging in

**"Project not found"**
- Verify project ID with `scripts/wspaces_project.sh --list`
