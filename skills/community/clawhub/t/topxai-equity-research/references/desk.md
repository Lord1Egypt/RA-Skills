# Coverage watch and settlement

> Prerequisite: `judgment.md` sections 4 and 7 (settleable ratings, settlement of prior calls). This file covers what happens
> **after a report is published**: someone notices when a falsifier fires, calls that come due are settled on time, and what
> settlement teaches goes into the brief for the next report.

## 0. Why this file exists

A report that says "settled on the event" or "an early trigger counts as a miss" has promised something. If nothing watches
the calendar, the promise is empty. `judgment.md` section 7 says that silently not settling is cherry-picking. The leak is
this step: a ledger fills up with calls, and nobody opens it.

The desk borrows three habits from institutional research desks and leaves the rest. It does not trade, size positions or
give personalised advice. Take only these:

- a **deterministic watch script** that fetches data and compares it, with no model calls;
- **settle and learn**: every settlement leaves one lesson the next report can follow;
- **review by theme**: look at which kinds of calls are winning and losing, not just individual calls.

## 1. Daily watch

```bash
python3 scripts/desk.py run                          # look back 3 days of filings (default)
python3 scripts/desk.py run --days 7                 # look back a week
python3 scripts/desk.py run --prices prices.csv      # add price triggers and mark-to-market
python3 scripts/desk.py check                        # every series in the ledger has an entry in research/watch.json
```

`desk.py` fetches data and compares it. It calls no model. It reads `research/watch.json` and `research/ledger.json`,
pulls SEC filings through the same code as `scripts/sec.py` (set `SEC_USER_AGENT="Name email"` first), and writes the result
to `research/desk/<date>.md`.

**Prices come from a CSV you supply** (`--prices prices.csv`): daily closes for each covered ticker and for every benchmark
named in `research/watch.json`. The expected columns are described at the top of `scripts/desk.py`. Without `--prices`,
sections 2 and 3 below are skipped and the output says so. The desk does not scrape a quote endpoint, because a scraped
price has no audit trail.

The output has five sections:

| Section | Content | How to read it |
|---|---|---|
| 1. New filings | New SEC filings for each covered company; 8-Ks listed with their Item numbers; each filing matched to open ledger calls and unsettled outlooks whose falsifier mentions that kind of filing | Read the original for every match, then handle it by section 2 below. Routine 8-Ks (Item 5.05, Item 5.07, exhibits only) do not match |
| 2. Price triggers | Price conditions written into the report text: a close below a level, N consecutive closes above a level, a price ratio beyond a band for N consecutive days | A crossed trigger settles the call as the report text says. Within 5% of a trigger, the output flags it |
| 3. Rating mark-to-market | Absolute, benchmark and relative return from the start date to the latest close, and which rating band today's price falls in | **This is tracking, not settlement.** A different band only means you should check whether a transition condition fired. A rating never changes on price alone |
| 4. Due | Outlook events that are due and unsettled (monthly, quarterly); ledger entries whose issue date plus horizon has passed or falls within 30 days | Settle overdue entries the same day. Do not wait for an update edition |
| 5. Earnings dates | Expected earnings dates in the next 21 days | Before earnings season, pull up the observation list of each affected report |

Rating bands, as relative return over the benchmark (`judgment.md` section 4): Buy above +15%, Overweight +5% to +15%,
Neutral -10% to +5%, Underweight below -10%. The watch entry's `method` is `diff` (stock return minus benchmark return)
or `ratio` ((1 + stock) / (1 + benchmark) - 1); use the one the report states.

Conventions:

- **Only closed trading days count.** Put only completed sessions in the price CSV you pass to `desk.py` (for US
  listings, after the 16:00 Eastern close plus a buffer). Once, a data site filled the intraday price into its table of
  historical closes, and two other sources each quoted a different number.
- Mark-to-market uses price return. Settlement uses total return. For dividend payers the two differ by a few tenths of a
  percentage point, so recompute on the basis the report states when you settle.

When to run it: before any research work starts, whenever the user asks, and after the close on each trading day around
earnings dates of covered companies. The script makes no model calls, so if you want a schedule, any scheduler works.

## 2. What to do with a finding

| Finding | Action |
|---|---|
| A new filing matches a ledger call | Read the original. If it does not trigger, write one line in today's desk file: "#N does not trigger, because ...". If it triggers the falsifier, run `python3 scripts/ledger.py settle ID miss --evidence '...' --lesson '...'`. Settle as `hit` early only if the report says an early hit is allowed; otherwise wait for the due date |
| A price trigger is crossed | Settle as the report text says (usually "record as a miss"). Then check whether the transition conditions call for a Delta update |
| A three-horizon outlook comes due | Go through the settlement column of the report's table item by item and record each as right or wrong with `ledger.py settle ID ...`. In the evidence, name each item and its source. If one item can only be judged from a later filing (for example, a share count that appears on a 10-Q cover), write the items already decided into the evidence, leave the call open, and say which document you are waiting for |
| A ledger entry is due | Settle it now. "No update edition yet" is not a reason to leave it open |

Monthly and quarterly outlooks live in the ledger as `tier` = `monthly` / `quarterly`, next to the `annual` rating and the
core judgments. The scoreboard shows all of them. The `events` in `research/watch.json` hold only the due date and the ledger
ID (`call`). Whether a call is settled is answered by the ledger alone; never record it a second time in `watch.json`.

## 3. Update triggers

Keep an earnings-change flag. After a development, re-run `calc/model.py`. If **revenue or EPS over the next four quarters
moves by 5% or more**, or any condition in the transition-condition box fires, record an **update candidate** with four
items: mechanism, size range, confidence, source.

Put update candidates at the end of that day's desk file. Accumulate them until an earnings season or a single major event,
then publish a Delta update (`references/pipeline/06-updates.md`). Anything under 5% is logged in the desk file and does not
produce an update. The 5% line keeps the desk from republishing noise.

### Earnings-day check

On the close of a covered company's earnings day (the date is in section 5 of the watch output), write three comparisons in
that day's desk file:

1. results and company guidance against the report's model;
2. the milestones in the report's three-horizon outlook;
3. every ledger falsifier whose observation point is this earnings release.

Then apply the 5% rule from the previous section to decide whether to record an update candidate. Settle any outlook or
ledger entry that this release decides.

## 4. Settlement lessons

Every `ledger.py settle` takes a mandatory `--lesson`. The script appends it to the top of `research/lessons.md`. Write the
lesson as one sentence the next report can act on ("check the tax-rate basis of the valuation engine first"). Do not write
reflections. Before every kickoff, read the last 30 lines of `research/lessons.md` (`references/pipeline/01-kickoff.md`).
The file is a working file for the desk; keep it out of published material.

## 5. Monthly review

On the first trading day of each month, write `research/desk/<date>-review.md`:

1. Group the ledger by rating direction, by theme in `research/patterns.md`, by catalyst type (earnings, contract 8-K,
   financing, governance) and by industry. Count settled hits and misses. List the entries settled this month and any theme
   that is new or getting stronger.
2. Update `research/patterns.md`: add new reports' entries to the themes they belong to and recount the "settled" column.
3. Look for systematic bias. Do calls in one theme or one rating direction share factors, so that they will flip together?
   If most open ratings are the same direction on the same exposure, one rally can settle them all as misses, and the
   scoreboard then measures one market move instead of the method.
4. Propose at most one change to the skill, with the reason and the evidence. If you adopt it, edit the skill file and cite
   the review in the commit message.

## 6. Registering a new report

This is the last step of `references/pipeline/05-publish.md`. Add one entry for the series to `research/watch.json`
(format: `assets/templates/watch-entry.json`):

- `rating`: the ledger ID, the rating label, the start date and start price **copied from the report text**, the benchmark
  and the method (`diff` or `ratio`);
- `triggers`: the price conditions written into the report text, each with its ledger ID in `call`;
- `events`: the monthly and quarterly outlooks, each with ledger ID `call`, due date, a one-line summary and the source line
  in the report.

Then run `python3 scripts/desk.py check`. It must report 0 uncovered series. Run `python3 scripts/desk.py run` once to see
that the new entry fetches data without errors.
