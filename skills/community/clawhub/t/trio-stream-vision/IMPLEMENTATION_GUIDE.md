# Trio Vision OpenClaw Skill — Implementation & Shipping Guide

## Overview

This guide walks you through shipping the `trio-vision` OpenClaw skill from development to ClawHub publication. The skill wraps the Trio API (by MachineFi) to give OpenClaw agents the ability to analyze live video streams using natural-language conditions.

---

## Step 1: Understand the Skill Structure

The skill is a **SKILL.md-only** skill (no JavaScript handler needed). This is the simplest and most common pattern — the agent reads the Markdown instructions and executes shell commands (curl) to interact with the Trio API.

```
trio-vision-skill/
├── SKILL.md              # The skill definition (already created)
├── IMPLEMENTATION_GUIDE.md  # This file (not published)
└── README.md             # Optional, for GitHub repo (not published to ClawHub)
```

### Why SKILL.md-only?

- Trio's API is straightforward REST — curl commands are sufficient
- No complex state management needed between calls
- The agent's built-in reasoning handles workflow orchestration
- Simpler skills have fewer security concerns (important post-ClawHavoc)

---

## Step 2: Local Testing

### 2a. Get a Trio API Key

1. Go to https://console.machinefi.com
2. Sign up (free, gives you 100 credits / $1.00)
3. Navigate to the API Keys section
4. Create and copy your API key

### 2b. Set the Environment Variable

```bash
export TRIO_API_KEY="your_api_key_here"
```

Or add it to your shell profile:
```bash
echo 'export TRIO_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 2c. Install the Skill Locally

Copy the skill to your OpenClaw skills directory:

```bash
# Option 1: User-level skills directory
mkdir -p ~/.openclaw/skills/trio-vision
cp trio-vision-skill/SKILL.md ~/.openclaw/skills/trio-vision/SKILL.md

# Option 2: Project-level skills directory (higher precedence)
mkdir -p ./skills/trio-vision
cp trio-vision-skill/SKILL.md ./skills/trio-vision/SKILL.md
```

OpenClaw has hot-reloading enabled by default, so the skill should appear immediately.

### 2d. Verify the Skill is Loaded

```bash
openclaw skills list --eligible
```

You should see `trio-vision` in the list. If not, check:
- Is `TRIO_API_KEY` set in your environment?
- Is `curl` available on your PATH?
- Run `openclaw skills check` for diagnostics

### 2e. Test the Skill

Open OpenClaw and try these commands:

**Quick check:**
```
/trio-vision
Check if there are any people visible on this stream: https://www.youtube.com/live/STREAM_ID
```

**Or just chat naturally:**
```
What's happening on this YouTube live stream? https://www.youtube.com/live/STREAM_ID
```

**Test workflow:**
1. Validate a known live stream URL
2. Run check-once with a simple condition
3. Start a short live-monitor (30 seconds)
4. Check job status
5. Cancel the job

### 2f. Test with Different Stream Types

Test each supported stream type:
- YouTube Live: `https://www.youtube.com/live/STREAM_ID`
- Twitch: `https://www.twitch.tv/CHANNEL_NAME`
- RTSP camera: `rtsp://camera-ip:554/stream`
- HLS: `https://example.com/stream.m3u8`

---

## Step 3: Iterate on the Skill

### Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Agent doesn't validate stream first | Add stronger "ALWAYS validate first" language in Rules section |
| Agent forgets to show explanation | Emphasize in Rules: "ALWAYS show the explanation field" |
| Agent starts monitor without warning about cost | Add cost disclosure to the monitor workflow |
| Condition writing is poor | The "Condition Writing Tips" section helps the agent write better conditions |
| Error messages are confusing | The `remediation` field from the API gives actionable guidance |

### Testing Checklist

- [ ] Stream validation works (live stream)
- [ ] Stream validation handles offline/invalid URLs gracefully
- [ ] Check-once returns triggered + explanation
- [ ] Check-once with include_frame works
- [ ] Check-once with clip mode works
- [ ] Live-monitor creates a job and returns job_id
- [ ] Job status check works
- [ ] Job cancellation works
- [ ] Live-digest creates a job
- [ ] Analyze-frame works with a local image
- [ ] Error handling shows remediation
- [ ] Agent warns about costs before starting monitor/digest
- [ ] Agent never exposes the API key

---

## Step 4: Prepare for Publication

### 4a. Set Up a GitHub Account

ClawHub requires a GitHub account that is at least **one week old**. If you're publishing from a new account, wait the required period.

### 4b. Install ClawHub CLI

The ClawHub CLI comes bundled with OpenClaw. Verify it's available:

```bash
clawhub --version
```

### 4c. Authenticate with ClawHub

```bash
# This opens a browser for GitHub OAuth
clawhub login
```

### 4d. Choose a Slug

The slug is the unique identifier on ClawHub. Recommended: `machinefi/trio-vision`

Format: `<publisher>/<skill-name>`

---

## Step 5: Publish to ClawHub

### 5a. Publish the Skill

```bash
clawhub publish ./trio-vision-skill \
  --slug machinefi/trio-vision \
  --name "Trio Vision" \
  --version 1.0.0 \
  --changelog "Initial release: check-once, live-monitor, live-digest, analyze-frame" \
  --tags "vision,video,streaming,monitoring,camera,surveillance,ai"
```

### 5b. Verify Publication

```bash
clawhub inspect machinefi/trio-vision
```

Also check on the web: https://clawhub.ai (search for "trio-vision")

### 5c. Test Installation from ClawHub

On a clean machine or in a fresh OpenClaw instance:

```bash
# Install from ClawHub
openclaw skills install machinefi/trio-vision

# Verify
openclaw skills list --eligible | grep trio
```

---

## Step 6: Distribution Beyond ClawHub

### 6a. GitHub Repository

Create a public GitHub repo for the skill:

```bash
cd trio-vision-skill
git init
git add SKILL.md README.md
git commit -m "Initial release of trio-vision OpenClaw skill"
git remote add origin https://github.com/machinefi/trio-openclaw-skill.git
git push -u origin main
```

Users can install directly from Git:
```bash
git clone https://github.com/machinefi/trio-openclaw-skill.git ~/.openclaw/skills/trio-vision
```

### 6b. Link from Trio Documentation

Add an "OpenClaw Integration" section to https://docs.machinefi.com/ with:
- One-line install command
- Link to ClawHub listing
- Link to GitHub repo
- Quick demo GIF/video

### 6c. Cross-promote

- Add to the `trio-examples` GitHub repo
- Mention in Trio API docs quickstart
- Post on the OpenClaw Discord (#skills channel, 116K members)
- Submit to awesome-openclaw-skills curated list (https://github.com/VoltAgent/awesome-openclaw-skills)

---

## Step 7: Version Management

### Semantic Versioning

Follow semver for updates:
- **Patch** (1.0.1): Bug fixes, wording improvements
- **Minor** (1.1.0): New features (e.g., adding analyze-frame support)
- **Major** (2.0.0): Breaking changes to skill behavior

### Publishing Updates

```bash
clawhub publish ./trio-vision-skill \
  --slug machinefi/trio-vision \
  --version 1.1.0 \
  --changelog "Added analyze-frame endpoint support, improved condition writing tips" \
  --tags "vision,video,streaming,monitoring,camera,surveillance,ai"
```

### Rollback

ClawHub supports tags for version pinning. The `latest` tag automatically points to the newest version. To rollback:

```bash
clawhub publish ./trio-vision-skill \
  --slug machinefi/trio-vision \
  --version 1.0.0 \
  --tags latest
```

---

## Step 8: Advanced — JavaScript Handler Version (Optional)

If you later want more sophisticated behavior (rate limiting, response caching, structured output), you can upgrade to a JavaScript-based skill:

```
trio-vision-skill/
├── SKILL.md           # Instructions (keep existing)
├── manifest.json      # Input schema definition
└── index.mjs          # Handler with run() function
```

**manifest.json:**
```json
{
  "name": "trio-vision",
  "version": "1.0.0",
  "description": "Monitor and analyze live video streams using Trio Vision AI",
  "schema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["validate", "check", "monitor", "digest", "analyze", "status", "cancel", "list"],
        "description": "The Trio API action to perform"
      },
      "stream_url": {
        "type": "string",
        "description": "URL of the live video stream"
      },
      "condition": {
        "type": "string",
        "description": "Natural-language condition to check or monitor"
      },
      "job_id": {
        "type": "string",
        "description": "Job ID for status check or cancellation"
      },
      "options": {
        "type": "object",
        "description": "Additional parameters (interval_seconds, webhook_url, etc.)"
      }
    },
    "required": ["action"]
  }
}
```

**index.mjs:**
```javascript
const BASE_URL = "https://trio.machinefi.com/api";

export async function run(params, ctx) {
  const apiKey = ctx.secrets.TRIO_API_KEY;
  if (!apiKey) {
    return { error: true, message: "TRIO_API_KEY is not set. Get one at https://console.machinefi.com" };
  }

  const headers = {
    "Authorization": `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  };

  const { action, stream_url, condition, job_id, options = {} } = params;

  try {
    switch (action) {
      case "validate": {
        const res = await fetch(`${BASE_URL}/streams/validate`, {
          method: "POST",
          headers,
          body: JSON.stringify({ stream_url }),
        });
        return handleResponse(res);
      }

      case "check": {
        const body = { stream_url, condition, ...options };
        const res = await fetch(`${BASE_URL}/check-once`, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
        });
        return handleResponse(res);
      }

      case "monitor": {
        const body = {
          stream_url,
          condition,
          interval_seconds: 10,
          monitor_duration_seconds: 600,
          max_triggers: 1,
          ...options,
        };
        const res = await fetch(`${BASE_URL}/live-monitor`, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
        });
        return handleResponse(res);
      }

      case "digest": {
        const body = {
          stream_url,
          window_minutes: 10,
          capture_interval_seconds: 60,
          ...options,
        };
        const res = await fetch(`${BASE_URL}/live-digest`, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
        });
        return handleResponse(res);
      }

      case "analyze": {
        const body = { ...options };
        const res = await fetch(`${BASE_URL}/analyze-frame`, {
          method: "POST",
          headers,
          body: JSON.stringify(body),
        });
        return handleResponse(res);
      }

      case "status": {
        const res = await fetch(`${BASE_URL}/jobs/${job_id}`, { headers });
        return handleResponse(res);
      }

      case "cancel": {
        const res = await fetch(`${BASE_URL}/jobs/${job_id}`, {
          method: "DELETE",
          headers,
        });
        return handleResponse(res);
      }

      case "list": {
        const query = new URLSearchParams(options).toString();
        const res = await fetch(`${BASE_URL}/jobs?${query}`, { headers });
        return handleResponse(res);
      }

      default:
        return { error: true, message: `Unknown action: ${action}` };
    }
  } catch (err) {
    return { error: true, message: err.message.slice(0, 500) };
  }
}

async function handleResponse(res) {
  const data = await res.json();
  if (!res.ok) {
    return {
      error: true,
      status: res.status,
      code: data?.error?.code,
      message: data?.error?.message,
      remediation: data?.error?.remediation,
    };
  }
  return data;
}
```

This is optional — the SKILL.md-only version is fully functional and recommended for the initial release.

---

## Step 9: Monitor & Iterate Post-Launch

### Metrics to Track

- **ClawHub installs** — check via `clawhub inspect machinefi/trio-vision`
- **API usage from skill** — track in Trio console (console.machinefi.com)
- **GitHub stars** — on the repo
- **Community feedback** — OpenClaw Discord, GitHub issues

### Responding to Reports

ClawHub auto-hides skills after 3 community reports. If your skill gets flagged:
1. Check the reports for specifics
2. Fix the issue
3. Publish a patch version
4. The flag count resets on new versions

### Iteration Ideas

- Add example stream URLs for testing (publicly available live cameras)
- Add a "security camera starter" workflow for common home/business monitoring
- Add integration with OpenClaw's scheduled jobs for recurring checks
- Add webhook server setup instructions for advanced users

---

## Quick Reference: File Locations

| File | Purpose |
|------|---------|
| `~/.openclaw/skills/trio-vision/SKILL.md` | User-level skill install location |
| `./skills/trio-vision/SKILL.md` | Project-level skill install location |
| `~/.zshrc` or `~/.bashrc` | Where to persist `TRIO_API_KEY` |
| OpenClaw config | Alternative API key storage via `skills.entries.trio-vision.apiKey` |

## Quick Reference: Commands

```bash
# Local testing
openclaw skills list --eligible
openclaw skills info trio-vision
openclaw skills check

# Publishing
clawhub login
clawhub publish ./trio-vision-skill --slug machinefi/trio-vision --version 1.0.0
clawhub inspect machinefi/trio-vision

# User installation (after publishing)
openclaw skills install machinefi/trio-vision
```

---

## Summary: Ship Checklist

- [x] **Step 1**: Skill structure created (SKILL.md)
- [ ] **Step 2**: Local testing with real Trio API key
- [ ] **Step 3**: Iterate on skill based on testing
- [ ] **Step 4**: Prepare GitHub account and ClawHub auth
- [ ] **Step 5**: Publish to ClawHub
- [ ] **Step 6**: Distribute (GitHub, docs, Discord, awesome list)
- [ ] **Step 7**: Set up version management workflow
- [ ] **Step 8**: (Optional) Upgrade to JavaScript handler
- [ ] **Step 9**: Monitor post-launch metrics and iterate
