# Delivery Backends

Controls where session summaries and final materials are sent when a session closes.

## Configuration: `~/.review-agent/profile/delivery_targets.json`

```json
{
  "on_close": [
    {
      "name": "boss-lark-dm",
      "backend": "lark_dm",
      "open_id": "ou_xxxxxxxxxxxxxxxxxx",
      "payload": ["summary", "final"],
      "role": "boss"
    },
    {
      "name": "briefer-lark-dm",
      "backend": "lark_dm",
      "open_id": "{{BRIEFER_OPEN_ID}}",
      "payload": ["summary"],
      "role": "briefer"
    },
    {
      "name": "archive-local",
      "backend": "local_path",
      "path": "~/Documents/review-archive/{{YYYY}}-{{MM}}/{{session_id}}/",
      "payload": ["summary", "final", "conversation", "annotations", "dissent"]
    },
    {
      "name": "boss-email-major",
      "backend": "email_smtp",
      "to": "admin@example.com",
      "subject": "[Review] {{session_subject}} — closed {{termination}}",
      "body_source": "summary",
      "payload": ["summary", "final"],
      "role": "boss",
      "filter": {"tags_any": ["major", "funding", "board"]}
    }
  ]
}
```

### Fields

- `name`: human label
- `backend`: one of `lark_dm`, `local_path`, `email_smtp`, `lark_doc` (v1), `gdrive` (v1)
- `role`: `boss` or `briefer` — used for routing double-delivery on close (G1)
- `payload`: array of what to include. Options:
  - `summary` — `sessions/<id>/summary.md`
  - `final` — `sessions/<id>/final/*` (briefer's last-uploaded final)
  - `conversation` — `sessions/<id>/conversation.jsonl`
  - `annotations` — `sessions/<id>/annotations.jsonl`
  - `dissent` — `sessions/<id>/dissent.md`
- `filter` (optional): deliver only if session matches. Available filters:
  - `tags_any`: session tags include any of these
  - `tags_all`: session tags include all of these
  - `termination`: `mutual` or `forced_by_briefer`

### Variable substitution

- `{{session_id}}`, `{{session_subject}}`, `{{briefer_open_id}}`, `{{BRIEFER_OPEN_ID}}`
- `{{YYYY}}`, `{{MM}}`, `{{DD}}`, `{{termination}}`

## Backend specs

### `lark_dm`
- Uses `~/bin/lark_send` (or the in-repo `scripts/send-lark.sh` if not installed globally)
- Sends: a text/post message + (attempt) file — if file upload fails (app missing `im:resource:upload`), inline as `post` rich text with linked summary
- Reads tenant access token via openclaw `feishu` config

### `local_path`
- Simple file copy
- Creates subfolder per `session_id`
- Uses `{{YYYY}}-{{MM}}` for month bucketing

### `email_smtp`
- Calls `~/bin/send_mail`
- Summary is the body; final materials as attachments
- Requires `send_mail` configured with Gmail SMTP (see user memory `reference_send_mail_smtp.md`)

### `lark_doc` (v1, not implemented)
- Creates a Lark doc with the summary; shares with boss
- For "annotation_mode: lark-doc" mode, this is already the working surface

### `gdrive` (v1, not implemented)
- Uses `~/bin/gdrive` to upload to a named folder
- Can convert markdown → Google Doc if configured

## Minimum viable for v0

Implement only:
- `lark_dm` (both parties)
- `local_path` (always for archive)
- `email_smtp` (optional per filter)

v1 adds the Lark Doc and Gdrive backends.

## Failure handling

- Each delivery is attempted once. Failures are logged to `~/.review-agent/logs/delivery.jsonl`.
- Local archive MUST succeed before IM/email delivery (otherwise retry from disk later).
- If Lark DM to boss fails (e.g., token expired), fallback to email_smtp (if configured) and log.
- Briefer delivery failure does not block boss delivery (and vice versa).
