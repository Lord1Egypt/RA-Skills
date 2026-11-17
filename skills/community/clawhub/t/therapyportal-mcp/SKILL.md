---
name: therapyportal-fpx
description: Read a TherapyNotes client portal (www.therapyportal.com/p/<practice>/) from a shell — upcoming therapy appointments, document/paperwork requests (pending and completed), always-available practice forms, balances due, payment receipts, secure-message threads, and completed forms or receipts downloaded as PDFs — through the user's signed-in portal tab with the fpx CLI. Use when asked about TherapyPortal / TherapyNotes, therapy appointments or sessions, paperwork the therapist sent, what is owed to the practice, or a therapy receipt.
---

# TherapyPortal (TherapyNotes client portal) via fpx

Every call goes through the user's signed-in portal tab via the ContextMint Bridge
browser extension. Read-only: the helper wraps no writes (sending messages, signing
forms and paying are all portal writes, and none of them are exposed here).

## One-time setup

```sh
npm i -g @fetchproxy/cli                     # provides `fpx`
fpx profile add therapyportal --domain therapyportal.com
fpx profile declare therapyportal --allow-download   # BEFORE the first pairing
export THERAPYPORTAL_PRACTICE=example12345  # the code in the portal URL: /p/<code>/
scripts/therapyportal patients               # first call prints a pair code on stderr
```

Approve the pair code in the ContextMint Bridge popup of the browser that is signed in to
the portal. If you run ContextMint Bridge in a second browser, every call also prints
`refusing an extension whose identity is not the one this MCP paired with` and a new pair
code on stderr, but the data still arrives on stdout. **Do not approve those codes.**
They come from the other browser, which is being turned away. `fpx trust list` shows
which browser each profile is pinned to; to re-pin, run `fpx trust clear fpx-therapyportal`
and pair from the right browser.

The browser must be signed in to the portal; keep a portal tab open (fpx relays each call through it).

## Commands

`scripts/therapyportal <command>` — stdout is JSON (projected; pipe to `jq`), stderr is status.

| command | returns |
|---|---|
| `patients` | clients linked to this login: `PatientId`, name, DOB. Get ids here first |
| `appointments` | **upcoming** appointments (the portal shows no past ones): start/end, clinician, telehealth, location, which client |
| `documents [pending\|completed\|all]` | paperwork the practice sent, with each document's `PortalDocumentId`, title, status, completed date |
| `forms` | always-available practice forms (to sign or upload as needed) |
| `counts` | per client: documents awaiting completion or approval |
| `balances` | amount due per client |
| `receipts` | payments, each with `PaymentId` and the line items it covered |
| `threads <PatientId> [n]` | that client's message threads; `null` means none |
| `messages <ThreadId>` | messages in one thread |
| `download <PortalDocumentId> <PatientId> [type=3]` | a document as a file; pass the document's `PatientDocumentType` (3 = a form the client filled in, rendered to PDF; 0 = a file the practice uploaded) |
| `receipt <PaymentId>` | a payment receipt as a PDF |
| `raw <path> [fields]` | any `/portal/practice/<path>.aspx`, **unprojected** |

Downloads land in the **browser's download folder** (`~/Downloads`). fpx prints
`{path, bytes, mime}`. Each download is logged by the practice, as it is in the UI.

Examples:

```sh
scripts/therapyportal appointments | jq '.appointments[:5]'
scripts/therapyportal documents completed | jq '.[] | .documents[] | {PortalDocumentId, title}'
P=$(scripts/therapyportal patients | jq -r '.[] | select(.FirstName=="Sam") | .PatientId')
scripts/therapyportal threads "$P"
```

## In context groups

The therapyportal MCP (not this fpx helper) joins the **health** group on an mcp-host
gateway. Its canonical reads, each answering one line per item with `view: "brief"`:

- **what's on** — `therapyportal_list_appointments`: upcoming sessions.
- **what's due** — `therapyportal_list_documents`: paperwork still to fill in.

Both take `client` as their subject: a client's name as listed at start (an enum of the
linked clients, e.g. each child in therapy) or a raw patientId. There is no date range;
the portal shows future appointments only. Nothing here is canonical for what's new
(message threads are unprojected). A compound ask looks like "when is the next therapy
session, and are there forms to fill in?" — the group fans out to both reads, once per
client.
On the browser bridge, when no signed-in portal tab is connected the group answers
"needs your browser open" for this source instead of an empty list.

## Exit codes

`0` ok · `1` usage · `2` bridge unavailable (extension not connected) · `3` bot wall ·
`4` upstream error (an HTTP error, or the portal's "Page Not Found" page for a bad
endpoint or missing field) · `5` signed out (sign in at the portal in the browser, retry).

## Privacy rules

These are mental-health records, often about a minor. Use the projected commands.
**Never print `raw document/getpatientsforportaluser`**: it carries the full demographic
record, including address, phone, email, an SSN field, and free-text comments. Run any
`raw` call through `jq` and pick only the fields you need.

`references/endpoints.md` covers the wire protocol (why every call needs `tnrac` + `tnv` +
the numeric `portalpractice`), each endpoint's fields, and what is not verified yet.
