---
name: rolling-suds-workiz-note-builder
description: Build concise internal Rolling Suds Workiz notes for exterior cleaning sales and estimating workflows. Use when turning rolling-suds-customer-quote-intake results, residential-property-rolling-suds-estimator results, appointment notes, or messy sales/job information into clean Workiz-ready internal notes, including appointment notes, estimate notes, comparison notes, and follow-up notes.
homepage: https://github.com/mwdearing/rolling-suds-workiz-note-builder
metadata:
  {
    "openclaw":
      {
        "emoji": "🗒️"
      },
  }
---

# Rolling Suds Workiz note builder

Current skill version: **0.1.5**

Turn intake and estimate context into clean internal notes for Workiz.

## Core job

Take any of these inputs:
- quote-intake output
- property-estimator output
- messy sales notes
- appointment details
- estimate details
- comparison pricing logic
- follow-up context

Convert them into short, practical Workiz-ready notes.

## Note types

Support these modes by default:

### 1) Appointment note
Use when a quote visit or appointment has been booked.
Include:
- customer name if known
- address
- visit date/time
- whether the appointment is in-person or virtual
- requested service(s)
- what still needs confirmation on-site or via photos/access

### 2) Estimate note
Use when a price or range has been prepared.
Include:
- scope being quoted
- estimate range or target
- important assumptions
- confidence or pending confirmation details

### 3) Comparison note
Use when the sales logic should show two choices.
Especially useful for:
- whole-house recommended vs partial-only minimum
- bundled work vs single-service minimum situations

### 4) Follow-up note
Use when the team still needs:
- photos
- scope clarification
- material confirmation
- schedule confirmation
- added services confirmation

## Core rules

- Keep notes short and internal-facing.
- Do not sound like marketing copy.
- Do not sound like a chatbot.
- Use factual wording.
- Prefer one strong paragraph or a few tight sentences.
- Preserve sales-important logic, especially when pricing comparison matters.
- If a customer asked for only part of the house, preserve the comparison between recommended whole-house pricing and the $250 partial-only minimum when relevant.
- Treat virtual quotes as a primary workflow, not a fallback.

## Default output style

Good Workiz notes should:
- be easy to paste
- capture the important business logic
- make follow-up needs obvious
- avoid fluff
- avoid fake precision

## Default workflow

1. Identify what kind of note is needed: appointment, estimate, comparison, or follow-up.
2. Pull out only the details that matter operationally.
3. Remove awkward source wording.
4. Preserve the key sales or estimating logic.
5. Output a clean Workiz-ready note.

## Preferred patterns

### Appointment note pattern
- Customer booked [in-person or virtual] quote appointment for [service] at [address] on [date/time]. [Key scope clue]. Final quote still depends on confirming [missing pieces].

### Estimate note pattern
- Quoted [service/scope] at [address]. Estimated range [range] based on [key assumptions]. Final pricing still depends on [missing or confirm-on-site items].

### Comparison note pattern
- Customer asked about [partial scope]. Because the single-service minimum is $250, note should show [recommended full option] as the better value and [partial-only option] as the minimum comparison.

### Follow-up note pattern
- Need follow-up on [missing details]. Estimate/quote still depends on [key unresolved items].

## Input pairing guidance

This skill pairs well with:
- `rolling-suds-customer-quote-intake` for appointment/follow-up notes
- `residential-property-rolling-suds-estimator` for estimate/comparison notes

## Interaction style

- Be practical.
- Be concise.
- Favor internal clarity over pretty writing.
- Keep the note usable by a sales or office person without translation.

Read `references/default-design.md` before major edits or iteration.
