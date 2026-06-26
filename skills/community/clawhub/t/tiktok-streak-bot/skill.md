---
name: tiktok-streak
version: 1.0.0
description: Browser-automated TikTok streak messaging skill using Playwright. Sends daily messages to configured usernames with state tracking, retry control, and optional content discovery via hashtags or keywords.
---

# TikTok Streak Skill

## Purpose

Send daily streak messages to a list of TikTok usernames using browser automation.

## Execution Flow

1. Load config and state
2. Initialize browser session using stored cookies
3. Validate session (TikTok homepage load)
4. Load usernames list
5. Filter users already processed today
6. For each remaining user:
   - Generate message (text or discovered content)
   - Send message via TikTok inbox
   - Update state
7. Persist updated cookies and state
8. Exit

## Features

### 1. Daily Streak Messaging

- Sends one message per user per day
- Default message: random short text

### 2. Content Discovery (Optional)

- If enabled in config:
  - Fetch random TikTok video using keyword/hashtag
  - Send link instead of text

### 3. State Tracking

- Prevent duplicate sends within same day
- Store last sent timestamp per username

### 4. Failure Handling

- Retry up to N times per user
- Skip on repeated failure

## Constraints

- Max users per run configurable
- Random delays between actions
- Session must be valid (cookies)

## Outputs

- Logs per execution
- Updated state.json
- Updated cookies.json

## Setup & Usage Instructions

### 1. Identify Target Users
Provide the profile usernames you would like to keep a streak with by creating a list in `data/usernames.json` (e.g. `["friend1", "friend2"]`).

### 2. Provide Authenticated Cookies
Export your TikTok authenticated browser cookies utilizing a standard browser extension (like "EditThisCookie") and save the JSON array securely within `data/cookies.json`.

### 3. Configure Execution
Optionally edit `data/config.json` to change default bot behaviors:
- Set `"enable_discovery": true` to pull and send trending videos utilizing your `"keywords"` list instead of plain generic text strings.
- Keep `"headless": true` to silently run in the background without UI interruption, or set to `false` to view the graphical browser UI during processing.

### 4. Run the Bot
Ensure all requirements are installed:
```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

Launch the skill via:
```bash
python scripts/main.py
```
