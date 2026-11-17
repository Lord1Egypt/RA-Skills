---
name: sportsinc-sportslink
description: >
  Sports Inc SportsLink API adapter — pull a dealer's invoices ("documents")
  from the Sports Inc SportsWeb Invoice Center and mark them consumed. Sports
  Inc is a buying group that does NOT send individual vendor invoices; its
  SportsLink REST API is where the invoices live. Use when you need to retrieve
  Sports Inc invoices for payables — "get the Sports Inc invoices", "pull
  SportsLink documents", "fetch this month's SI invoices to match against POs".
  This is the SOURCE adapter only: it authenticates, pages, normalises each SI
  document into a common invoice shape (po_number, invoice_number/date,
  lines[], charges, total, is_credit), and marks documents historical once
  imported. Some documents are scanned rather than EDI, so the API returns their
  header totals with NO line items (`has_lines: false`) — every retrieval names
  those in `needs_line_recovery`, and they are not billable as returned. For
  each, this skill logs in to the SportsWeb portal, downloads the invoice PDF,
  OCRs the scanned vendor invoice into text for the agent to read, and then
  checks the extracted lines against the API's own merchandise total before any
  of it is billable. It is customer-agnostic (every Sports Inc
  dealer uses this same API) and touches no ERP — pair it with a payables
  workflow (e.g. `drivethru-payable-matching`) to match against POs and create
  the bill.
version: 0.7.1
emoji: 🏟️
homepage: https://www.sportsinc.com
metadata:
  openclaw:
    requires:
      # SPORTSINC_API_KEY is deliberately NOT listed here. openclaw gates a
      # skill OUT of the model's view when a `requires.env` key is absent from
      # the *boot* environment — but in A2A mode (see "Agent-to-Agent (A2A)
      # Mode" below) this key is brokered per-turn by the platform and is
      # absent at boot by design, so gating on it would hide this skill from
      # the very delegated flow it exists to serve. The key stays fully
      # documented via `primaryEnv`/`envVars`, and the helper self-guards at
      # runtime (`config_error`/`auth_error`) when it is genuinely missing.
      # `python3` stays gated because it must be present at boot.
      bins: [python3]
    primaryEnv: SPORTSINC_API_KEY
    envVars:
      SPORTSINC_API_KEY:
        required: true
        description: >
          SportsLink API key, sent as the `X-API-KEY` header. Request one from
          mhoerner@hq.sportsinc.com. Treat as a secret; never paste into chat.
      SPORTSINC_API_URL:
        required: false
        description: Base URL, default `https://api.sportsinc.com/`.
      SPORTSINC_DRY_RUN:
        required: false
        description: If truthy, `mark-historical` is simulated (no state change).
      SPORTSINC_WEB_USERNAME:
        required: false
        description: >
          SportsWeb portal login, used only by `fetch-invoice-doc` to pull a
          scanned document's PDF. This is the dealer's own portal user and is
          SEPARATE from SPORTSINC_API_KEY. Treat as a secret; never ask for it
          in chat.
      SPORTSINC_WEB_PASSWORD:
        required: false
        description: SportsWeb portal password. Treat as a secret.
      SPORTSINC_WEB_BASE_URL:
        required: false
        description: >
          Invoice Center host, default `https://swv2h.sportsinc.com/`.
      SPORTSINC_WEB_HOME_URL:
        required: false
        description: >
          Home screen, default `https://swv3.sportsinc.com/home` — a DIFFERENT
          host from the Invoice Center. This is where login lands and the only
          page carrying the search box.
      SPORTSINC_WEB_TIMEOUT_MS:
        required: false
        description: >
          Per-step wait, default 25000. Every wait is for a concrete element;
          nothing waits on `networkidle`, which the Vue home screen may never
          reach.
      SPORTSINC_WEB_HEADLESS:
        required: false
        description: >
          Default `true`. Set falsy to run the portal browser headed — on a
          Linux host with no display an Xvfb virtual display is started
          automatically (needs the `xvfb` system package).
      SPORTSINC_WEB_STATE_PATH:
        required: false
        description: >
          File path for a persisted logged-in session (Playwright
          `storage_state`). Set it to skip the Auth0 round trip on later runs,
          and as the escape hatch if the login ever requires MFA — log in once
          by hand with this set and subsequent runs reuse the session.
      SPORTSINC_OCR:
        required: false
        description: >
          `auto` (default — use the best installed engine), `off`, or an engine
          name (`rapidocr`, `tesseract`). Controls whether scanned pages are
          OCR'd into text before the images are offered.
      SPORTSINC_PDF_DIR:
        required: false
        description: >
          Where a scanned PDF is written so the agent can read it (defaults to
          the system temp dir). Only image-only PDFs are ever written; a
          document with a text layer never touches disk.
    install:
      uv:
        - requests>=2.28
        # Text-layer extraction for the header-only PDF fallback.
        - pypdf>=4.0
        # Converts the scanned vendor-invoice pages to PNGs the agent can read.
        # Needs a build with JPEG 2000 support (SI's scans are JPX); without it
        # the raw stream is written instead and the tool says so.
        - pillow>=10.0
        # Browser automation for pulling those PDFs from the SportsWeb portal.
        # As with drivethru-adidas-click, this installs the Playwright *package*;
        # the Chromium binary is a separate download handled on first use.
        - playwright>=1.40
        # OCR for the scanned vendor-invoice pages, so text rather than a 300dpi
        # image goes into context. Pip-only and cross-platform — no system
        # package, unlike tesseract (which is used instead when present).
        # Without it the pipeline still works, falling back to the images.
        - rapidocr-onnxruntime>=1.3
---

# Sports Inc SportsLink adapter

Sports Inc is a buying group: BaconCo (and every other SI dealer) buys through
Sports Inc, and Sports Inc does **not** email individual vendor invoices —
they're published in the SportsWeb Invoice Center and exposed through the
**SportsLink REST API**. This skill is the source adapter for that API. It does
one job: hand a payables workflow a clean, normalised list of invoices, and
mark them consumed once they've been imported. It never touches Odoo.

The single helper is `scripts/sportslink.py`:

```bash
# The un-imported inbox: every active document, normalised. Scanned documents
# come back with no lines and are named in `needs_line_recovery` — see the
# retrieval procedure below. Do NOT pass `ediOnly: true` for a billing run: it
# filters those documents out of the result entirely, so they are never billed
# and simply age.
python3 scripts/sportslink.py list '{"active": true, "lines": true}'

# A specific document (ignores the active-only filter)
python3 scripts/sportslink.py get '{"poNumber": "P13189"}'

# Mark documents consumed — AFTER they've been billed (honors SPORTSINC_DRY_RUN)
python3 scripts/sportslink.py mark-historical '{"siDocNumbers": [12345, 23456]}'

# A2A-safe action for agent-to-agent calls (structured request/response contract)
python3 scripts/sportslink.py get-for-a2a '{"customer_ref": "DEALER-001", "date_range": {"start": "2024-01-01", "end": "2024-12-31"}, "statuses": ["open"]}'

# Header-only (scanned) document: get its PDF, read it yourself, then get checked
python3 scripts/sportslink.py fetch-invoice-doc '{"si_doc_number": 23962348}'
python3 scripts/sportslink.py reconcile-lines '{"si_doc_number": 23962348, "lines": [...]}'
```

Every command prints one JSON object, or `{"error": {...}}` with a non-zero
exit. Needs `SPORTSINC_API_KEY` (if unset, exits `config_error` — stop and tell
the user to configure it; never ask for the key in chat).

## ⚠ Retrieval procedure — required, every time

**A Sports Inc retrieval is not finished when `list` returns.** Some documents
come back with header totals and no line items, because Sports Inc scanned the
supplier's invoice instead of receiving it as EDI. Those are **not billable as
returned** — there is nothing to match against a PO.

Every `list` / `get` / `get-for-a2a` result names them:

```json
"needs_line_recovery": [24682750, 24684277],
"credits": [24690002],
"next_step": "2 document(s) have no line detail from the API …"
```

**If `needs_line_recovery` is non-empty, you must resolve every document in it
before billing any of them.** For each one:

```bash
# 1. Fetch it. Logs in to the portal, downloads the PDF, and OCRs the scanned
#    vendor invoice into text. Active tab first, Archived automatically after.
python3 scripts/sportslink.py fetch-invoice-doc '{"si_doc_number": 24684277}'

# 2. Read the returned `text` and extract the line items yourself.
#    See references/pdf_extraction.md — which pages to skip, the field mapping,
#    and the rules (transcribe don't compute, never infer a quantity).

# 3. Hand them back to be checked against the API's own merchandise total.
python3 scripts/sportslink.py reconcile-lines '{"si_doc_number": 24684277, "lines": [...]}'
```

Step 3 returns `status: "verified"` — a normalised invoice with real
`lines[]`, indistinguishable downstream from an EDI one — or
`status: "needs_review"` with the variance named.

Non-negotiables:

- **Bill only a `verified` invoice.** `needs_review` means the extracted lines
  do not tie to Sports Inc's own header; escalate and leave the document active.
- **Never bill a document from header totals alone.** A `docTotal` with no lines
  behind it cannot be matched to a PO, and that is the whole point of matching.
- **Never skip a document because it is inconvenient.** It reappears on the next
  run, unbilled, and ages.
- `credits` (`is_credit: true`) are never billed at all — they go to a human,
  whatever their line detail looks like.
- Exactly-once is unchanged: `mark-historical` only **after** the bill exists.

If `fetch-invoice-doc` reports `portal_tab: "archived"`, the document has
already been marked historical — which happens only after a bill was created.
Check whether it has already been paid before creating another.

## Normalised invoice shape

`list`/`get` return `{count, total_count, invoices: [...]}`, each invoice:

```json
{
  "source": "sports_inc",
  "po_number": "P13189",          // dealer PO number → the match key to a PO
  "si_doc_number": 12345,          // SI's document id → used to mark-historical
  "invoice_number": "…",           // supplierDocNumber (falls back to si_doc_number)
  "invoice_date": "…",             // supplierDocDate, else siDocDate
  "due_date": "…", "supplier": "…",
  "is_credit": false,               // credit memo → handle separately, never a bill
  "has_lines": true,                // false for scanned/OCR docs (header totals only)
  "placeholder_lines": 0,           // empty rows the API returned and we dropped
  "placeholder_note": null,         // what they said, e.g. "SEE VENDOR INVOICE FOR DETAIL."
                                    // has_lines false ⇒ this document appears in
                                    // `needs_line_recovery`; see the retrieval
                                    // procedure above before billing it
  "lines_source": "pdf",            // present only when lines were recovered from a PDF
  "total": 0,                       // docTotal
  "charges": {"merchandise", "freight", "freight_allowance", "si_upcharge",
              "svc_handle", "sales_tax", "excise_tax", "discount"},
  "lines": [{"item","upc","description","size","color","unit",
             "qty_ordered","qty_shipped","qty_backordered",
             "list_price","discount_pct","net_price","extension"}]
}
```

This is the **same shape a PDF-extracted invoice would have**, so a payables
workflow reconciles it without caring that it came from SportsLink.

## Rules that matter

- **Don't pull before ~10:30am ET** — SI's internal processing runs first; earlier
  reads can be incomplete. Schedule accordingly.
- **Line data is EDI-only, so scanned documents need the portal.** They come
  back with header totals and no usable `lines` (`has_lines: false`) and are
  named in `needs_line_recovery`. Recover each one via the retrieval procedure
  above; if that cannot produce a *verified* result, escalate rather than
  blind-bill. `ediOnly: true` exists to fetch *only* EDI documents — useful for
  a narrow query, wrong for a billing run, because the documents it filters out
  are still owed and will simply age.
- **A scanned document returns a placeholder line, not an empty array.** One row
  with no item and no UPC, zeroes throughout, and the description
  `"SEE VENDOR INVOICE FOR DETAIL."` — SI's own instruction, the same sentence
  printed on the PDF's cover page. A line counts only if it identifies a product
  (item number or UPC) or carries a non-zero number; a description alone does
  not, or that row reads as real. Dropped rows surface as `placeholder_lines` /
  `placeholder_note`. See `references/sportslink_api.md`.
- **`is_credit: true` is a credit memo** — route it to a human / vendor credit,
  never create it as a payable.
- **Exactly-once — the golden rule.** Import first, `mark-historical` **after**
  the bill is created. This adapter deliberately does **not** use the API's
  `moveToHistorical=true` GET flag (which marks on read, before billing) — a
  crash between read and bill would silently drop the invoice. The natural loop:
  `list active` → bill each in the ERP → `mark-historical` the ones that
  succeeded; failures/escalations stay active and are retried next run.
- **Paging** is automatic (`all: true`, the default). Max 1000 docs/call on SI's
  side; the helper pages to the end (capped at 50 pages as a backstop).

## Header-only documents: recovering lines from the PDF

Sports Inc scans some supplier invoices instead of receiving them as EDI. Those
documents arrive with header money but no `lines`, and the line detail exists
only in the PDF in the SportsWeb Invoice Center — there is no API for it. This
skill recovers those lines in three beats, with **you** as the middle one:

```
fetch-invoice-doc  →  you read the PDF  →  reconcile-lines
   (Python: I/O)      (the only fuzzy step)   (Python: arithmetic)
```

No extraction *model* is involved anywhere: OCR transcribes the scan, the agent
interprets the text, and arithmetic checks the result. Scanned pages are OCR'd
before you see them, so what lands in context is text rather than a 300dpi
image — the images stay on disk for when the text is not good enough.

**What a download contains.** Not one invoice — a stack of documents, each being
a landscape **SI cover page** (native text, no line detail, it says
`SEE VENDOR INVOICE FOR DETAIL.`) followed by the **vendor invoice**, usually a
300dpi scan. That scan is where the line items are; the SI cover is useless for
extraction, since if it held line detail the API would have had it too. One PDF
routinely bundles several such pairs — one per SI document on the PO — so
`fetch-invoice-doc` groups the pages into `documents` and flags which group is
the one you asked for.

> **Build status.** Working end to end. Extraction and reconciliation are
> covered by `scripts/_selftest.py` (33 tests) and were run against a real
> two-document download (PO P13554), with both documents' lines reconciling to
> the cent, and the **whole chain has since run end to end on a live document**:
> API lookup → placeholder detected → portal login → download → segment → OCR →
> reconcile → `verified`, variance 0.00 (SI 24684277, 183.20 + 215.20 = 398.40).
> The portal automation was confirmed on the live portal: a
> `capture-portal` run logged in, searched, parsed both rows, ticked one, and
> pulled back a 121,619-byte PDF in 17.9s. `fetch-invoice-doc` has then been run
> end to end for a single `si_doc_number` — it matched that one row, downloaded
> a 2-page document (not the 4-page PO bundle), and extracted the scanned vendor
> invoice to a PNG for reading.
>
> **Headless is confirmed** — a cold run completed the same chain in 20.7s.
> Still open, and listed in
> [`references/sportsweb_flow_notes.md`](references/sportsweb_flow_notes.md):
> every run has been from a **local machine**, so a datacenter IP is untested
> (Auth0 treats a cloud runner as a new device);
> **multi-page results** are not handled (`hdnMaxPage` is read but the driver
> takes page 1 only); and the Archived-tab fallback has never been exercised.
> `{"pdf_path": "/path/to/invoice.pdf", "si_doc_number": 24682750}` still works
> for a PDF pulled by hand.

### The portal flow

```
www.sportsinc.us  →  click DEALER LOGIN  →  sportsweb.us.auth0.com/u/login
  →  swv3.sportsinc.com/home        ← the home screen, and the only search box
  →  type the PO, click Search      → swv2h.sportsinc.com/Member/InvoiceCenter/…
  →  tick the matching row(s)  →  Downloads  →  "PDF File"
```

Three steps in that chain are counter-intuitive, and each cost a debugging round:
the login redirect **403s** if navigated to directly (it must be clicked from the
public site); home and the Invoice Center are **different hosts**, so a session
check pointed at the wrong one always fails and forces a needless re-login; and
the Invoice Center **404s** on a direct hit even though its URL appears in the
address bar after a search.

Nothing waits on `networkidle` — the Vue home screen holds connections open and
may never reach it, and a long wait for an event that will not come looks exactly
like a hang. Every wait targets a concrete element, and each step is recorded
with elapsed milliseconds in the `trace` that `capture-portal` returns. Downloading is **two clicks**: `Downloads` opens
an in-page dialog, and `PDF File` inside it merges every ticked document into
one PDF.

Selectors bind to what is durable. WebForms ids are
`<framework prefix>_<authored control name>`, so controls are matched on the
**suffix** (`table[id$='grdInvoices']`, `input[id$='_chkItem']`); Auth0's classes
are per-build hashes and are never used, its ids are. Rows are matched on their
`SI Doc No.` cell, never by position — downloading the wrong invoice is the one
failure reconciliation cannot catch, since another document's lines are
internally consistent and simply tie to a different header.

One trap worth knowing about, because it would fail quietly: the grid's
frozen-header script **clones the entire `<thead>` into body cells**, so a naive
cell read returns every column heading followed by the value. Cell text is read
with a tree walker that skips cloned headers, and any value that still carries
one is rejected rather than trimmed.

### `capture-portal` — run this first

```bash
python3 scripts/sportslink.py capture-portal '{"search": "P13554"}'
python3 scripts/sportslink.py capture-portal '{"search": "P13554", "probe_download": true}'
```

Add `{"archived": true}` to exercise the Archived-tab path (tab switch, column
selection, re-search) — the one branch of the flow that has never run.

A read-only diagnostic: logs in, runs the search, and reports the landing URL,
which elements it located, the portal's own hidden state fields, and the rows it
parsed — plus a full-page screenshot and the page HTML. With `probe_download` it
walks the download dialog and records how the file arrives (a download event or
an inline response), its size, and whether it starts with `%PDF-`. Nothing is
modified either way. Add `{"headless": false}` to watch it run.

`download_format` reaches the dialog's other options (`pdf_zip`, `csv`,
`csv_items`, `pdf_and_csv`); `pdf` is the default and the only one this skill
uses. In particular the portal's *CSV with Header and Item Detail* export is
**not** a shortcut around reading the scan — for a header-only document it comes
back with no item detail, because it is fed by the same EDI line data the
SportsLink API exposes. If the CSV had the lines, the API would have had them.

### `fetch-invoice-doc`

```bash
python3 scripts/sportslink.py fetch-invoice-doc '{"si_doc_number": 24682750}'
```

Fetches the PDF, classifies every page, and makes the readable parts readable:

- `documents` — the stack split into `{si_cover_page, detail_pages,
  si_doc_number_candidates, supplier_doc_candidates, detail_is_scanned,
  matches_requested}`. Read the group with `matches_requested: true` and
  reconcile one document at a time.
- `text` — **every readable page, native or OCR'd**, page-marked. A transcribed
  page is labelled `[OCR: rapidocr, mean confidence 0.98]` so it can never be
  mistaken for the document's own text layer — only one of the two can misread a
  digit.
- `image_paths` — PNGs extracted from the scanned pages (`…-p2.png` for page 2).
  Kept as the cross-check even when OCR succeeded. The scans sit two levels deep
  inside Form XObjects, so they are pulled out explicitly rather than left to a
  PDF renderer that may not exist on the host.
- `pages[].kind` — `si_cover` | `text` | `image` | `blank`, per page.
- `readable_text_covers_all_pages` — the flag that matters: every page has text,
  from either source. (`has_text_layer` is true whenever *any* page has a native
  layer, and the SI covers always do, so a naive read of it concludes a scanned
  invoice is fully readable when it contains no line detail at all.
  `text_covers_all_pages` means native text alone was enough.)
- `ocr_pages` / `ocr_engine` / `pages_without_text` — which pages were
  transcribed, by what, and which could not be read at all.
- `pdf_path` — the whole PDF, kept as a fallback when any page is scanned.

Multi-page results are handled: a single document is found by narrowing the grid
search to its SI Doc No. rather than paging, and a whole-PO fetch reads every
page and merges the per-page downloads (selection does not survive paging).
`pages_searched` and `download_parts` in the response say what it took.

Identify what to fetch with `si_doc_number` (one document — preferred, less to
disambiguate) or `po_number` (every supplier invoice on that PO in one browser
trip; the Invoice Center searches by PO and returns a row per invoice, and its
*Downloads* button combines the ticked rows into one PDF).

**Active then Archived, automatically.** A miss on the Active tab re-runs the
search on Archived — no flag, because a caller usually cannot know which tab a
document is on. `portal_tab` in the response says where it was found, and a hit
on Archived also returns `already_historical_warning`: Sports Inc marks a
document historical only after it has been billed, so finding it there is a
duplicate-payment tell, not a routing detail. `stash`
(`auto` | `always` | `never`) controls what gets written. Other options:
`pdf_path` (read a PDF off disk instead of the portal), `force` (re-read a
document that *does* have EDI lines — normally refused), and inline `username` /
`password` / `base_url` portal overrides.

The response carries the document's identity — PO, invoice number, date,
supplier, credit flag — but **deliberately not its money**. Extraction should be
blind to the total it will be checked against; an agent that knows the
merchandise total can unconsciously bend a misread line to hit it, which is the
exact error the next step exists to catch.

### You read it

[`references/pdf_extraction.md`](references/pdf_extraction.md) is the extraction
guide: which pages to read and which to skip, how to confirm you are on the
right vendor invoice, the field mapping, the rules (transcribe don't compute,
never infer a quantity, bill the shipped quantity, one object per printed row,
skip subtotals and freight), and a worked example from a real download. Read it
before extracting.

### `reconcile-lines`

```bash
python3 scripts/sportslink.py reconcile-lines '{"si_doc_number": 23962348, "lines": [...]}'
```

Normalises your lines into the canonical shape and checks them against the
header **fetched fresh from SportsLink** — never against numbers you supply,
since a check against what the same agent just read verifies nothing:

1. **Per-line math** — `qty_shipped × net_price` = `extension`, ±$0.02.
2. **The anchor** — extensions must sum to `merchandiseTotal`, allowing a cent
   of rounding per line. Falls back to `docTotal` minus charges when the header's
   merchandise total is missing (an OCR gap).
3. **Doc-total reassembly** — informational.

Returns `status: "verified"` — an invoice in the ordinary normalised shape, with
`lines_source: "pdf"`, that the payables workflow bills exactly like an EDI one —
or `status: "needs_review"` with a per-issue breakdown.

**A `needs_review` invoice is never billed.** Re-reading the PDF and re-running
is fine and often the fix (a variance equal to one line's extension usually means
a missed row on page two). Adjusting a line to make the total tie is not: the
whole value of this path is that a model's reading gets audited by arithmetic it
doesn't control. If a second reading agrees with the first, escalate and leave
the SI document active.

`reconcile-lines` marks nothing historical — the exactly-once seam stays exactly
where it is.

## Where this fits

Source adapter (this) → payables **workflow** (`drivethru-payable-matching`) →
ERP **adapter** (`drivethru-odoo` / `drivethru_mcp`). This skill owns only the
"get the invoices + mark them consumed" half; matching to POs, correcting
pricing, and creating the draft bill live in the workflow. See that skill's
`references/sportsinc_payables.md` for the end-to-end procedure.

That procedure currently escalates every header-only document to a human. Once
the portal capture lands and `fetch-invoice-doc` works unattended, its
"**No lines?** → escalate" step should instead route through the PDF fallback and
escalate only on `needs_review`.

## References

- [`references/sportslink_api.md`](references/sportslink_api.md) — the API
  itself: parameters, document/line fields, and the semantics behind them.
- [`references/pdf_extraction.md`](references/pdf_extraction.md) — how to read a
  scanned invoice PDF into line items. **Read before extracting.**
- [`references/sportsweb_flow_notes.md`](references/sportsweb_flow_notes.md) —
  the portal capture checklist. **Start here to finish the browser flow.**

Offline tests for the extraction/reconciliation halves:
`python3 scripts/_selftest.py` (needs `pypdf`; `reportlab` optional).

## Agent-to-Agent (A2A) Mode

The `get-for-a2a` action provides a **contract-driven interface** for inter-agent
communication. Deploy this skill on a dedicated Sports Inc agent and let the
internal agent that needs invoices (e.g. an Accounts Payable agent) reach it via
a **delegation connection** in the Knoxville platform.

### Where `SPORTSINC_API_KEY` comes from (credential broker)

The `SPORTSINC_API_KEY` is bound to the **calling** agent (the one that
represents your company — e.g. Accounts Payable), not to this Sports Inc agent.
On that agent's delegation connection to this one, the operator chooses to
**share** `SPORTSINC_API_KEY` with the connection.

The value is **pulled on demand**, not pushed. When this agent handles a
delegated call (`X-Knox-Caller-Kind: agent`), **the runtime** (not you) fetches
the shared `SPORTSINC_API_KEY` for this conversation and places it into the
skill's **execution environment for this turn only**, before your `exec` runs.
The platform verifies this agent is the target of the delegated conversation and
that the connection shares the credential, and **logs the access in
`agent_connection_audit_log`**. `sportslink.py` then reads `SPORTSINC_API_KEY`
from the environment exactly as it does standalone. You do **not** see this value
in your context — it is deliberately kept out of the model prompt.

**So on a delegated turn, just run the tool.** Your first action for a Sports
Inc request is the `exec` call itself — e.g.
`python3 scripts/sportslink.py get-for-a2a '{...}'`. Do **not**, before running
it:

- call `get_my_bundle`, `get_delegated_credentials`, or any tool to look for or
  "verify" the key — it is intentionally invisible to you, so you will always
  find nothing and wrongly conclude you have no access;
- spawn a sub-agent (`sessions_spawn`) to do this skill's job — you are the agent
  that runs it;
- tell the caller you lack the key or access **before** you have actually run the
  script and read its output.

If the script itself reports an `auth_error` (or `config_error`), the caller's
connection hasn't shared the credential — surface that error rather than
guessing, and never print the credential value into the chat reply.

### Request Contract

`get-for-a2a` params (all optional):

```json
{
  "customer_ref": "DEALER-001",
  "date_range": { "start": "2024-01-01", "end": "2024-12-31" },
  "include_historical": false
}
```

- `include_historical` (default `false`) → active/un-imported invoices only;
  set `true` to also include historical/consumed docs.
- `customer_ref` is **advisory only** — the SportsLink API key is per-dealer and
  the API has no customer filter, so this field does **not** scope the result. It
  is echoed back in `metadata.customer_ref` for the caller's audit.

### Response Contract

Unlike the other actions (which exit non-zero on error), `get-for-a2a` **always
exits 0** and reports failure in-band, so an A2A caller reads one envelope shape
either way.

Success:

```json
{
  "success": true,
  "invoices": [ { "source": "sports_inc", "po_number": "P13189", "si_doc_number": 12345, "total": 1500.00, "lines": [] } ],
  "metadata": { "count": 42, "total_count": 50, "pages_read": 1, "source": "sports_inc", "customer_ref": "DEALER-001", "include_historical": false },
  "error": null
}
```

Error:

```json
{
  "success": false,
  "invoices": null,
  "metadata": null,
  "error": {
    "type": "auth_error|connection_error|api_error|validation_error",
    "message": "Human-readable error message",
    "retriable": true
  }
}
```

### Replying to a delegated *task* — compact markdown, not raw JSON

The JSON envelope above is the contract for a **synchronous** `send_message`
call, where the caller reads the object programmatically. But when the payables
agent reaches you as an **async delegated task** (it `start_task`s you a request
and you report back with an outcome/summary), your reply is **free text another
agent reads**, and that summary field has a hard **~20,000-character limit**. A
raw JSON dump of several POs' invoices overflows it and is **silently
truncated** — which hands the payables agent a half-parsed payload and corrupts
its billing. (This is exactly what happened once: five POs of pretty-printed
JSON, cut off mid-object.)

So on a delegated task, **run `get-for-a2a` / `list` as usual, then hand back a
compact markdown breakdown** in your outcome summary — never paste the raw
JSON. Markdown carries all the same data in a fraction of the characters and the
payables agent reads it directly (it does not need strict JSON). Include every
field it needs, terse, and **do not wrap it in a code fence** (fences add bulk
and confuse parsing):

- One `## <po_number>` heading per PO.
- One bullet per SI document: `si_doc_number`, `invoice_number`,
  `invoice_date`, `due_date`, `is_credit`, `has_lines`, and the money from
  `charges` + `total` (`merchandise`, `freight`, `si_upcharge`, `total`).
- Under each document with `has_lines: true`, one terse line per item:
  `item`, `upc`, `size`, `qty_shipped`, `net_price`, `extension`, `description`.
  For a `has_lines: false` document write `detail no` and omit item lines.

Example — keep it this tight (normalised field values, no code fence around it
in your real reply):

```text
## P09409
- SI 23962348 | inv# 6164920830 | 2026-02-16 | due 2026-05-10 | credit no | detail yes | merch 51.00 freight 8.58 upcharge 0.48 total 60.06
  - JP1477 | 197612326076 | S | qtyShip 1 | net 12.75 | ext 12.75 | TF SHRT TIGHT M BLACK
  - JP1477 | 197612326083 | M | qtyShip 3 | net 12.75 | ext 38.25 | TF SHRT TIGHT M BLACK
- SI 23972779 | inv# 6164929812 | 2026-02-17 | due 2026-05-10 | credit no | detail yes | merch 180.61 freight 0.00 upcharge 1.45 total 182.06
  - JJ1179 | 196476717082 | L | qtyShip 1 | net 25.50 | ext 25.50 | GG SL HD MGREYH
```

If even the compact form would be too large (many POs, many lines), **never cut
it silently**: return the POs you can and end with an explicit
`NOTE: truncated — returned N of M POs, ask again for the rest`, so the caller
knows to re-request rather than bill from a partial payload.

The `retriable` flag indicates whether the caller should retry (transient
connection errors) or escalate (auth/config errors).
