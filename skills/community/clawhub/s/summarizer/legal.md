# Contracts, Policies, and Regulation

Scope: contracts, MSAs, SOWs, NDAs, terms of service, privacy policies, employment agreements, leases, insurance policies, regulation, and court filings. The reader wants to know what they must do, by when, what it costs to get out, and what is missing.

**Before summarizing an agreement with a party the user already deals with**, read `~/Clawic/data/contacts/contacts.md` for the counterparty and `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for the prior version — the value of the second summary of a contract is the diff against the first.

**Contents:** [What the Reader Needs](#what-the-reader-needs) · [Reading Order](#reading-order) · [The Clause Inventory](#the-clause-inventory) · [Dates Are the Product](#dates-are-the-product) · [Money Clauses](#money-clauses) · [Language That Changes Meaning](#language-that-changes-meaning) · [Absence Is a Finding](#absence-is-a-finding) · [Red Flags](#red-flags) · [Comparing Versions](#comparing-versions) · [Output Shape](#output-shape)

## What the Reader Needs

Four questions, in this order. Everything else is context.

1. **What am I obliged to do, and by when?**
2. **What can the other side do to me, and what does it cost me if they do?**
3. **How does this end — notice, term, auto-renewal, termination for convenience?**
4. **What is not in here that should be?**

A summary that describes the agreement's structure ("Section 4 covers payment terms") has answered none of them. Quote clause numbers as pointers, never as content.

## Reading Order

1. **Definitions** — a defined term can invert an entire clause. "Confidential Information" that excludes anything "independently developed" is a different NDA.
2. **Term, renewal, and termination** — this is where the reader is most often surprised.
3. **Schedules, exhibits, annexes, and order forms** — the commercial substance usually lives at the back; the body is boilerplate.
4. **Payment, fees, and price escalation.**
5. **Liability, indemnity, and caps.**
6. **Anything incorporated by reference** — a URL to a policy the vendor can change unilaterally is part of the contract and is not in the file you were given. Name it.
7. **The body prose** — last, and mostly cuttable.

## The Clause Inventory

The checklist for a commercial agreement. Present = summarize the substance; absent = say so (→ Absence Is a Finding).

| Clause | What the summary states |
|---|---|
| Parties and signatories | Exact legal entities, not brand names — the subsidiary that signs is who owes |
| Term and effective date | Start, length, and whether it has already started |
| Renewal | Auto-renew yes/no, notice window, and the resulting deadline |
| Termination | For cause, for convenience, notice period each way, what survives |
| Fees | Amount with currency, frequency, escalation formula or index, late-payment terms |
| Payment terms | Net days, invoicing trigger, disputed-invoice mechanism |
| Scope / deliverables | What is promised, and what is expressly out of scope |
| SLA and remedies | Target, measurement window, whether the credit is the sole remedy |
| Liability cap | Amount or formula, and every carve-out that escapes it |
| Indemnity | Who indemnifies whom, for what, and whether it is capped |
| IP ownership | Who owns deliverables, background IP, and derived data |
| Data and privacy | Processing purpose, sub-processors, location, deletion on exit, breach notice window |
| Confidentiality | Duration, carve-outs, return/destruction obligation |
| Exclusivity and non-compete | Scope, geography, duration |
| Assignment and change of control | Whether the counterparty can transfer the contract to an acquirer |
| Governing law and venue | Jurisdiction, and arbitration versus courts |
| Force majeure | Whether it excuses payment |
| Amendment | Whether unilateral changes by reference are permitted |

## Dates Are the Product

Every date in an agreement becomes a deadline for someone, and deadlines are the one part of a contract summary that has to leave the summary and enter a calendar.

- **Compute the notice deadline, do not restate the notice period.** "60 days' notice before the 31 March renewal" means the action date is **29 January**, and that is the number the reader needs. Formula: `action date = renewal or expiry date − notice period`; if the clause counts business days, say so, because it moves the date.
- **Auto-renewal without a diarized notice date is how a contract renews itself.** It is the single most common commercial loss this skill can prevent.
- **Distinguish effective date, signature date, and commencement date** — they differ often enough that assuming they match produces a wrong deadline.
- **Cure periods** ("30 days to remedy after written notice") are deadlines on the reader too.
- Any date computed here goes into the `## Due` table of `memory.md` as a one-off row (`Every: once`), because a deadline that lives only in a chat message is not a deadline.

## Money Clauses

| Item | Read for | Common surprise |
|---|---|---|
| Fee escalation | Fixed %, index-linked (CPI), or "at vendor's discretion" | Index-linked with no cap compounds; state the formula, not "annual increase" |
| Minimum commitment | Floor payable regardless of usage | Priced per-seat but with a minimum — the effective unit price is higher |
| Overage | Rate above the committed volume | Frequently a multiple of the committed rate |
| Liability cap | Amount, or a formula like "fees paid in the preceding 12 months" | A formula cap on a new contract is near zero in year one |
| Cap carve-outs | Breach of confidentiality, IP infringement, gross negligence, data breach | Carve-outs make the cap decorative; list them |
| Late payment | Interest rate and suspension rights | Suspension of service on late payment is an operational risk, not a finance one |
| Currency and FX | Which currency, who bears conversion | Always write the currency in the value (`120,000 EUR`), never a bare symbol |
| Taxes | Whether fees are inclusive or exclusive of VAT/sales tax | "Plus applicable taxes" moves the real number |

## Language That Changes Meaning

Small words with large consequences. These are copied verbatim, never paraphrased (SKILL.md Rule 3).

| Wording | Means |
|---|---|
| "shall" / "must" | Obligation |
| "may" | Permission, no obligation — never summarize as "will" |
| "commercially reasonable efforts" | A materially weaker standard than "best efforts" |
| "including without limitation" | The list is examples, not the boundary |
| "sole discretion" | No obligation to be reasonable; the clause has no floor |
| "material" (breach, change) | Undefined unless defined; a dispute waiting to happen |
| "notwithstanding the foregoing" | The previous clause has just been overridden |
| "subject to Section X" | The clause you are reading is conditional on one you have not read |
| "as amended from time to time" | The other side can change it unilaterally |
| "net 30 from receipt of a valid invoice" | The clock starts on validity, which the payer judges |

## Absence Is a Finding

A contract summary that lists only what is present is half a summary. Explicitly check for and report missing: liability cap, termination for convenience, data-deletion obligation, breach-notification window, SLA remedy, IP assignment of deliverables, assignment restriction, and a defined dispute process. "The agreement contains no cap on the customer's liability" is often the most valuable line in the output.

## Red Flags

Signals that suspend the ordinary compression: they go in the summary regardless of length target, and the summary says plainly that a lawyer should look at them. This skill summarizes documents; it does not advise on whether to sign.

| Signal (observable) | Why it matters | Action |
|---|---|---|
| Unlimited or uncapped liability for one side | One incident can exceed the contract's value | Name it in the first three lines |
| Auto-renewal with a notice window already inside 30 days | The decision window is closing now | State the action date first, before any other content |
| Unilateral amendment by URL reference | Terms can change without signature | Name the URL and that it is incorporated |
| IP assignment covering pre-existing work | Background IP transferred by accident | Quote the clause verbatim |
| Personal guarantee by an individual | Corporate shield removed | Name the individual and the amount |
| Governing law in an unexpected jurisdiction | Enforcement cost may exceed the claim | State jurisdiction and forum |
| Non-compete with no geographic or time bound | May be unenforceable, may not; either way it is a live risk | Quote it |
| Indemnity flowing only one way | Asymmetric risk allocation | State the direction explicitly |
| A defined term that contradicts its ordinary meaning | The whole document reads differently | Lead the summary with the definition |
| Anything in this table | — | Flag it, quote the clause, and recommend legal review of that clause specifically |

## Comparing Versions

When a redline, a renewal, or a counterparty's markup arrives, the summary is a diff, not a fresh reading.

- Report by consequence, not by section order: what got worse for the reader, what got better, what is new, what was deleted.
- **A deletion is a change.** Removing the liability cap leaves no text to notice.
- Numeric changes are stated as `was → now` with both values and the delta.
- Definition changes propagate: a changed definition silently edits every clause that uses the term. Check usage count before calling it minor.

## Output Shape

```
<Agreement type> — <Party A> / <Party B>, <effective date>. Term: <length>, <renewal type>.

Act by: <date> — <what happens if you do not>
Money: <fees with currency, frequency, escalation>
Exit: <notice each way, what survives>
Risk: <liability cap and its carve-outs; indemnity direction>
Data: <processing, location, deletion, breach notice window>
Missing: <clauses that are not present and should be>
Flagged for legal review: <clause numbers with one line each>
Omitted: <boilerplate not covered>
```

**After summarizing an agreement**, write every computed deadline as a one-off row in the `## Due` table of `~/Clawic/data/summarizer/memory.md`; register the document in `## Sources`; write the full summary to `summaries/<counterparty>-<agreement>-<year>.md` when `store_summaries: full`, with every credential, account number, and tokenized link replaced by its `<kind>:<locator>` pointer; add defined terms that recur across the user's agreements to `glossary.md`; put the counterparty in the shared `~/Clawic/data/contacts/contacts.md` by name only; and if the agreement belongs to a tracked engagement, note it in `~/Clawic/data/projects/<project>.md`. Formats and thresholds: `memory-template.md`.
