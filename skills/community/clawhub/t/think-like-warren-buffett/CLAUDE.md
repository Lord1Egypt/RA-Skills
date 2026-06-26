# Buffett Oracle — Claude Code Instructions

When working in this project, always follow these rules.

---

## Startup Checklist

At the start of every session:
1. Read `buffett_brain.md` — this is the investment framework
2. Read `backtest_results.md` — this is the accumulated analysis history
3. Check `company_cards/` — pre-extracted data for analyzed companies
4. Never re-fetch data for a company that already has a card in `company_cards/`

### Scope Rule
The current repo is a **curated benchmark set**, not the full Buffett/Berkshire investment universe.
- Do not imply that the 29 indexed rows are exhaustive
- If you add new historical cases beyond the current set, treat that as benchmark expansion and update `coverage_scope.md`
- If a user asks about total Buffett history, answer explicitly that Berkshire invested in far more than these benchmark rows

---

## Running an Analysis

### Point-in-Time Rule
Use only information that was publicly available **on or before** Buffett's decision date.
- Do not use later earnings, later management commentary, later market structure changes, or later outcomes to justify the decision
- Post-decision facts belong only in the final "what actually happened" reveal
- If a later fact materially changes your thesis, it is evidence that the original thesis was fragile, not evidence you were allowed to know it then

### Step 1: Check if card exists
```
Does company_cards/<TICKER>_<YEAR>.json exist?
  YES → load it, skip to Step 3
  NO  → fetch 10-K from SEC EDGAR (or equivalent), extract hard gate numbers, create card
```

### Step 2: Create company card
After fetching data, immediately save to `company_cards/<TICKER>_<YEAR>.json` using the schema in `company_cards/_schema.json`. This prevents re-fetching in future sessions.

### Step 3: Run 7 hard gates
Apply all 7 gates from `buffett_brain.md`. If ANY gate triggers → output PASS immediately. Only continue to Step 4 if all gates pass (or a named exemption applies).

**Named exemptions (must state explicitly):**
- `CRISIS_PREFERRED`: Goldman 2008, BAC 2011, GE 2008 type deals — use crisis preferred channel
- `INFRA_EXEMPTION`: Rail/utility monopolies — earnings yield gate ⑥ waived if EV/EBITDA < 15x + monopoly confirmed
- `GROWTH_EXCEPTION`: ROE/FCF gates may be waived for high-growth companies if ROIC > 20% and earnings yield passes — must justify explicitly

**Gate review overlays (required when triggered):**
- If `g2` fails but `g7` still passes, add `review_notes.owner_earnings_note`
- If `g6` fails but `g7` still passes, add `review_notes.quality_multiple_note`
- For new live / expansion memos, include `review_notes.management_veto` with `clear`, `watch`, or `fail`

### Step 4: Moat analysis (gate ⑦)
Answer: "Can I describe in one paragraph why competitors cannot replicate this business in 10 years?"
- YES with confidence → continue
- NO or UNCERTAIN → PASS

### Step 5: Control group
Pick 2 comparable companies from same industry/era that Buffett did NOT buy. Apply hard gates to them. They should fail — if they pass, explain the differentiator.

### Step 6: Lock conclusion
Write BUY or PASS **before** revealing Buffett's actual decision. No changing conclusion after reveal.

### Step 7: Save results
Append to `backtest_results.md` using existing format, then update `analysis_index.json` so the backtest row and `company_cards/` cache stay linked.

---

## Hard Gates Reference

```
① Normalized ROE/ROIC < 12% (3-yr avg, ex one-time items)
② FCF / Net Income < 0.8
③ Net Debt / EBITDA > 4x  [Banks: Tier 1 Capital < 8%]
④ Structural revenue decline (cyclical OK, structural not OK)
⑤ Gross margin declining 2+ consecutive years
⑥ Earnings yield (Net Income / EV) < 6%  [infra exemption available]
⑦ Moat test fails — no describable structural competitive advantage
```

---

## Company Card Format

See `company_cards/_schema.json`. Always create a card after fetching new data, even for PASS results.
If the gate-review overlays above are triggered, the corresponding `review_notes` fields are part of a complete memo, not optional commentary.

---

## Contribution Rules

- Do not modify `buffett_brain.md` without documenting the change in its version table
- Do not change a concluded analysis — if you disagree, open a new entry labeled `[REVISION]`
- Always include control groups — analyses without control groups are incomplete
- Always update `analysis_index.json` when adding or changing a backtest row
- Raw 10-K files go in `raw_data/` (gitignored) — only the card gets committed

---

## Cost Management

- `company_cards/` is the cache — always check before fetching
- For 10-K fetching: use SEC EDGAR press release pages first (shorter), fall back to full 10-K only if needed
- If a company appears in `backtest_results.md`, its key numbers are in memory — no fetch needed
