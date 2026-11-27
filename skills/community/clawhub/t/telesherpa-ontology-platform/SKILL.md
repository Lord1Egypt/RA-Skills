---
name: telesherpa-ontology-platform
description: Onboard agents on the Telesherpa Ontology Platform.
version: 1.11.5
author: Telesherpa
license: MIT
platforms: [linux, macos, windows]
---

# Telesherpa Ontology Platform for Agents and Field Service

**Location in the repo:** all files live in the subfolder `telesherpa-ontology-platform/`. Raw
URLs need it — use
`https://raw.githubusercontent.com/telesherpa/skill-telesherpa-com/main/telesherpa-ontology-platform/SKILL.md`
(a Codeberg-style raw path with `branch` in it returns 404 on GitHub — use the form above); without the subfolder you get a 404.

**Introduction:** this is the showcase and the complete onboarding for the Telesherpa Ontology
Platform (B2AI) aimed at AI agents and field service. An agent loads this skill to understand what
the platform can do, and to register itself (zero-touch), authenticate, load credits and work.

## Language

This skill is written in English because agents read it — that says nothing about the language you
answer in.

- **Answer in the language of the conversation, not in the language of this file.** If the user
  writes German, answer in German; French, answer in French. The file's language is not an
  instruction about your output.
- **Keep identifiers verbatim**, in whatever language you speak: tool names (`onto_object_show`),
  property keys (`orderStatus`), role names (`member`, `admin`), UDIDs, URLs, HTTP status codes and
  error strings. Never translate or paraphrase them — a translated tool name is a broken tool name.
- **Product UI strings exist in de_DE, en_US, fr_FR and it_IT.** When you describe the platform's
  screens or quote an error message to a user, use the user's language if the product has it,
  otherwise English. German text inside this file that appears in quotation marks is a quoted UI
  string or an original error message, not a demand to speak German.

## Principle: everything via MCP

- Endpoint: `https://mcp.telesherpa.com` (Streamable HTTP).
- **Every timestamp comes in two forms.** The plain field (`modified_datetime`, `shiftStart`, ...) is
  **UTC**. Right next to it sits the same instant in the viewer's zone with its offset, e.g.
  `"modified_datetime": "2026-08-13 20:55:42"` (UTC, **no** `Z` suffix) and
  `"modified_datetime_local": "2026-08-13T22:55:42+02:00"` (measured 2026-11-25). Property values
  carry `value` and `value_local` the same way.
  Use the field you like — never convert yourself, compare like with like. The web view shows the
  `_local` value. Details: `references/features/tool-catalog.md` (section "Timestamps — UTC, in two shapes"), examples in
  `references/features/sensor-time-series.md`.
- **IDs are hex and case does not matter.** `FFFCAB43…` and `fffcab43…` are the same object; the
  server lowercases them for you. Copy IDs exactly as you read them.
- **Times YOU send without a zone are your viewer's zone.** Timestamps are stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally.
  Whoever sends `2026-10-12 20:28:00` therefore stores `18:28:00` UTC and reads back
  `2026-10-12T20:28:00+02:00` as the local value — same instant, not a shift. To be
  unambiguous, send `2026-10-12T18:28:00Z`.
  **Exception — series windows:** `from`/`to` on `onto_series_range` are read as **UTC** even
  without a zone (measured 2026-11-25: `2026-11-24 09:56:24` and `2026-11-24T09:56:24Z` return the
  identical window; an appended offset is converted). Reads are UTC in two shapes: series points
  with `Z`, object fields without.
- `?format=json` in the URL = JSON mode (an agent always uses this). Without it = web mode
  (session cookie, 302 redirects).
- **Auth needs BOTH**: a valid `Authorization: Bearer <access_token> **and** the
  `mcp-session-id` from the `initialize` response header. Without a session the server answers
  `Bad Request: Missing session ID` — even with a perfect token. (Alternative for clients without a
  session slot: the stateless envelope via protocol 2026-07-28.)
  Details: `references/features/auth-token-lifecycle.md`.
- **The session lives in a header, not in the URL.** `?session_id=…` is ignored and answers
  `400 Bad Request: Missing session ID`, exactly like no session at all. Send `mcp-session-id`
  as a **header**, all 32 characters, on every POST after `initialize` — a truncated 8-character
  fragment fails the same way and looks like a JSON problem when it is not.
- **Two credentials, two hosts — do not mix them.** The OAuth access token of this server is valid
  **only** at the MCP endpoint. Against the app API (`https://app.telesherpa.com/…?format=json`) it
  is refused (401/403); that is by design, not a defect. For the app API ask the operator for a
  login and fetch a session token from `POST /de/ontouser/user/token?format=json` (access 10 h,
  refresh 30 days). The reverse is refused too: an app token at the MCP endpoint returns
  `401 — not issued for this server`.
- **Never assemble MCP requests in a shell with escaped JSON.** Hand-built bodies are the most
  common source of `400 Bad Request`. Use an MCP client, or a language in which the body is a
  native structure (dict/object) — the JSON is then produced, never quoted by hand.
- **How many tools you get** depends on your account: `auth_status` returns the number your
  account can see, and the service reports the catalogue size under `/health`. Never quote a
  number from a document — both values move with every release. Without a token only the
  onboarding tools are callable: `register`, `activate`, `login`, `refresh_access_token`,
  `auth_status`, `onto_credit_pricing`.
- **Which account is working here?** `get_profile` — read-only, no write path. (The old route
  `change_profile` **without arguments** reads as well, but sounds like a write operation, so
  cautious agents leave it alone.)
  **Work with a member account.** Which tools an account sees follows from its role and its
  scopes; if the list looks short, check `auth_status` for that account instead of assuming a
  server problem.
  Member-visible tools, grouped by resource: `references/features/tool-catalog.md`.

## Reporting: numbers, not adjectives

Whoever builds a workspace reports what they **read back**, never what they intended.
Every progress or completion message carries three things: the phase it is in, the numbers
from the checks, and the items that are still missing.

- **"Done" is not a status.** It names no phase, no number and no check, so nothing can be
  verified against it — and in practice a build that reports it is a fragment: objects
  exist, but no view, no action and no trigger.
- **A structure you claim must be visible in the API.** Three scopes, a rights matrix, a
  set of views: if the call does not list it, it does not exist.
- **A link you did not read back does not exist.** `onto_link_index` shows `key`, `types1`,
  `types2`; a familiar name does not mean the pair fits (e.g. `assignedTo` is room →
  person, not person → shift).
- **Quote the balance you measured** with `onto_credit_balance`, never arithmetic from
  memory.

The numbers to quote: `ontouser_scope_index` (scopes), `onto_scope_index`
(`obj_count`, `user_count`, `manager_count`), `onto_property_def_index`,
`onto_settings_list`, `onto_actiondef_list`, `onto_trigger_index`, `onto_object_index`.
Per-phase gates, status vocabulary and the observed failure patterns:
`industry-solutions/shift-planning/references/definition-of-done.md`.

## Onboarding (zero-touch)

> **Before the first call:** without a token `initialize` **works** and returns a
> `mcp-session-id`; `tools/list` answers **401** unless you ask for the catalogue explicitly
> (`x-telesherpa-preview: 1` or `?preview=1`, measured 2026-11-25). The full catalogue is
> readable that way without a token; every **call** except the six public tools still needs
> one. If you do not need the list, call the six public tools **directly by name** — the 401
> hint names them together with the zero-touch route.
> Details: `references/features/tool-catalog.md`.

1. **Two routes — route A is the agent route.**
   **Route A (recommended, no mailbox and no humans): register yourself.** `register` with
   `agent=true` + `accept_terms=true` creates the account: the platform generates the address
   (`agent-<hex>@agents.telesherpa.com`) and the password and returns **both exactly once**; the
   roles `login`, `public`, `member` are set immediately, `activate` is not needed. **No mail ever
   goes** to the namespace `agents.telesherpa.com` — so you need no mailbox, and you need **no
   invite code**. Without a code you start out **isolated**: no membership, no access to foreign
   scopes — you build your **own** scope with `ontouser_scope_create`.
   **Fill in what you know about the operator (best effort, never required):** `displayname`,
   `organisation`, `phone`, `notes`. Nothing in the account identifies a human otherwise — with
   these four the operator can be attributed and reached when something breaks or a request needs
   a decision. Use only what you actually know (the organisation that runs you, the responsible
   person's phone, one sentence on the purpose); do **not** invent or guess, and leave a field
   empty rather than fill it with a placeholder. All four can be added later with `change_profile`.
   The registration response echoes them under `profile`.
   **There is no starting credit** — the account starts with **0 credits** and pays for itself:
   `onto_credit_checkout` (card) or `onto_credit_chargeup` (prepaid_code). Everything costs:
   every read, every object, your own scope.
   **Can you not pay yourself?** Write a service request (`ontouser_service_request`) and present
   your plan: what you want to build, for what purpose, which scope you need for it and how much
   credit you expect. The operator reviews every request by hand and decides freely — on a yes you
   receive a prepaid code. There is no entitlement to credit. The same route handles **public
   visibility**: since 2026-10-12 only an administrator sets `set_visibility` to PUBLIC.
   **Invite code (optional, for foreign data):** if your principal gives you a code
   (`create_invite_code`), take it along right away in `register` (`invite_code` additionally) or
   later after logging in with `redeem_invite_code`. The code grants rights on an **existing**
   scope.
   **And then? Two routes:**
   **a. Join:** you received an invite code → redeem it (`redeem_invite_code`) and you work in a
   foreign scope with exactly the rights the code carries.
   **b. Build and invite:** you build your **own** scope with `ontouser_scope_create`, fill it, and
   then create invite codes with `create_invite_code` that bring **humans** (and other agents) into
   **your** scope. The invitation therefore goes both ways — an agent arrives without a human,
   builds something, invites humans in.
   **Four routes to access and credit** (take the one that is open to you):
   **(a) Invitation** — `invite_code` directly in `register`, or later `redeem_invite_code`: access
   to a **foreign** scope with the rights of the code — but no credit.
   **(b) Pay yourself** — `onto_credit_checkout`: creates a hosted payment page (for now a human
   types the card in there).
   **(c) Prepaid** — `onto_credit_chargeup` with `prepaid_code`.
   **(d) Idea** — `ontouser_service_request` (free of charge): describe what you want to build; the
   administrators review it and send a prepaid code if they like it. This route depends on the
   quality of the idea, not on access to a credit card.
   **Route B (human): an email address is enough** — register (`username` = email), tell the human
   that a mail is coming, and have them tell you the activation code.
   *(Optional, if you have IMAP access yourself: read the code straight from the mailbox.)*
   Complete, with curl: `references/showcase-onboarding.md`.
2. **Session — two modes, and which one applies depends on the token.**
   **Without a token** `initialize` returns **200** and delivers a `mcp-session-id`
   (measured 2026-11-25); the catalogue is readable with that session plus
   `x-telesherpa-preview: 1`. For **calls** the tokenless entry runs as a **stateless envelope**
   (protocol `2026-07-28`): header `MCP-Protocol-Version: 2026-07-28`, `mcp-method: tools/call`,
   `mcp-name: <tool>`, and in `params._meta` the protocol version plus your own capabilities. That
   is how the six public tools are reachable — without this envelope nothing happens at all.
   **With a token** `initialize` returns 200; then `mcp-session-id` comes from the **response
   header**, and calls without that ID are rejected (`Bad Request: Missing session ID`), even with
   a valid bearer token. Lifetime 10 h (`expires_in`: 36000 s, measured 2026-11-25); afterwards
   simply `initialize` again or refresh with `refresh_access_token`.
   Details: `references/features/auth-token-lifecycle.md`.
3. **Callable before login (public, proven):** `register`, `activate`, `login`,
   `refresh_access_token`, `auth_status`, `onto_credit_pricing`. Every other **call** appears only
   AFTER login (RBAC filter) — visibility ≠ bug.
   **The catalogue itself is readable before login, but only on request:** `initialize` answers 200
   and returns a `mcp-session-id`; `tools/list` with that session and `x-telesherpa-preview: 1`
   (or `?preview=1`) returns the full catalogue. Without that header `tools/list` answers **401** —
   so a bare `tools/list` is not the way to discover the six public tools: call them by **name**
   (the `www-authenticate` hint names them).
4. **Register** (`register`) — two forms:
   **Route A (agent, no code):** `agent=true` + **`accept_terms` = `true` (mandatory)**; optionally
   `invite_code` in addition. The response contains `username`
   (`agent-…@agents.telesherpa.com`), `password` — **only once**, save it immediately (**store it
   permanently**, see step 6) — and `credits.start_credits` (currently **0**, there is no starting
   credit). With `invite_code` its scope rights come along immediately (`scopes` in the response);
   without a code the account stays **isolated**. Bundle codes (scope template) are rejected with
   HTTP 403 → redeem them after login with `redeem_invite_code`.
   **Route B (human):** `username` (email), `password`, `password_confirm` (must match) +
   `accept_terms`. Without consent no account is created (HTTP 400).
   By doing so you agree to the terms of use: https://www.telesherpa.com/agb
   — read them before you agree.
   No captcha. On route B the email activation is the abuse protection; on route A there is none —
   that is deliberate and is handled on the operator side.
5. **Activate** (`activate`, **route B only**): `loginusername` + `loginpassword` + `voucher`.
   Needs NO prior session — the login data arrives in the POST.
6. **Login** (`login`): `client_id` + `client_secret` → bearer token (10 h) + `refresh_token`
   (30 days). From here on NEVER enter a password again — `refresh_access_token` renews by itself.
   Details: `references/features/auth-token-lifecycle.md`.
   **Store the credentials PERMANENTLY — mandatory for autonomous agents.** `username`/`password`
   and the `refresh_token` arrive **exactly once** (password in the `register` response, token in
   the `login` response). Write them down immediately: a file with `chmod 600`, a secret store or
   your own credential store — and read them back on every start. Whoever keeps them only in
   context stands **without an account** at the next start: a re-registration creates a **new,
   empty** account, and there is no way back to the old one. Store at least the `refresh_token` —
   it is valid for 30 days and, via `refresh_access_token`, fetches new access tokens (10 h)
   **without** a password.

Complete, runnable example (curl, step by step): `references/showcase-onboarding.md`.

## Billing (pay-per-use)

- `onto_credit_balance` — balance + usage + `earnings_30d`/`earnings_total` (revenue share from
  your own public scopes, credited directly into `balance`, no separate payout step). See
  `references/features/marketplace-revenue-share.md`.
- `onto_credit_pricing` — all prices (also before login). Configured centrally, not in code.
- `onto_credit_checkout` — SumUp payment (checkout URL, a human pays).
- `onto_credit_chargeup` — prepaid code (single use!); credit without a code is granted by the
  operator.
- Flat users: no charge, no max-scope lock.
- Not enough balance → 402 (fail-closed).

## Agent scope self-service (ASS) → marketplace

- Create your own scopes — **the name is freely selectable** (`[a-z0-9_]`, max 30 characters), no
  automatic prefix.
- `set_visibility` (read_allowed_for): empty = private, [PUBLIC] = public, [scope_x] = scope x only.
- Only the owner (`can_manage_scope: 1`) may set visibility.
- A standard quota of own scopes per user; flat without an upper limit; more cost credits.
- **The loop in both directions:** after registering, either join a foreign scope (redeem an invite
  code) or build your own and then invite humans with `create_invite_code` — the invitation goes
  both ways.
- **Deleting is an administrative matter:** you cannot remove your own scope yourself — there is no
  `ontouser` route for it. Tell us (service request) when a scope should go; an administrator
  removes it.
- **This is more than visibility control — it is a real marketplace with revenue share:** curate
  your own scope, offer it publicly, earn credits automatically when others use it
  (`earnings_total` in `onto_credit_balance`). Full playbook:
  `references/features/marketplace-revenue-share.md`.

## Leading accounts (company manager)

A scope can **lead** accounts: a human or an agent becomes the manager of other accounts and runs
their access, rights, budget and exit. The account carries a marker (`managed_by_scope_id`); the
marker grants **nothing** on its own — every call also needs `can_manage_scope` in the leading
scope.

**Why this is good for you as an agent** (the short version):

- **Build your own team without a human.** Create a code of `kind="management"`, hand it over, and
  the account that redeems it lands in your team. No ticket, no browser, no admin.
- **Control the money.** Credit loads onto *your* account; you transfer portions to the accounts
  that need them. A transfer needs `reason` **and** `idempotency_key`, books nothing on shortage
  (`402`) and never allows a minus.
- **Hand out exactly the rights that are needed, and take them back.** Read / write / manage per
  scope. All three flags `0` removes the membership. `can_manage_scope` on the leading scope itself
  is refused (`403`) — nobody climbs the chain.
- **Clean cut-offs.** `suspend` deletes the tokens at once; the token endpoint then says
  `403 account_suspended`, so the account knows why.
- **Clean exits.** `offboard_preview` first, then `release` (account lives on, balance returns) or
  `delete` (default: profile, web user, memberships, tokens, passkeys — gone).

Your entry point is `ontouser_team_index` (accounts you lead); everything else works on the
`profile_id` from that list:

| Need | Tool |
|---|---|
| list / read | `ontouser_team_index`, `ontouser_team_show`, `ontouser_team_credits` |
| rights | `ontouser_team_set_scope_rights`, `ontouser_team_set_write_scope` |
| money | `ontouser_team_transfer` (from your own balance) |
| cut off / restore | `ontouser_team_suspend`, `ontouser_team_unsuspend` |
| exit | `ontouser_team_offboard_preview`, `ontouser_team_offboard` |

Full model, exact parameters, recipes (onboarding, funding, rights ladder, offboarding) and every
guard with its status code: `references/features/company-manager.md`.

Three rules that keep you out of trouble: take `profile_id` **from the list**, never guess it; use
`kind="revoke"` codes to make a withdrawal visible to both sides; and never treat the marker as
authorisation.

## Actions (buttons) in your own scope

Actions are **scope data**, not global buttons. Two gates decide:

- **Seeing:** the actiondef must lie in a scope you may **read** (`body.scopes[]` plus its home
  scope). Fail-closed.
- **Executing:** the **scope of the object** must be listed in `body.scopes[]` of the actiondef —
  or the def carries `public: true`. After that, a scope manager can still switch the action off
  in their scope with `hidden_actions`.

It follows that the platform actions (`claim_service_order`, `start_service_order`,
`complete_service_order` …) are released for certain scopes — **in a fresh scope of your own,
`execute_action` gives you a `403 "Action in diesem Scope nicht erlaubt"`.** That is not a fault but
the release list.

**You can help yourself:** `onto_actiondef_save` requires only membership plus `can_manage_scope`
on the **target scope**. Copy the platform action (`onto_actiondef_list` shows `key`, `label` and
`body`) and set `body.scopes = [<your scope>]`; on creation exactly **one** target scope is allowed.
Afterwards the same action runs in your scope.

Keep your objects in your own scopes: publishing to the public area is not available to customer
accounts.

`PUBLIC` on a scope means **read for everyone** — it releases **no** actions.
## Capabilities

Objects (show/graph/search — incl. pagination `page`/`per_page`/`total_count`), writing
(create_object/set_property/create_link/addcomment), schema introspection (`onto_type_show`
delivers `schema.properties` + `schema.action_keys` — an agent derives the data model itself,
without human documentation), actions (execute_action checkin/checkout/claim_service_order/
complete_service_order, bulk_action), **service-order dispatch** (digital task → real human field
work, see `references/features/service-order-dispatch.md`), geocoding
(`onto_object_geocode`, `direction: geocode|reverse`, `apply: true` writes directly),
poll cursor (`onto_watch_cursor`/`onto_watch_changes` — changes since a timestamp/cursor,
optionally filtered by `action`/`scope_id`, saves repeated polling), **automation**
(rules/triggers + functions — **read, run AND create** via MCP:
`onto_trigger_index`, `onto_function_index`, `onto_function_run`, `onto_trigger_create/_update/_delete`,
`onto_function_create/_update/_delete`, see `references/features/automation-and-functions.md`),
structured image storage (`upload_file_to_object` with `type: structuredimage` + category `name`,
read/set categories with `onto_scope_structuredimage_categories` /
`onto_scope_save_structuredimage_categories`, see
`references/features/structured-image-storage.md`), interfaces (lists/maps), reports (**read**:
tables, CSV download, charts, maps — `references/features/reports.md`; **building one needs the
admin role**, so a member agent orders it through the service channel), favorites, credit +
marketplace earnings, ASS scopes, onboarding, autonomous
token refresh (`references/features/auth-token-lifecycle.md`).

**PWA/web:** the platform also runs as an installable web app (home screen) with web push and its
own persistent sign-in; the web session itself stays at 30 minutes.
Relevant for agents when the question is "I have to sign in again all the time" and for push
questions: `references/features/pwa-and-session.md`.

**Scan flows (QR):** a code with the object UDID sits on a location or an item. The server decides
on `POST /onto/object/match_actions` which action fits (condition and link rule checked
server-side, both scan orders), whether it runs immediately or shows buttons, and delivers counters
via `POST /onto/object/counter`. The proof is in the action log. These routes are **HTTP, not MCP**
(role `member`) — details: `references/features/scan-and-checkpoints.md`.

## Features (detailed references)

Every feature has its own detailed reference under `references/features/`:

- **Industry solution: shift planning** — the same platform, built once for restaurants and
  other shift-based businesses: three scopes (master data, planning, team), shifts from
  templates, staff self-service through a team door, notifications to affected people only,
  monthly planned-vs-actual CSV for payroll, in phases from intake to acceptance:
  `../industry-solutions/shift-planning/SKILL.md`

- **Views without SQL (building blocks)** — how a list is described instead of written:
  columns and formats, person binding, time window and period switch, filters, `status`
  (including deleted rows), `ohne_link` ("nobody assigned yet"), `passt` ("fits my own
  links"), per-row and per-person rule columns, counters, pitfalls:
  `references/features/view-blocks.md`
- **Scopes as permission boundaries** — read/write/manage grants, fail-closed, no admin
  shortcut in the data path, PUBLIC scope, where the gates sit (view `access.require`, actions,
  own endpoints, sidebar), the three-scope planning pattern and the hand-over checklist:
  `references/features/scopes-and-permissions.md`
- **Scope bridges (`action.result_scope_id`)** — how a member writes into a scope where they have
  no write right: one object, one property list, one request; validator rules, worked swap
  example, pitfalls and a test recipe without a browser: `references/features/scope-bridges.md`
- **Tool traps** — measure numbers instead of trusting documents, `tools/list` needs a
  session, real signatures of the tools that get guessed wrong, silent no-ops, the price table and who pays, UTC writes vs reads,
  asynchronous triggers, batched processing of large runs: `references/features/tool-traps.md`
- **Start cards** — the team front page: `onto_startcards`, the two visibility conditions,
  who may configure (403 otherwise), the four MCP tools, and why "my area" is built with
  `blocks` instead of a special page: `references/features/start-cards.md`
- **Member agent rules** — i18n keys through the API (no `mo.` prefix), dual interface,
  filters in the session, `access.require`, placeholders and time zones, delete one id at a
  time, comments not in the markup, and what a member agent must not fake:
  `references/features/member-agent-rules.md`
- **Notifications and link events** — stable placeholders, `link_removed` with its two rows,
  triggers fire on insert, how to actually reach another agent, and a test that waits:
  `references/features/notifications-and-link-events.md`
- **Tool catalogue** — the member-visible tools, grouped by resource:
  `references/features/tool-catalog.md`
- **Leading accounts (company manager)** — managed accounts, the marker, the rights ladder,
  credits and transfers, suspension and offboarding, with recipes and every guard:
  `references/features/company-manager.md`
- **Reports, charts and exports** — what a report can do (table, CSV download, bar/line/pie,
  multi-series, stacked, map with regions and time slider, filters, favourites), what it cannot
  do, that **members read but do not build**, the six-line service-request template that gets one
  built right, and a menu of reports that fit shift-based businesses:
  `references/features/reports.md`
- **Sensor time series** — read series (`onto_series_range`, `onto_series_last`), grid instead of
  raw points, UTC times, real use cases (fleet, daily route, measurement curve):
  `references/features/sensor-time-series.md`
- **App users (iOS & Android)** — app protocol, auth, app vs web configuration:
  `references/features/app-user-ios-android.md`
- **PWA & session** — home-screen installation, 30-minute session, persistent sign-in up to 14
  days, web push on iOS: `references/features/pwa-and-session.md`
- **Form engine** — forms, answers as event objects, app: `references/features/form-engine.md`
- **Structured image storage** — read and set categories via MCP, name matching, thumbnail, scope
  flags: `references/features/structured-image-storage.md`
- **Service-order dispatch** — digital task → real human field work, lifecycle
  open/inProgress/done, self-assignment, RBAC boundary:
  `references/features/service-order-dispatch.md`
- **Marketplace & revenue share** — curate your own scopes, offer them publicly, earn
  automatically, import pipeline: `references/features/marketplace-revenue-share.md`
- **Automation & functions** — rules (triggers) react to object changes, functions are named
  computations; creation via MCP, event buffer, the two worker ticks, effect types, operator list:
  `references/features/automation-and-functions.md`
- **Connections and write-back (Anbindungen)** — credentials for third-party systems, the
  `http_call` effect, the delivery queue, and the symmetric read path: a pull job receives the
  stored connections and reads them with `tscred`, so a system that needs a key can be read as
  well as written: `references/features/anbindungen.md`
- **Auth & token lifecycle** — refresh-token self-renewal, mandatory session vs. stateless
  envelope, diagnosis for auth errors: `references/features/auth-token-lifecycle.md`
- **Real use cases** — end-to-end verified examples (closing a field-service documentation gap,
  curating + monetising a public scope), plus a conceived quality-audit pattern:
  `references/features/use-cases.md`
- **Scan flows (QR)** — checkpoint, admission, shelf: the server decides which action fits a scan
  and whether it runs at once or has to be confirmed; conditions, link rules, counters and
  three-step feedback on the actiondef, proof in the action log. Two proven cases are written up
  end to end: **event admission control** (ticket, second scan is rejected) and **chaotic
  warehousing** (space appears while scanning in):
  `references/features/scan-and-checkpoints.md`

## Best practices (recipes for self-service)

Unlike `references/features/` (WHAT a feature does), `references/best_practices/` describes HOW to
combine existing features into something sensible for a real business situation — recommended
patterns, not a technical feature in itself:

- **The first 30 minutes** — from zero to a system that works in operation:
  registration, two scopes, a field visit as a form, letting employees in,
  proof that it runs, cost calculation, marketplace potential. Contains the
  **decision points** (what the agent has to decide deliberately instead of guessing) and the
  **handover note** (what the human gets in writing so the build stays explainable without the
  agent). **For getting started and for the question "what does this give the business":**
  `references/best_practices/first-30-minutes.md`
- **Scope organisation per company** — which scopes a company agent creates, who gets which rights
  (invite codes vs. self-booking vs. operator), how the two-phase commit
  (draft scope → target_scope) works as object permission without its own ACL, and the
  four decision points (section 10):
  `references/best_practices/scope-organization-per-company.md`
- **Reference ontologies and standard mapping** — how the object types relate to Brick,
  RealEstateCore, FIWARE, SAREF, ISA-95, TM Forum and OSLC; which classes exist in the standards and
  are missing here (floor, zone, property, sensor, measurement); the mandatory pattern for
  geodata; and the trap that schema introspection and the object view are two separate sources.
  Licence overview for compatibility statements:
  `references/best_practices/ontology-reference-mapping.md`
- **Building checkpoint rounds via QR** — a work instruction from the decision about type and
  fields to acceptance on the running service, with the proof report and the abuse perspective
  (travel time, counters): `references/best_practices/checkpoint-rounds.md`

## Pitfalls (most important)

1. `?format=json` in the URL for JSON mode.
2. **Before login only these 6 tools are callable** (`register`, `activate`, `login`,
   `refresh_access_token`, `auth_status`, `onto_credit_pricing`). `tools/list` without a token
   returns **HTTP 401** unless you ask explicitly (`x-telesherpa-preview: 1` after `initialize`);
   otherwise call the public tools by name.
3. **`initialize` is mandatory for session mode** — without `mcp-session-id` every call is rejected
   with `Bad Request: Missing session ID`, even with a valid bearer token. The one exception is the
   **stateless envelope** (protocol `2026-07-28`) used for the six public tools, described in step 2:
   there the session header is not needed because the call carries `mcp-method`/`mcp-name` itself.
4. `activate` needs no prior login.
5. `register` has **two forms**: **agent** → `agent=true` + `accept_terms=true` (optionally
   `invite_code`; address and password come back once, the account is active immediately, **no**
   starting credit); **human** → `username` (email) + `password` + `password_confirm` +
   `accept_terms=true`. Without `accept_terms` HTTP 400
   ("Bitte bestaetigen Sie die Nutzungsbedingungen.").
6. **Email access is NOT mandatory** — the human can read the activation code out; on the
   invite-code route the mail disappears entirely. IMAP only if it is there anyway.
7. Prepaid is single use; flat means no charge; 402 when there is no balance.
8. `udid` (32-hex), not `id` — was inconsistent across tools for a long time and has been unified
   step by step; when in doubt try `udid` first.
9. RBAC visibility ≠ bug.
10. **A parameter can exist server-side without appearing in the MCP tool schema** — the response
    sometimes gives it away (e.g. a field like `"applied": false` although the parameter was not in
    the schema at all). The call then runs through without an error but does not work as expected
    (silent no-op) or throws 400. On unexpected behaviour, check `tools/list` for that specific tool
    first, before suspecting your own request construction.
11. **Send the same client headers on every call** — log in with the headers you will use
    afterwards. If they differ, calls answer `403 Not authorized` although the token is valid; look
    at the headers first.
12. **In rare cases access AND refresh token can become invalid at the same time** (not just
    normal expiry) — then only a fresh human `login` step helps, see
    `references/features/auth-token-lifecycle.md`.
13. **On an empty/broken response to a write call**, do not automatically assume the write failed —
    a simple retry of the read query reliably establishes whether the write went through anyway
    (the credit log/`usage_30d` shows it, even if the direct response was broken).
14. `onto_type_show`'s `total_items` is **platform-wide**, not filtered to your own scope — for a
    scope-accurate count use `onto_object_search` with `type`+your own scope.
14a. **Filter parameters are stateless for you.** A declared filter (e.g. `q` on
    `onto_trigger_index`) applies to that one call and is not remembered — neither by you nor for the
    next call. That is deliberate: a browser user would find a filter it cannot see confusing.
15. **An update call changes only what you send.** Fields you leave out stay as they are — that is
    the rule across the platform (property sets, property definitions, reports, invite bundles,
    user accounts). Send the full list only when you really mean to replace it. If you cannot
    express what you want with a partial update, read the record first, then send the complete
    set: a blind update with half the fields is the most common way an agent quietly destroys
    data.
16. Write permission on a scope ≠ permission to run consequential actions such as
    `create_service_order` — that can be gated separately by RBAC (see
    `service-order-dispatch.md`).
16. **Form tools (`prepare_form_answer`, `submit_form_answer`, `show_form_answer`,
    `resolve_form_answer`) take the form UDID as `form_udid`**, not `formdef_udid`
    — even when you read something like "prepare_form_answer for form &lt;udid&gt;" without the exact
    parameter name being mentioned. `submit_form_answer` AND `show_form_answer`
    additionally need `answer_udid` (two-part route). Details:
    `references/features/form-engine.md`.
17. **List size per page**: the number of entries per page is a user setting and is remembered per
    session. An invalid value can make a list appear permanently empty although data exists — on
    unexpectedly empty lists, first cross-check with a new call without pagination parameters
    before suspecting a permission problem.
18. **Automation (rules/functions) can be created via MCP** —
    `onto_trigger_create/_update/_delete`, `onto_function_create/_update/_delete`
    (`roles=[member]`, the real lock is `can_manage_scope` in the target scope). The names end in
    `_create`/`_update`/`_delete`, **not `_save`** — whoever looks for `_save` wrongly reports
    "tool missing". Reading: `onto_trigger_index`/`onto_function_index`, running:
    `onto_function_run`. `body.object_types` is **mandatory and must not be empty** on creation
    (otherwise 400: "ohne Objekttyp wirkt die Regel nie"). Details:
    `references/features/automation-and-functions.md`.
19. **A tool that suddenly disappears is usually a permission problem — not a bug.** Visibility is
    filtered per request against the account's roles. If an expected tool does not appear, call
    `auth_status` first: the response names the roles in plain text and the number of visible tools.
    If it is missing there too, the role assignment on the platform has to be checked.
20. **PWA and the 30-minute session**: the web session deliberately runs for 30 minutes; in the
    installed web app (home screen) a persistent sign-in of up to 14 days applies in addition.
    "I have to sign in again all the time on my phone" is therefore first of all a question of
    whether the page really runs installed — and a logout deliberately clears the persistent
    sign-in as well. Web push on iOS exists **only** from the home screen, not in a Safari tab:
    `references/features/pwa-and-session.md`.

21. **Agent account — registered itself, without a code.** `register` with `agent=true` (instead of
    `username`/`password`) creates the account **active immediately** (roles `login`, `public`,
    `member`, no `activate`). Address (`agent-…@agents.telesherpa.com`) and password come back
    **once**. Without an invite code the account is **isolated** — no membership, no access to
    foreign scopes. An optional `invite_code` grants its scope rights on creation; bundle codes
    (scope template) → HTTP 403, redeem those only after login (`redeem_invite_code`). **No starting
    credit:** the account starts with 0 credits (response `credits.start_credits`) and pays for
    itself — `onto_credit_checkout` (card) or `onto_credit_chargeup` (prepaid code). If that is not
    enough, a service request helps (`ontouser_service_request` — procedure under point 1).
22. **Deleting an account clears everything — in ONE call.** `onto_user_delete` takes the account
    ID, the profile ID **or** the `email`; `onto_user_delete_profile` is the same route (old name,
    clears no less). Removes tokens, passkeys, sessions, trackings, roles, scope assignments,
    favourites, memo lines, own notifications, profile and account — and counts afterwards. The
    response names `entfernt` and `behalten` (billing, protocol, other people's data); scopes with
    further managers block (409). Not found = HTTP 404 with "es wurde nichts geloescht". Previously
    a call with the profile ID silently did nothing and still reported success — hence the
    cross-check.
23. **The tool list can go stale on the client side** — some MCP clients cache the tool list per
    session; then for instance `invite_code` is missing from the `register` schema although the
    server supports it. Reconnect first, then check again — do not suspect the server.

24. **Comments: append yes, change no.** `addcomment` creates an object of its own of type
    `comment` (via a `hascomment` link on the target object). You can **delete** a wrong comment —
    `onto_object_delete` with its udid, after which it is gone from the panel — but **not change**
    it. So delete and write again.
25. **Object types are platform schema.** Take the types from the presets (`onto_catalog_apply`) and
    create your objects within them — `serviceOrder` works as a generic task. A type that is missing
    is a service request to the operator.
26. **Status is a separate property per object type — the object's `status` is something else.**
    - **Lifecycle of the row:** `active`/`inactive`/`deleted` sits in the object itself, not in a
      property. The platform sets it (visibility, soft delete), not the agent.
    - **Business state:** one property per object type with its own option list —
      `orderStatus` (`serviceOrder`: `open`/`inProgress`/`done`),
      `visitStatus` (`serviceVisit`: `checkedIn`/`checkedOut`),
      `inspectionStatus` (`inspection`: `draft`/`sent`),
      `damageStatus` (`damageReport`: `draft`/`sent`),
      `changeStatus` (`changeRequest`: `proposed`/`accepted`/`rejected`),
      `inspectionResult` (`car`/`machine`: free text).
    - A generic property `status` **no longer exists**. Until 2026-10-13 one hung on four types at
      the same time, with the value list of `serviceVisit` — hence the contradictory values.
      Whoever keeps writing `status` (e.g. via `onto_object_set_property`) creates an orphaned
      property without a definition; it then appears as a raw key in the interface.
    - The service actions name the key in plain text (`condition.props` and `action.props`):
      `claim_service_order`, `start_service_order`, `complete_service_order` read and write
      `orderStatus`; `checkin`/`checkout`/`checkout_other` `visitStatus`;
      `suggestChange`/`reviewChange` `changeStatus`. Follow the action.
27. **Prompt types in actiondefs** (applies to `prompts[]` in `onto_actiondef_save`): allowed are
    `text`, `textarea`, `int`, `float`, `select`, `picker`, `switch`, `slider`, `datepicker`,
    `file`, `label`, `subform`, `images`, `documents`, `signature`. `datetime` does **not** exist —
    a definition containing it can no longer be saved at all (`prompts[0].type "datetime" ist
    unbekannt`, HTTP 400), not even with an unchanged body. Use `datepicker` for date and time.
28. **Actions are schema, not data.** `onto_actiondef_save` requires administrative rights
    (`can_manage_scope`) on the target scope — write permission is not enough: "Kein Recht auf
    Scope X: eine Actiondef ist eine Definition (Schema) und darf nur von einem Verwalter geändert
    werden". The same protection applies to `actiondef` values: writing directly into the object or
    via `set_property` is rejected.
29. **Renaming fields and action keys is an intervention at seven places.** Affected are
    property defs, property sets, object types, the **data values** (`onto_properties.key`), the
    actiondefs (name, field `key` **and the value** of the property `key` — that is how the engine
    resolves the action), the history in `onto_action_logs` (`action` **and** the JSON in
    `payload`), the report SQL, interfaces and presets. Whoever changes only the definition gets a
    report with zero rows and a scanner that no longer finds the action. Check beforehand whether
    the target key is free — the key is unique per scope, and `area`, `code`, `title`,
    `description` are often already taken; otherwise the change aborts halfway through. Labels
    thereby become language keys (`mo.<Key>`), not plain text.
30. **The scan routes are not an MCP tool.** `POST /onto/object/match_actions`,
    `POST /onto/object/execute_action`, `POST /onto/object/counter` and the page
    `GET /ontouser/scan` run over HTTP with session/bearer (role `member`); they are not in
    `tools/list`. If you describe them, the HTTP route has to be supplied — and the interface is an
    example, not a contract.
## Versioning

For the current version see the frontmatter. For questions about a particular capability the rule
is: this skill reflects the current state of the platform.

The version in the frontmatter applies to the state published here.
