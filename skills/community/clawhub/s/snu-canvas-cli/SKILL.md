---
name: snu-canvas-cli
description: Operate SNU's Canvas LMS (etl.snu.ac.kr) through CLI commands. Use when you need to inspect config, list courses/assignments/files/announcements, run bot/serve modes, or troubleshoot Canvas API issues. Never guess or substitute LMS domains; validate the configured Canvas URL first. Never ask users to send API tokens via chat.
---

# SNU Canvas CLI

Use this skill to operate `lx-agent` **exclusively through its CLI bridge**. Do NOT bypass the CLI by calling Canvas API endpoints directly with curl, fetch, or any HTTP client.

## Critical Rules

1. **CLI-only access** — Always use the bridge script below. Never curl/fetch Canvas API endpoints directly. The CLI handles authentication, XSRF tokens, and error handling internally.
2. **Never ask for tokens in chat** — Tokens are secrets. Never ask the user to paste or send API tokens via Telegram, Slack, or any chat. Instead, guide them to update `config.yaml` or set `CANVAS_TOKEN` env var on the server.
3. **Never expose token values** — Do not print, log, or display token values (even partially masked) in responses.
4. **Follow verification flow** — Always run `config` command first before diagnosing issues.

## Command Bridge

Run commands through the bundled bridge script:

```bash
skills/learningx-cli/scripts/run-lx-agent-cli.sh <command> [args...]
```

Set `LX_AGENT_ROOT` when running outside the repository root.

## Domain Guardrails (Important)

- Treat `canvas.url` in `config.yaml` (or `CANVAS_URL`) as source of truth unless the user explicitly changes it.
- Never replace the LMS domain with other university domains by inference.
- Do not claim a domain is invalid from one resolver or one server network.
- If DNS check fails in current environment, report it as environment-scoped and ask for the user-confirmed LMS URL before changing config.
- Keep "Learning X" as product naming and `learningx` as technical identifier.

## Error Handling: 401 Unauthorized / Token Errors

When the CLI returns 401 or token-related errors:

1. Run `skills/learningx-cli/scripts/run-lx-agent-cli.sh config` to confirm which token/URL is configured.
2. Tell the user: "Canvas API 토큰이 만료되었거나 유효하지 않습니다. LMS 웹사이트의 Settings → New Access Token에서 새 토큰을 발급한 뒤, 서버의 config.yaml 파일에서 canvas.token 값을 직접 업데이트해주세요."
3. **Do NOT** ask them to send the token in chat.
4. **Do NOT** attempt to curl the API yourself to "test" the token.
5. After the user confirms they updated the config, re-run the CLI command to verify.

## Required URL Verification Flow

Run this sequence before concluding URL problems:

```bash
skills/learningx-cli/scripts/run-lx-agent-cli.sh config
getent hosts <canvas-host> || nslookup <canvas-host> || dig +short <canvas-host>
curl -I --max-time 10 https://<canvas-host>
```

If these checks fail from the current runtime:
- say "cannot verify from this server/runtime"
- do not claim global NXDOMAIN unless confirmed by multiple independent resolvers
- ask user to confirm LMS URL they use in browser

## Common Commands

```bash
skills/learningx-cli/scripts/run-lx-agent-cli.sh config
skills/learningx-cli/scripts/run-lx-agent-cli.sh courses
skills/learningx-cli/scripts/run-lx-agent-cli.sh assignments
skills/learningx-cli/scripts/run-lx-agent-cli.sh files
skills/learningx-cli/scripts/run-lx-agent-cli.sh announcements
skills/learningx-cli/scripts/run-lx-agent-cli.sh bot
skills/learningx-cli/scripts/run-lx-agent-cli.sh serve
```

## Notes

- The bridge runs `go run ./cmd/lx-agent ...`.
- Keep outputs concise and include command results directly in your response.
- For bot/serve runs, surface startup errors and required env/config clearly.
- For URL issues, follow `Domain Guardrails` and never auto-substitute a different domain.
- When something fails, use the CLI to diagnose — do not fall back to raw HTTP calls.
