# Stanley Druckenmiller Workflow

Thesis-driven market analysis skill for OpenClaw.

This skill is designed for Druckenmiller-inspired macro/equity thinking with a live PM memo voice:
- Liquidity and rates first
- Consensus vs variant explicitly separated
- D1/D2 (first derivative / second derivative) regime logic
- Evidence anchors and safety disclaimers

Current product framing:
- Goal: hand most repetitive monitoring work to the machine and leave the highest-value judgment to the human.
- V1 scope: US-led macro engine + China / A-share transmission layer.
- Honest limitation: the skill can help with first-layer macro judgment, not fully replace second-layer execution judgment.
- Core panels and source reference: `references/core-panels-and-sources.md`
- A-share tape design reference: `references/a-share-tape-v1_1.md`

## What This Skill Produces

Depending on trigger, it can generate:
- AM morning brief (thesis + validation)
- EOD wrap
- Weekly review
- Monthly regime review
- Pre-trade thesis collision check
- Asset divergence monitor

All outputs are narrative and decision-oriented (not raw JSON dumps).

## Folder Structure

```text
stanley-druckenmiller-workflow/
  SKILL.md
  README.md
  references/
    core-panels-and-sources.md
    a-share-tape-v1_1.md
  scripts/
    market_panels.py
```

## Data Source Fallback (updated)

`market_panels.py` now has two layers:

### Global / cross-asset layer
Per symbol, the default order is:
1. finshare (default `first` mode)
2. Yahoo chart API
3. Stooq CSV
4. FRED proxy mapping
5. Local cache

### A-share structure layer
A-share internal structure now uses **AkShare** when available, mainly for:
- northbound flow
- Shibor / China government bond yields
- margin financing and securities lending
- property-chain, transport, consumer-tiering, and credit-sensitive proxy baskets

### Runtime cache scope (security fix)
By default, `market_panels.py` now writes cache files only inside the skill directory:
- `stanley-druckenmiller-workflow/.runtime/market-snapshots/`

It no longer writes to a workspace-level `memory/` directory by default.

If you explicitly want a different runtime/cache directory, set:

```bash
export STANLEY_RUNTIME_DIR=/your/explicit/runtime/path
```

If unset, the script stays confined to the skill-local runtime folder.

### Minimal finshare integration (optional)

Default mode is `first`:
- try finshare first
- if finshare fails, fall back to Yahoo / Stooq / FRED / Cache
- use `auto` to switch back to “Yahoo first, finshare as fallback”

#### 1) Install optional dependencies

```bash
pip install finshare akshare
```

#### 2) Enable / disable modes

- CLI arguments (single run)

```bash
python3 scripts/market_panels.py --finshare-mode first
python3 scripts/market_panels.py --finshare-mode auto
python3 scripts/market_panels.py --finshare-mode off
```

- Environment variables (default global behavior)

```bash
export FINSHARE_MODE=first  # default: prefer finshare
export FINSHARE_MODE=auto   # Yahoo first, finshare as fallback
export FINSHARE_MODE=off    # disable finshare completely
```

- FRED API key (optional, improves macro-series stability)

```bash
export FRED_API_KEY="<your_fred_api_key>"
```

> If both CLI arguments and environment variables are present, `--finshare-mode` takes precedence.

#### 3) Rollback

If compatibility issues appear, roll back to “no finshare” mode:

```bash
export FINSHARE_MODE=off
python3 scripts/market_panels.py --output /tmp/stanley-panels.json
```

This restores the workflow to: Yahoo -> Stooq -> FRED -> Cache, with no finshare dependency.

## Core Design Principles

1. Public data only (no private-info claims)
2. No explicit trade orders (no entry, stop, target, size)
3. Probabilistic language over certainty
4. Facts and interpretation separated
5. Mandatory fields:
   - what_would_change_my_mind
   - data_timestamp (ISO8601)
6. If data is missing, downgrade safely (DATA LIMITED)

## Language Resolution Policy

Resolve output language in this order:
1. explicit user instruction
2. account-level preference
3. current-session language habit
4. platform locale / Accept-Language
5. message-language detection

Rules:
- explicit instruction overrides everything
- session habit should not silently overwrite account-level preference unless explicitly confirmed
- if account preference and session habit conflict across multiple turns, ask once and persist at the appropriate layer
- if ambiguity remains, default to the language of the latest user message
- preserve equivalent analytical depth across languages

## Triggers and Modes

- Mode A (AM brief):
  - `morning brief`
  - `macro update`
  - `analyze the market with Stan-style workflow`
  - `how should I view today`

- Mode B (EOD wrap):
  - `EOD`
  - `close review`
  - `today's market recap`

- Mode C (Weekly):
  - `weekly brief`
  - `weekly review`
  - `how to view next week`

- Mode D (Pre-trade consult):
  - `pre-trade check`
  - `should I buy/sell`
  - `sanity-check this trade`

- Mode E (Monthly):
  - `monthly brief`
  - `monthly review`
  - `regime review`

- Mode F (13F rationale):
  - `13F`
  - `why did he buy XLF`
  - `Q3 to Q4 holdings changes`

- Mode G (Asset divergence):
  - `watch [TICKER]`
  - `check divergence for [TICKER]`
  - `asset divergence alert`

## Evidence and Safety Contract

- Include `Evidence anchors` section (top 6-12; Mode G: 3-5)
- Each anchor should include:
  - panel/metric
  - direction/change
  - lookback window
  - timestamp
  - source
- Missing evidence must be tagged:
  - `[EVIDENCE INSUFFICIENT: missing X]`

Safety footer (always append):
- append the standard disclaimer in the resolved user language:
  `Disclaimer: The above content is research framework information and does not constitute investment advice or trading instructions.`

## Local Validation Checklist (Before Publish)

1. `SKILL.md` frontmatter valid (`name`, `description`, metadata)
2. Trigger words route to expected mode
3. Output contains mandatory fields
4. DATA LIMITED behavior works when data is missing
5. No explicit trading instructions in output
6. Chinese and English depth parity is preserved

## Publish Checklist (ClawHub)

Do this only when you are ready to publish.

1. Login:

```bash
clawhub login
clawhub whoami
```

2. Optional dry run checks:

```bash
clawhub list
```

3. Publish command template:

```bash
clawhub publish ./skills/stanley-druckenmiller-workflow \
  --slug stanley-druckenmiller-workflow \
  --name "Stanley Druckenmiller Workflow" \
  --version 1.0.0 \
  --changelog "Initial public release: thesis-driven macro workflow with A-G modes, evidence protocol, and safe downgrade behavior."
```

4. Verify result:

- Confirm package page on ClawHub
- Install from a clean env and run one trigger from Mode A and one from Mode G

## Versioning Suggestion

- Start: `1.0.0`
- Behavior changes in output contract: bump minor (`1.1.0`)
- Trigger or schema breaking changes: bump major (`2.0.0`)

## Global Macro Expansion (v2 in progress)

The skill now includes global proxy panels in `scripts/market_panels.py`:
- Global equities: FEZ, EWJ, FXI, EWH, EEM, VGK
- Global FX: EURUSD=X, USDJPY=X, USDCNH=X
- Global rates proxies: BNDX, BWX, EMB

Mode A output contract is updated to include a Regional Scoreboard (US / Europe / Asia) and explicit cross-region coverage checks.

## Notes

- This skill is Druckenmiller-inspired and should never claim direct affiliation.
- Keep style high-conviction but evidence-auditable.
