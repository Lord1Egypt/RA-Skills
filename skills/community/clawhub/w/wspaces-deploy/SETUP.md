# W-Spaces Deploy - Setup Guide

## Setup

### 1. Get your API key

**Register a new account:**
```bash
scripts/wspaces_auth.sh --register --email you@example.com --password yourpass --name "Your Name"
```

**Check your email** and click the verification link.

**Login to get API key:**
```bash
scripts/wspaces_auth.sh --login --email you@example.com --password yourpass
```

Copy the `apiKey` from the response.

### 2. Set the API key

```bash
export WSPACES_API_KEY="wsk_live_xxxx..."
```

To persist:
```bash
echo 'export WSPACES_API_KEY="wsk_live_xxxx..."' >> ~/.bashrc
source ~/.bashrc
```

### 3. Verify

```bash
scripts/wspaces_auth.sh --me
```

Should return your user info and credits balance.

## Usage

Just tell your agent:
- **"Create a W-Spaces project called My App"**
- **"Push this HTML to W-Spaces"**
- **"Deploy to wspaces.app"**

## What It Does

- Create projects on W-Spaces
- Push HTML/CSS/JS code
- Deploy to live URLs (`*.wspaces.app`)
- Manage API keys
- View deployment history

## What It Doesn't Do

- No code generation
- No AI website builders
- No magic — just deploys what you give it
