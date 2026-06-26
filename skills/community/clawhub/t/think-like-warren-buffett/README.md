# Buffett Oracle

A collaborative framework for applying Warren Buffett's investment thinking to real companies — built with Claude Code, improved by the community.

---

## What This Is

A structured process for analyzing companies the way Buffett does:

1. **Hard gates** — 7 quantitative filters that auto-reject bad businesses
2. **Moat analysis** — qualitative assessment of competitive advantages
3. **Control groups** — every BUY must explain why comparable companies were rejected
4. **Binary output** — BUY or PASS, no hedging
5. **Point-in-time discipline** — use only data available at the decision date; later facts are for the reveal only
6. **Graham operating layer** — separate investment from speculation, default to defensive-investor logic, and prefer valuation over timing calls

The framework runs inside Claude Code. Each analysis is stored as a `company_card` so future analyses can reference past work without re-reading 10-Ks. The local `oracle.py` helper now also audits repo consistency so cards, docs, and backtest summaries do not drift apart.

Important scope note: the current repo covers a **curated 29-case benchmark set**, not the full Buffett/Berkshire investment universe. See [coverage_scope.md](coverage_scope.md).
Additional non-benchmark cases now live in a separate [universe_expansion.md](universe_expansion.md) track so new research does not pollute the benchmark hit-rate.

---

## What This Is NOT

- Not investment advice
- Not a trading bot
- Not a model being trained (Claude's weights don't change — only the framework and knowledge base evolve)
- Not a claim that Buffett only made 29 investments

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/buffett-oracle
cd buffett-oracle

# 2. Validate local repo state
python3 oracle.py status
python3 oracle.py validate
python3 oracle.py methodology
python3 oracle.py gate-review

# 3. Open in Claude Code
claude .

# Claude will automatically read CLAUDE.md and know what to do
# Then just say: "Analyze Coca-Cola 1988"
```

Requirements: [Claude Code](https://claude.ai/code) with SEC EDGAR web access.

## Website

This repo now ships with a zero-dependency static website.

```bash
# Build the public site into docs/
python3 oracle.py site --site-url https://your-domain.example

# Preview locally
python3 oracle.py serve-site --port 8000
```

The generated site includes:
- A chat-first Buffett Oracle landing page with one central question box
- Natural-language routing for company lookups, framework questions, asset-allocation prompts, and queue/progress questions
- A searchable backtest explorer backed by `company_cards/`
- A visible benchmark queue when the selected case set is not yet complete
- A methodology audit so the headline score is shown with its caveats
- Shareable metadata, manifest, robots, sitemap, favicon, and social preview assets for public publishing

## Sell / Marketplace

This repo can now generate a sellable bundle in three formats: raw files, a standalone skill folder, and a Codex plugin catalog.

```bash
python3 oracle.py marketplace-bundle
```

Artifacts are written to `dist/clawmart/`:
- `listing-copy.md` — paste-ready listing copy
- `publish-checklist.md` — upload checklist and scope caveats
- `package/buffett-oracle/` — buyer-facing raw files bundle
- `skill/buffett-oracle/` — standalone skill folder with `SKILL.md` and `agents/openai.yaml`
- `plugin-catalog/` — Codex-ready plugin catalog containing `.agents/plugins/marketplace.json`
- `buffett-oracle-clawmart-v<framework>.zip` — raw-files upload package
- `buffett-oracle-skill-v<framework>.zip` — standalone skill install zip
- `buffett-oracle-codex-plugin-v<framework>.zip` — Codex plugin install zip

The seller kit keeps the same research core across all three delivery formats: `SKILL.md`, `agents/openai.yaml`, the portable `buffett-oracle.md` prompt, framework files, cached `company_cards/`, and the repo helper CLI. It also keeps the curated-benchmark scope note in every package so marketplace listings do not accidentally overclaim coverage.

## Publish

If this repo is pushed to GitHub, the included workflow at `.github/workflows/deploy-pages.yml` will build `docs/` and deploy to GitHub Pages.

Typical flow:

```bash
git add .
git commit -m "Publish Buffett Oracle website"
git push origin main
```

Then enable **Settings → Pages → Build and deployment → GitHub Actions** in the GitHub repo.

For GitHub Pages project sites, the workflow will automatically build with:

```bash
python3 oracle.py site --site-url https://<owner>.github.io/<repo>
```

---

## Repo Structure

```
buffett-oracle/
├── agents/openai.yaml     ← Skill UI metadata for Codex/OpenAI-compatible loaders
├── assets/                ← Brand assets reused by skill/plugin bundles
├── CLAUDE.md               ← Instructions for Claude Code (read this)
├── buffett_brain.md        ← The framework: Buffett + Graham overlay + 7 hard gates
├── backtest_results.md     ← All completed analyses
├── analysis_index.json     ← Canonical map from backtest rows to company cards
├── universe_expansion.md   ← Separate non-benchmark expansion cases
├── universe_expansion_index.json ← Card map for expansion cases
├── buffett_investment_universe.md ← Working registry beyond current audited cards
├── methodology_audit.md    ← Why the headline score is not true predictive accuracy
├── gate_review.md          ← Which hard gates are helping vs. misfiring
├── coverage_scope.md       ← What the 29-case benchmark does and does not cover
├── oracle.py               ← CLI helper
├── site/                   ← Static site source files
├── docs/                   ← Generated website ready for GitHub Pages
├── company_cards/          ← Pre-extracted hard gate numbers per company
│   ├── _schema.json        ← Card format definition
│   └── *.json              ← One card per analyzed company/year
└── raw_data/               ← Raw 10-K extracts (gitignored by default)
```

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md).

**Short version:**
1. Pick an unanalyzed case from `backtest_results.md`
2. Read the 10-K (or equivalent annual report)
3. Run the analysis in Claude Code following `CLAUDE.md`
4. Save the company card to `company_cards/`
5. Append results to `backtest_results.md`
   Or, for non-benchmark cases, append to `universe_expansion.md`
6. Open a PR

---

## Current Progress

| Completed | Framework Version | Methodology Snapshot |
|---|---|---|
| 29 / 29 benchmark cases | v1.2 | 29/29 retrospective consistency; 3 ambiguous, 6 exceptions |
| 29 / 29 expansion cases | v1.2 | separate universe track; excluded from benchmark methodology math |

See `backtest_results.md` for benchmark details and `universe_expansion.md` for the broader universe track. For a stricter breakdown, run `python3 oracle.py methodology` and read `methodology_audit.md`. For gate-level reflection, run `python3 oracle.py gate-review` and read `gate_review.md`. For the scope boundary, read `coverage_scope.md`.

---

## Known Limitations

- **Hindsight bias**: We know outcomes before analyzing. Partially mitigated by hard gates + control groups, but not fully solvable.
- **Selection bias**: We only test companies Buffett invested in. Control groups partially address this.
- **Framework flexibility**: Qualitative moat analysis still has subjectivity.

We document these honestly. Any contributor claiming "100% accuracy, no bias" is lying.
