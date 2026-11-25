<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Emails

## `attio api emails-list [options]`

- What: List emails
- Call: `GET /v2/emails`, effect: read
- Sign-in: oauth2 (email:read, record\_permission:read, object\_configuration:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--linked-object <value>` | no | linked\_object |
| `--linked-record-ids <value>` | no | linked\_record\_ids |
| `--participants <value>` | no | participants |
| `--domain <value>` | no | domain |
| `--sent-after <value>` | no | sent\_after |
| `--sent-before <value>` | no | sent\_before |
| `--exclude-automated-participants <value>` | no | exclude\_automated\_participants |
| `--all` | no | read every page, as the API pages it |
