# 4. Adversarial audit (required before publishing)

> This is step 4 of the pipeline in `SKILL.md`. Previous step: `03-writing.md`. Next step: `05-publish.md`.

The goal is to **find errors**, not to confirm that the report passes. The current form is **two rounds, five lanes each,
with a verifiability lane, a skeptic lane and a cross-edition consistency lane** (the verifiability lane was added in 1.1.0):

| Round | Lane | What it checks |
|---|---|---|
| **Round 1** (primary-language draft), five lanes | 1. Financials, capital structure, valuation | Must re-run `python3 calc/model.py` and diff against the output file, then read the body |
| | 2. Contracts, counterparties, sites, governance | Compare every item with the primary document (fetch the original from EDGAR with a self-identifying user agent) |
| | 3. Tradability, summary and risks, procedure compliance | Go through `judgment.md` section by section: does the conclusion rest on a mispricing that has evidence, does the catalyst path hold, can the rating be settled, is the payload-chain grade high enough, do the probabilities have a basis |
| | 4. Appearance and copy | `quality-bar.md` sections 3, 4, 5 and 7: headline formula, chart form, layout repetition, decorative indicators; scan the draft for filler, hype and templated phrasing; run `scripts/check_report.py` first and log every failed gate as a finding |
| | 5. Verifiability and originals | Can a reader trace each source back to its sentence? Open 30 randomly chosen footnotes and every exhibit source, go to the stated page, section or table, and check that the text and numbers are there and that no quotation was altered or cut out of context. Check that each "new fact" is really new (search mainstream financial media and sell-side summaries; a widely reported fact becomes background) and not overstated. Check that the company quotes in Part 3 are verbatim and correctly dated |
| **Round 2** (after the dispositions produce v2 and the second-language edition is synced), five lanes | Skeptic | Stand on the opposite side of the rating. Using the report's own data and **changing parameters only, never formulas**, re-run the model and give the combination of assumptions that would flip the rating, with its evidence grade. Check that all scenarios use one discounting timing convention (`investigative.md` section 1). Also check that the owner of every judgment sentence is clear at a glance |
| | Tradability | As above, but audit v2 only |
| | Financials | Re-check only the model changes |
| | Cross-edition consistency | After the alignment check shows zero differences, check the financial English and the definitions by hand, and compare Appendix C with `assets/disclaimer.md` word for word. Skip this lane if the report has one language edition |
| | Appearance re-check | Look only at the revised places |

Round 2 does not repeat the full fact-check. In practice, the value of round 2 sits mainly in the skeptic and tradability
lanes, and pure fact-checking returns diminishing value after two rounds.

Lanes 1 and 2 are both fact-checks, and they cannot stop the most likely failure mode: **every number correct and the
conclusion hanging in the air**. That is lane 3's job.

**Keep a record of every disposition.** Dispatch one `research-auditor` per lane. Each writes `audit-vN-<lane>.md`. After
each round the editor writes `audit-vN-decisions.md` (template: `assets/templates/audit-decisions.md`). For every finding
(lane initial plus serial number): upheld, partly upheld or rejected; the action taken; which table or chapter changed. A
change that affects valuation starts in `calc/model.py`: bump the version number and regenerate
`calc/model-vN-output.txt`. Summarise substantive revisions in the Appendix C revision log (original statement -> revised
statement -> nature of the change).

For scale: a four-lane first round typically yields on the order of a hundred findings and a few dozen revisions. A
two-round, nine-lane audit has produced a blocker that flipped the rating. That is normal and not an embarrassment.

**Two self-checks run alongside the audit:**

1. Compare the report with every entry in the definitions-pitfall list in `references/pitfalls.md`. Where one applies, say so
   in the definitions box or in the known limitations.
2. Check that the **eight required components** from `framework.md` section 5 are all present (the list is in step 3). If
   one is missing, send the report back.
