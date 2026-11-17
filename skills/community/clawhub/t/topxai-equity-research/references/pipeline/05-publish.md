# 5. Publish: deliverable, final checks, ledger and watch registration

> This is step 5 of the pipeline in `SKILL.md`. Previous step: `04-audit.md`. Next step: `06-updates.md`.

The output format (Markdown, HTML, PDF) is yours to choose. The rules below apply to every format.

## 5.1 Deliverable structure

- **Title block**: title, ticker, series key, rating line (rating, 12-month horizon, benchmark, start date), and the three
  layers of data dates (market basis date, financials through, filing cutoff). The compilation and disclosure pointer from
  `assets/disclaimer.md` appears here once and in Appendix C once. Do not repeat a disclaimer on every page.
- **Summary** (chapter 1): the core judgments, each marked with its evidence strength, and the **three-horizon outlook**
  (annual, quarterly, monthly) with the transition-condition box. This table appears once in the whole report.
- **Numbered tables and figures.** Tables are "Table N", figures are "Figure N", each numbered in document order. Put a
  "Source:" line directly under every table and figure. Do not write figure numbers inside a chart specification: number
  them in the build step, and count the figures before you cite one in the text.
- **Evidence grades** [A]-[D] sit inline on each number. Never put a grade tag inside an SVG: it breaks the parser.
- **Page header**: the report name and the data basis date, on every page.
- **Appendices**: A glossary and definitions; B sources and known limitations; C disclosures, audit revision log and version;
  D derivations and calculations (`calc/model-vN-output.txt` is the source of every number in it).
- **Document metadata** (author, creator, producer) is set on purpose. An empty field is not neutral: some readers fill it
  with the name of the generating tool. When you scrub authorship traces from the text, keep names that are research
  subjects, such as a real customer of the covered company. Deleting them would falsify the report.

## 5.2 Bilingual parity

If the report ships in two languages, the editions must match in content.

- The second edition is **not a machine translation**. Finance has fixed expressions (guidance, take rate, net revenue
  retention, operating leverage), and a literal rendering of a source-language term marks the text as translated. Build a
  glossary (`research/<report-id>/glossary.md`) before the first translation batch, and give every translator the same one.
  In a past report one literal rendering of "definition" appeared 47 times.
- **Numbers, table numbers, figure numbers and evidence grades are identical across editions, cell by cell.** A reader will
  reconcile the two editions, and one differing number ends the credibility of the whole report.
- Start the second edition only after the primary one has passed the round-1 dispositions (v2). After each later revision,
  sync only the chapters that changed, by diff.
- After every assembly, run a comparison over every table cell, every chart value and every evidence grade in both editions.
  The audit begins only when it reports zero differences.
- If the second edition is not in a CJK language, it must contain no CJK characters. Count them:
  `python3 -c "import sys;print(sum(1 for c in open(sys.argv[1],encoding='utf-8').read() if 0x3400<=ord(c)<=0x9fff))" FILE`
  must print 0. Appendix C of each edition uses the matching-language text of `assets/disclaimer.md`.

## 5.3 Final checks

Copy `assets/templates/checks.md` to `research/<report-id>/checks.md` and fill it in. Every row gets `pass`, `fixed` or
`n/a`, and `fixed` and `n/a` need one sentence. A row ticked without a note counts as not checked. Any blocker sends the
report back to `04-audit.md`.

## 5.4 Register every call in the ledger

Do this after the report is final and published. The scoreboard is built from the ledger, and a scoreboard is a
performance claim, so it must be complete.

**What to register** (see `assets/templates/ledger-entries.json` for the fields):

- every numbered core judgment on the summary page ("N core judgments"), with no `--tier`;
- the annual rating and target price, if they are not among the core judgments: `--tier annual`;
- the monthly and the quarterly outlook, one entry each: `--tier monthly` and `--tier quarterly`. The claim is the text of
  the "Outlook" cell. The falsifier is the "Timing" cell followed by the "Settlement" cell. The benchmark field holds the
  "Observation" cell, which names the verification source.

So the ledger gains: the number of core judgments, plus one rating, plus two outlooks. Print the ledger ID range in
Appendix C ("Registered in ledger: #... to #...").

```bash
python3 scripts/ledger.py add --report <report-id> --series <TICKER> \
  --claim 'Claim text, verbatim, with amounts such as $45' \
  --falsifier 'What happening means the call is wrong' --horizon 12 \
  --benchmark 'S&P 500 total return' --issued YYYY-MM-DD [--tier annual|quarterly|monthly]
python3 scripts/ledger.py list    # read every row back against the "falsifiable conditions" table in the report
```

**Rules**

- **Register all of them.** Registering only the calls you are confident about is cherry-picking, and it makes a published
  scoreboard misleading. Enter text verbatim and do not rewrite it later.
- **Ledger rows are only ever added, never deleted.** A typing error may be corrected back to the original text, on the day
  of registration only. If the thesis itself must change, settle the call as a miss or leave it open.
- **Single-quote every argument.** Claims nearly always contain `$` amounts. In double quotes, the shell reads `$18.5` as the
  positional parameter `$12` and silently drops it; the command still succeeds, with no error. If the text contains a single
  quote (an English possessive) or a backtick, call `ledger.py` from a short Python script with an argument list, so no shell
  quoting is involved.
- **The settlement window of a rating starts at the close of the publication date, not at the market basis date.** Price
  movement between the basis date and publication cannot be acted on by a reader, and counting it flatters the record.
  Valuation, price-derived figures and the target date stay anchored to the basis date. Only three things change: the rating
  window, the ledger `issued` date, and the known-limitation entry "events after the basis date" (edit both editions). A
  move large enough to nearly reach a rating-band threshold between those two dates is the case that makes this matter.

## 5.5 Register the report in the watch file

Add the report to `research/watch.json` (format: `assets/templates/watch-entry.json`): the rating (ledger ID, label, start date
and start price copied from the report text, benchmark, method), the price triggers written in the report, and the monthly
and quarterly events with their ledger IDs. Delete any trigger example the report does not state. Then run:

```bash
python3 scripts/desk.py check     # must report 0 uncovered series
python3 scripts/desk.py run       # confirm the new entry fetches data without errors
```

Details of each field are in `references/desk.md` section 6.
