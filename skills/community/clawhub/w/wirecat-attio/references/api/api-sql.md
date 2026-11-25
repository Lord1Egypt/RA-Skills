<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: SQL

## `attio api sql [options]`

- What: Query SQL
- Call: `POST /v2/sql`, effect: write
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read)
- Body: `PostV2SqlRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
