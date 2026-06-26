# Sources and refresh notes

This skill was built from first-party Resend sources and the public Resend CLI source tree.

## Primary sources

### Official CLI announcement

Used for:

- release date
- install methods
- “built for humans and AI agents”
- 53 commands across 13 resources
- natural-language scheduling examples for broadcasts
- profile switching and CI-oriented JSON output positioning

URL:
- https://resend.com/changelog/cli

### CLI repository README

Used for:

- auth priority
- login behaviour
- config paths and permissions
- `doctor`
- global flags
- machine-mode contract
- Node 20+ local-dev note
- current release pointer

URL:
- https://github.com/resend/resend-cli

### CLI source files

Used for exact command surfaces and agent-relevant implementation details.

Representative files:

- `src/lib/output.ts`
- `src/lib/client.ts`
- `src/lib/config.ts`
- `src/lib/pagination.ts`
- `src/commands/emails/send.ts`
- `src/commands/emails/batch.ts`
- `src/commands/emails/receiving/*.ts`
- `src/commands/domains/*.ts`
- `src/commands/webhooks/*.ts`
- `src/commands/broadcasts/*.ts`
- `src/commands/templates/*.ts`
- `src/commands/contacts/create.ts`
- `src/commands/topics/create.ts`
- `src/commands/segments/create.ts`
- `src/commands/api-keys/create.ts`

Repository root:
- https://github.com/resend/resend-cli

### Official product/API docs

Used for underlying Resend platform semantics that still matter when the CLI is the chosen surface:

- webhook verification with Svix and raw body handling
- exact-domain mismatch behaviour
- `resend.dev` restrictions
- scheduling limits
- inbound/receiving behaviour
- MCP as a valid fallback surface

Representative URLs:

- https://resend.com/docs/api-reference/introduction
- https://resend.com/docs/webhooks/verify-webhooks-requests
- https://resend.com/docs/knowledge-base/403-error-domain-mismatch
- https://resend.com/docs/dashboard/receiving/introduction
- https://resend.com/docs/mcp-server
- https://resend.com/changelog

## Refresh checklist

When updating this skill:

1. check the latest release version
2. re-read the README auth/output sections
3. inspect `emails send` for hosted-template flags
4. inspect `domains update` for receiving/sending capability toggles
5. inspect `listen` commands for output/stream changes
6. re-test the stderr/stdout JSON behaviour
7. update the command catalogue and gap map accordingly
