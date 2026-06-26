---
name: rolling-suds-customer-quote-intake
description: Normalize messy Rolling Suds customer or salesperson inputs for exterior cleaning jobs into a clean intake summary, estimator-ready handoff, Workiz-friendly internal note, follow-up questions, and manual-review flags. Use when the input is a text message, pasted chat, call summary, address plus notes, photos plus notes, or any rough service request for house washing, driveways, patios, porches, sidewalks, decks, fences, or window cleaning.
homepage: https://github.com/mwdearing/rolling-suds-customer-quote-intake
metadata:
  {
    "openclaw":
      {
        "emoji": "🧾"
      },
  }
---

# Rolling Suds customer quote intake

Current skill version: **0.1.10**

Turn messy job requests into clean, actionable intake output for sales and estimating.

## Core job

Take rough real-world inputs such as:
- customer text messages
- salesperson notes
- pasted chat transcripts
- address only
- address plus notes
- photos plus notes
- rough call summaries

Convert them into:
1. intake summary
2. estimator handoff
3. Workiz note
4. follow-up questions
5. manual-review flags

## Core rules

- Require the **Lead number** before producing an estimator-ready handoff. Example: `Lead 502` or `Lead 501`.
- If the Lead number is missing, stop and ask for it before handing off to the estimator.
- Clean up the input before pricing anything.
- Do not price the job directly unless the user explicitly asks; prefer handing off to `residential-property-rolling-suds-estimator`.
- If the wording says the customer agreed to an in-person visit, treat that as a real-quote appointment signal.
- If the wording says the customer agreed to a virtual appointment, treat that as a real virtual-quote appointment signal.
- Normalize vague phrasing into clear service names and property clues.
- Separate **known facts** from **assumptions**.
- Address is required before estimate workflow can move forward.
- Ask only the smallest useful set of follow-up questions.
- Flag manual-review issues early instead of pretending confidence.
- Keep output short, practical, and internal-use friendly.

## Recognize these services

Normalize messy language into these service categories when possible:
- house wash
- driveway cleaning
- patio cleaning
- porch cleaning
- sidewalk cleaning
- deck cleaning
- fence cleaning
- window cleaning

Examples of messy wording to normalize:
- pressure wash the house
- powerwash driveway
- front concrete
- back patio
- clean windows
- wash the fence
- soft wash siding

## Output format

Always return these blocks.

### 1) Intake summary
```text
Intake Summary
- Lead number:
- Address:
- Service area fit:
- Requested services:
- Property clues:
- Condition clues:
- Scheduling notes:
- Intake confidence:
```

### 2) Estimator handoff
```text
Estimator Handoff
Address:
Requested services:
Known details:
Missing details:
Manual review flags:
```

### 3) Workiz note
```text
Workiz Note
...
```

### 4) Follow-up questions
```text
Follow-up Questions
- ...
- ...
```

### 5) Manual review flags
```text
Manual Review Flags
- ...
```

## Intake workflow

1. Read the raw input.
2. Extract Workiz Lead # when present, address, city, services requested, property clues, condition clues, schedule clues, appointment status clues, appointment type clues, and obvious blockers.
3. If the Lead number is missing, stop and request it before estimator handoff.
4. Normalize services and remove duplicate phrasing.
5. If the wording indicates an agreed in-person visit, classify it as a quote appointment rather than a vague lead.
6. If the wording indicates a virtual appointment, classify it as a quote appointment and note any photo/access dependency.
7. Decide what is known versus assumed.
8. Produce an estimator-ready handoff only when the Lead number and required estimating data exist.
9. Produce a short Workiz note.
10. Ask only the highest-value missing questions.
11. Flag manual-review items.

## Follow-up question priorities

Ask only what meaningfully improves estimate quality.

High priority:
- Lead number if missing
- exact address if missing
- services requested if unclear
- photos available?
- whether the quote is virtual or in-person if unclear
- siding type if relevant to house wash
- fence type if fence cleaning is requested or mentioned
- deck/fence wood finish if natural wood risk exists
- timing / preferred schedule if relevant

Also ask when clearly needed:
- driveway size clues
- gate / dog / access issues
- heavy stains, oxidation, rust, or unusual buildup
- whether windows are part of the request

## Manual-review triggers

Flag these by default when present or strongly implied:
- chain link fence
- commercial or multi-unit property
- incomplete or invalid address
- outside St. Louis metro / beyond 50 miles
- natural wood deck or fence
- unknown fence type
- mixed exterior materials
- heavy oxidation, rust, oil, or unusual staining
- low-confidence scope with no photos
- steep access, gate issues, dogs, or unusual site constraints

## Confidence guidance

Use **high** intake confidence when:
- address is complete
- requested services are clear
- important materials/features are identified
- few critical follow-up questions remain

Use **medium** when:
- major services are clear
- some property clues are present
- a few useful questions remain

Use **low** when:
- address is incomplete or unverified
- services are vague
- scope depends heavily on missing photos or unknown materials

If the Lead number is missing, do not continue to estimator-ready workflow.
If address is missing, do not continue to estimator-ready workflow as if the lead were valid for pricing.

## Handoff behavior

When enough information exists, make the estimator handoff easy to paste directly into `residential-property-rolling-suds-estimator`.
Preserve the Workiz Lead # in the handoff.

If the input is too weak for estimating, say so and emphasize the missing pieces.
If customer/contact details are missing only because they were not included in a pasted lead description blob, say that clearly instead of implying the CRM lacks them.
If the Lead number is missing, treat that as required missing data and do not produce an estimator-ready handoff.
If the address is missing, treat that as required missing data and do not produce an estimator-ready handoff.

If the customer asks for only part of the house, note that the $250 single-service minimum may make a whole-house quote the better customer value.
For those cases, tee up the estimator to provide both a recommended whole-house quote and a separate $250 partial-only comparison quote.

This skill is designed to hand off cleanly to `residential-property-rolling-suds-estimator`.
When possible, make the `Estimator Handoff` block easy to paste directly into that skill.

## Workiz note style

Keep the Workiz note:
- short
- factual
- internal-facing
- easy to paste
- free of assistant fluff
- clear about whether this is an in-person or virtual quote appointment when the wording implies that

Good style:
- Customer requesting house wash and driveway cleaning at single-family home in Florissant. Notes suggest vinyl siding and large driveway. Final estimate pending confirmation of exterior condition and any additional surfaces.

## Interaction style

- Be practical.
- Prefer short bullets over long paragraphs.
- Do not act like a chatbot.
- Do not use fake certainty.

## Wording interpretation rule

Some cold-calling or lead-gen services use awkward phrasing.
Interpret intent, not just literal wording.

Examples:
- "agreed to an in-person visit" -> treat as a real quote appointment
- "agreed to a virtual appointment" -> treat as a real virtual quote appointment
- "interested to avail" -> treat as interest in service, not as a literal phrase to preserve
- awkward grammar should be normalized into clean internal wording

Read `references/default-design.md` before major edits or iteration.
