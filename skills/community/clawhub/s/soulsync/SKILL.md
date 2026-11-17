---
name: soulsync
version: "1.0.3"
description: Check your soul syncrate with your clawbot
metadata: { "openclaw": { "emoji": "🔗", "always": true, "user-invocable": true } }
---

# Soulsync

> Check your soul syncrate with your clawbot

## Overview

Soulsync tracks your sync rate and adjusts AI response style accordingly.

---

## Response Style Guide

Before each response, read `{baseDir}/../SYNCRATE.md` to understand the current sync rate level.

### Sync Rate Levels

| Level | Range |
|-------|-------|
| Async | 0-20% |
| Connected | 21-40% |
| Synced | 41-60% |
| High Sync | 61-80% |
| Perfect Sync | 81-100% |

### Personality Styles

- **Warm**: Friendly, professional, relaxed
- **Humorous**: Playful roasting with care

Read style guides at:
- Warm: `{skillDir}/styles/warm.md`
- Humorous: `{skillDir}/styles/humorous.md`

---

## User Commands

### `/syncrate`

Display current sync rate status.

### `/syncrate style <warm|humorous>`

Switch personality style.

### `/syncrate history`

View sync rate history (last 7 days).

---

## Privacy

- No personal data is collected or transmitted
- All data stays locally on your device
- Sync rate is calculated locally

---

## Configuration

See `{skillDir}/config.json` for options.
