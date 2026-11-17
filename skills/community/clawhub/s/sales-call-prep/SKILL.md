---
name: sales-call-prep
description: Run the ten-stage sales call-prep route on a company and produce a formatted PDF brief (account brief, earnings-call pain, contact role, discovery questions, opener, buying committee, objections, competitors, battle card, follow-up plan). Use when the user gives a company name for call prep, account research, or a battle card.
version: 1.0.0
author: Eric Gonzalez (route), packaged for Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [sales, research, call-prep, pdf, battle-card]
    related_skills: []
---

# Call-Prep Route

The user gives you a company. You run all ten stages in order and return a PDF.
They should never have to write a research prompt.

Support files (load on demand):
- `references/prompts.md` - the ten prompts, stop-rule fallbacks, and "done" criteria. Read first.
- `references/seller-profile.md` - the user's product, proof points, pricing, method.
- `scripts/build_brief_pdf.py` - JSON payload to PDF. Schema is in its header docstring.
- `assets/sample_payload.json` - complete fictional payload showing the exact shape.

## When to Use

- "Prep me for a call with X", "research X for a sales call", "brief me on X"
- "Build a battle card for X", "run the route on X"
- A bare company name in a sales context

Do not use for general company research with no sales purpose.

## Procedure

1. **Intake (ask at most once).** Required: company name. Optional: contact name and title, deal
   type. Read `references/seller-profile.md`; if `STATUS: TEMPLATE`, ask ONE batched question for
   the fields marked (*) and offer to save the answers into that file. If the user says just run
   it, proceed and tag solution-fit content "inferred". Resolve the company with a search, verify
   the domain from results (never guess it), state the identity you chose in one line, and ask
   only if the name is truly ambiguous.
2. **Load `references/prompts.md`** and run stages 01 to 10 in order. Carry findings forward:
   discovery questions trace to stages 01-03, the opener to a dated finding, the battle card to
   stages 06-08, the follow-up to everything. Budget about 12-20 searches or page extractions;
   search each distinct item separately; prefer primary sources (company site, IR pages, SEC
   filings, press releases); extract full pages rather than relying on snippets.
3. **Apply the stop rule at every stage.** If a source is gated or missing, record it in `gaps[]`
   with a concrete ask ("Paste her last 3 posts"). Never bypass logins or paywalls. Never invent
   names, quotes, prices, metrics, or customer results; write "Not public" or "Needs rep input".
   Tag each claim `sourced` (with a source id) or `inferred`.
4. **Quotes.** Stage 02 needs exact wording: short verbatim excerpts (at most two sentences) with
   speaker, call, and link. If exact wording is unavailable, drop the quote and tag "inferred".
5. **Write the payload** to `~/call-prep/<company-slug>/payload.json`, matching
   `assets/sample_payload.json`. Set `meta.prepared_on` to today and `meta.sample` to false.
   Write `snapshot.takeaways` last.
6. **Validate**: `python3 scripts/build_brief_pdf.py <payload.json> --validate` (run from the
   skill directory, `~/.hermes/skills/sales-call-prep/`). Fix real warnings.
7. **Build**: `python3 scripts/build_brief_pdf.py <payload.json> ~/call-prep/<company-slug>/<company-slug>-call-prep-<YYYY-MM-DD>.pdf`.
   If reportlab is missing, `pip install reportlab`.
8. **Deliver.** Attach the PDF if the current platform supports file attachments; otherwise print
   the full path. Reply briefly: the three findings most likely to change the call, then the gaps
   that need the user's input. State that the follow-up email is a draft and nothing was sent.

## Pitfalls

- Wrong-company research from a guessed domain. Verify from search results.
- Turning a fact into a bigger claim ("hired a VP of Data" is not "building an AI team"). Label inference.
- Inventing proof points or competitor pricing. Only use the seller profile or cited sources.
- Long verbatim passages from transcripts. Keep excerpts short.
- Payload item counts off: 3 pain points, 5 discovery questions, 3 objections, 5 battle-card entries.
- Unicode symbols outside Latin-1 in text; the script replaces them, so avoid them.

## Verification

- `--validate` prints no unresolved source ids or count warnings.
- Every empty stage has a matching `gaps[]` entry.
- Open one or two rendered pages (`pdftoppm -r 60 -png file.pdf out`) and check for clipped text
  or orphaned headings.
- The PDF page 1 shows the snapshot, meta table, and route status; the last page lists gaps and sources.
