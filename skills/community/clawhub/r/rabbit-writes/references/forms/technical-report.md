# Form: technical-report

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A commissioned document that answers a question somebody asked, with the work shown. Its reader is deciding something and needs to be able to check the reasoning, which is what separates it from a post about the same subject: a technical blog post is read by whoever finds it, and a report is read by whoever has to defend acting on it.

If it recommends a course of action to somebody who has to approve it, `forms/proposal.md` applies. If it is published to persuade a market rather than delivered to a client, `forms/whitepaper.md` applies. If it documents a specific failure, `forms/incident-report.md` applies.

## Slots

- **Title and provenance.** What was studied, for whom, and over what period. Provenance is a slot rather than a courtesy: a report with no dates is a report nobody can date the conclusions of.
- **Executive summary.** Its own form. `forms/executive-summary.md` has the slots.
- **Scope and what was excluded.** Both halves. An exclusion stated up front is a limit. The same exclusion discovered by the reader is a hole.
- **Method.** Enough that somebody with the same access could repeat it. Tools, versions, sample sizes, and the decisions made when the method met something it did not cover.
- **Findings.** One per section, each with the evidence under it. Ordered by consequence, not by the order the work happened in.
- **Analysis.** What the findings mean together, kept separate from the findings themselves. The separation is the form's main discipline: a reader must be able to accept a measurement and reject the reading of it.
- **Recommendations.** Each traceable to a finding by number. A recommendation with no finding behind it is an opinion in a document that promised evidence.
- **Limitations.** What the method could not see.
- **Appendices.** Raw data, full configurations, and anything a reader would need to reproduce rather than to follow.

## Bands

| Purpose | Band |
|---|---|
| A focused answer to one question | 1,500 to 4,000 words plus appendices |
| A full assessment | 4,000 to 12,000 words, and the summary carries most readers |
| Past that | it is several reports, and the binding is not an argument |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "A comprehensive analysis was performed." By whom, on what, with what.
- "Industry best practices" with no named standard behind it.
- "Results indicate a significant improvement" with no baseline and no interval.
- "It should be noted that" in front of a sentence that stands on its own.
- A findings section that states conclusions and an analysis section that restates them.
- A recommendation the report's own evidence does not reach.
- A method section written after the conclusions, describing the path that was found rather than the path that was taken.
- Passive constructions that remove the actor from a decision somebody made.

## What the mechanical layer sees here

The `formal` rung's extra-strict cells apply, and the two to watch are significance inflation and promotional language. A report is commissioned, which means somebody is paying for a conclusion, and that is exactly the pressure those two cells exist to catch.

A report of this length clears the reliability floor comfortably, so burstiness, type-token ratio, and paragraph spread are all measuring something real. Read the paragraph number against the prose sections only. A findings list or a configuration block is one paragraph to the engine, and a report is full of both.

Run `verify.py` without `--allow-facts` on any edit to a report. Numbers, dates, and quotations are the substance here, and a rewrite that loses one has broken the document rather than styled it.
