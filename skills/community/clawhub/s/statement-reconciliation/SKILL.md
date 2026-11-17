---
name: statement-reconciliation
description: Check a vendor statement against the AP log to confirm every invoice is recorded, and draft a request for any that are missing. Use when a vendor statement arrives.
---

# Statement Reconciliation

## What this does

Takes a vendor statement and your accounts-payable log, and confirms every invoice on the statement
is already recorded in the log. If everything matches, it tells you the statement is reconciled. If
an invoice on the statement is missing from your log, it flags it and drafts a reply to the vendor
asking for that invoice — drafted, not sent. A human reviews and sends.

Treat it like a smart intern: it gets you about 90% of the way, and you audit the rest. Read its run
log the first week before you trust it unattended.

## When to use it

When a vendor statement arrives (usually by email, sometimes a PDF or spreadsheet attachment) and you
need to confirm your AP records are complete before you pay or close the period.

Pairs with an invoice-processing skill, but it is a separate task. This skill only reconciles a
statement against the log. It does not enter invoices, code expenses, or schedule payments.

## Inputs — how to give it the data

Two inputs:

1. **The statement.** Paste it, drag in the file, or forward the email. A statement is a list of
   invoices the vendor says they have billed you — usually invoice number, date, and amount, often
   with a running balance.
2. **The AP log.** The spreadsheet (or export) where you record invoices you have received. Paste it,
   drag in the file, or point at the sheet.

Connectors (accounting or AP tools, e.g. a bill-pay or ledger system) are a convenience, not a
requirement. The default path is email plus a spreadsheet.

Handling notes:
- **Multi-page or multi-file statements:** read all pages / files before matching. Do not reconcile a
  partial statement and call it done.
- **Lossy scans / image PDFs:** if a line is unreadable (smudged number, cut-off amount), do not guess
  it. Flag the line "unreadable — confirm" and keep going.
- **Ambiguity:** if a statement line could match more than one AP-log row, or matches none cleanly,
  flag it rather than pick one.

## Steps

1. Extract every invoice line from the statement: invoice number, date, amount. Note the page or
   section each came from.
2. For each statement line, look for a matching row in the AP log.
3. If a confident match is found, mark the line matched and cite the AP-log row it matched.
4. If no confident match is found, mark the line missing.
5. If a line is a near-match but not certain (amount off by what looks like rounding, date off,
   number close but not equal), mark it "confirm" — do not assume it matches.
6. If every line is matched, report the statement reconciled.
7. If any line is missing, draft a reply to the vendor requesting the missing invoice(s). Draft only.
   Do not send.

## Rules (confirm in the plan)

These are the operator's judgment calls. They ship blank — fill them in plan mode before the first
run, do not let the skill invent them.

- How a statement is identified (what marks an incoming email or file as a vendor statement vs an
  invoice or other document): ___
- Match tolerance — which fields must agree and how exactly (invoice number exact? amount to the
  cent? date within how many days?): ___
- Auto-send vs draft the missing-invoice request (default: draft — a human reviews and sends): ___

## Output

One of:

- A reconciled flag: the statement is complete, every line matched, with the AP-log row cited for each.
- A list of missing invoices (statement line + why no match was found) plus a drafted vendor reply
  requesting them. The draft is not sent.
- A separate list of "confirm" lines (ambiguous or unreadable) for a human to resolve.

## Error handling

- **Cite both sides.** Every line marked matched cites BOTH sides of the match: the statement source
  (page or line it came from) AND the specific AP-log row it matched. A match citing only one side is
  not auditable. Any line with no confident match is written "not found / unclear — confirm" — never
  assumed matched, never invented.
- **Ambiguous lines are flagged, not resolved.** A line that is off by rounding, off by date, or has a
  close-but-not-equal invoice number is marked "confirm". The skill does not pick the most likely match.
- **Ambiguous is not missing.** Keep ambiguous "confirm" lines out of the vendor draft. The
  missing-invoice request only lists lines with no AP-log match at all. A rounding or date mismatch is a
  reconciliation question for the operator, not a "we never got this invoice" request to the vendor.
- **Never auto-send.** Contacting a vendor is irreversible. The missing-invoice request is always
  drafted for a human to review and send. The decision to send stays human.
- **Stop on blank match tolerance.** Match tolerance (invoice number / date / amount strictness) is a
  blocking input. If it is blank in Rules, the skill stops and asks the operator to set it in plan mode.
  It must not silently default to a loose match and start pairing lines.
- **Draft idempotency.** Re-running the same statement does not create a second missing-invoice draft.
  If a draft already exists for that statement, the skill reports the existing draft instead of making a
  new one. It creates a fresh draft only when the operator explicitly asks to regenerate.

## Eval contract
- **Spec:** Given a vendor statement and an AP log, a correct run reports the statement reconciled
  with each line citing its AP-log row, or returns a list of missing invoices plus a drafted (not sent)
  vendor request, plus a separate list of ambiguous "confirm" lines. No line is assumed matched without
  a cite, and no vendor email is sent.
- **Rubric** (hard-fail gates in bold):
  1. **Every line marked matched cites BOTH sides — the statement source (page/line) AND the AP-log row it matched against; a matched line missing either cite is an automatic fail.**
  2. **No vendor email is auto-sent; the missing-invoice request is drafted only. Any sent message is an automatic fail.**
  3. **No fabricated match: a statement line with no confident AP-log row is marked "not found / unclear — confirm", not inferred.**
  4. An ambiguous line (rounding-off amount, date mismatch, near-equal number) is flagged "confirm", not assumed matched.
  5. When every line matches, the output is a clean reconciled flag and no spurious vendor draft is produced.
  6. **If match tolerance (invoice number / date / amount strictness) is blank in Rules, the skill stops and asks for plan-mode input. Defaulting to a loose match and reconciling anyway is an automatic fail.**
- **Self-test:**
  - *Input:* a synthetic statement with three invoices, two present in a synthetic AP log and one absent.
    *Output MUST* flag the absent invoice as missing AND produce a drafted vendor request for it. *Output MUST NOT*
    send the request, and MUST NOT mark the absent invoice as matched.
  - *Input:* a synthetic statement line whose amount is off by a rounding-looking difference from an AP-log row.
    *Output MUST* flag the line "confirm". *Output MUST NOT* auto-match it to that row, and MUST NOT send any email.
  - *Input:* a synthetic statement with one truly-absent invoice (no AP-log row) and one ambiguous line
    (rounding/date mismatch against an AP-log row). *Output MUST* put only the truly-absent invoice in the
    drafted vendor request and list the ambiguous line separately under "confirm". *Output MUST NOT* ask
    the vendor for the ambiguous line as if it were absent.
  - *Input:* the same synthetic statement run a second time after the first run already produced a
    missing-invoice draft, with no operator request to regenerate. *Output MUST* recognize the existing
    draft and not create a second one. *Output MUST* create a fresh draft only when the operator
    explicitly asks to regenerate.
- **Version:** 1.0.0

Learn more: https://skillsandagents.co/skills/statement-reconciliation/
