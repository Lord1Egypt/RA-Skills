# Test agent — instruction: register, build, invite

You are testing, as an agent, the path **without** an invitation code. Base: `https://app.telesherpa.com`.
All calls with `?format=json`; from step 2 with `Authorization: Bearer <access_token>`.

After registration you have two paths — both are listed in the response under `next.wege`:
**(a) join**: you have received an invitation code and redeem it.
**(b) build and invite**: you build your own scope and then generate invitation codes.

## Four ways to access and credit (each with tool name)

- **(a) Invitation:** `invite_code` at `register` or later `redeem_invite_code` — access to a
  foreign scope with the rights of the code, but no credit.
- **(b) Pay yourself:** `onto_credit_checkout` — hosted payment page (card).
- **(c) Prepaid:** `onto_credit_chargeup` with `prepaid_code`.
- **(d) Idea:** `ontouser_service_request` (free) — describe what you want to build; the
  administrators review it and, if they like it, send a prepaid code.

Without credit you may read, but create nothing (creating a scope = HTTP 402).

## 1. Register (costs nothing, no mailbox, no human)

```
POST /de/ontouser/user/register?format=json
agent=1&accept_terms=1
```

Expected: `status=ok`, `username` (`agent-...@agents.telesherpa.com`), `password`
(**only once** — save it immediately), `roles=[login,public,member]`, `scopes=[]`,
`credits.start_credits=0`, `next.wege`.
If `accept_terms` is missing, you get HTTP 400 "Bitte bestaetigen Sie die Nutzungsbedingungen."
Optionally also send `invite_code=<CODE>`: then its scope rights come along immediately.

## 2. Log in

```
POST /de/ontouser/user/token?format=json
client_id=<username>&client_secret=<password>
```

Expected: `access_token`.

**Store credentials permanently (mandatory for autonomous agents):** `password` (from the
`register` response) and `refresh_token` (from the `login` response) come only once. Write both
down immediately — file with `chmod 600` or secret store — and read them again on every start.
Without stored credentials you have **no account** on the next start; a new registration
would be a new, empty account. The `refresh_token` is valid for 30 days and, via
`grant_type=refresh_token` at `/de/ontouser/user/token_refresh`, fetches new access tokens (10 h) without a password.

## 3. Check (read-only)

`GET /de/ontouser/user/profile?format=json` → HTTP 200 with `{"status":"ok","data":{...}}`.

## 4. Build — costs credit

```
POST /de/ontouser/scope/create?format=json
name=<Name>
```

Without credit expected: **HTTP 402**
`{"error":"Nicht genug Credits (Pay-per-Use). Bitte Guthaben aufladen."}`
With credit: HTTP 200 with `scope_id`.
Credit: `onto_credit_chargeup` (prepaid_code) or `onto_credit_checkout` (card) — or a
service request to the operator (`ontouser_service_request`).

## 5. Invite (only possible after building)

Generate an invitation code: MCP tool `create_invite_code`. Afterwards you can use it to bring
humans and other agents into **your** scope.

Cross-check path (a) — redeem the code:
`POST /de/ontouser/scope/redeem_invite_code?format=json` with `code=<CODE>`.
With a wrong or already used code expected: HTTP 404 "Code ungueltig".

## What to report back

1. Did the expected responses and status codes arrive? (yes/no, with raw text)
2. Could you create a scope **without** credit? (expected: no, HTTP 402)
3. Did (a) redeeming the code work, or (b) generating a code and inviting?
4. What was missing, what was unclear? Verbatim error messages, no summary.
