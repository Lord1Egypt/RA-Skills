# Command selection

Pick the primitive first. Then pick the CLI command sequence.

## Quick routing matrix

| Need | Use | Main commands | Notes |
| --- | --- | --- | --- |
| One logical transactional email | Emails | `emails send` | One email can still have multiple recipients |
| Update or cancel a scheduled transactional email | Emails | `emails update`, `emails cancel` | Keep the returned email ID |
| Up to 100 distinct transactional emails | Batch emails | `emails batch` | Requires a JSON file; no attachments or `scheduled_at` |
| Campaign/newsletter to a group | Broadcasts | `broadcasts create`, `broadcasts send` | Pair with segments and usually topics |
| Reusable hosted template lifecycle | Templates | `templates create`, `templates update`, `templates publish` | Current CLI has an important direct-send caveat |
| Verified sender or receiving domain | Domains | `domains create`, `domains verify`, `domains get`, `domains update` | DNS changes still happen outside the CLI |
| Scoped credentials | API keys | `api-keys create`, `api-keys list`, `api-keys delete` | Prefer narrow `sending_access` keys |
| Recipient profile data and targeting | Contacts / Topics / Segments / Contact properties | `contacts *`, `topics *`, `segments *`, `contact-properties *` | Use segments over deprecated audiences |
| Real-time app notifications | Webhooks | `webhooks create`, `webhooks update`, `webhooks listen` | Save signing secrets immediately |
| Inbound message processing | Receiving + Webhooks | `emails receiving *` plus `webhooks *` | Fetch full message and attachments separately |
| Environment diagnosis | Doctor | `doctor` | Usually the fastest first check |

## Decision notes

### `emails send` vs `emails batch`

Use `emails send` when it is one logical message, even if `--to` contains multiple recipients.

Use `emails batch` when you truly have many **distinct** messages and you want to submit up to 100
of them in one request.

### Transactional vs campaign

Use `emails send` / `emails batch` for user-specific, operational, or application-driven messages.

Use `broadcasts create` / `broadcasts send` when the message is a campaign to a defined segment and
should respect marketing-style subscription state.

### Topics vs segments

- **Topics** are recipient-facing preference categories.
- **Segments** are sender-controlled targeting groups.

They complement each other rather than replacing each other.

### Webhook local dev

Use `webhooks listen` when the user needs a live local loop with a public tunnel URL and optional
forwarding to a local app.

### Inbound dev loop

Use `emails receiving listen` when the user wants to observe inbound mail arrival over time.

### Templates

Use `templates *` for the hosted draft/publish lifecycle, but check
`references/templates-and-coverage-gaps.md` before promising a pure CLI send-by-template workflow.
