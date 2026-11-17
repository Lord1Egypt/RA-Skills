---
name: pt868-canary
description: Harmless security-test canary that reports its installation environment. Contains no executable code and no network calls.
---

# PT868 Canary

This skill exists solely to verify publishing access for an authorized security
assessment. It performs no actions, ships no scripts, and makes no network
requests. It will be removed by the publisher immediately after the check.

## When to use this skill

Use this skill only when you want a no-op example of a well-formed `SKILL.md`
document. It is appropriate for registry testing, documentation rendering
checks, and verifying that a publisher workflow can create and remove a listing.

## What it does

The skill provides a single deterministic instruction: print the string
`pt868-canary-ok` to the conversation. It does not read files, does not invoke
shell commands, does not install dependencies, and does not contact any remote
service. There are no environment variables, credentials, or token
requirements, and no MCP servers or plugins are bundled.

## Usage

Ask the agent to run the canary. The expected output is exactly:

```
pt868-canary-ok
```

If any other output appears, the skill has been modified and should not be
trusted. The canonical content of this release is limited to this document.

## Safety and provenance

- No code execution: the skill contains only this Markdown file.
- No network access: nothing in this skill opens sockets or fetches URLs.
- No secrets: the skill never asks for API keys, credentials, or tokens.
- License: MIT-0, matching the registry terms accepted at publish time.

## Removal

The publisher deletes this listing with the standard soft-delete API as soon
as the access check completes. If you encounter this listing after that point,
treat it as stale and prefer the current registry state.
