# 2. Research (follow the nine steps in the matching method file)

> This is steps 2 and 2.5 of the pipeline in `SKILL.md`. Previous step: `01-kickoff.md`. Next step: `03-writing.md`.

- **Follow the nine steps in `references/<type>.md`.** Do not collect material by feel. The nine steps are the question list
  for every lane.
- **Organise research by lane, not by step.** For a company the default lanes are `financials`, `contracts`, `governance`,
  `power` (or the cause layer of that industry), `peers` and `market`. Dispatch one `research-collector` per lane. Each
  lane produces `notes-<key>.md` and `data-<key>.json`. Every notes file opens with the same header: key; data basis date;
  filing cutoff; evidence grade; attribute tag (cause, process or outcome); structured data file; list of primary documents
  (every one with a URL). Add a lane when the subject needs one, such as peer valuation.
- **Two more lanes since 1.1.0** (`investigative.md`); most new facts come from them:
  - `records`: primary records beyond the SEC statements: 8-K exhibits and full contracts, SEC correspondence, regulatory
    dockets, interconnection queues, court and bankruptcy files, local permits and hearing minutes, procurement records,
    satellite measurements and outside data. Check the kickoff's F1-F3 first, then look for more.
  - `statements`: the company's own words: past investor decks, calls, responses to regulators, old web pages (Wayback
    Machine), management interviews. Three outputs: a statement comparison table, a year-by-year statement timeline, and a
    list of management's public statements on the points in dispute (taken apart in Part 3 of the report).
- **How every fact is recorded** (all lanes): the original text quoted verbatim, its location (page, section, table, note
  number, Item or slide), the document name and date, the URL and the evidence grade. Footnotes are written from these
  records and exhibits are cut at the same location (`scripts/exhibit.py`). A number recorded without a location cannot be
  footnoted; go back for it.
- **Pull SEC data through `scripts/sec.py` first.** `python3 scripts/sec.py facts <TICKER>` gives the last eight quarters
  of flows and the latest point-in-time values. A derived quarter (Q4 = full year minus three quarters) is tagged `derivedQ`,
  and a tag that has not been updated for years is tagged `stale`. `python3 scripts/sec.py filings <TICKER>` gives recent
  filings with 8-K Items. The script needs `SEC_USER_AGENT="Name email"`. Raw SEC JSON stays in the script's on-disk cache.
  Do not read it into context: that is the largest single waste in the research budget.
- **Mark items you only read by title or abstract "title only".** A title-only item may not enter a payload chain. Read the
  full text or find the primary filing before you use it.
- **The editor builds an independent set of notes**: `notes-xbrl-independent.md` and `data-xbrl-independent.json`. Pull
  the quarterly series, remaining performance obligations, debt instrument by instrument and share counts straight from
  companyfacts, and reconcile them cell by cell against the `financials` lane.
- **Before writing, the editor writes `notes-crosscheck.md`** (template: `assets/templates/crosscheck.md`): a list of
  conflicts (topic / a / b / resolution) and a list of gaps. If a conflict can be settled, write the settlement. If it
  cannot, show both versions side by side in the text. In one report a fully diluted share count came back as six
  different numbers from seven lanes.
- **Look up indicators and sources in `references/indicators.md`, and decide first whether each indicator is a cause, a
  process or an outcome.** The check that can actually be run is the **payload-chain check** (`framework.md` section 1.1):
  each core conclusion has three to five key numbers, and at least one must be a cause or a process. A conclusion carried
  by outcomes alone is downgraded to "observation". **Do not use a self-scored ratio such as "cause and process length
  divided by outcome length".** The framework rejects it as pseudo-checkable, because you label both the numerator and the
  denominator.
- **Primary sources first**: SEC EDGAR (10-K, 10-Q, 8-K, DEF 14A, Form 4), exchange announcements, company investor
  relations, national statistics offices and central-bank databases, trade associations. Every EDGAR request carries a
  self-identifying user agent (`SEC_USER_AGENT`).
- **Inventory what the project already holds before pulling anything**: earlier reports in `research/`, and for a report on
  the same chain the `data-peers.json` and `data-market.json` of the previous one. Reuse their pipelines and fields.
- **Confirm each key number from at least two independent sources.** For earnings-call quotes, cross-check two independent
  transcripts.
- **Record every source**: publisher, file name, location (page, section, table), date, URL, access date. Footnotes and the source list in the appendix are written from these records.
- First time you use a source listed in `indicators.md`, **open it and check the current definition**. If it does not
  match, fix that file on the spot.
- "Must answer" means **you must determine whether the answer is obtainable and record the finding**. It does not mean
  "answer anyway". If it is not obtainable, degrade as `judgment.md` section 8 says: do a substitute analysis and add it to
  the known limitations. **Forcing an answer to a question with no source produces only compliant filler.**

## 2.5 Bull/bear debate (notes complete, before the rating is set)

Run this once, after `notes-crosscheck.md` is written and the first version of `calc/model.py` has produced output, and
**before you write the rating and valuation chapters**:

1. Dispatch `research-bull` and `research-bear` in parallel. The brief gives only the report directory and the basis date.
   Each side reads the notes, the model output and the last 30 settlement lessons, does no new research, and writes its
   three strongest arguments (payload numbers cited from the notes, with evidence grades) plus "the weakest link on my
   side".
2. When both files are back, message each side once for a rebuttal (one round only). The rebuttal is appended to its own
   file.
3. The editor reads both and sets the rating. **If the rating is not neutral, the first three arguments of the side that
   opposes the rating must be answered one by one in the body** (in the misreading chapter or the operating framework,
   with the reply anchored to a specific number). An argument you cannot answer goes into the known limitations, or the
   rating changes.

Why it sits here: in an earlier workflow the skeptic lane ran only after the rating was set, and one rating flipped at that
point, forcing a full round of rework. Moving the debate forward puts the strongest counter-argument on the table before
drafting. The second-round skeptic stays, because its job is different: it re-runs the model with changed parameters and
unchanged formulas.

## Pitfalls (collected from past work)

- **When a notes file changes, every draft that cites it is revised.** A lane's notes were completed after other chapters
  were final. The editor revised only the lane's own chapter and did not send the update back to the already-submitted
  drafts. A second chapter then argued from a retracted supply-gap figure as a live point, and both auditors flagged it.
- **Notes also contradict each other.** One round produced a double-counted category, a capacity figure summed across
  overlapping lists, and two lanes giving different megawatt numbers for the same site. Downstream writers threw each one
  back, and nobody quietly smoothed it over. "Do not smooth over upstream conflicts" belongs in the writing contract
  (`assets/templates/writing-contract.md`).
- **Before you write "only", ask whether the alternatives were in the sample.** A claim that a company was the only listed
  equipment exposure to a given technology was overturned by audit: three obvious alternatives had never entered the sample
  (zero hits), so "only" was circular. The same company was at the time the target of a stock-swap acquisition, so its
  price-to-sales ratio was merely exchange-ratio arithmetic. It had already reached the core-judgment chapter, and it was
  the heaviest misjudgment of that round.
- **A close number is not the same line item.** An XBRL tag and a footnote caption were a fraction of a percent apart in
  value, yet they were two different accounts. Company-defined extension tags are often not returned by the XBRL API. Go back
  to the footnote and check the account name before you merge the figures.
- **Selective presentation.** A report quoted a capex cut at one of two peers and left out the other's large increase. It
  also quoted "20 GW signed against 3 GW shipped", where 18 GW was production-slot reservations. On an order basis the ratio
  pointed the other way. A falsification threshold must use the same basis as the evidence. On the report's own numbers, the
  falsifier had already triggered.
- **An intraday price is not a close.** Checking one stock while the US market was open, a data site had already filled the
  intraday price into its history table, and two other sources each quoted a different number. The basis date uses only closed
  trading days (for US listings, after the 16:00 Eastern close plus a buffer).
- **Never type a CIK by hand.** Vertiv's is 0001674101; 0001674910 is Valvoline. Always take it from the SEC
  `company_tickers.json`.
- **Agents most often die after collecting and before writing to disk.** After a limit resets, message the same agent to
  continue (the data is still in its context). That costs far less than a rerun. This is why every brief demands the
  skeleton first and the sections after.
