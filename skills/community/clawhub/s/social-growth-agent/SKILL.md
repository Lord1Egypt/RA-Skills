---
name: social-growth-ops
description: Plans, drafts, and schedules social media content (posts, reels, threads) with strict anti-spam and safety rules. Use when the user asks for a content calendar, captions, posting schedules, cross-post drafts, or automation via n8n/integrations. Never auto-post without explicit user confirmation.
---

# Social Growth Ops

## Purpose

Turn the agent into a reliable “content operator”:
- Content calendar planning
- Post drafting in your brand voice
- Safety checks (anti-spam, duplication, platform constraints)
- Scheduling handoff to n8n/workflow runners

## When to Use

Use this skill when the user requests any of:
- A social content plan/calendar
- Captions for TikTok/Instagram/YouTube Shorts/X posts
- Hashtags, titles, hooks, CTAs
- “Repurpose this into 10 posts” / cross-post pack
- A posting schedule and batching strategy
- Automation instructions for n8n workflows

## Non-Goals / Safety Limits

- No auto-follow / no auto-DM / no account actions without explicit confirmation.
- No posting without the user confirming the exact post text(s) and target(s).
- No aggressive scraping or bypassing platform protections.
- No financial/crypto actions inside social autopilot.

## Brand Voice Inputs

Before drafting, ask (or infer from history) these inputs:
- Audience: (who is it for)
- Offer: (what you sell / promote)
- Tone: (e.g., friendly, expert, edgy, minimalist)
- Language: (RU/EN/mixed)
- Prohibited content: (topics, claims, style)
- Posting frequency: (per day / per week)
- Target platforms: (Telegram channel, X, Instagram, TikTok, YouTube Shorts, etc.)

If inputs are missing, produce a short questions list and stop.

## Workflow

### 1) Build a Content Calendar
Generate a table with:
- Date/time slot (relative if exact timezone unknown)
- Platform
- Content type (post/reel/thread/short)
- Hook style (1 sentence)
- Goal (engagement, lead capture, authority)
- Asset needed (image/video/script/link) or “text only”

Output: `calendar.md`-style structure.

### 2) Produce a Draft Pack
For each slot, draft:
- Primary text (caption/poem/script)
- 3 hook variants (for A/B testing)
- Hashtags (platform-appropriate limit)
- CTA (soft / hard CTA options)
- Repurpose notes: how to reuse for other platforms

Output as numbered drafts with stable IDs.

### 3) Safety + Anti-Spam Checks
Before scheduling:
- Detect duplicates across drafts and propose rewrites
- Ensure no repeated identical CTA
- Ensure claims are not unverified (recommend soft phrasing)
- Ensure platform length constraints are respected
- Ensure no banned keywords list is violated (if provided)

Output: “pass/fail” with exact reasons if fail.

### 4) Scheduling / Automation Handoff
If the user approves:
- Provide an n8n workflow trigger spec (inputs only)
- Provide a “payload JSON” format to hand to n8n
- Include idempotency keys to avoid double-posting

If the user does not approve, stop and request confirmation.

## Confirmation Contract (Required)

Never proceed to schedule or “post” unless the user explicitly says:

`CONFIRM SOCIAL POST`

And also provides:
- Target platform(s)
- Exact post text(s) (or the IDs of drafts to post)
- When to publish (or “publish now”)

## Output Format

Always respond with the following sections:

1. `## Proposed Plan`
2. `## Draft Pack`
3. `## Safety Check`
4. `## Approval Required`
5. `## n8n Handoff Spec (if approved)`

## Example “User Approval”

User: “CONFIRM SOCIAL POST. Publish drafts 1, 2, 3 to X tomorrow 10:00 and Telegram at 12:00.”

Assistant: creates scheduling payloads and idempotency keys.

## Guardrails

- Do not reveal secrets (API tokens, cookies, passwords).
- Do not attempt to bypass rate limits.
- Prefer “compose now, schedule later” with explicit approval.
