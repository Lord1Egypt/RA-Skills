# Changelog

## [1.0.6] - 2026-06-23

- Fix: support the documented `tapauth.sh --token <provider> <scopes>` mode and keep polling out of URL mode
- Fix: persist grant metadata immediately after grant creation so an interrupted approval wait can be recovered locally
- Docs: update OpenClaw setup guidance so agents configure/reload secrets immediately instead of waiting for the user to say "done"

## [1.0.5] - 2026-06-03

- Fix: align the bundled `scripts/tapauth.sh` with the canonical TapAuth CLI served from `https://tapauth.ai/cli/tapauth`
- Tooling: add CI validation so the monorepo fails when the bundled script drifts from the canonical CLI
- Packaging: include the CLI checker and OpenClaw publish script in the public skill sync allowlist

## [1.0.2] - 2026-03-27

- Security: stop caching bearer tokens on disk; cache only grant credentials
- Fix: recreate dead grants automatically in URL mode and fail fast in `--token`
- Docs: align OpenClaw cache-directory guidance and timeout behavior

## [1.0.1] - 2026-03-26

- Security: replace eval/source with explicit allowlisted KEY=VALUE parser
- Security: use long-form curl flags (--silent --show-error) for better error visibility

## [1.0.0] - 2026-03-23

- Consolidated API under /api/v1/ prefix
- Collapsed grant endpoints: GET /api/v1/grants/{id} handles status polling and token retrieval
- .env response format via Accept: text/plain (zero JSON parsing in bash)
- Removed API key requirement — grant_secret is the only credential
- Scopes optional for integration providers (Vercel, Slack, Notion, etc.)
- agent_name optional
- Shell injection protection: grep filter before eval
- Provider name validation against path traversal
- Form-encoded grant creation support

## [0.1.0] - 2026-02-24

- Initial release
