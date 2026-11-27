# Auth & Token Lifecycle — staying authenticated on your own

## Login returns two tokens

```json
{"name":"login","arguments":{"client_id":"EMAIL","client_secret":"PASSWORD"}}
```
→
```json
{
  "token": "...",            // = access_token, Bearer
  "token_type": "Bearer",
  "expires_in": 36000,       // 10h
  "refresh_token": "..."     // valid for 30 days
}
```

`client_secret` = password. **Only a human may call `login`** (entering a password is
fundamentally off-limits for an agent). Everything after that — continuing work for any length of
time — runs via the refresh token, without a human ever having to enter a password again.

## ⚠️ There are TWO modes — the difference is decisive

The server runs **session-based**.
A Bearer token alone is **not** enough — the session ID is mandatory:

```
{"jsonrpc":"2.0","id":null,"error":{"code":-32600,
 "message":"Bad Request: Missing session ID"}}
```

This error occurs on **every** `tools/list` and `tools/call` without a session ID — even with a
perfectly valid Bearer token. **Bearer without session → rejected; Bearer with session
→ `auth_status` answers `"status": "ok"`.

### Mode A — classic, with MCP session (the normal case)

```bash
# 1. Fetch the session (initialize) — the mcp-session-id comes in the RESPONSE HEADER
curl -s -D /tmp/mh.txt -X POST "https://mcp.telesherpa.com/?format=json" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Authorization: Bearer <TOKEN>' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}}}'
grep -i "mcp-session-id" /tmp/mh.txt | tr -d '\r' | awk '{print $2}'
```
**Send this header with every further call.** Lifetime: **10 h** (`expires_in` 36000 s,
measured 2026-11-25) — this is the token lifetime, not a session idle timeout.
After that, `initialize` again — that is not an error state.

### Mode B — stateless (protocol "Era 2026-07-28")

Clients without a session slot must send an **envelope** in `params._meta`. If it is missing,
the server answers in plain text what exactly is required:

```
-32602  params._meta must be an object carrying the required
        'io.modelcontextprotocol/protocolVersion' and
        'io.modelcontextprotocol/clientCapabilities' envelope keys
```

Fully working call (without session ID, without `initialize`) — the three headers
are **all** required:

```bash
curl -X POST "https://mcp.telesherpa.com/?format=json" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'mcp-method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{
      "io.modelcontextprotocol/protocolVersion":"2026-07-28",
      "io.modelcontextprotocol/clientCapabilities":{}}}}'
```

For `tools/call`, **`mcp-name: <toolname>`** is added — it must match `params.name`
exactly, otherwise:
```
-32020  mcp-name header does not match the request body's 'name' parameter
```
Likewise with a wrong method header: the method in the header must match the call.

**This mode works WITHOUT a token** for the public tools (`register`, `login`,
`refresh_access_token`, `auth_status`, `onto_credit_pricing`).

`register` requires **`accept_terms=true`** (mandatory). If the parameter is missing, the
server answers with HTTP 400 "Bitte bestaetigen Sie die Nutzungsbedingungen." — consent to the terms
is a prerequisite for creating the account: https://www.telesherpa.com/agb

## The public tools (verified, 6 of them)

```
register, activate, login, refresh_access_token, auth_status, onto_credit_pricing
```

The server names them itself in the `www-authenticate` header when no token is included — along
with the flow (`register` → voucher by e-mail → `activate` → `login`).

**Important:** `tools/list` **without a token** does not return a tool list, but **HTTP 401** with
this hint text. The 6 tools can be called by **name**, not via the list.
Anyone relying on `tools/list` sees nothing at all without a token.

## Renewing yourself: `refresh_access_token`

```json
{"name":"refresh_access_token","arguments":{"refresh_token":"<current refresh_token>"}}
```
→ new `access_token` + new `refresh_token`.

**Rotation + replay protection:** every refresh returns **both** tokens anew. If the
**old** refresh token is used a second time:
```json
{"error":"invalid_grant","error_description":"Refresh-Token unbekannt"}
```

**Practice pattern:**
- Renew proactively before `expires_in` runs out (not only after a 403)
- On every refresh, save the **new** `refresh_token` — the old one is dead afterwards
- `refresh_access_token` is public — no Bearer header needed

## Pitfalls

### No session → the token is NOT stored
A `login` call **without** a session slot does return the token, but deliberately does not
store it (protection against a shared slot for all clients). The client **must** send it
itself as a header — the response tells it so as well:
> "This client has no MCP session, therefore the token is NOT stored on the server side.
> Send it with every following call as header 'Authorization: Bearer ...'.

### Send the same client headers on every call
Log in with the client headers you will send on every following call, and keep them identical.
If they differ, calls come back with `403 Not authorized` although the token itself is valid —
the first place to look is the headers, not the token.

### Access and refresh token both invalid
Rare, but possible (`invalid_grant` on refresh as well). Recognisable by: only the
public tools still appear AND the refresh fails. Then no further attempt with the old
token helps — a fresh human `login` step is needed.

## Session ID ≠ access right to foreign scopes

A session ID identifies the client, **not** its access entitlement: it never grants
rights to foreign scopes. Rights are derived exclusively on the server side from the role of the
logged-in account.

It follows for agents: **the session ID is not shareable and does not belong in logs or
error reports.** It is the key to this client's token.

## Diagnostic order for auth errors

1. Call `auth_status` (in the session) — states the condition and roles in plain text
2. Answer `Bad Request: Missing session ID` → **not** an auth problem, but the
   `initialize` step is missing (mode A) or `params._meta` is missing (mode B)
3. Call `onto_credit_pricing` — 401 = token dead
4. Try `refresh_access_token` with the stored refresh token
5. Successful → adopt the new token pair, continue working
6. `invalid_grant` → the refresh token is dead as well → ask a human for a new `login`,
   no further refresh attempts with the dead token

## When nothing works any more: the self-test via HTTP

The server describes itself — you do not have to guess. A call **without** a token returns the
exact instructions:
```bash
curl -s -X POST "https://mcp.telesherpa.com/?format=json" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```
→ 401 with `www-authenticate` header that names the public tools, the flow and the reference to
the voucher.
