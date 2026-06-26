---
name: QClaw
description: Summarize noisy WeChat group chats into decisions, action items, mentions, risks, and tracked keywords for OpenClaw workflows.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💬"
---

# QClaw

QClaw is a WeChat group chat signal extraction skill.

Use this skill when the user wants to:
- summarize a WeChat group chat
- extract decisions and action items
- track keywords such as project names, clients, or deadlines
- identify direct or implicit mentions that may need attention
- detect conflict, urgency, or risk in busy group discussions

## What this skill does
- compresses long group conversations into short, useful summaries
- separates signal from noise
- extracts decisions, tasks, blockers, and next steps
- highlights mentions of tracked keywords
- identifies messages that likely require the user's attention

## How to use

### Prerequisites
- OpenClaw installed
- A WeChat group chat log pasted as text, or exported as txt/json
- Optional tracked keywords supplied by the user

### Accepted input
- plain text chat log
- JSON array of messages with timestamp, sender, and content
- copied chat transcript

### Best output structure
1. Executive summary
2. Decisions made
3. Action items
4. Mentions and keyword hits
5. Risks / conflicts / urgency
6. Suggested follow-up

## Privacy & Security
- Prefer anonymized or redacted chat logs when possible
- Do not retain chat content longer than needed for the current workflow
- Mark uncertainty clearly
- Never fabricate missing context

## When NOT to use QClaw
- personal 1-on-1 chats
- groups with very few messages
- real-time alerting workflows
- legal or compliance workflows requiring verbatim records
