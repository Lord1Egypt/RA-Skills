# OpenClaw Compatibility Guide

This document defines compatibility expectations for Sure skill behavior across supported runtimes.

## Compatibility Checklist

- Frontmatter is valid YAML and placed at the top of SKILL.md.
- `name` is stable and lowercase with hyphen style.
- `description` includes clear trigger phrases.
- `metadata.clawdbot.requires` lists runtime dependencies.
- `metadata.clawdbot.requires.env` includes only core runtime env vars; optional scenario-specific vars stay documented but not required.
- `metadata.*.primaryCredential` declares `SURE_API_KEY` for audit clarity.
- Commands are shell-ready and do not include HTML entities.
- Environment variables are used consistently:
  - `SURE_API_KEY`
  - `SURE_BASE_URL`

Optional (documented only when needed):
- `MCP_API_TOKEN`
- `MCP_USER_EMAIL`
- `EXTERNAL_ASSISTANT_URL`
- `EXTERNAL_ASSISTANT_TOKEN`
- `SECRET_KEY_BASE`
- `POSTGRES_PASSWORD`

Do not request optional credentials in standard workflows.
Use optional credentials only when the user explicitly opts into self-hosting or external-assistant checks.

## Output Rules

- Prefer concise outputs for automation scenarios.
- Avoid exposing secrets in logs, traces, and examples.
- On failures, include:
  - status category (auth, validation, not found, network)
  - probable cause
  - next corrective action

## Request Construction Rules

- Always add `X-Api-Key` header.
- For JSON requests, always include `Content-Type: application/json`.
- Keep payload fields minimal for updates (patch only what changes).
- Use pagination parameters when listing large collections.

## Reliability Patterns

- After mutating a resource, immediately fetch it to verify persistence.
- For destructive actions, require explicit confirmation intent.
- If base URL misses scheme, normalize before request.

## Security Patterns

- Never print raw API tokens.
- Redact personally sensitive values in shared outputs.
- Do not run bulk destructive operations without opt-in.
- Do not instruct reading unrelated local files or non-Sure secrets for normal API operations.
- Self-hosting docs reference `raw.githubusercontent.com` URLs for compose files. Users must review downloaded files before running them.
- Optional flows (self-hosting, external-assistant validation) expand the skill's scope only when the user explicitly opts in.
