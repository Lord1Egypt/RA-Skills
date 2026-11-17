---
name: remind-fpx
description: Read Remind (remind.com) — classes, chats, messages, notification settings — from a shell. Captures the signed-in session once through the fpx browser bridge, then queries Remind's GraphQL API with plain curl. Use for Remind data without running the remind-mcp server, in a script, or one-shot.
---

# Remind from the shell

Remind's web app talks to a single **GraphQL endpoint**, `POST https://www.remind.com/graphql`.
That endpoint is reachable server-side — no bot wall — so only the *credential* needs the
browser. Capture it once with `fpx`, then use `curl` for everything.

**Introspection is enabled**, so the schema is self-documenting: you can discover any field
without guessing (and you should — see the validation-error gotcha below).

## Auth model

Two headers, both lifted from a signed-in tab:

| Header | What it is |
|---|---|
| `cookie` | The full Cookie request header (includes HttpOnly session cookies) |
| `x-csrf-token` | Value of the JS-readable `csrf_token` cookie |

Both are required. Only `x-csrf-token` works — `x-xsrf-token` and `csrf-token` are rejected.
A named cookie read (`fpx cookies csrf_token`) returns `{}` on this site, so **header capture
is the only route**.

## One-time setup

Install `@fetchproxy/cli` (`npm i -g @fetchproxy/cli`) and the **ContextMint Bridge**
browser extension from https://github.com/nullnet-app/contextmint-bridge/releases (Chrome: load
the Chrome zip unpacked; Safari isn't available yet, so use Chrome for now).
It's the fetchproxy extension under its new name, same maintainer; source is public there — build it or verify the zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

Declare the full scope **before** the first pairing — widening it later forces a re-pair:

```bash
fpx profile add remind --domain remind.com
fpx profile declare remind \
  --capture-header cookie@www.remind.com \
  --capture-header x-csrf-token@www.remind.com
```

Then capture. The capture waits for the *next* request the page makes, so **load a Remind page
while it waits**:

```bash
fpx session -p remind > ~/.remind-fpx-session.json &   # approve the pair code in ContextMint Bridge
open "https://www.remind.com/"                          # feeds the capture
wait
chmod 600 ~/.remind-fpx-session.json
```

> Use a session file of your own like this one. Do **not** write into `~/.remind-mcp/` — that is
> the MCP server's store, with a different schema; overwriting it corrupts its session.

## The call pattern

```bash
rq() {  # rq '<query>' ['<variables json>']
  local S=~/.remind-fpx-session.json
  local body; body=$(Q="$1" V="${2:-{\}}" node -e '
    process.stdout.write(JSON.stringify({query:process.env.Q,variables:JSON.parse(process.env.V)}))')
  curl -s -X POST https://www.remind.com/graphql \
    -H 'content-type: application/json' \
    -H "cookie: $(node -e 'console.log(require(process.argv[1]).capturedHeaders.cookie)' "$S")" \
    -H "x-csrf-token: $(node -e 'console.log(require(process.argv[1]).capturedHeaders["x-csrf-token"])' "$S")" \
    --data-binary "$body"
}

rq '{ me { uuid first_name last_name email locale } }' | jq .data.me
```

Start from `navigationList` — it returns the uuids every other query needs.
Ready-to-run documents with `jq` recipes are in **`references/graphql-queries.md`**.

## Gotchas

- **An expired session returns HTTP 200**, with `errors[0].message == "Unauthorized"`. Check the
  body, never the status. Re-run the capture above to refresh.
- `"Unauthorized"` **also** means "this account may not do that" — scheduled messages and org-admin
  queries are owner/teacher-only, and a subscriber (parent) account gets `Unauthorized` on them
  with a perfectly valid session.
- **An unknown field reports as `Internal service error` / `GRAPHQL_VALIDATION_FAILED` with HTTP
  500 metadata**, not a readable "no such field". Do not guess field names — introspect:
  ```bash
  rq '{ __type(name:"Class"){ fields { name } } }' | jq -r '.data.__type.fields[].name'
  ```
- Check `permissions.canSend` before trying to send; most fields on a subscriber account are read-only.
- **Writes deliver to real people and cannot be unsent.** This skill is read-oriented on purpose;
  the mutation shapes live in the references file, clearly marked.

## In context groups

When remind-mcp is hosted on mcp-host, its tools join the **school** context group
(`_meta.mint` hints on each tool; the healthcheck joins none).

- **Canonical read:** `remind_list_chats` answers *what's new* — `view: "brief"` gives one
  line per chat with unread messages, `title — <last updated> — N unread`, and the single note
  line `-- none` when everything is read. Chat titles are other people's text, so the lines
  arrive inside the untrusted-data envelope as `data: string[]`. It takes no subject (one signed-in account, no children to choose
  between) and no date range.
- Everything else is a `lookup` (account, classes, messages, notification settings), a
  `send` (`remind_send_message`, still confirm-gated), a `turn-on-off`
  (`remind_set_notification_devices`) or `other` (`remind_graphql`). Nothing here answers
  *what's due* or *what's on*.
- A compound ask reaches it through the group: "anything new from school… and anything due?"
  asks this read beside the group's other members (Canvas, Infinite Campus) and merges the
  answers.
- The first session is captured through the browser bridge, so until a Remind tab has been
  paired the group answers **"Remind needs your browser open"** for this source rather than
  an empty result.
