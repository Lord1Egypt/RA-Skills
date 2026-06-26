# W-Spaces Deploy Skill

**Deploy static websites to [wspaces.app](https://wspaces.app). Create projects, push HTML code, and deploy to a live URL — all via the W-Spaces Public API.**

## What This Skill Does

- Deploy static HTML/CSS/JS websites to wspaces.app
- Create and manage projects via API
- Push code and create versioned deployments
- Get live URLs like `https://your-project.wspaces.app`

## Quick Start

### 1. Register & Get API Key

```bash
# Register (sends verification email)
scripts/wspaces_auth.sh --register --email you@example.com --password yourpass --name "Your Name"

# Verify email, then login
scripts/wspaces_auth.sh --login --email you@example.com --password yourpass
# → Returns: wsk_live_xxxx...
```

### 2. Set the API Key

```bash
export WSPACES_API_KEY="wsk_live_xxxx..."
```

### 3. Deploy

Tell your agent:
- **"Create a project called My Site on W-Spaces"**
- **"Push index.html to my W-Spaces project"**
- **"Deploy my W-Spaces project"**

Or use scripts directly:
```bash
scripts/wspaces_project.sh --create --name "My Site"
scripts/wspaces_push.sh --project <id> --file ./index.html
scripts/wspaces_deploy.sh --project <id>
# → https://my-site-abc123.wspaces.app
```

## Use Cases

- Landing pages for startups
- Portfolio sites
- Quick prototypes
- HTML/CSS demos
- AI-generated websites

## Requirements

- W-Spaces account (free, 10 credits on signup)
- API key (via login endpoint)
- `curl` and `jq` installed

## License

MIT
