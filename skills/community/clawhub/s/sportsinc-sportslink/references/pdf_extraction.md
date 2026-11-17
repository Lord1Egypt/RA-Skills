# Reading a Sports Inc invoice PDF — extraction guide

You are here because a SportsLink document came back `has_lines: false`. Sports
Inc scanned it rather than receiving it as EDI, so the API has the header money
but no line items.

The *interpretation* is *your* job. The Python around you does everything
deterministic first: it fetches the PDF, classifies its pages, extracts the
scanned ones, **OCRs them into text**, and then audits the lines you hand back.

So you are normally reading text, not looking at a picture. That ordering is
deliberate — text is a fraction of the context cost, and it can be diffed,
grepped and logged. The images stay on disk for when the text is not good
enough, and there is no extraction *model* anywhere in the pipeline: OCR
transcribes, you interpret, arithmetic checks.

## The loop

```bash
# 1. Get the document and make it readable.
python3 scripts/sportslink.py fetch-invoice-doc '{"si_doc_number": 24682750}'

# 2. You read it. (This document.)

# 3. Hand the lines back to be checked against the API's header money.
python3 scripts/sportslink.py reconcile-lines '{"si_doc_number": 24682750, "lines": [...]}'
```

Step 3 returns `status: "verified"` — a normalised invoice the payables workflow
consumes exactly like an EDI one — or `status: "needs_review"`. **Only a
`verified` invoice may be billed.**

## What a Sports Inc download actually contains

Not one invoice. A stack of documents, each of which is two parts:

| | Page | Content |
|---|---|---|
| **SI cover** | landscape, native text | Sports Inc's own invoice. **No line detail** — it says, in as many words, `SEE VENDOR INVOICE FOR DETAIL.` Carries the SI document number, the PO number, and the totals. |
| **Vendor invoice** | portrait, usually a **300dpi scan** | The actual supplier invoice. **This is where the line items are.** |

One PDF routinely holds several of these pairs — one per SI document on the PO.

**Ignore the SI cover pages.** They are useless for extraction; if they held line
detail, the API would have had it too. Their only jobs are to divide the stack
into documents and to tell you which SI document number each vendor invoice
belongs to.

`fetch-invoice-doc` does that division for you:

```json
"documents": [
  {"si_cover_page": 1, "detail_pages": [2], "detail_is_scanned": true,
   "si_doc_number_candidates": [24682750], "supplier_doc_candidates": ["SI3503366"],
   "matches_requested": true},
  {"si_cover_page": 3, "detail_pages": [4], "detail_is_scanned": true,
   "si_doc_number_candidates": [24684277], "supplier_doc_candidates": ["SI3503509"],
   "matches_requested": false}
]
```

**Extract the document with `matches_requested: true`, and reconcile one document
at a time.** Its lines tie to *its* SI document's totals, not to the stack's.
The others in the same PDF are separate SI documents with their own
`si_doc_number`; handle each with its own `fetch-invoice-doc` /
`reconcile-lines` pair. If nothing matches, `notes` will say so — stop and check
you have the right PDF rather than extracting the first document you see.

## How to read the pages — text first

**Read `text`.** It carries every readable page in page order, including the
scanned ones, which are OCR'd before you see them. A transcribed page is marked:

```
----- page 2 of 2 -----  [OCR: rapidocr, mean confidence 0.976]
     A062RY       ROYAL     Adult1-1/2"   80EA   80EA   0EA   $2.29   $183.20
     AS1RY-L      ROYAL                   80PR   80PR   OPR   $2.69   $215.20
                                                Subtotal:             $398.40
```

Column positions are reconstructed from the OCR boxes, so a line still reads as
a row. Note what OCR gets wrong even on a clean scan: `OPR` for `0PR`, `$O` for
`$0`, and the size `L` on the second line dropped entirely. **Digits and money
are what matter, and those came through exactly.**

The other fields:

- `image_paths` — PNGs of the scanned pages. Kept even when OCR succeeded, as
  the cross-check for anything that looks wrong.
- `readable_text_covers_all_pages` — every page has text, from either source.
- `ocr_pages` / `ocr_engine` — which pages were transcribed and by what.
- `pages_without_text` — pages nothing could read. If this is non-empty, the
  images are the only way in.
- `pages[].kind` — `si_cover` / `text` / `image` / `blank` per page.
- `pdf_path` — the whole PDF, kept as a last resort.

Do not trust `has_text_layer` on its own: it is true whenever *any* page has a
native text layer, and the SI covers always do.

### When to look at the image instead

OCR is the cheap first attempt, not the last word. Read the image when:

- a row's numbers look implausible, or a column is obviously missing;
- the row appears in `low_confidence_rows`. That list is deliberately narrow: a
  row is flagged only when a token **carrying a number** is doubtful, and
  `weakest_value` names it. A shaky colour or product name does not qualify,
  because no arithmetic downstream consumes it — on a real scan the money read
  at 1.00 while whole rows scored 0.68 on the backorder zeros, and flagging
  those would mark every line item on every invoice as suspect. Each row also
  reports `confidence` (worst token of any kind) next to `value_confidence`
  (worst number), so you can see the difference;
- **`reconcile-lines` comes back with a variance.** That is the designed
  escalation: text → image → escalate to a human. A misread digit is exactly
  what the merchandise-total check exists to catch, so a failed reconciliation
  is a prompt to look at the scan, not to give up.

This ordering is why OCR is safe here at all. Nothing it transcribes reaches a
bill without tying to the API's own header.

Note what is **not** in the response: the merchandise total, the doc total, the
charges. That omission is deliberate. Extraction must be blind to the number it
will be checked against — knowing the target is how a misread line quietly gets
bent to hit it. Transcribe what the page says and let the check do its job.

## Cross-check you have the right invoice

Before extracting, confirm the vendor invoice you are reading belongs to the SI
document you asked for:

- The vendor invoice's **PO #** should match the SI document's `po_number`.
- The vendor invoice's **INVOICE #** should match the SI cover's supplier
  document number, ignoring punctuation — `SI-3503366` on the vendor invoice is
  `SI3503366` in `supplier_doc_candidates` and in SportsLink's
  `supplierDocNumber`.

If they disagree, stop. Reconciliation will *not* reliably catch a
wrong-document mix-up: another invoice's lines are internally consistent, they
just belong to a different header.

## The fields

One object per line item, in reading order. Field names are flexible (`style`,
`quantity`, `unit_price`, `amount` and other common aliases are accepted), but
these are the canonical ones:

| Field | What it is | Required |
|---|---|---|
| `item` | The supplier's item/SKU number | strongly preferred |
| `upc` | UPC/barcode, digits only | if printed |
| `description` | The product description as printed | if printed |
| `size` | Size as printed (`S/M`, `L`, `Adult 1-1/2"`) | if printed |
| `color` | Color as printed | if printed |
| `unit` | Unit of measure — **`EA` and `PR` are not the same thing** | if printed |
| `qty_shipped` | Quantity **shipped/billed** — the one the money is based on | **yes** |
| `qty_ordered` | Quantity ordered, when both are shown | if printed |
| `qty_backordered` | Quantity backordered (`B.ORDERED`) | if printed |
| `list_price` | Undiscounted unit price | if printed |
| `discount_pct` | Discount percentage | if printed |
| `net_price` | The unit price actually billed (`UNIT PRICE`) | **yes** |
| `extension` | The line's extended amount (`ITEM TOTAL`) | **yes** |

A line missing any of the three required fields comes back `needs_review` — that
is intended. An unreadable row is a reason to escalate, not to guess.

## Rules

**Transcribe, don't compute.** Report the numbers the invoice prints. If a page
prints qty, unit price, and item total, give all three even when they look
inconsistent — an inconsistency you preserve is a caught error, one you silently
fix is a billing error. (When a value genuinely isn't printed, leave it out; the
normaliser derives the one missing leg of qty × net = extension and marks it
`derived`.)

**Never infer a quantity.** Price and extension can sometimes be recovered from
each other. A quantity cannot. If you can't read it, leave it out.

**Bill the shipped quantity.** Invoices show ORDERED, SHIPPED, and B.ORDERED.
The money follows SHIPPED; put the other two in their own fields.

**One object per printed line.** Don't merge two sizes of one item into a
combined quantity, and don't split a line into per-unit rows. Size-broken
apparel invoices repeat the same item number many times — keep each row.

**Skip everything that isn't a line item.** Subtotal, Freight Flatrate, TOTAL,
tax, remittance blocks, "continued" markers. Freight and the SI upcharge are
already in the API header — adding either as a line will fail reconciliation,
which is exactly what should happen.

**Multi-page vendor invoices continue.** A per-page subtotal is not the invoice
total. Read every detail page in the document's `detail_pages` before you stop.

**Credits are negative.** On a credit memo (`is_credit: true` on the fetch
response), transcribe amounts as negative. A credit memo is never billed
regardless of what reconciliation says — it goes to a human.

**UPCs are digits.** Strip spaces and hyphens; keep leading zeros.

## Worked example — PO P13554

The download holds two documents. Reading the second one's vendor invoice
(page 4, a Champro scan):

```
INVOICE #: SI-3503509        PO #: P13554
PRODUCT / SKU   COLOR   SIZE          ORDERED  SHIPPED  B.ORDERED  UNIT PRICE  ITEM TOTAL
MVP Belt
A062RY          ROYAL   Adult 1-1/2"    80 EA    80 EA      0 EA        $2.29     $183.20
Pro Sock
AS1RY-L         ROYAL   L               80 PR    80 PR      0 PR        $2.69     $215.20
                                                            Subtotal:            $398.40
                                                            Freight Flatrate:         $0
                                                            TOTAL:               $398.40
```

Extract:

```json
{
  "si_doc_number": 24684277,
  "lines": [
    {"item": "A062RY", "description": "MVP Belt", "color": "ROYAL",
     "size": "Adult 1-1/2\"", "unit": "EA",
     "qty_ordered": 80, "qty_shipped": 80, "qty_backordered": 0,
     "net_price": 2.29, "extension": 183.20},
    {"item": "AS1RY-L", "description": "Pro Sock", "color": "ROYAL",
     "size": "L", "unit": "PR",
     "qty_ordered": 80, "qty_shipped": 80, "qty_backordered": 0,
     "net_price": 2.69, "extension": 215.20}
  ]
}
```

Subtotal, Freight Flatrate, and TOTAL are **not** lines. Reconciliation sums the
two extensions to 398.40 and ties them to the SI document's merchandise total —
the SI upcharge of 3.19 that makes up the 401.59 document total is SI's, not a
vendor line.

## What the check actually checks

1. **Per-line math** — `qty_shipped × net_price` = `extension`, ±$0.02.
2. **The anchor** — extensions must sum to the API's `merchandiseTotal`, allowing
   a cent of rounding per line. Catches a dropped line, a doubled line, or a
   misread that per-line math can't see. Falls back to `docTotal` minus charges
   when the header has no merchandise total.
3. **Doc total reassembly** — informational.

A vendor invoice's own TOTAL normally equals the SI merchandise total, since SI
adds its upcharge and freight on top. If the two disagree, that is a real
discrepancy for a human — not something to reconcile away.

## When it comes back `needs_review`

Read the `issues` list; each names the line and the variance. Then:

- **Re-read and re-run.** Usually the answer — a variance equal to one line's
  extension means a row was missed, often on a second detail page.
- **Escalate.** If a second reading agrees with the first, the document is the
  problem, not your reading. Leave it; the SI document stays active and
  reappears next run.
- **Do not override the check**, adjust a line to make the total tie, or bill a
  `needs_review` invoice. The whole point of this path is that a model's reading
  gets audited by arithmetic it doesn't control.

## After a verified invoice is billed

Nothing changes about the exactly-once rule: `reconcile-lines` marks nothing.
The bill gets created first, then `mark-historical`.
