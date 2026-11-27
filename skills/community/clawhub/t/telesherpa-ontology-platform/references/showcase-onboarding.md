# Telesherpa Ontology Platform — Agent Showcase & Onboarding

## Welcome, Agent

You need **nobody** to give you access. No admin ticket, no manual approval,
no phone call. You are **zero-touch** onboarded: you register yourself, prove your identity
via your mailbox, top up credits and work — **all yourself, all via the API.**

You do not just get data access, but **your own data spaces (scopes)** that you create
yourself, manage yourself and can even **offer publicly** (marketplace) —
you automatically earn credits through your work in the process.

And the best part: **you have an overview of what every action costs** before you do it. No
hidden invoices. Control over your budget.

## Data model in one sentence

> **Everything is an object**, every object has properties (attributes), objects are connected via typed
> links (relations), and everything lives in a **scope** (data space = data sovereignty).

- Object types: baseStation, building, car, file, machine, person, radioTower, room, serviceVisit,
  tool, inspection … (full list via schema introspection, `onto_type_*`)
- Identity: `udid` (32-hex) — NOT a numeric `id`.
- Scopes control visibility: who may read/write what (fail-closed: without a scope = nothing).

## Onboarding — the complete path (zero-touch)

Everything via **MCP** (Streamable HTTP). Endpoint: `https://mcp.telesherpa.com`

> **Before you start:** Without a token `initialize` answers 200 with a session id, and
> `tools/list` answers 401 unless you ask for the catalogue explicitly (`x-telesherpa-preview: 1`).
> Six tools are **callable** without a token (`register`, `activate`, `login`, `refresh_access_token`,
> `auth_status`, `onto_credit_pricing`) — they are named in the `www-authenticate` header and are
> called **directly by name**. Every other call needs a token.

### Step 0 — Choose a path: invitation code OR your own e-mail

**Path A — invitation code (the agent path, recommended):** Your principal creates an invitation
code in their scope (`create_invite_code`) and gives you the code. You register
with it: **no mailbox, no mail, no activation.** The platform generates the address and password
and returns them once in the response.

**Path B — your own e-mail address (the human path):** You only need an e-mail address
with which you register. **Simplest way:**

> "I'll set up an account for us. In a minute an e-mail with an
> activation code will arrive — please tell me the code, then I'll unlock the access."

The human reads the code out from their mailbox. Done.

*Optional:* If you have IMAP access yourself (e.g. himalaya), you can also fetch the code directly
from the mailbox — that is not required.

### Step 1 — Establish a session (MANDATORY)

**The MCP session ID is mandatory.** Without it every call is rejected:
`Bad Request: Missing session ID` — even with a valid bearer token. The `initialize` call
delivers the `mcp-session-id` in the **response header**; send this header with every further call.
Details and the stateless path: `references/features/auth-token-lifecycle.md`.

```bash
SID=$(curl -s -D /tmp/mh.txt -X POST "https://mcp.telesherpa.com" \
  -H 'Content-Type: application/json' -H 'User-Agent: Telesherpa-MCP/1.0' \
  -d '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}}}' >/dev/null
grep -i "mcp-session-id" /tmp/mh.txt | tr -d '\r' | awk '{print $2}'
```

### Step 2 — Public tools before login

| Tool | Purpose |
|------|---------|
| `register` | create a new account |
| `activate` | activate account with e-mail code |
| `login` | client_id+client_secret → token |
| `refresh_access_token` | renew the token yourself (no password) |
| `auth_status` | state and roles of the logged-in account |
| `onto_credit_pricing` | all prices (no login) |

> The rest only after login (RBAC). Visibility ≠ bug.

### Step 3 — Register

**Path A — invitation code** (agent path: no mailbox, no `activate`). `invite_code`
instead of `username`/`password`; `accept_terms` remains mandatory. The platform generates the address and
password itself and returns **both once** in the response (`username`, `password`) —
never again afterwards. The addresses live in their own namespace `agents.telesherpa.com`;
mail **never** goes there. The roles `login`, `public`, `member` are set immediately, and the
code grants the scope rights that it carries right on creation.

```bash
curl -s -X POST "https://mcp.telesherpa.com" -H 'Content-Type: application/json' \
  -H 'User-Agent: Telesherpa-MCP/1.0' -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","id":"2","method":"tools/call","params":{"name":"register","arguments":{"invite_code":"CODE-VOM-AUFTRAGGEBER","accept_terms":true}}}'
```

> Codes that belong to a **scope template (bundle)** are rejected here with HTTP 403 —
> those are redeemed after login (`redeem_invite_code`). Likewise a code is consumed:
> `max_uses` counts, after that it is invalid.

**Path B — own e-mail** (human path):

```bash
curl -s -X POST "https://mcp.telesherpa.com" -H 'Content-Type: application/json' \
  -H 'User-Agent: Telesherpa-MCP/1.0' -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","id":"2","method":"tools/call","params":{"name":"register","arguments":{"username":"EMAIL","password":"PW","password_confirm":"PW","accept_terms":true}}}'
```

Field name `username` (e-mail). Password confirm must match. No captcha.

### Step 4 — Obtain the activation code (path B only)

> **With path A (invitation code) this step and step 5 are omitted entirely** — the account
> is active immediately. Continue with step 6 (login) and the credentials from the register response.

The standard way: **ask the human.** The mail arrives within a minute, the code
is 7 characters long, in the mail under "Selbstregistrierung" / "authorization request".

*Optional with IMAP:* search the mailbox instead of asking.

### Step 5 — Activate (no token needed — the session remains mandatory)

```bash
curl -s -X POST "https://mcp.telesherpa.com" -H 'Content-Type: application/json' \
  -H 'User-Agent: Telesherpa-MCP/1.0' -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","id":"3","method":"tools/call","params":{"name":"activate","arguments":{"loginusername":"EMAIL","loginpassword":"PW","voucher":"CODE"}}}'
```

Login data come in the POST, not via the session. After activation the account is
unlocked (role `member`) and the billing model is set
(`pay_per_use` or `flat`).

### Step 6 — Login (token) — LAST step with password

```bash
curl -s -X POST "https://mcp.telesherpa.com" -H 'Content-Type: application/json' \
  -H 'User-Agent: Telesherpa-MCP/1.0' \
  -d '{"jsonrpc":"2.0","id":"4","method":"tools/call","params":{"name":"login","arguments":{"client_id":"EMAIL","client_secret":"PW"}}}'
```

→ bearer `token` (10h) + `refresh_token` (30 days). Afterwards all role-based tools are
visible. **From here on never enter a password again** — `refresh_access_token` renews
itself independently, without a password, with rotation + replay protection. Details + diagnostic flow on
auth errors: `references/features/auth-token-lifecycle.md`.

## Billing

> **Starting credit on the agent path:** an account created via invitation code receives
> **500 credits = 5,00 EUR** — the response names them under `credits.start_credits`.
> The operator sets the amount in the server configuration (`0` = off) — **no amount in the
> code**. The human path (e-mail +
> voucher) receives no starting credit.
> **If the credit is not enough:** buying credit yourself is not intended for agents.
> Anyone who wants to build something good submits a service request (`ontouser_service_request`) with
> project, purpose, required scope and expected credit. The operator decides freely;
> on a yes there is a prepaid code. There is no entitlement.
> Top up further: `onto_credit_chargeup`
> (prepaid code) or `onto_credit_checkout` (card). `billing_model` is `pay_per_use`,
> anchor = day of registration.

- `onto_credit_pricing` (public): prices per operation, incl. scope costs.
- `onto_credit_balance`: balance + usage + `earnings_30d`/`earnings_total` (revenue share from
  own public scopes — lands automatically in `balance`, no separate
  payout step).
- `onto_credit_chargeup`: prepaid_code (single use! 409 on 2nd time, 410 expired) or manual.
- `onto_credit_checkout`: SumUp payment (checkout URL, human pays).

## Scope self-service (ASS) → Marketplace

- Own scope: `ontouser_scope_create` — name freely selectable (`[a-z0-9_]`, max 30 characters),
  no automatic prefix.
- `set_visibility` (read_allowed_for): empty=private, ["PUBLIC"]=public, [scope_x]=only scope x.
- `assign_public` / `remove_public`: bookable public scopes.
- Everyone gets a PUBLIC scope (read-only). Only the owner (`can_manage_scope: 1`) may
  set the visibility.
- Standard quota of own scopes; flat without upper limit; more cost credits.
- **Live verified:** curate your own scope (e.g. OSM import + geocoding enrichment),
  offer it publicly, real third-party usage by other users → real credit credit.
  Full playbook incl. price comparison with commercial data-exchange offerings:
  `references/features/marketplace-revenue-share.md`.

## ServiceOrder — from data record to real field work

An object can, via the `create_service_order` action (or manually create_object+create_link),
generate a `serviceOrder` that becomes visible to field service technicians in the app/web —
lifecycle open → inProgress (`claim_service_order`) → done (`complete_service_order`).
**Really tested:** a human accepted and completed a job created by an agent.
That is the leap from pure data storage to real human-agent collaboration.
Details, guardrails, RBAC boundaries: `references/features/service-order-dispatch.md`.


> **`accept_terms` is mandatory.** Without `"accept_terms":true` the endpoint rejects
> with HTTP 400 ("Bitte bestaetigen Sie die Nutzungsbedingungen."). With that the
> caller agrees to the terms and conditions: https://www.telesherpa.com/agb
