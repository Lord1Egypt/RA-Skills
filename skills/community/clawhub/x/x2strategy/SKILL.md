---
name: x2strategy
description: >
  ALAGENT X2Strategy: any research input (PDF paper, Markdown draft,
  DOCX report, text notes, or keyword search) → structured strategy
  specification → executable Backtrader code → backtest → diagnosis report.
  Two core capabilities: (1) paper2spec extracts multi-strategy specs from
  any document via 5-layer LLM extraction, and (2) spec2code generates
  validated Backtrader code, runs backtests, and compares against paper
  metrics. Use this skill whenever the user wants to analyze a quant paper,
  extract trading strategies, generate strategy code, run a backtest, search
  for papers, or go end-to-end from any input to executable results. Also
  triggers on: "look at this paper", "what strategies does this use",
  "implement this strategy", "search for momentum papers", "turn this into
  code", or any request about quantitative finance research → implementation.
  Even if the user doesn't mention "strategy" explicitly — if they provide a
  finance paper or research document, use this skill.
argument-hint: "[paper.pdf | strategy.md | report.docx | search query]"
metadata:
  version: 0.6.0
  author: ALAGENT AI (alagent-ai)
  tags: [quantitative-finance, paper-parsing, strategy-extraction, code-generation, backtesting]
---

# X2Strategy

Any research input → Strategy spec → Executable code → Backtest → Diagnosis.

## Capabilities

| Capability | What it does | Deep dive |
|-----------|-------------|-----------|
| **paper2spec** | Any document (PDF/MD/DOCX/TXT) → structured strategy specification | [references/paper2spec.md](references/paper2spec.md) |
| **spec2code** | Strategy spec → Backtrader code → validate → backtest → diagnosis | [references/spec2code.md](references/spec2code.md) |

Input format auto-detected from extension:

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF (papers) | `.pdf` | PyMuPDF → Mode A (direct) or Mode B (FAISS) |
| Markdown (drafts) | `.md`, `.markdown` | Direct text read |
| DOCX (reports) | `.docx` | python-docx (requires `uv sync --extra docx`) |
| Plain text | `.txt` | Direct read |

---

## Interaction Principles

**You are the executor. The user is the requester.**

- Run tools silently, present results and insights in natural language.
- Never show CLI commands (`uv run python scripts/...`) unless user asks.
- Offer next actions conversationally: "Would you like me to implement the second strategy as well?"

When reporting results, focus on **what you found**, not how:

```
❌ Bad:  "I ran `uv run python scripts/analyze.py paper.pdf` and got 3 strategies."
✅ Good: "This paper contains 3 independent strategies: [1] minimum distance method, [2] ADF stationarity, and [3] Johansen cointegration. Which one should I implement?"
```

**Use interactive tools aggressively.** When your platform provides
interactive question tools — `vscode_askQuestions` (VS Code Copilot),
`AskUserQuestion` (Claude Code), or equivalent — use them for ALL
user-facing choices. Interactive tools present clickable options,
which is faster and less error-prone than asking the user to type.

Apply interactive tools to:
- First-Run Setup choices (workspace path, API provider, key input)
- Gate 1 confirmation (proceed / adjust settings)
- Gate 2 action menu (implement / deep dive / compare / adjust / export / re-extract)
- Search result selection (pick papers from a numbered list)
- Any scenario where the user picks from options

If no interactive tool is available, fall back to numbered text menus.

---

## First-Run Setup

On first use, walk through three steps. Skip any already-configured step.
Persist all choices to `.env` (gitignored) for session stability.

### Step 1 — Workspace Location

Present choice via interactive tool:
- `./library/` (default, recommended)
- Custom path

Write `PAPER2SPEC_LIBRARY_PATH=/absolute/path` to `.env`.
Scan the directory for existing `metadata.json` to detect prior analyses.

### Step 2 — LLM API Key

Check env for `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `OPENAI_API_KEY`.
If none found, present via interactive tool:

```
An LLM API key is required for strategy extraction and code generation. Recommended options:
  1. DeepSeek (best cost-performance, about ¥0.7 per paper) → https://platform.deepseek.com
  2. OpenRouter (one key for access to multiple models) → https://openrouter.ai/keys
Please provide your API key and tell me which provider it belongs to.
```

> Do NOT check for or suggest `ANTHROPIC_API_KEY`.

Once received, write key + matching model to `.env`, then verify:
`uv run python -c "from paper2spec.llm import chat; print(chat('Say OK'))"`.

See [references/skill-internals.md](references/skill-internals.md) for
`.env` format examples per provider.

### Step 3 — Python Environment

```bash
cd <skill-path>
uv sync --all-extras    # Recommended: installs everything
```

If `uv` unavailable: `pip install -e ".[codegen,agent,dev]"`.
Always use `uv run` to execute scripts (auto-activates correct venv).

See [references/skill-internals.md](references/skill-internals.md) for
selective install options and non-uv alternatives.

### Completion

Once configured, confirm naturally with examples:

```
✅ Setup complete. You can now ask me for tasks directly, for example:

  • "Analyze this paper" + attach a PDF file
  • "Search for papers about momentum trading"
  • "Implement this strategy based on this paper" + provide the file path
  • "I wrote a strategy draft in Markdown; extract the spec and generate code"
  • "Compare the strategy differences between these two papers"

Just tell me what you want to do, and I will handle the rest.
```

---

## Routing

| User Intent | Route | Action |
|-------------|-------|--------|
| "Analyze this paper/doc" | paper2spec | Parse + extract specs |
| "Search for papers about X" | paper2spec | Search → **Gate 1** |
| "Here's my strategy draft" (MD/DOCX/TXT) | paper2spec | Auto-detect format, extract |
| "Generate code / Implement this" | spec2code | Spec → code → validate → backtest |
| "Run a backtest" | spec2code | Execute strategy.py |
| "End to end from paper" | both | paper2spec → **Gate 2** → spec2code |
| "Compare results with paper" | spec2code | Read backtest output + spec, compare metrics |

---

## Interaction Gates

Two mandatory HITL gates. Skip only when user says "fully automatic" /
"end to end without stopping".

**Always present gate choices through interactive tools when available.**

### Gate 1 — Input Confirmation

**When:** After receiving/finding input, BEFORE extraction.

Three scenarios — present via interactive tool (or numbered text menu):

**Scenario A — User provided a file:**
```
📄 Received: "Tactical Asset Allocation" (Faber, 2007)
   Format: PDF, 18 pages
   Abstract: [first 2 sentences]

I'll extract trading strategies. ~30-60s, ~$0.01.
→ Proceed with extraction?
→ Or adjust settings first? (parser mode, model, output location)
```

**Scenario B — Search results returned:**
```
🔍 Found 8 papers for "momentum trading strategy":
  1. ⭐ "Time Series Momentum" (Moskowitz et al., 2012) — 847 citations
  2. "Momentum Crashes" (Daniel & Moskowitz, 2016) — 523 citations
  ...
Which paper to analyze? (pick number, "1, 3" for multiple, or refine search)
```
Do NOT auto-analyze. Always let user pick.

**Scenario C — Raw text / strategy idea:**
```
📝 I see you've described: "[brief summary]"
   I'll structure this into a formal spec. → Proceed? → Add more details first?
```

Keep it light for straightforward inputs — single confirm with default-proceed.

### Gate 2 — Spec Review & Action Menu

**When:** After extraction completes, BEFORE code generation.

Show extraction summary, then present action menu via interactive tool:

```
✅ Strategy Extraction Complete
📋 Paper: "Pairs Trading: Does Volatility Timing Matter?"
   Detected: 3 independent strategies

   [1] Minimum Distance Method
       • 4 indicators (spread, SMA, Z-score, distance)
       • Entry: spread Z-score > 2σ, Exit: mean reversion

   [2] Stationarity-Based (ADF Test)
       • 3 indicators, Entry: cointegrated pair + spread deviation

   [3] Cointegration (Johansen)
       • 5 indicators, Entry: Johansen test + Z-score threshold
```

Then 6 actions:

1. 🚀 **Implement** — Generate executable code (pick strategy # or "all")
2. 🔍 **Deep dive** — Explain a strategy's logic in detail
3. 📊 **Compare** — Side-by-side of detected strategies
4. ✏️ **Adjust** — Modify spec parameters/constraints
5. 💾 **Export only** — Save specs, stop here
6. 🔄 **Re-extract** — Different model or parser mode

**Key behaviors:**
- "Implement" → confirm which strategy index before generating code.
- "Deep dive" → explain, then return to the same menu.
- After code gen + backtest → present results, offer next decision.
- Never silently chain extraction → code generation.

### Gate Bypass

If user says "end to end" / "fully automatic" / "don't stop", collapse
gates into inline status:

```
📄 Parsing paper... ✓ (3 strategies detected)
💻 Generating code for strategy 1... ✓
📊 Running backtest... ✓
📈 Results ready — see below.
```

Still stop on unexpected issues (0 strategies, errors, validation failures).

---

## Agent Pipeline Flow

```
1. Receive input (file / search query / text)
2. ── Gate 1: Input Confirmation ──
3. [paper2spec] Parse document, extract strategy specs
4. ── Gate 2: Spec Review & Action Menu ──
5. User selects strategy + action
6. [spec2code] For each selected strategy:
   a. Read spec.json + reference docs
   b. Generate self-contained Backtrader strategy.py
   c. Validate (AST + structural checks)
   d. Run backtest, compare metrics vs paper
7. Present results + diagnosis
8. Offer next actions
```

For code generation patterns: [references/spec2code.md](references/spec2code.md)
For Backtrader patterns: [references/backtrader_patterns.md](references/backtrader_patterns.md)

---

## Internal Toolchain

> Agent-only. Run silently; present results in natural language.

```bash
# End-to-end: any document → spec
uv run python scripts/analyze.py <file> -o library/<slug>/

# Validate generated code
uv run python scripts/validate_strategy.py library/<slug>/strategy_1.py

# Run backtest
uv run python library/<slug>/strategy_1.py

# Search papers
uv run python scripts/search.py "<query>" -n 5

# Step-by-step
uv run python scripts/parse.py <file> -o content.json
uv run python scripts/extract.py content.json -o spec.json
```

For full flags, output formats, and library management:
[references/skill-internals.md](references/skill-internals.md)

---

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PAPER2SPEC_LIBRARY_PATH` | `./library` | Output root |
| `PAPER2SPEC_MODEL` | `openai/gpt-4o-mini` | Default LLM ([litellm-supported](https://docs.litellm.ai/docs/providers)) |
| `DEEPSEEK_API_KEY` | — | DeepSeek (recommended) |
| `OPENROUTER_API_KEY` | — | OpenRouter (multi-model) |
| `OPENAI_API_KEY` | — | OpenAI direct |
| `PAPER2SPEC_ARXIV_MIN_INTERVAL` | `3.0` | Seconds between arXiv requests |
| `PAPER2SPEC_SEARCH_MAX_RETRIES` | `3` | Retry on HTTP 429/5xx |

Any [litellm-supported model](https://docs.litellm.ai/docs/providers) works.
The `--model` flag on any script overrides `PAPER2SPEC_MODEL`.
Full config + .env examples: [references/skill-internals.md](references/skill-internals.md)

---

## References

Read on demand for implementation details:

- [references/paper2spec.md](references/paper2spec.md) — Parser modes, multi-strategy detection, output schemas
- [references/spec2code.md](references/spec2code.md) — Code generation workflow, Backtrader patterns
- [references/skill-internals.md](references/skill-internals.md) — Script flags, output formats, .env examples, library management, project structure
- [references/backtrader_patterns.md](references/backtrader_patterns.md) — Strategy class, data loading, position sizing
- [references/indicator_cookbook.md](references/indicator_cookbook.md) — Built-in and custom indicators
- [references/data_sources.md](references/data_sources.md) — yfinance, akshare, FRED API

## Limitations

- **Mode A** truncates at 100K chars (first 90K + last 10K). Use Mode B for >100 page papers.
- **Tables/formulas**: not yet extracted from PDFs.
- **Multi-strategy**: conservative — may merge borderline-distinct strategies.
- **DOCX**: paragraph text only (tables, images not preserved — use PDF for rich docs).
- **SSRN search**: best-effort HTML scraping, may break on layout changes.
