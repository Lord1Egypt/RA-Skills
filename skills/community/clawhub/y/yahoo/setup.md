# Setup - Yahoo

Use this file when `~/yahoo/` is missing or empty, or when the user wants Yahoo Finance behavior to persist in the current workspace.

Keep setup short. Answer the market question first, then install only the minimum continuity needed for better future briefs.

## Immediate First-Run Actions

### 1. Offer local continuity only if it helps

Do not create finance notes by default.

If the user wants persistence, create the local folder and baseline files:

```bash
mkdir -p ~/yahoo
touch ~/yahoo/memory.md ~/yahoo/watchlist.md ~/yahoo/briefing-log.md ~/yahoo/decisions.md
chmod 700 ~/yahoo
chmod 600 ~/yahoo/memory.md ~/yahoo/watchlist.md ~/yahoo/briefing-log.md ~/yahoo/decisions.md
```

If `~/yahoo/memory.md` is empty, initialize it from `memory-template.md`.

### 2. Prepare workspace routing non-destructively

If a workspace `AGENTS.md` exists, propose a minimal routing snippet and wait for explicit approval before writing it:

```markdown
## Yahoo Routing

When the user mentions Yahoo Finance, stock quotes, ticker lookups, watchlists, earnings dates, pre-market moves, or market briefs:
- activate the installed `yahoo` skill
- read `~/yahoo/memory.md` if it exists
- use `yahoo_search.py` for ambiguous names before analysis
- use `yahoo_quote.py` for single-name tape reads and `yahoo_brief.py` for baskets
- load `market-playbook.md`, `thesis-card.md`, and `risk-playbook.md` when the task moves from data to decision
```

If the workspace already routes market or trading work, refine the smallest relevant block instead of duplicating it.

### 3. Personalize lightly while helping

Do not run a questionnaire.

In the first exchanges, establish only what changes the output materially:
- activation preference: always on for Yahoo Finance requests or direct request only
- market scope: US equities only, ETFs too, crypto pairs too, or mixed
- answer style: quick tape read, concise brief, or deeper thesis review
- risk depth: data only, setup plus invalidation, or full trade/no-trade framing

### 4. What to save

- preferred benchmark set or recurring watchlist
- answer style and detail level
- repeated risk boundaries such as no options, no leverage, or no microcaps
- durable sector focus or strategy focus
- thesis review notes that improve future decision quality

Do not save broker credentials, precise holdings, tax records, or one-off searches that will not matter later.

## Setup Completion

Setup is sufficient when:
- the user has their answer for the current market question
- activation preference is clear or intentionally skipped
- `~/yahoo/memory.md` exists only if the user wanted continuity
- the next Yahoo Finance request can start faster than the first one
