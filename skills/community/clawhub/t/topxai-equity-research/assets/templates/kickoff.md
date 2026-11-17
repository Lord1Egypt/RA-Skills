# <Company full name> (<TICKER>) <type> report · Kickoff brief · <YYYY-MM-DD>

> Template. Save as `research/<report-id>/notes-00-kickoff.md`.
> Procedure: `references/pipeline/01-kickoff.md`.

## One-sentence claim (gate, `investigative.md` section 1)
One falsifiable claim with a per-share impact (rough; state the share count basis and the timing). Example: "The company
should be liable for about $20 billion, roughly $20 a share after tax, discounted."

## Value bridge
The mechanism that turns facts into money (cap and exceptions / covenants and maturities / contract terms / dilution
channels / rate base / accounting triggers / funding gap). Name the inputs of the bridge; every new fact must land on one.

## New facts (at least three, gate, `investigative.md` section 2)
| # | Fact (text or number) | Source (document, page / section / table, date, URL) | Why the market missed it | Which bridge input it changes, and by how much |
|---|---|---|---|---|
| F1 | | | | |
| F2 | | | | |
| F3 | | | | |

Fewer than three: write "do not publish" or "downgrade to a short note", with restart triggers. Re-computed filed numbers
do not count as new facts.

## How management will answer
Management's most likely response to the claim (quote existing public statements) and the facts it depends on; research
those facts.

## Core tension
One or two sentences: what the market currently treats this company as, and where we suspect that is wrong. If you cannot
state a tension, go back to the candidate comparison.

## Why this one, why now
Why this company and why this period. Include a judgment on "is there anything new to write this period?". If there is not,
write "do not publish" and the restart triggers.

## Why not the other candidates
| Candidate | Evidence density | Differentiation | Tradable judgment | Reader demand | Reason for exclusion |
|---|---|---|---|---|---|
| ... | 1-10 | 1-10 | 1-10 | 1-10 | Out if evidence density or tradable judgment is 4 or lower |

Liquidity threshold: market cap of at least $2 billion and 20-day average daily turnover of at least $20 million (waived
only if the user names the company).
Factor overlap with open ratings (read `research/patterns.md`):

## Settlement record to read first
The few entries among the last 30 lines of `research/lessons.md` that bear on this topic. For each, write "how this report
avoids it".

## Basis dates and rules
- Market basis date (a closed trading day):
- Financials through / filing date:
- Filing cutoff:
- Rating benchmark and why it was chosen (investable, and free of unrelated exposure; `judgment.md` section 4):
- Rating settlement window: starts at the close of the publication date
- Hard constraint on form: do not repeat the previous report's framework (state which framework the previous report used):

## Research lanes and budget
| Lane key | Role | Question list source | Output | Token limit |
|---|---|---|---|---|
| financials | research-collector | equity.md Step ... | notes-financials.md / data-financials.json | |
| records | research-collector | investigative.md section 2 (primary records beyond the SEC statements) and checking F1-F3 | notes-records.md / data-records.json | |
| statements | research-collector | investigative.md sections 3 and 5 (the company's own words over time, to regulators and investors; management's defence) | notes-statements.md / data-statements.json | |
| ... | | | | |
| xbrl-independent | the editor | none | notes-xbrl-independent.md | |

If the research budget is under the usual level, say which lane saves the difference. If a run goes over, stop and ask the
user.

## Data plan (pull first)
What the project already holds (earlier reports in `research/`, and for the same chain the previous report's `data-peers.json`
and `data-market.json`) and the list of primary documents still to fetch.
