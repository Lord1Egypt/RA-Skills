# Errors & Troubleshooting — TallyPrime XML

This file is a practical troubleshooting guide for CA automation using TallyPrime XML-over-HTTP.

## Quick triage checklist

1. **Server reachable**: `curl -s --max-time 5 "$TALLY_URL"`
2. **Company correct**: `SVCURRENTCOMPANY` exact spelling (including spaces/case).
3. **Date format**: `YYYYMMDD`, and within the company’s configured financial year.
4. **Dependent masters exist**: ledgers, stock items, UOM, voucher types.
5. **Totals match**: Dr/Cr totals equal.
6. **XML escaped**: narration and names don’t contain raw `&`, `<`, `>`.

## Common errors (what they mean + how to fix)

| Symptom / error text | Likely cause | Fix |
|---|---|---|
| Connection refused / timeout | TallyPrime not running or wrong port | Open TallyPrime; confirm port; check `$TALLY_URL` |
| Response doesn’t contain “Server is Running” | Wrong URL or Tally integration not enabled | Verify TallyPrime is running and integration is enabled |
| XML parser throws `ParseError` / "no element found" | Export Data responses are XML fragments (no single root) — this is by design | Use Python regex instead of `xml.etree.ElementTree`; see parsing guide in `reference/reports.md` |
| `curl ... > file` produces truncated or empty file | Shell redirect can silently truncate in compound commands | Use `curl --output /tmp/file.xml` (the `-o` flag) |
| `Could not find Report 'X'` | Wrong `REPORTNAME` | Use report names in `reference/reports.md`; if still failing, verify in TallyPrime Developer |
| `Could not find Collection 'X'` | Collection not available | Use custom TDL pattern (see `reference/reports.md`) |
| `Ledger 'X' does not exist` | Missing ledger master | Create ledger first (see `reference/masters.md`) |
| `Stock Item 'X' does not exist` | Missing inventory master | Create stock item/UOM (see `reference/inventory.md`) |
| `Voucher date is missing` / `The date ... is Out of Range` | Date outside configured FY | Ask user to confirm FY settings in the company; use a valid date |
| `Voucher totals do not match!` | Dr/Cr totals mismatch (or wrong sign conventions) | Ensure totals balance; export a known-good voucher from UI and match signs/tags |
| `DESC not found` | Incorrect envelope structure / wrong request shape | Compare to base templates; ensure `REQUESTDESC` and `REQUESTDATA` are placed correctly |
| `CREATED=0` with `ERRORS>0` | Generic import failure | Inspect response details; reduce to minimal fields; add fields incrementally |
| Silent wrong-company data | Wrong `SVCURRENTCOMPANY` | Confirm exact company name as seen in Tally |

## Import response XML (what to look for)

Tally typically returns an import “statistics” block indicating how many objects were created/altered and error counts.

Common fields include:

- `CREATED`
- `ALTERED`
- `DELETED`
- `ERRORS`
- `EXCEPTIONS`
- “Last Voucher ID imported” (varies)

Rule: treat any non-zero `ERRORS` or `EXCEPTIONS` as a failure and **do not assume** posting succeeded.

## XML escaping rules (minimum)

If user-provided text contains reserved XML chars, escape them before embedding:

- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&apos;`

High-risk fields: `NARRATION`, ledger names, party names, item names.

## Debugging workflow (recommended)

When a write fails:

1. Retry with **minimal** voucher: only required tags + two ledger lines.
2. If minimal works, add optional fields one at a time (bill allocations, GST ledgers, inventory lines).
3. If minimal fails, export a similar voucher created in UI and diff structure/signs.

## Best practice: “export-first” for fragile setups

For each new client setup:

1. Create one example voucher type in UI (Sales, Purchase, Receipt, Payment, Contra, Credit Note, Debit Note).
2. Export the voucher/master to XML.
3. Store/derive the template from exported XML (this avoids sign/view surprises).

## Where to look for report names and variables

If a report or variable is inconsistent across client environments:

- Use **TallyPrime Developer** → Navigate → Jump to Definition → Report → search name (e.g., `Profit and Loss`).
- Use exported XML from the UI version of the report to infer variables (e.g., ageing slabs).

