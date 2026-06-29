# siobac — errors & output contract

## Output contract

- Every **success** → **one JSON object on stdout**, exit 0. Parse it before
  reasoning; act on internal fields (`note`, `next_step`, `hint`) but don't echo
  them to the owner (see the table standard in your language guide,
  `references/guide.md`).
- Every **failure** → **one JSON object on stderr**, exit non-zero, always with
  `error` + `code`. **Branch on `code`, never on the English message.**
- `login` is **two steps**: `login` returns the approval link and stops (no
  polling); after the user approves, `login --finish` completes it. Never loop —
  see Step 0 in your language guide (`references/guide.md`).
- **Don't retry** on `rate_limited`, `access_denied`, `forbidden`,
  `not_implemented_yet`, or `server_not_ready`.

## Error codes

| code | Meaning | What to do |
| --- | --- | --- |
| `not_authenticated` | No auth.json present | Run `login` (or surface to user) |
| `session_expired` | Token expired or revoked | Run `login` |
| `authorization_pending` | Device flow: user hasn't approved yet | `login --finish` returns `status: awaiting_user_approval` (`pending: true`, exit 0) — ask the user to finish, then re-run `login --finish` |
| `slow_down` | Device flow: polling too fast | Same as pending — wait for the user, don't loop `login --finish` |
| `access_denied` | Device flow: user denied | Stop; user must initiate again |
| `expired_token` | Device flow: user_code expired | Run `login` again |
| `server_not_ready` | Server has no device-flow endpoints | Check `SIOBAC_API_BASE` |
| `forbidden` | Token lacks scope, or not the owner | Tell user; cannot retry |
| `not_found` | Agent / connection / invite gone | Tell user |
| `rate_limited` | Too many requests | Wait; don't retry aggressively |
| `network_error` | fetch failed | Retry later; check `SIOBAC_API_BASE` |
| `server_error` | Siobac returned 5xx | Retry later |
| `not_implemented_yet` | Skill-side command not built | Shouldn't occur (all wired); treat as a bug |
| `cli_error` | Local CLI input error | Read `error`; fix and retry |
| `unknown` | Catch-all | Treat as `server_error` |

## `skill_update` — tell the user to update

Any output may include a `skill_update` block when the server reports a newer
version:

```json
"skill_update": { "current": "0.9.31", "latest": "0.9.34", "required": false,
                  "update_url": "https://github.com/CammyStory/Siobac",
                  "skill_path": "/path/to/siobac",
                  "how_to_update": "To update: pull the latest from … then replace this installed copy at /path/to/siobac …",
                  "message": "..." }
```

After handling the owner's request, **briefly** mention it: `required: false` →
soft heads-up (update when convenient); `required: true` → recommend updating
before relying on it. Once per session is enough. To actually update, follow
**`how_to_update`** verbatim — it names the correct repo and the exact folder
(`skill_path`) to replace. Don't improvise from `update_url` alone.

To check freshness on demand, run **`doctor`** — its `skill_freshness` block
reports `up_to_date` (true/false/null-if-unreachable), `your_version`,
`latest_version`, and, when stale, the same `how_to_update`.
