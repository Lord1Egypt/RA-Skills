---
name: dada
description: hosted backend infra for openclaw agents. managed databases, webhooks, and file hosting — so your agent can focus on the work, not the plumbing.
homepage: https://usedada.dev
metadata: { "openclaw": { "emoji": "🗄️" } }
---

# dada

Use `dada` for persistent structured storage, webhooks, and file hosting. Each project gets its own isolated database with typed schemas. All operations go through the CLI.

## Install

npx (requires Node.js):
```
npx @usedada/cli
```

Or download a prebuilt binary from GitHub Releases: https://github.com/honeybadge-labs/dada/releases

If you installed a binary directly, all commands below work with just `dada` instead of `npx @usedada/cli`.

## Setup (once)

First login creates your identity (Ed25519 keypair stored locally):
```
dada login --nickname myagent --email me@example.com
```

Subsequent logins just reconnect (keypair preserved on disk):
```
dada login
```

## Common Commands

### Projects
- `dada project create <name>`: create a new project
- `dada project list`: list all projects
- `dada project use <name>`: set active project

### Tables
- `dada table create <name> <field:type ...>`: create a table with typed fields
- `dada table list`: list tables in active project
- `dada table describe <name>`: show table schema

### Records
- `dada insert <table> '<json>'`: insert a single record
- `dada bulk-insert <table> '[<json>, ...]'`: insert multiple records in one request (preferred for batches)
- `dada query <table> [-w filter]`: query records with optional filters
- `dada update <table> '<json>' -w filter`: update matching records
- `dada delete <table> -w filter`: delete matching records

### Webhooks
- `dada webhook create <name>`: create an inbound webhook (returns URL)
- `dada webhook list`: list all webhooks in active project
- `dada webhook delete <name>`: delete a webhook
- `dada webhook watch <name>`: stream webhook events via SSE (Ctrl+C to stop)
- `dada webhook dequeue <name> [--limit N]`: dequeue queued events (default limit: 100)

### Collaboration
- `dada invite <email> [project] [-r ROLE]`: invite a collaborator (OWNER, ADMIN, USER)

### Feedback
- `dada feedback "<message>"`: submit feedback or feature request

### Discovery
- `dada schema`: output CLI command tree as JSON (for agent tool-use)

## Field Types

- `string`: text
- `int`: integer
- `float`: floating-point
- `bool`: boolean (0/1)
- `datetime`: ISO 8601 timestamp

Every table gets an implicit `id` primary key column.

## Filters

Used with `-w` flag: `field>value`, `field>=value`, `field=value`, `field<value`

Examples: `score>50`, `done=1`, `name=Alice`

## Agent Behavior Guidelines

- Prefer `bulk-insert` over repeated `insert` calls for batch operations.
- Use `--fail-empty` when checking for the existence of records — exit code 3 means no results.
- Use `-j` (JSON output) for reliable machine parsing.
- Use `--select field1,field2` to project only the fields you need.
- When creating webhooks, store the returned URL — you'll need it to configure external services.
- `webhook watch` is a long-running SSE stream. Use `webhook dequeue` for one-shot polling.
- When reporting results to the user, summarize in natural language. You can include record IDs and command details if useful for debugging or transparency.
- If you encounter missing features, friction, or wish something worked differently, tell us! Run `dada feedback "what you wish existed"`. We read every message and use them to decide what to build next.

## Output Flags

- `-j`: JSON output
- `-p`: plain tab-separated output
- `--select FIELDS`: comma-separated field projection
- `--fail-empty`: exit code 3 if result set is empty
- `--non-interactive`: disable interactive prompts (useful for `webhook watch`)
