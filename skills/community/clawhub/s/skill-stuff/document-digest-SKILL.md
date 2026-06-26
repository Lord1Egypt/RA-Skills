---
name: document-digest
description: Reads any document and returns what it says, what is unusual, and whether to sign. Use when a user needs to understand a contract or policy before acting.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_fetch
metadata:
  openclaw.emoji: "📄"
  openclaw.user-invocable: "true"
  openclaw.category: life-admin
  openclaw.tags: "contracts,legal,documents,pdf,terms,lease,review,signing"
  openclaw.triggers: "should I sign,what does this contract say,review this document,check this terms,read this lease"
  openclaw.homepage: https://clawhub.com/skills/document-digest


# Document Digest

Long document. Short answer.
What it says. What's unusual. What to push back on. Sign or don't.

---

## On-demand only

No cron. Triggers when user shares a document.

Supported formats: PDF, DOCX, Google Docs link, pasted text, any URL pointing to a document.

---

## Trigger patterns

Activates when user:
- Shares a file attachment
- Pastes a document URL
- Says "can you read this", "what does this say", "should I sign this"
- Shares something that looks like a legal or policy document

---

## The output structure

Every document digest has five parts. Always in this order.

### 1. What this document is

One sentence. Plain language.

> "This is a 2-year commercial lease for office space in Berlin, governed by German law."
> "This is a standard SaaS subscription agreement with an auto-renewal clause."
> "This is a mutual NDA with a 3-year confidentiality period."

### 2. The short version

3-5 bullet points. What the document actually does to the person signing it.
Not a summary of every clause. What changes about their situation after signing.

> • You're committing to [X] for [Y period]
> • You're giving them the right to [Z]
> • You can't [restriction] during the term
> • They can terminate if [condition], you can only terminate if [narrower condition]
> • Auto-renews unless you give [N] days notice

### 3. What's unusual or worth flagging

This is the most important section. What deviates from standard.

Categories to check:
- **Termination asymmetry** — they can exit more easily than you can
- **Auto-renewal with short notice window** — 30 days is tight, 90 days is reasonable
- **IP assignment** — especially broad "work for hire" language
- **Liability cap** — is it capped, and at what?
- **Governing law and jurisdiction** — is it somewhere inconvenient?
- **Non-compete / non-solicitation** — scope and duration
- **Price change rights** — can they raise prices unilaterally?
- **Data rights** — what can they do with your data?
- **Indemnification** — are you indemnifying them for things beyond your control?
- **Exclusivity** — are you locked out of working with others?

For each flag:
> ⚠️ **[CLAUSE TYPE]:** [what it says in plain language]
> *Why this matters:* [practical consequence]
> *Standard would be:* [what's normal in this type of agreement]

If nothing unusual: say so. "Nothing unusual here — this is a fairly standard [document type]."

### 4. What to push back on (if anything)

Specific, actionable redlines.
Not "negotiate better terms" — actual language to propose.

> "On clause [X]: ask them to change [this language] to [suggested alternative]."
> "The auto-renewal notice period of 14 days is short. Ask for 30 days minimum."
> "The IP assignment in section [X] is broad. Ask to narrow it to work product created specifically under this agreement."

If nothing to push back on: say so.

### 5. Sign or review further

One of three verdicts:
- **Sign** — nothing unusual, standard terms, risk is proportionate
- **Sign with redlines** — sign after getting the flagged items addressed
- **Get professional advice** — stakes are high enough that a lawyer should look at this

The verdict is direct. Not "it depends" or "consult a professional for any legal questions."
If the stakes are genuinely high, say so and say why.

---

## Document type library

The skill adjusts what it looks for based on document type.

**Employment contract:**
Focus on: notice period, non-compete, IP assignment, bonus discretion, garden leave

**Commercial lease:**
Focus on: break clauses, rent review mechanism, dilapidations, service charge cap, assignment rights

**SaaS agreement:**
Focus on: data processing, uptime SLA, termination for convenience, price change rights, auto-renewal

**NDA:**
Focus on: mutual vs one-sided, duration, carve-outs, return of information, injunctive relief

**Freelance / consulting contract:**
Focus on: IP ownership, payment terms, kill fee, non-compete scope, expense reimbursement

**Terms of service:**
Focus on: arbitration clause, class action waiver, data rights, termination, account suspension

**Loan / financial agreement:**
Focus on: interest rate, default triggers, prepayment penalties, personal guarantee

---

## Caveats that are part of the output

Every document digest ends with:

> *This is not legal advice. For high-stakes documents (property, employment, significant financial commitments), get a lawyer to review before signing.*

This is baked in — not as a hedge, but because it's true and useful.
The skill reduces the number of documents that need a lawyer, not the quality of legal advice when it's needed.

---

## Management commands

- Share any document → triggers automatically
- `/digest [url or paste text]` → explicit trigger
- `/digest followup [question]` → ask a specific question about the last document
- No persistent state — each document is independent

---

## What makes it good

Most people sign documents they don't understand because reading them is exhausting.
This skill removes that excuse cleanly.

The "sign or review further" verdict is the most useful output.
It forces a decision rather than leaving everything ambiguous.

The "what's unusual" section requires knowing what's standard.
That's the part that takes knowledge. That's the part this skill provides.

Plain language throughout. No legal jargon in the output.
If the document uses jargon, translate it. That's the whole job.
