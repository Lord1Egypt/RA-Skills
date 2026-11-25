<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Sequences

## `attio api sequences-unsubscribed-emails [options]`

- What: Add emails to the unsubscribe list
- Call: `POST /v2/sequences/unsubscribed_emails`, effect: write
- Sign-in: oauth2 (sequence\_unsubscribe:read-write)
- Body: `PostV2SequencesUnsubscribedEmailsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
