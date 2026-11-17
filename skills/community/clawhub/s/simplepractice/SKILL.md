---
name: simplepractice
description: >-
  Read a SimplePractice Client Portal through the simplepractice-mcp server —
  upcoming appointments, invoices/statements/superbills/receipts, balance and
  saved cards, paperwork waiting to be signed, and practice announcements.
  Use when the user asks about their therapy or healthcare appointments,
  what they owe a practice, a superbill for insurance, or forms their
  provider has sent them.
---

# SimplePractice Client Portal

`simplepractice-mcp` reads the Client Portal a practice gives its clients —
the patient side, not the clinician side. It is **read-only**: nothing here
cancels an appointment, signs a form, or pays a bill.

## Signing in

The portal has **no password**. SimplePractice emails a one-time link (or a
6-digit PIN), and that is the only way in.

1. `simplepractice_session_status` — check first; a session persists between
   runs, so most of the time there is nothing to do. It also reports which
   practice is in play, and whether that came from a link, the environment, or
   the saved session.
2. If the user already has the email, skip straight to step 4 — asking for a
   second link when one is in their inbox spends a rate limit for nothing.
3. `simplepractice_request_sign_in_link` with the user's portal email. It asks
   for confirmation because it sends a real email and the endpoint is
   rate-limited **per address and per IP** — a retry loop locks the user out of
   the only auth path there is. A client that can show a prompt gets one
   (unless the server sets `MCP_CONFIRM_ELICITATION=off`); otherwise the
   first call sends nothing and returns a preview plus a `confirmToken`: show
   the user the preview, and only after they approve call again with the same
   arguments and that `confirmToken`. Never send twice. If the server
   does not know the practice yet, pass `practice` (the slug, host, or portal
   URL) — otherwise it has no portal to ask.
4. The user opens the email and gives you the link. Pass it **whole** to
   `simplepractice_verify_sign_in_token` — it takes the token out of the
   fragment *and* the practice out of the host, which is why the whole link is
   worth more than the token alone. Tokens are single-use and last 24 hours.

Nothing has to be configured: the practice comes from the link, and the stored
session remembers it. `SIMPLEPRACTICE_PRACTICE` only pins the server to one
practice. Two link shapes name no practice and need one already known — the
mobile variant on the bare `clientsecure.me` apex, and a bare token pasted
without its link.

There is no refresh token. When a session lapses the tools say to sign in
again; that means another email.

`simplepractice_sign_out` only forgets the session stored on this machine. It
does not revoke it: SimplePractice is never told, so the session token stays
valid on SimplePractice's side until it expires there, and it does not sign the
Client Portal out anywhere else. Do not tell the user they are "signed out of
SimplePractice" — say the server forgot its session.

## Reading

- `simplepractice_get_account` — the practice, the current client, and the
  clients this login covers. **Start here**: one portal login can act for
  several people (a parent for two children), so confirm *whose* record you
  are about to report on before you report on it. It also returns the
  practice's real cancellation policy and the client's feature permissions.
- `simplepractice_list_appointments(status?, page?, pageSize?, view?)` — `status: "scheduled"` for confirmed and
  upcoming, `"requested"` for ones the practice has not confirmed yet.
- `simplepractice_list_document_requests` — paperwork. `outstandingOnly: true`
  answers "is anything waiting for me?", which is the usual question. It (and
  `list_documents` / `list_announcements`) reads only the newest `pageSize`
  rows, max 50: when `hasMore` is `true` the `outstanding` / `unread` counts
  cover that page only, so do not say nothing is outstanding.
- `simplepractice_get_billing_overview(view?)` — balance due and per-category counts.
  Cheaper than listing the billing collections to find out they are empty.
- `simplepractice_list_billing_items(kind?, before?, pageSize?, view?)` — invoices, statements, **superbills**
  (the receipt to claim out-of-network insurance), receipts, or account
  history. Pages by cursor: pass the returned `nextCursor` back as `before`.
- `simplepractice_list_payment_methods`, `simplepractice_list_documents`,
  `simplepractice_list_announcements`.

## Response shape (`view`)

Five of the reads take `view: "compact" | "full"` (two of them, and
`simplepractice_list_document_requests`, also take `"brief"` — see "In context
groups"), and **`compact` is the default**: `simplepractice_list_appointments`,
`simplepractice_list_billing_items`, `simplepractice_get_billing_overview`,
`simplepractice_get_document_request` and
`simplepractice_list_announcements`.

That default is the point of the parameter. This rung used to be a
`compact: false` boolean — opt-in, so a caller had to know the slim shape
existed and ask for it. An efficiency that has to be requested is one that
usually is not, and the caller paying for it is the one least able to know.

**Compact is not one thing here.** One of the tools gets a real field
projection; the other four get media stripping and no field projection at all,
and the difference matters because expecting a named field set from the second
group would be expecting something that was never going to be there.

- **`simplepractice_list_appointments` is projected**, down to
  `{id, startTime, endTime, service, clinician, location, videoRoomUrl,
  confirmationStatus, clientConfirmationStatus, isCancellable, fee}`.
  `clinician` is the first and last name JOINED into one string, and
  `location` collapses the office record to `"telehealth"` or
  `"name, city, state"` — so if you are reaching for `clinician.firstName` or
  the `office` object, they are on `full` only.
- **`list_billing_items`, `get_billing_overview`, `get_document_request` and
  `list_announcements` are media-stripped only.** No field projection is
  claimed, and that is deliberate rather than unfinished: `billing-items` is
  one polymorphic collection switched five ways (`invoice`, `statement`,
  `superbill`, `receipt`, account history), and a field list picked for an
  invoice would quietly drop half of a superbill. The same is true of
  `document-requests`, where a consent form, a questionnaire and a Good Faith
  Estimate are different shapes under one endpoint. What compact takes is the
  practice logo and the clinician avatars; it touches nothing whose key names
  an amount, a date, or a document link.

One consequence worth knowing on announcements: the rung drops media keys,
never nulls. `readAt: null` is data — it is what "unread" means — so it
survives, and the `unread` count stays reconcilable against the rows beneath
it.

`view: "full"` returns SimplePractice's whole record. There is **no `raw`
rung**: `full` already IS the untouched upstream payload, so a third value
could only alias it. And `view` never reaches SimplePractice — it is
destructured off before the request is built, because `client.list` turns
whatever it is handed into a JSON:API query string and a stray `view=compact`
would arrive as a filter SimplePractice never defined.

The other ten tools take no `view`, and each has its own reason:

- **`simplepractice_get_account`, `simplepractice_list_document_requests` and
  `simplepractice_list_payment_methods` are ALREADY hand-written
  projections** — every field on them was picked by name with knowledge of the
  payload. There is no un-projected shape left underneath, so a `view` there
  would be a parameter that changes nothing, and running a blind rung over that
  output would let an un-grounded rule overrule a grounded one.
  (`list_document_requests` also takes `includeBody`, a field the caller
  explicitly asked for; a blind rung could only take back something chosen on
  purpose.)
- **`simplepractice_list_documents` is the exception worth stating**: its
  PRODUCT is the file references. A practice that shares a scan shares it as a
  `.jpg` or `.png`, and the blind rung drops any string whose path ends in an
  image extension — so compacting here would not shrink the answer, it would
  empty exactly the rows you came for.
- **`simplepractice_session_status` and `simplepractice_healthcheck`** answer
  with status, not records.
- **`simplepractice_request_sign_in_link`, `simplepractice_verify_sign_in_pin`,
  `simplepractice_verify_sign_in_token` and `simplepractice_sign_out`** are
  writes. A write's response is a receipt, with nothing to strip and everything
  to keep.

## In context groups

Every tool except the healthcheck carries a `_meta.mint` hint placing it in
mcp-host's **`health`** group, so a host that groups connectors can answer a
health question across this MCP and its siblings in one ask. The canonical
reads, each taking `view: "brief"` (one line per item,
`title — <ISO date | no date> — <status>`, at most 120 characters, inside the
untrusted-data envelope as `data: string[]` because the titles are the
practice's; a line starting `-- ` is a note — `-- none` when there is
nothing, `-- more` when the page came back full — and an item whose title
starts with `-- ` or `\` is escaped with one leading `\`):

- **what's on** — `simplepractice_list_appointments`: the scheduled
  appointments (`<service> with <clinician> — <start> — <status>`).
- **what's due** — `simplepractice_list_document_requests`: in `brief`, the
  OUTSTANDING paperwork only, with `no date` because the portal sets none.
- **what's new** — `simplepractice_list_announcements`: in `brief`, the
  UNREAD announcements only.

None takes a subject or a range: one portal login answers for the signed-in
client, and no tool takes an argument naming whose record to read. A
compound ask reads like "any therapy appointments this week, and is there
paperwork I still owe?" — the host fans out to the what's-on and what's-due
reads here and beside it. A signed-out session answers as an error naming the
sign-in tools, not as an empty list; it is not a browser-bridged MCP, so
there is no "needs your browser open" state.

## Reading the results honestly

- **An empty billing list is a real answer.** Plenty of practices invoice
  entirely outside the portal. "No invoices in the portal" is the true
  statement; "you owe nothing" is not one you can make from it.
- **Do not tell someone they can cancel an appointment.** `isCancellable` and
  the practice's `clientMayCancelAppointments` / `cancellationNoticeHours`
  are what govern it, and cancelling has to happen in the portal anyway.
- **This is medical information.** Report what was asked. Don't volunteer
  diagnoses, session notes, or a family member's records into a conversation
  that wasn't about them.

## The shell alternative

`simplepractice-fpx` does the same reads with `curl` and no server, for
scripts or a machine without the MCP installed.
