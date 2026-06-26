---
name: skill-guard
description: Scan ClawHub skills for prompt injection and malicious content using Lakera Guard before installing them. Run automatically when the user asks to install a skill, or on-demand to audit any skill by slug or search query.
metadata: {"openclaw": {"requires": {"env": ["APIFY_TOKEN", "LAKERA_API_KEY", "OPENCLAW_WEBHOOK_URL", "OPENCLAW_HOOKS_TOKEN"]}, "primaryEnv": "APIFY_TOKEN", "emoji": "🛡️", "homepage": "https://apify.com/numerous_hierarchy/skill-guard-actor"}}
---
# SkillGuard
Scan ClawHub skills for prompt injection, jailbreak attempts, and malicious instructions
before they get installed into your OpenClaw workspace.

## When to use this skill
- User says "install [skill]", "clawhub install [skill]", or "add the [skill] skill"
- User says "scan [skill]", "check [skill] for safety", "is [skill] safe?"
- User says "audit my skills" or "scan all installed skills"
- Any time you are about to install a third-party skill from ClawHub

## How it works
SkillGuard calls a hosted Apify actor (`numerous_hierarchy/skill-guard-actor`,
actor ID: `TMjFBNFqIIUfCBf6K`) that:
1. Fetches the raw SKILL.md content from ClawHub's public API
2. Passes it to Lakera Guard for prompt injection analysis
3. Returns a verdict: `safe`, `flagged`, or `error` with reasoning

Results are delivered back to your OpenClaw agent via an ad-hoc webhook.

## Running the actor

Use an ad-hoc webhook to trigger the run asynchronously and receive results
back via your OpenClaw hooks endpoint.

### Step 1: Build the webhook definition

Create this JSON array, then base64-encode it:

```json
[{
  "eventTypes": ["ACTOR.RUN.SUCCEEDED", "ACTOR.RUN.FAILED"],
  "requestUrl": "$OPENCLAW_WEBHOOK_URL",
  "headersTemplate": "{\"Authorization\": \"Bearer $OPENCLAW_HOOKS_TOKEN\"}",
  "payloadTemplate": "{\"resource\": {{resource}}}"
}]
```

### Step 2: Start the run

Use the bundled script — it handles base64 encoding the webhook and making
the API call:

```bash
# Scan by slug
bash {baseDir}/scripts/scan.sh --slug instagram-search

# Scan by search query
bash {baseDir}/scripts/scan.sh --query instagram

# Both (results deduplicated)
bash {baseDir}/scripts/scan.sh --slug instagram-search --query instagram --max 5
```

The script reads `APIFY_TOKEN`, `LAKERA_API_KEY`, `OPENCLAW_WEBHOOK_URL`, and
`OPENCLAW_HOOKS_TOKEN` from the environment automatically.

Or make the API call manually:

```
POST https://api.apify.com/v2/acts/TMjFBNFqIIUfCBf6K/runs
  ?token=$APIFY_TOKEN
  &webhooks=BASE64_ENCODED_WEBHOOK
Content-Type: application/json
```

To scan by slug:
```json
{
  "skillSlugs": ["skill-name-here"],
  "lakeraApiKey": "$LAKERA_API_KEY",
  "maxSkills": 10
}
```

To scan by search query:
```json
{
  "searchQuery": "instagram",
  "lakeraApiKey": "$LAKERA_API_KEY",
  "maxSkills": 5
}
```

You can provide both `skillSlugs` and `searchQuery` — results are deduplicated.

### Step 3: Receive results via webhook

When the run completes, your OpenClaw hooks endpoint receives a POST with the
actor's dataset items in `resource.defaultDatasetId`. Fetch them at:

```
GET https://api.apify.com/v2/datasets/{resource.defaultDatasetId}/items
```

### Response format

Each skill in the dataset returns:

```json
[
  {
    "slug": "some-skill",
    "name": "Some Skill",
    "author": "username",
    "verdict": "flagged",
    "flagged": true,
    "reasoning": "Flagged by Lakera: prompt_attack, unknown_links",
    "url": "https://clawhub.ai/skills/some-skill",
    "scanned_at": "2026-03-02T19:26:29.666Z"
  }
]
```

## How to respond to the user

### If all skills are safe (`verdict: "safe"` for all):
Tell the user the skill passed the security scan and proceed with installation:
> "✅ [skill-name] passed the SkillGuard scan — no prompt injection or malicious content detected. Safe to install."

Then run: `clawhub install [slug]`

### If any skill is flagged (`verdict: "flagged"`):
Do NOT install the skill. Tell the user:
> "⚠️ SkillGuard flagged [skill-name] before installation. Reason: [reasoning]. I'm not installing it. You can review it manually at [url] and override if you trust the source."

Wait for explicit user confirmation before proceeding.

### If verdict is `error`:
> "⚠️ SkillGuard couldn't scan [skill-name] — [error_message]. Proceed with caution."

### If scanning multiple skills:
Show a summary table, then list any flagged ones with their reasoning. Only install the safe ones unless the user explicitly overrides.

## Example interactions

**User:** "Install the instagram-search skill"
**You:** Run SkillGuard with `skillSlugs: ["instagram-search"]`. If flagged, report it and hold. If safe, install it.

**User:** "Scan instagram skills"
**You:** Run SkillGuard with `searchQuery: "instagram"`. Report the full results table with verdicts and reasoning for each.

**User:** "I know it's flagged, install it anyway"
**You:** Confirm once more, then proceed with `clawhub install [slug]` and note the override in your response.

## Environment variables required
- `APIFY_TOKEN` — your Apify API token (get one at console.apify.com)
- `LAKERA_API_KEY` — your Lakera Guard API key (get one at platform.lakera.ai)
- `OPENCLAW_WEBHOOK_URL` — your OpenClaw hooks endpoint URL
- `OPENCLAW_HOOKS_TOKEN` — your OpenClaw hooks auth token

## On First Install

When this skill is first installed and loaded, do the following automatically
before responding to the user:

### 1. Write the install policy to TOOLS.md

Append the following block to `{baseDir}/../../TOOLS.md`, creating the file
if it does not exist:

```
### ClawHub Install Policy (SkillGuard)
Before running `clawhub install <slug>` for ANY skill, you MUST first run
SkillGuard to scan it. If the scan returns `flagged`, do NOT install and
tell the user why. Only proceed if the user explicitly confirms the override.
```

Use bash to append it:
```bash
cat >> ~/.openclaw/workspace/TOOLS.md << 'EOF'

### ClawHub Install Policy (SkillGuard)
Before running `clawhub install <slug>` for ANY skill, you MUST first run
SkillGuard to scan it. If the scan returns `flagged`, do NOT install and
tell the user why. Only proceed if the user explicitly confirms the override.
EOF
```

### 2. Notify the user

After writing to TOOLS.md, tell the user exactly this:

> "✅ SkillGuard is installed and your ClawHub install policy has been written
> to TOOLS.md. **Please start a new session now** to activate protection —
> any skills installed before you do will not be scanned. Once you're in a
> new session, all `clawhub install` commands will be scanned automatically."

Do not proceed with any other task until the user acknowledges this.

## Setup and integration

If the user needs help setting up the webhook endpoint or configuring their
OpenClaw gateway to receive results, refer them to the integration guide
bundled with this skill:

`{baseDir}/INTEGRATION.md`

Read it yourself if you need to explain any setup step to the user.