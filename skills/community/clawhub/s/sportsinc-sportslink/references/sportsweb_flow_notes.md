# SportsWeb portal — invoice PDF flow

The reverse-engineered flow behind `scripts/sportsweb_browser.py`, captured from
a live walkthrough of the portal.

**Status: confirmed end to end on the live portal.** A `capture-portal` run with
`probe_download` logged in, searched, parsed both P13554 rows, ticked one, and
pulled back a 121,619-byte PDF in 17.9 seconds — see "What the live run proved"
below.

## Hosts

| | |
|---|---|
| Public site | `https://www.sportsinc.us/` — Wix marketing site. **The entry point**: its DEALER LOGIN button must be *clicked*. |
| Login entry | `https://swv3.sportsinc.com/login-redirect` — the button's href. **Returns 403 on a direct hit**; only works as a click-through. |
| Identity provider | `https://sportsweb.us.auth0.com/u/login?state=…` (Auth0 Universal Login) |
| **Home screen** | `https://swv3.sportsinc.com/home` — where login lands, and the **only** page with a search box |
| Invoice Center | `https://swv2h.sportsinc.com/Member/InvoiceCenter/Default.aspx` — where the search navigates to |

**Home and the Invoice Center are different hosts.** That is not cosmetic: a
session check pointed at `swv2h` can never find the search box, so it always
reports "not logged in" and sends every run through a full login it did not
need. `SPORTSINC_WEB_HOME_URL` overrides the home; `SPORTSINC_WEB_BASE_URL` the
Invoice Center host.

The Invoice Center is **ASP.NET WebForms**; the home screen around it is a Vue
app. Both appear in the flow.

## Waiting — never on `networkidle`

The home screen is a Vue app that holds connections open, so `networkidle` may
simply never arrive. Waiting on it is indistinguishable from a hang, and it is
what made the first live run appear to freeze. Every wait is for a concrete
element, timeouts default to 25s (`SPORTSINC_WEB_TIMEOUT_MS`), and every step is
recorded with elapsed milliseconds in the `trace` that `capture-portal` returns —
so a slow run reports where it is instead of going quiet. A selftest guards
against `networkidle` being reintroduced.

## Selector strategy

Generated ids are avoided where they are truly generated, but WebForms ids have
a useful property: `ctl00_ContentPlaceHolder1_grdInvoices` is
`<framework prefix>_<developer's control name>`. The **suffix** is authored and
stable; the prefix is the framework's. So controls are matched on the suffix —
`table[id$='grdInvoices']`, `input[id$='_chkItem']`,
`a[id$='lbDisplayDownload']` — which survives a page restructure that moves the
prefix. Auth0's classes are per-build hashes (`c72825458`) and are never used;
its ids (`#username`, `#password`) are.

A row is matched on its **SI Doc No.** cell, never by position. Downloading the
wrong invoice is the one failure reconciliation cannot catch: another document's
lines are internally consistent and simply tie to a different header.

---

## Step 1 — Login ✅ confirmed live

Load `https://www.sportsinc.us/` and **click** the DEALER LOGIN button
(`a[href*='login-redirect']` — its Wix classes are generated, the href is not).
The button carries `target="_blank"`, which is stripped before the click so the
flow stays in one page; a popup is adopted if one opens anyway.

Do **not** navigate to the button's href directly: it returns 403. (It does
eventually bounce to the login form on its own, which is why an early version
appeared to work — it was just outlasting the 403 page with a 45s wait.)

The chain then reaches Auth0 with a per-session `state`. **Never construct that
URL** — let the redirect produce it.

| Element | Selector |
|---|---|
| Username / email | `input#username` |
| Password | `input#password` |
| Submit | `button[type=submit][name=action]` ("Continue") |
| Session token | `input[name=state]`, hidden, submitted with the form |

Unused: **Continue with Google** (`form[data-provider=google]`) and *Reset
password*. Staying on `sportsweb.us.auth0.com` after submit means failure; the
driver reads `#ulp-error-announcer` / `[role=alert]` for the reason, and a `/mfa`
URL raises a distinct error pointing at `SPORTSINC_WEB_STATE_PATH`.

Login lands on `https://swv3.sportsinc.com/home`. The definitive "we are in"
signal is that page's search box — not a load state.

**Still to confirm:** whether MFA/device verification appears from a datacenter
IP (a local Windows run did not trigger one).

### Session reuse

`SPORTSINC_WEB_STATE_PATH` persists the session (Playwright `storage_state`) and
restores it next run, skipping Auth0 entirely — and it is the escape hatch if MFA
turns out to be mandatory: log in once by hand with it set.

## Step 2 — Reaching the Invoice Center ✅ confirmed live — **not by URL**

```
https://swv2h.sportsinc.com/Member/InvoiceCenter/Default.aspx?search=P13554
```

That URL appears in the address bar after a search, and it is the `href` of the
search button — **but navigating to it directly returns 404.** The page is only
reachable by submitting the home screen's search box.

So after login, on the home screen:

| Element | Selector |
|---|---|
| Search box | `.search-bar input[placeholder='Search for Invoice']` (Vue component) |
| Search button | `.search-bar .search-button a` |

Fill, click, wait for the grid. The button's `href` is built by the page's own
script, so it is clicked rather than read and re-navigated.

## Step 3 — The results grid ✅ confirmed live

Grid: `table[id$='grdInvoices']`. Rows: `tr.gridview-row` / `tr.gridview-alt-row`
(alternating classes). Columns, in order:

`☐ · Supplier · Supplier Doc No. · PO No. · SI Doc No. · SI Doc Date · Due Date ·
Archived Date (hidden on Active) · Discount Date · Total`

P13554 returns two rows: SI3503366 / 24682750 / $5.23 and SI3503509 / 24684277 /
$401.59.

### ⚠ The frozen-header trap

The page's frozen-header script **clones the entire `<thead>` into individual
body cells**. The PO cell is really:

```html
<span id="…_dealerPONum"><thead>…every column heading…</thead>P13554</span>
```

Consequences, all of which the driver handles explicitly:

- A naive `td.textContent` returns `"Supplier Supplier Doc No. PO No. … Total
  P13554"`. Cell text is therefore read with a `TreeWalker` that skips any node
  inside a `thead`/`th`, and any value that still contains a heading is
  **rejected**, not trimmed — trimming would be guessing at which invoice to
  download.
- An unscoped `table.locator("th")` matches the clones too and shifts every
  column index. Headers are read as `:scope > thead > tr > th`.
- Each cloned header carries a copy of the **select-all** checkbox
  (`chkAll`), so "the first checkbox in the row" finds the wrong control. Row
  selection targets `input[id$='_chkItem']`.

### Tabs — switching **resets the results**

`#activeInv` / `#histInv` anchors, backed by hidden submits
(`btnViewActive` / `btnViewHistorical`, both `class="hidden"` — click the
anchors, not the inputs).

The Archived tab does **not** inherit the home screen's search. Reaching an
archived document is a three-step sequence, and skipping any of it silently
reads the wrong result set:

1. click `#histInv`;
2. set `select[id$='ddlSearchBy']` to the column you are searching — normally
   `DealerPONum` (PO No.), or `ASWDocNum` when only the SI doc number is known.
   It defaults to `-- select search column --`, which matches nothing;
3. fill `input[id$='tbSearch']` and click `input[id$='btnSearchInvoices']`.

Then the checkbox and download flow is identical to Active.

`fetch-invoice-doc` runs this fallback **automatically** when the Active tab has
no matching row — callers do not pass a flag, because they usually cannot know
which tab a document is on. The response reports `portal_tab`, and an Archived
hit also carries `already_historical_warning`: under this skill's exactly-once
rule a document becomes historical only after a bill was created, so finding one
there means it may already have been paid.

`hdnInvoiceView` flips to the historical view and is asserted after the tab
click, so a switch that silently did not happen fails loudly rather than
searching the Active tab and reporting "not found".

Every one of those buttons is a real form submit, so each click is a
*navigation*. The driver waits for it — reading rows in the gap between click
and reload returns the **previous** search, which looks like a correct result
for the wrong query.

### In-grid search

Beyond the home-screen search there is a column-scoped search on the results
page: `select[id$='ddlSearchBy']` + `input[id$='tbSearch']` +
`input[id$='btnSearchInvoices']`. The dropdown's values answer the open question
about what is searchable:

`SupplierName` · `SupplierDocNum` · **`ASWDocNum` (SI Doc No.)** · `ASWDocDate`
· `HistoricalDate` · `DueDate` · `DiscountDate` · **`DealerPONum` (PO No.)** ·
`DocTotal`

Not currently used — the driver searches by PO from the home screen and matches
rows client-side — but it is the way to narrow a PO with many invoices.

### Paging ✅ handled

The portal reports its own position: `hdnPageIndex` (0-based) and `hdnMaxPage`
(a count). Read those rather than inferring from the links — the whole pager is
`display: none` when there is one page. Navigation is
`lbFirstPage` / `lbPrevPage` / `lbNextPage` / `lbLastPage`, all `__doPostBack`;
the numbered links only ever show a five-page window, so Next/Prev is what the
driver walks, verifying `hdnPageIndex` actually moved after every hop.

Two rules, because page 1 alone cannot tell *"this document is not here"* from
*"this document is on page 3"*:

- **Looking for one document?** Narrow rather than page. `search_in_grid` by
  `ASWDocNum` collapses the result to that single row on page 1 in one postback,
  regardless of how many pages the PO spans.
- **Fetching a whole PO?** Read every page, even when page 1 already matched —
  otherwise the download silently covers a subset of the PO.

**Selection does not survive paging.** The pager is a postback that re-renders
the grid, so ticks are lost. Rows spanning pages are therefore downloaded a page
at a time and the parts merged with `pypdf`, which keeps the rest of the pipeline
oblivious: `prepare()` segments the combined file exactly as it does a
single-page download. `download_parts` in the fetch metadata says how many
downloads went into it.

Other hidden state worth reading: `hdnInvoiceView` (`Active`/`Historical`),
`hdnIsSearch`.

## Step 4 — Download ✅ confirmed live — **two clicks, not one**

1. `a[id$='lbDisplayDownload']` ("Downloads") — a `__doPostBack` that opens an
   in-page jQuery-UI dialog, `#downloadOptions`.
2. A format link inside that dialog.

| Format | Control | Note |
|---|---|---|
| **PDF File** | `a[id$='lbPDFPrint']` | "all selected documents to a **single** PDF" — what this skill uses |
| PDF Zip File | `a[id$='btnDownloadPDF']` | one PDF per document, zipped |
| CSV with Header Detail | `a[id$='btnDownloadCSV']` | header only |
| CSV with Header and Item Detail | `a[id$='btnDownloadWithItemDetails']` | ✗ empty for these documents — see below |
| PDF and CSV | `a[id$='btnDownloadBoth']` | zipped |

### ✅ Settled: the CSV export is not a shortcut

`CSV with Header and Item Detail` promises "item details **if they exist**", which
looked like it might beat reading a scan outright — structured data, no
extraction, no reconciliation risk. It is **not** a way out: for a header-only
document it comes back with no item detail, because it is fed by the same EDI
line data the SportsLink API exposes. If the CSV had the lines, the API would
have had them, and this fallback would not exist.

So the PDF path is the primary and only route for scanned documents. The other
formats stay mapped in `DOWNLOAD_FORMATS` because they are a faithful catalog of
the dialog and `capture-portal` can reach them, not because any of them help
here.

### ✅ Confirmed: a browser download, from a session-bound URL

The file arrives as a real download (`mechanism: "download"`), from:

```
https://swv2h.sportsinc.com/Member/InvoiceCenter/InvoicePDF.aspx?v=SupplierName&x=ASC&t=1786041790403
```

Those parameters are the grid's **sort column**, **sort direction**, and a
cache-buster. There is **no document identifier**. Which documents the PDF
contains is held in server-side session state from the ticked checkboxes, so:

- `context.request.get(url)` is not an option — that URL means nothing without
  the session's selection, and re-fetching it later would return whatever is
  ticked then.
- There is no way to skip the browser. Driving the page *is* the API.

The driver reads the download's bytes and unlinks the temp file. It still
watches for an inline PDF response as a fallback, in case the portal changes.

The dialog does appear with only one row ticked, and a single-row selection
returns just that document (121,619 bytes for SI 24682750, against 248,559 for
the two-document bundle).

- [ ] Whether `View` differs from `Downloads` (inline viewer vs. file). Not
      needed — noted only for completeness.

## Step 5 — Bot mitigation / headless

No WAF interstitial, CAPTCHA, or device check appeared on a headed run from a
local Windows machine. What remains untested is the environment this will
actually run in.

### What headless changes, and what is done about it

Headless differs from headed in three ways that break portals, none of them
about rendering:

1. **The user agent** says `HeadlessChrome`. Overridden with a desktop Chrome UA.
2. **`navigator.webdriver` is true.** Hidden by
   `--disable-blink-features=AutomationControlled`, with an init script masking
   the property as belt-and-braces for builds where the flag alone does not.
3. **The default viewport is 1280×720** — small enough for a responsive layout
   to collapse its desktop navigation. The home screen's search box is a Vue
   component, and a collapsed layout could hide it outright, so the viewport is
   pinned to 1440×900 rather than left to the default. This is the most likely
   headless-specific failure and the least obvious.

### Failure artefacts

A headless run has no window to look at, so any failure now writes
`failure-<label>.png` and `failure-<label>.html` to the scratch directory and
names them in the error, alongside the step trace. The first failing run is the
diagnostic one — there is no need to reproduce it to find out what happened.

- [x] **Headless works.** A cold run (session file deleted, so a full Auth0
      login) completed the whole chain in 20.7s and downloaded the same
      121,619-byte PDF: `"headless": true`, `logged_in: true`, both rows parsed,
      `mechanism: "download"`.

      Worth recording precisely: that run was on the code from *before* the
      hardening above — no pinned viewport, no webdriver mask, no stealth flag —
      and it still worked at the default 1280×720. So the portal applies no
      headless-specific blocking, and the search box survives a narrow viewport.
      The hardening is insurance for the datacenter case, not a fix for
      something observed.
- [ ] Any WAF or device check on login from a **datacenter IP**? A local run is
      not evidence here — Auth0 treats a cloud runner as a new device. This is
      the last real unknown in the flow.
- [ ] Does the deploy host's egress reach `swv2h.sportsinc.com`,
      `swv3.sportsinc.com`, and `sportsweb.us.auth0.com`? This dev container
      reaches none of them.

### Timing

A full cold run took 17.9s headed, 20.7s headless — the difference is noise, and
the public Wix site is 9–12s of either. Everything after login is under 4s. With
`SPORTSINC_WEB_STATE_PATH` set, a warm run should skip the first ~15s entirely;
the trace will start at `session-restored` rather than `public-site-loaded`.

Note that a run *writes* the session file on the way out, so testing a cold
login twice in a row means deleting it in between — otherwise the second run
silently skips the step being tested.

---

## Closing the gaps: run the capture

```bash
export SPORTSINC_WEB_USERNAME=... SPORTSINC_WEB_PASSWORD=...

# Log in, search a PO, report what is there. Read-only.
python3 scripts/sportslink.py capture-portal '{"search": "P13554"}'

# Same, plus tick the first row and walk the download dialog.
python3 scripts/sportslink.py capture-portal '{"search": "P13554", "probe_download": true}'
```

`download_format` reaches the dialog's other options (`pdf_zip`, `csv`,
`csv_items`, `pdf_and_csv`) if one is ever needed; `pdf` is the default and the
only one this skill uses.

It reports the landing URL, which elements it located, the portal's own hidden
state fields, the parsed rows, and — with `probe_download` — the download
mechanism, byte count, whether the bytes start with `%PDF-`, and where the file
was saved. It also writes a full-page screenshot and the page HTML.

Add `{"headless": false}` to watch it run.

## What the live runs proved

A `capture-portal` run (headed, Windows, `'{"search": "P13554"}'`) returned:

```json
"landing_url": "https://swv3.sportsinc.com/home",
"logged_in": true,
"invoice_center_url": "https://swv2h.sportsinc.com/Member/InvoiceCenter/Default.aspx?search=P13554",
"page": {
  "title": "Dealer Invoice Center",
  "results_grid_found": true,
  "headers": {"Supplier":1,"Supplier Doc No.":2,"PO No.":3,"SI Doc No.":4,
              "SI Doc Date":5,"Due Date":6,"Archived Date":7,"Discount Date":8,"Total":9},
  "elements": {"grid":1,"row_checkboxes":2,"downloads_link":1,
               "download_dialog":1,"active_tab":1,"archived_tab":1},
  "state": {"hdnInvoiceView":"Active","hdnMaxPage":"1"},
  "row_count": 2
},
"rows": [
  {"row_index":0,"Supplier":"CHAMPRO SPORTS","Supplier Doc No.":"SI3503366",
   "PO No.":"P13554","SI Doc No.":"24682750","Total":"$5.23"},
  {"row_index":1,"Supplier":"CHAMPRO SPORTS","Supplier Doc No.":"SI3503509",
   "PO No.":"P13554","SI Doc No.":"24684277","Total":"$401.59"}
]
```

A second run with `probe_download` added:

```json
"download": {"ok": true, "format": "pdf", "mechanism": "download",
             "url": ".../InvoicePDF.aspx?v=SupplierName&x=ASC&t=1786041790403",
             "bytes": 121619, "looks_like_pdf": true},
"trace": [{"step":"public-site-loaded","ms":9025},
          {"step":"login-form-visible","ms":11138},
          {"step":"credentials-submitted","ms":12949},
          {"step":"logged-in","ms":14580,"url":"https://swv3.sportsinc.com/home"},
          {"step":"search-submitted","ms":15446},
          {"step":"grid-loaded","ms":16048},
          {"step":"rows-selected","ms":17407,"count":1},
          {"step":"downloads-clicked","ms":17515},
          {"step":"download-dialog-open","ms":17539},
          {"step":"download-event","ms":17859}]
```

Settled by that:

- Auth0 login works unattended; no MFA from a local Windows run.
- The session carries across `swv3` → `swv2h`.
- **The frozen-header defence works.** `"PO No.": "P13554"` — the tree walker
  stripped the cloned headings, and the leak guard did not fire.
- Column indices are right (0 is the unnamed checkbox column).
- `row_checkboxes: 2` — `chkItem` targeting finds the real per-row boxes, not
  the cloned select-all.
- Both tabs, the Downloads link, and the dialog element are all present.
- The two-click download works: the dialog opens on one ticked row, and
  "PDF File" returns that one document as a browser download.
- No MFA, WAF interstitial, or device check on a local headed run.

A third run exercised the real entry point — `fetch-invoice-doc` with a specific
`si_doc_number`, which matches one row rather than taking the first:

```json
"pdf_source": "sportsweb", "page_count": 2, "pdf_bytes": 127435,
"documents": [{"si_cover_page": 1, "detail_pages": [2], "detail_is_scanned": true,
               "si_doc_number_candidates": [24684277],
               "supplier_doc_candidates": ["SI3503509"], "matches_requested": true}],
"text_covers_all_pages": false, "image_pages": [2],
"image_paths": ["…/si-24684277-p2.png"]
```

Two pages, not the four of the PO-level bundle — so row matching selected the
requested document. The cover page's text layer carries 398.40 / 3.19 / 401.59
and the sentinel "SEE VENDOR INVOICE FOR DETAIL.", the scan was extracted to a
PNG, and the whole chain from API lookup to readable image ran unattended.

Note `"home_search_input": 0` in that output: `describe()` ran on the results
page (swv2h), where the home search box does not exist. Expected, not a fault.

## What is still open

The portal flow is proven; these are the gaps around it.

- **Headless, and from a datacenter IP.** Every run so far has been headed on a
  local Windows machine. Auth0 treats a cloud runner as a new device.
- ~~Multi-page results~~ — handled (see Paging above), but not yet exercised
  against a PO that actually spans pages.
- **The Archived tab fallback.** Now implements the full three-step sequence
  (tab → column → search) rather than just clicking the tab, but is still
  unexercised: no test document has been marked historical. Test it with
  `capture-portal '{"search": "<PO>", "archived": true}'`.
- **A wrong-document guard.** After fetching, the SI cover page's text layer
  carries the SI document number and PO — cross-checking them against what was
  requested would close the one hole reconciliation cannot.
- `python3 scripts/_selftest.py` green (33 tests) — the offline half.
