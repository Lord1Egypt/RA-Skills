---
name: topxai-equity-research
description: Institutional-grade equity, industry and macro research workflow for AI agents. Use it whenever the user wants a stock deep dive, an industry or value-chain report, a macro / strategy note, an earnings-season update of an existing report, a valuation with scenarios and a settleable rating, a bull/bear debate on a company, an adversarial audit of a research draft, SEC EDGAR / XBRL financial pulls, or to register, track and settle research calls (coverage watch, call ledger, track record). Also use it for Chinese requests such as 写研报, 个股深度, 产业链报告, 更新研报, 结算台账, 跑值守, even when the user does not say "research report". Every number must trace to a primary source with an evidence grade; every conclusion must be falsifiable; ratings are research judgments, never personalised investment advice.
compatibility: Python 3.9+ (standard library only). Network access to sec.gov and data.sec.gov for the bundled SEC tool. Subagents are optional (Claude Code, Cowork); other agents run the roles in sequence.
metadata:
  author: TopxAI
  homepage: https://ai.topxea.com
  version: "1.1.0"
---

# TopxAI Equity Research

A research desk in a skill: it takes a company, a value chain or a macro question from kickoff to a published report,
then keeps watching the calls the report made and settles each one when it comes due. The method is built for
reports that a professional reader would pay for, so it is strict about evidence and about saying how you could be wrong.

**The whole system in one sentence.** Markets, earnings and news are *outcomes*. A report earns its keep by explaining
the *process* (how the mechanism works) and the *next step* (what follows from it), plus the *observation points*
(how you will know you were wrong). A well-written summary of outcomes is a news digest, worth nothing.

Answer in the user's language. The method files are in English; the report can be written in any language, and
multi-language editions must match number for number (see `references/pipeline/05-publish.md`).

## How to use this skill

1. Find the step you are on in the **pipeline map** below. A new report starts at step 1; settling calls, the
   coverage watch and updates have their own entry points.
2. Read only that step's file and the method files the map names for it. Do not load everything at once.
3. Every step writes files under `research/<report-id>/` in the user's project and has an exit gate. Move on only
   when the gate passes.
4. You are the **editor**: you run the desk and do the deterministic work yourself (assembling, running scripts,
   registering calls). Research lanes, the debate, translation and audits go to the bundled agents
   (`references/agents.md`); without subagents, play each role in turn with the same file contracts.

**First run in a project.** Scripts live in this skill's `scripts/` folder (the skill's base directory is shown when
it loads). Run them from the project root so their files land in the project's `research/` folder. The SEC tool needs
a contact string: SEC contact configured for this plugin: `${user_config.sec_user_agent}`. If that is empty or still a
placeholder, ask the user once for a name and email and supply it as `SEC_USER_AGENT="Name email"` on each call.

## Hard rules (break one and the report does not ship)

1. **Real data only, and checkable by the reader.** Every key number and every quotation carries a footnote to the page,
   section or table, with a URL. If you cannot find it, write "not verified"; never fill the gap with an estimate presented
   as a reported figure. Own calculations say so and point to the derivations appendix (`pipeline/03-writing.md`).
2. **Grade every piece of evidence** (at the end of the footnote, not in body paragraphs). [A] primary filings and exchange or company disclosures; [B] major news
   organisations; [C] institutional estimates or your own calculation (say it is an estimate and show the formula);
   [D] unconfirmed reports. When sources disagree, show both; never pick one silently.
3. **One basis date, in three layers.** Price basis = the latest *closed* trading session (an intraday price is not a
   close); financials as of = the latest period end and its filing date; filing cutoff = nothing filed after it is used.
   Print all three on the title page, keep a section on events between the balance-sheet date and the basis date,
   and list "events after the basis date are not reflected" among the known limitations. When the basis date or price
   changes, change only the derived numbers by re-running the model; never search-and-replace a price string.
4. **Never pose as a licensed firm or give personalised advice.** No analyst licence claims; call ratings
   "research judgments, not orders"; use the disclosure template in `assets/disclaimer.md` (conflicts of interest
   listed one by one, even when the answer is "none").
5. **No reverse causality.** Do not explain the future with lagging outcomes (profits, CPI, the share price); reason
   from cause to process to outcome.
6. **No naked historical analogies.** An analogy needs three conditions under which it would fail, or it stays out
   of the conclusions.
7. **Every core conclusion is falsifiable.** If you cannot write "if X happens, I am wrong", demote it to an observation.
8. **Conclusion strength never exceeds evidence strength.** No [D] in a core conclusion's load-bearing numbers; a [C]
   input needs a ±30% sensitivity that does not flip the conclusion (`references/judgment.md` section 6).
9. **Probabilities need a basis**: historical frequency, market-implied, or an explicit subjective weight with its
   reason and a ±10pp sensitivity. A default 25/50/25 split is a violation of rule 1.
10. **Ratings are settleable**: 12 months, relative to a named benchmark, from a stated start date (the
    publication-date close). Bands: buy > +15%, overweight +5% to +15%, neutral −10% to +5%, underweight < −10%.
11. **Valuation numbers have one source**: `research/<report-id>/calc/model.py` and its saved output. No hand
    arithmetic in the text.
12. **Register and settle every call.** Core conclusions, the annual rating and the monthly and quarterly outlooks
    all go into the ledger; a public track record shows all of them, the method, and "past performance does not
    indicate future results".
13. **Claim first, with new facts.** The title is one falsifiable claim with a per-share impact. At kickoff, produce at
    least three primary-source facts the market has not absorbed that change an input of the value bridge; without them,
    do not publish (`references/investigative.md` sections 1-2). A report that only re-computes filed numbers does not ship.
14. **Ordered by the argument, and short.** Claim, evidence, valuation, the company's account and the opposing case,
    tracking; full coverage goes to an appendix. Body at most 15,000 words; key facts shown as screenshots of the original
    with a red box; no internal codes in the text. `scripts/check_report.py` exits 0.

## Pipeline map

| Step | What happens | Main outputs (`research/<report-id>/`) | Exit gate | Read |
|---|---|---|---|---|
| 1 Kickoff | One-sentence claim and value bridge, at least three new facts, compare candidates, read past lessons, fix the three basis dates and the benchmark | `notes-00-kickoff.md` | Claim with per-share impact and three or more new facts; evidence density and tradability both > 4/10; or a written "do not publish" with restart triggers | `references/pipeline/01-kickoff.md`, `references/investigative.md`, `references/framework.md` |
| 2 Research | Lanes of research (including `records` and `statements`), an independent XBRL pull by the editor, a cross-check of all notes | `notes-*.md`, `data-*.json`, `notes-crosscheck.md` | Conflict list and gap list written; key numbers confirmed by two sources and recorded with location and verbatim text | `references/pipeline/02-research.md`, `references/investigative.md`, `references/equity.md` / `industry.md` / `macro.md`, `references/indicators.md` |
| 2.5 Debate | Bull and bear each argue three points from the notes only, then rebut once | `debate-bull.md`, `debate-bear.md` | Both files with rebuttals | `references/pipeline/02-research.md` |
| 3 Writing | Ordered by the argument (title claim, summary, evidence, valuation, the company's account and the opposing case, tracking, appendices); footnotes; exhibits; valuation only from the model output | `parts/`, `exhibits/`, `calc/`, assembled report | `scripts/check_report.py` exits 0; writing contract met; plain language | `references/pipeline/03-writing.md`, `references/quality-bar.md` |
| 3.5 Judgment | Consensus reconstruction → mispricing evidence → catalysts → settleable rating → decision chapter → evidence binding | inside the summary, valuation and decision chapters | `references/judgment.md` section 9 | `references/judgment.md` |
| 4 Audit | Two rounds of adversarial review, including verifiability, a skeptic and a cross-language check; every finding dispositioned | `audit-vN-*.md`, `audit-vN-decisions.md`, `checks.md` | No open blockers; revisions logged in the appendix | `references/pipeline/04-audit.md`, `references/pitfalls.md` |
| 5 Publish | Deliverable structure, language-edition parity, final checks, register calls, add to the watch list | report files, ledger entries, `research/watch.json` | `ledger.py list` shows every call; `desk.py check` passes | `references/pipeline/05-publish.md` |
| Watch | New filings against open falsifiers, price triggers, calls coming due | `research/desk/<date>.md` | Overdue items settled the same day | `references/desk.md` |
| Settle | Settle due or triggered calls, one lesson each | `research/ledger.json`, `research/lessons.md` | Nothing left silently unsettled | `references/desk.md`, `references/judgment.md` section 7 |
| Update | Settle the previous edition, then a delta update or a full redo | new report id, same series | "Previous edition settled" chapter written | `references/pipeline/06-updates.md` |

## Method files

| File | What it is | When to read |
|---|---|---|
| `references/investigative.md` | Building the case: the claim and value bridge, where new facts hide, letting the company speak, getting times and places right, taking apart the company's account, how far inference may go, what not to copy | Before every kickoff |
| `references/framework.md` | The core method: cause / process / outcome, fixed / probabilistic / unknown, who sets the price, the first-principles layer, the transmission chain, falsifiability, the eight required components | Before every report |
| `references/quality-bar.md` | The quality bar: seven gates, the three-horizon outlook, the decision chapter, chart matching, audit routes | Before every report and before publishing |
| `references/judgment.md` | From analysis to a settleable judgment: consensus, mispricing evidence E1–E5, catalysts, ratings, decision chapter, evidence binding, settlement, the degrade path, final checks | Before writing the conclusions and before publishing |
| `references/equity.md`, `industry.md`, `macro.md` | The nine-step flows for each report type | During research |
| `references/indicators.md` | Indicator and primary data-source library, tagged cause / process / outcome | When choosing what to measure and where to get it |
| `references/pitfalls.md` | Catalogue of measurement and accounting traps | After drafting, item by item |
| `references/desk.md` | Coverage watch, settlement, update triggers, lessons, monthly review | After publishing, and before each new report |
| `references/agents.md` | Agent roster, delegation rules and brief templates | Before delegating any work |
| `assets/disclaimer.md` | Disclosure and conflict-of-interest template | Every report |

## Agents (bundled with the plugin)

| Agent | Used in | Writes |
|---|---|---|
| `research-collector` | step 2, one per lane | `notes-<key>.md`, `data-<key>.json` |
| `research-bull`, `research-bear` | step 2.5 | `debate-bull.md`, `debate-bear.md` |
| `research-auditor` | step 4, one per lane | `audit-vN-<lane>.md` |
| `research-translator` | step 5, other language editions | target-language chapter files |

They cannot spawn their own subagents and hand back at most 120 words, so the editor's context holds conclusions,
not raw notes. Brief templates are in `references/agents.md`.

## Scripts (standard library, Python 3.9+)

| Script | Purpose |
|---|---|
| `scripts/sec.py facts TICKER` | Last 8 quarters of revenue, gross profit, operating income, net income, operating cash flow, capex, plus latest cash, debt, RPO, shares; raw SEC JSON stays in a cache |
| `scripts/sec.py filings TICKER` / `sec.py feed` | Recent filings with 8-K items and links; new filings across the coverage list |
| `scripts/ledger.py add / settle / void / list / stats` | The call ledger and settlement lessons (`research/ledger.json`, `research/lessons.md`) |
| `scripts/desk.py run / check` | Coverage watch: filings matched to falsifiers, price triggers from your own price CSV, calls coming due |
| `scripts/check_report.py` | Report form gate: body length, title-page claim, footnote sources, exhibits, sentence density, internal codes |
| `scripts/exhibit.py` | Exhibits: crop a passage out of a filing (PDF, or HTML printed through Chrome) and box it in red; needs `pip install pymupdf` |
| `scripts/check_skill.py` | Self-check for anyone editing this skill |

## Templates (`assets/templates/`)

`kickoff.md` · `crosscheck.md` · `writing-contract.md` · `audit-decisions.md` · `checks.md` ·
`ledger-entries.json` · `watch-entry.json`

## Scale

A full company deep dive is a large job: several research lanes, two audit rounds and a second language edition can
run to millions of tokens. Most of that budget is reading. Use `scripts/sec.py` instead of loading raw filings data,
keep agent hand-backs short, and decide the lanes and a token budget in the kickoff note. If a lane overruns, stop and
ask the user rather than cutting scope silently.
