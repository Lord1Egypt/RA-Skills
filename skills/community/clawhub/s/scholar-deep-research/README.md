# scholar-deep-research — From Question to Cited Report

[中文文档](README_CN.md) &middot; 🌐 **Website:** [agents365-ai.github.io/scholar-deep-research](https://agents365-ai.github.io/scholar-deep-research/)

An 8-phase (Phase 0..7), script-driven academic research workflow that turns a research question into a structured, cited report. Multi-source federation across OpenAlex, arXiv, Crossref, and PubMed with deduplication, transparent ranking, citation chasing, and a mandatory self-critique pass.

## What it does

- **End-to-end research** — from question decomposition (Phase 0) to a finished report with bibliography (Phase 7), with 7 enforced phase-transition gates in between
- **Agent-native CLI** — structured JSON envelopes with `request_id` / `latency_ms` / `cli_version` on every response; `--idempotency-key` on every mutating command; `--dry-run` previews; destructive operations (`init --force`) gated behind a paired `--dangerous` acknowledgement; gate failures carry a `next: [commands]` hint so agents recover without a discovery round-trip
- **4 federated sources** — OpenAlex (primary, free, 240M+ works), arXiv (preprints), Crossref (DOI metadata), PubMed (biomedical)
- **Transparent ranking** — papers are scored with a published formula (`α·relevance + β·citations + γ·recency + δ·venue_prior`), components written into state
- **Deduplication across sources** — DOI-first, then title-similarity merge; one paper, one record
- **Citation chasing (snowball)** — forward + backward graph expansion via OpenAlex
- **Persistent state file** — `research_state.json` tracks every query, paper, decision, and phase. Research is resumable and auditable
- **Saturation-based stop signal** — discovery ends when a new round adds <20% novel papers AND no new paper has >100 citations
- **5 report archetypes** — `literature_review` / `systematic_review` / `scoping_review` / `comparative_analysis` / `grant_background`, picked from user intent
- **Mandatory self-critique** — Phase 6 runs a 14-point adversarial checklist; findings go in the report appendix
- **Citation rigor** — every claim in the body carries a `[^id]` anchor; unanchored claims fail the gate
- **BibTeX / CSL-JSON / RIS export** — the bibliography is generated from state, not retyped
- **PDF text extraction** — `pypdf`-based, with scanned-PDF detection. `--doi` mode resolves papers via [paper-fetch](https://github.com/Agents365-ai/paper-fetch) (5-source OA chain) or Unpaywall fallback
- **MCP enrichment, not dependency** — uses Semantic Scholar (asta) and Brave Search MCP tools when available, but the workflow is fully functional without them
- Triggers proactively when a user question requires academic grounding

## Multi-Platform Support

Works with all major AI coding agents that support the [Agent Skills](https://agentskills.io) format:

| Platform | Status | Details |
|----------|--------|---------|
| **[Claude Code](https://claude.ai/code)** | ✅ Full support | Native SKILL.md format |
| **[OpenCode](https://opencode.ai/)** | ✅ Full support | Reads from `~/.config/opencode/skills/`, `.opencode/skills/`, and (cross-compat) `~/.claude/skills/` and `~/.agents/skills/` |
| **[OpenClaw](https://openclaw.ai/) / [ClawHub](https://clawhub.ai/)** | ✅ Full support | `metadata.openclaw` namespace, dependency gating, `clawhub install` |
| **Hermes Agent** | ✅ Full support | `metadata.hermes` namespace, category: research |
| **[pi-mono](https://github.com/badlogic/pi-mono)** | ✅ Full support | `metadata.pimo` namespace |
| **[OpenAI Codex](https://openai.com/index/introducing-codex/)** | ✅ Full support | `agents/openai.yaml` sidecar with capabilities and prerequisites |
| **[SkillsMP](https://skillsmp.com/)** | ✅ Indexable | GitHub topics configured |

## Comparison

### vs No Skill (native agent)

| Capability | Native agent | This skill |
|------------|--------------|------------|
| Search a single source | Yes (often Google Scholar via tool) | Yes — 4 sources federated |
| Multi-round search with saturation gate | No — one shot | Yes — explicit `saturation` check |
| Cross-source deduplication | No | Yes — DOI-first, title-similarity fallback |
| Transparent ranking formula | No — opaque | Yes — formula printed, components in state |
| Forward/backward citation chase | No | Yes — OpenAlex graph expansion |
| Resumable state | No — stateless per turn | Yes — `research_state.json` |
| Choice of report archetype | No — generic outline | Yes — 5 archetypes selected from intent |
| Self-critique pass | No | Yes — mandatory 14-point checklist (Phase 6) |
| Citation anchors enforced | No — claims float | Yes — every claim needs `[^id]` |
| BibTeX / CSL-JSON / RIS export | No | Yes — generated from state |
| PDF text extraction | Sometimes | Yes — pypdf with scanned-PDF detection |
| Confirmation-bias backstop | No | Yes — explicit critique search for top-cited papers |
| MCP graceful degradation | N/A | Yes — scripts work even when MCP times out |

### vs Other research skills

| Feature | This skill | Generic "literature-review" prompts | Browser-driven scrapers |
|---------|------------|-------------------------------------|-------------------------|
| **Approach** | Scripts + SKILL.md | Pure prompt | Headless browser automation |
| **Determinism** | ✅ Same input → same papers | ❌ Vibes-based search | 🟡 Brittle to UI changes |
| **API key required** | ❌ None for OpenAlex/arXiv/Crossref | N/A | Often yes |
| **Rate-limit aware** | ✅ Polite-pool email opt-in | ❌ | 🟡 |
| **Resumable** | ✅ State file | ❌ | ❌ |
| **Citation chasing** | ✅ via OpenAlex graph | 🟡 ad hoc | ❌ |
| **Cross-source dedup** | ✅ Deterministic | ❌ | ❌ |
| **Self-critique gate** | ✅ Mandatory | ❌ | ❌ |
| **Archetype templates** | ✅ 5 | ❌ | ❌ |

### Key advantages

1. **Scripts-first, MCP-optional** — the workflow runs on stdlib HTTP. Semantic Scholar / Brave MCP tools are enrichment, not dependencies. When MCP times out, research keeps going.
2. **Transparent ranking** — the formula is printed, the weights are in state, every paper's component scores are inspectable. The report's methodology appendix can cite its own ranking.
3. **Persistent, auditable state** — every query, every dedupe, every selection lives in `research_state.json`. Research is resumable across sessions and reviewable by a third party.
4. **Saturation as stop signal** — discovery ends when the data says it should, not when the model gets tired.
5. **Self-critique is a phase, not a checkbox** — the 14-point Phase 6 checklist catches unanchored claims, venue/author skew, recency collapse, and untested high-citation papers. Findings go into the report appendix.
6. **5 report archetypes** — the right structure for the right question (literature review vs systematic vs scoping vs comparative vs grant background).
7. **Citation anchors enforced** — every claim in the body has `[^id]`; the export step catches unanchored prose.

## How it works

```
Phase 0  Scope        question decomposition + archetype + state init
Phase 1  Discovery    multi-source search → dedupe → saturation check
Phase 2  Triage       transparent ranking → top-N selection
Phase 3  Deep read    PDF extract → evidence per paper
Phase 4  Chasing      citation graph (forward + backward)
Phase 5  Synthesis    thematic clustering → tension map
Phase 6  Self-critique  14-point adversarial checklist (mandatory)
Phase 7  Report       render archetype template → export bibliography
```

Each phase transition has an enforced gate (G1..G7 in `scripts/_gates.py`). The workflow advances one gate at a time via `python scripts/research_state.py --state <path> advance` — a call that runs the gate predicate and refuses with a structured `gate_not_met` envelope (listing failing checks *and* suggested next commands) when criteria aren't met. There is no way to skip a gate by setting `phase` directly.

Every mutating command (`ingest`, `rank`, `dedupe`, `citation-chase`, plus the replay subcommands under `research_state.py`) accepts `--idempotency-key` — a retried call with the same key returns the original result without re-mutating state, so agent crash-recovery is contract-idempotent, not just naturally so. The state file itself is written under a sibling `.lock` file with atomic `os.replace`, so concurrent Phase 1 searches are race-free.

### Pipeline diagram

```mermaid
flowchart LR
    Q([Question]) --> P0[0 · Scope]
    P0 --> P1[1 · Discover]
    P1 --> P2[2 · Triage]
    P2 --> P3[3 · Deep read]
    P3 --> P4[4 · Chase]
    P4 --> P5[5 · Synthesize]
    P5 --> P6[6 · Self-critique]
    P6 -- blockers --> P1
    P6 --> P7[7 · Report]
    P7 --> OUT([Cited report + .bib])

    STATE[(research_state.json)]
    P0 & P1 & P2 & P3 & P4 & P5 & P6 & P7 <-.-> STATE

    classDef phase fill:#eef5ff,stroke:#1F6FEB,color:#0b2e66;
    classDef state fill:#f6ffed,stroke:#389e0d,color:#135200;
    class P0,P1,P2,P3,P4,P5,P6,P7 phase;
    class STATE state;
```

Every phase reads and writes `research_state.json` — it's the single source of truth that makes the workflow resumable and auditable. Phase 6 (self-critique) can loop back to Phase 1 when it finds gaps; everything else is linear.

## Prerequisites

- **Python ≥ 3.9**
- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
  Pulls in `httpx` (HTTP client) and `pypdf` (PDF text extraction).

No API keys are required. For higher OpenAlex / Crossref / PubMed rate limits, pass `--email <you@host>` (polite pool) or `--api-key` (NCBI). All scripts work without these.

## Skill Installation

### 🪄 Quickest — just ask your agent

The simplest install is to let your coding agent do it. In **Claude Code**, **OpenAI Codex**, **OpenCode**, **OpenClaw**, **Hermes Agent**, or **pi-mono**, paste this:

```
Install https://github.com/Agents365-ai/scholar-deep-research for me, then run pip install -r requirements.txt inside it.
```

The agent will:
1. Recognize this as an Agent Skills repo (`SKILL.md` at the root)
2. `git clone` it into the correct skills directory for whichever platform is hosting it (e.g. `~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.openclaw/skills/`, `~/.hermes/skills/research/`, `~/.pimo/skills/`, or `~/.agents/skills/`)
3. Install Python dependencies (`httpx`, `pypdf`)
4. Confirm the skill is loaded and ready

After that, ask for a research report and the skill triggers automatically. No manual `git clone` needed.

If you prefer to do it by hand, the per-platform commands are below.

### Claude Code

```bash
# Global install (available in all projects)
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.claude/skills/scholar-deep-research

# Project-level install
git clone https://github.com/Agents365-ai/scholar-deep-research.git .claude/skills/scholar-deep-research
```

### OpenCode

```bash
# Global install
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.config/opencode/skills/scholar-deep-research

# Project-level install
git clone https://github.com/Agents365-ai/scholar-deep-research.git .opencode/skills/scholar-deep-research
```

### OpenClaw / ClawHub

```bash
# Via ClawHub
clawhub install scholar-deep-research

# Manual install
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.openclaw/skills/scholar-deep-research

# Project-level install
git clone https://github.com/Agents365-ai/scholar-deep-research.git skills/scholar-deep-research
```

### Hermes Agent

```bash
# Install under research category
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.hermes/skills/research/scholar-deep-research
```

Or add an external directory in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/myskills/scholar-deep-research
```

### pi-mono

```bash
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.pimo/skills/scholar-deep-research
```

### OpenAI Codex

```bash
# User-level install
git clone https://github.com/Agents365-ai/scholar-deep-research.git ~/.agents/skills/scholar-deep-research

# Project-level install
git clone https://github.com/Agents365-ai/scholar-deep-research.git .agents/skills/scholar-deep-research
```

### SkillsMP

```bash
skills install scholar-deep-research
```

### Updating

The skill **auto-updates on invocation.** Every time a host LLM activates `scholar-deep-research` for a new research task, Phase 0 Step 0 runs `python scripts/check_update.py`, which:

1. `git fetch`es the upstream remote (the one network call) — typically a few hundred milliseconds
2. Fast-forwards the local checkout if an update is available
3. Refuses to touch your working tree if you have local edits — you'll see a one-line `[Skill update skipped — you have local changes …]` notice instead of having work clobbered
4. Detects `requirements.txt` drift and surfaces a hint; **pip install is never run automatically** (the skill doesn't know which Python / venv is yours)
5. Never fails the workflow — offline, no remote, or package-manager install all degrade silently to `check_failed` / `not_a_git_repo` and research proceeds with the current version

When an update is applied you'll see a single line in the chat, e.g. `[Skill updated: abc123 → def456 (3 commits). Continuing with new version.]`. The `from` / `to` short SHAs let you run `git log abc123..def456` in the skill directory to see exactly what changed.

**Pinning a version.** If you want to hold a specific commit — for a paper submission, a reproducibility run, or while a downstream script is being validated — set:

```bash
export SCHOLAR_SKIP_UPDATE_CHECK=1
```

With that set, the auto-update check short-circuits and the skill runs exactly the version on disk until you unset the variable. You can also combine with a `git checkout <sha>` to pin a specific historical version.

**Manual update** (also works as a last resort):

```bash
cd ~/.claude/skills/scholar-deep-research   # or your install path
git pull --ff-only
pip install -r requirements.txt              # only if you see the deps-changed hint
```

Users installed through a package manager (ClawHub, SkillsMP, Hermes registry) should use that manager's own update command instead; `check_update.py` will detect the non-git install and stay out of its way.

### Installation paths summary

| Platform | Global path | Project path |
|----------|-------------|--------------|
| Claude Code | `~/.claude/skills/scholar-deep-research/` | `.claude/skills/scholar-deep-research/` |
| OpenCode | `~/.config/opencode/skills/scholar-deep-research/` | `.opencode/skills/scholar-deep-research/` |
| OpenClaw / ClawHub | `~/.openclaw/skills/scholar-deep-research/` | `skills/scholar-deep-research/` |
| Hermes Agent | `~/.hermes/skills/research/scholar-deep-research/` | Via `external_dirs` config |
| pi-mono | `~/.pimo/skills/scholar-deep-research/` | — |
| OpenAI Codex | `~/.agents/skills/scholar-deep-research/` | `.agents/skills/scholar-deep-research/` |
| SkillsMP | N/A (installed via CLI) | N/A |

## Usage

Just describe what you want:

```
Run a deep research report on CRISPR base editing for Duchenne muscular dystrophy.
```

The agent will:
1. Restate the question and pick an archetype
2. Run multi-source searches with saturation tracking
3. Rank, dedupe, and select the top-N
4. Deep-read PDFs and extract evidence
5. Chase citations (forward + backward)
6. Cluster themes and map tensions
7. Run a self-critique pass
8. Render the chosen archetype with bibliography

The output lives at `reports/<slug>_<YYYYMMDD>.md` plus a `.bib` bibliography.

## Example phases

```
[Phase 0] Restating: "What is the current state of CRISPR base editing as a
          therapeutic for Duchenne muscular dystrophy?"
          Archetype: literature_review
          → research_state.json initialized

[Phase 1] OpenAlex + PubMed + arXiv + Crossref across 3 clusters...
          Round 1: 187 hits, 142 unique. Round 2: 94 hits, 31 new.
          Saturation: new=11%, max_new_citations=23 → SATURATED

[Phase 2] Ranking with literature-review weights...
          Top 20 selected. Score components written to state.

[Phase 3] 17/20 full text, 3 abstract-only (flagged shallow).

[Phase 4] Citation chasing on top 8 seeds, depth 1.
          Added 24 candidates, 6 re-scored into top 20.

[Phase 5] Themes: delivery, editing efficiency, off-target safety,
          pre-clinical, clinical translation.
          Tensions: AAV serotype optimality (3 papers disagree).

[Phase 6] Self-critique flagged 2 single-source claims and a recency gap.
          Ran focused search; added 4 papers.

[Phase 7] reports/crispr-base-editing-dmd_20260411.md (84 refs)
```

## Files

```
scholar-deep-research/
├── SKILL.md                       # Skill instructions (the only required file)
├── README.md                      # This file
├── README_CN.md                   # 中文文档
├── requirements.txt               # httpx, pypdf
├── agents/
│   └── openai.yaml                # OpenAI Codex sidecar (interface, capabilities, prereqs)
├── scripts/
│   ├── _common.py                 # Shared paper schema + emit helper
│   ├── research_state.py          # Central state file management
│   ├── search_openalex.py         # OpenAlex (primary)
│   ├── search_arxiv.py            # arXiv preprints
│   ├── search_crossref.py         # Crossref REST
│   ├── search_pubmed.py           # NCBI E-utilities
│   ├── dedupe_papers.py           # Cross-source deduplication
│   ├── rank_papers.py             # Transparent scoring
│   ├── build_citation_graph.py    # Forward + backward snowball
│   ├── extract_pdf.py             # PDF extraction with DOI resolution (paper-fetch / Unpaywall)
│   └── export_bibtex.py           # BibTeX / CSL-JSON / RIS
├── references/
│   ├── search_strategies.md       # Boolean, PICO, snowballing, saturation
│   ├── source_selection.md        # Which database for which question
│   ├── quality_assessment.md      # CRAAP, tier, retraction, preprints
│   ├── report_templates.md        # Archetype selection guide
│   └── pitfalls.md                # 14 failure modes with fixes
└── assets/
    ├── templates/
    │   ├── literature_review.md
    │   ├── systematic_review.md
    │   ├── scoping_review.md
    │   ├── comparative_analysis.md
    │   └── grant_background.md
    └── prompts/
        └── self_critique.md       # 14-point Phase 6 checklist
```

> **Note:** Only `SKILL.md` and `scripts/` are required for the skill to work. `references/` and `assets/` are progressive-disclosure resources the model loads on demand.

## Known Limitations

- **No Google Scholar / Web of Science / Scopus** — these have no public API or require institutional access. Mention in report appendix as "not consulted" if it matters.
- **Scanned PDFs** — `extract_pdf.py` detects them but doesn't OCR. Use a separate OCR step if needed.
- **DOI resolution requires open access** — `--doi` mode only finds legally open-access PDFs (via [paper-fetch](https://github.com/Agents365-ai/paper-fetch) or Unpaywall). Paywalled papers fall back to abstract-only.
- **arXiv has no citation counts** — arXiv-only papers get `citations=null` and a 0 contribution from the citation component of the rank score.
- **PubMed full abstracts** — fetched on demand only (`--with-abstracts`); the default round-trip uses esummary for speed.
- **English-language bias** — all four sources index non-English work but search quality varies. Note in the report's limitations if the topic has substantial non-English literature.
- **Ranking is bag-of-words for relevance** — for semantic re-ranking, plug an embedding model and write the result back into `state.papers[*].score_components.relevance`. The pipeline is designed for that override.

## License

MIT

## Support

If this skill helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
