# Telegram Reply Templates

Instance A speaks in **accountant-friendly English**. Never mention XML, HTTP, bridge, OpenClaw, or API internals unless the user asks for technical detail.

## Entry posted (success)

```
Entry posted to Tally.

Company: {company}
Type: {voucher_type}
Party: {party_name}
Voucher / Invoice No: {number}
Date: {date_formatted}
Amount: ₹{total_formatted}
{tax_breakdown_line}

{masters_line}
```

`{tax_breakdown_line}` examples:

- Purchase/Sales GST: `Taxable: ₹{taxable} + IGST: ₹{igst}` or `+ CGST: ₹{cgst} + SGST: ₹{sgst}`
- Receipt/Payment: omit or use `Against: {narration}`

`{masters_line}` (only if non-empty):

```
New ledger(s) created: {comma_separated_names}
```

## Needs clarification (from bridge)

```
I need a few details before posting this to Tally:

{numbered_questions}

Please reply with the missing information.
```

Example questions:

- "What is the party GSTIN?"
- "Which voucher class should I use? (e.g. Purchase @ 18 %)"
- "Which bank ledger should I use for this receipt?"

## Low confidence before posting (Instance A self-check)

```
I've extracted the invoice but I'm not fully sure about:

{field_list}

Please confirm or correct these values before I post to Tally.
```

## Tally not running (health check failed)

```
Tally is not running on your machine right now. Please open TallyPrime, ensure the company "{company}" is loaded, and send the document again.
```

## Bridge unreachable

```
I couldn't reach your Tally setup right now. Please check that your connection tunnel is active and try again in a few minutes.
```

## Extraction in progress

```
Received your invoice. Extracting details now…
```

## Duplicate / already posted

```
This invoice was already posted to Tally earlier (Invoice {number}, {date_formatted}). No duplicate entry was created.
```

## Error (generic)

```
Something went wrong while posting to Tally: {user_safe_message}

Please try again. If it keeps failing, check that TallyPrime is open and the company name is correct.
```

## User asks for PDF (redirect mentally — optional on A)

If user asks for a PDF **after** posting, Instance A may reply:

```
PDF generation runs on your Tally machine. I've asked the system to generate it — you'll receive the file shortly.
```

(Only if `/v1/generate-pdf` is wired; otherwise say PDF requests should be sent while Tally bridge is up and handled on Instance B.)

## Tone rules

- Use ₹ and Indian number formatting (e.g. ₹46,199.83)
- Dates: `18 May 2026` not `2026-05-18` in user messages
- Say "Entry posted" not "XML import succeeded"
- Say "Tally is connected" not "health endpoint returned 200"
