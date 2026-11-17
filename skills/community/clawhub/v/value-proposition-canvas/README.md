# Value Proposition Canvas

**Run a Value Proposition Canvas workshop through both phases — Customer Profile and Value Map — with explicit user acceptance gates between every step. Tables as the primary output format. Soft rigor: hypotheses are welcomed, not rejected.**

You have user research (or need to gather some). This skill structures it into a fully-mapped VPC: Jobs, Pains, Gains (Phase 1), then Pain Relievers, Gain Creators, and a Products & Services bundle (Phase 2), then a prioritization framework selection (Phase 2.5). UVP drafting is **out of scope** — the user writes it after Kano.

## What it does

The skill has two modes:

1. **Research Ingestion** (primary) — you bring transcripts, interview notes, persona docs, or any other evidence about a specific persona or segment. The agent structures it into Phase 1 (Jobs/Pains/Gains) with verbatim source quotes, then maps it through Phase 2 (Pain Relievers, Gain Creators, Products & Services), then asks which prioritization framework you want next.
2. **Research Collection** (secondary) — you have no data yet. The agent produces a research plan: persona quality check, recruiting spec, semi-structured interview script, listening guide, capture template. You execute the plan, then the agent runs the same v2.0 pipeline.

The output is a durable Markdown artifact (`vpc-result.md` or `vpc-[persona-slug].md`) with three tables (Customer Profile, Value Map, Framework Selection) and explicit acceptance gates between every step.

The skill **stops** at "framework selected, ready for prioritization". UVP is downstream.

### Number rules (focus beats mass)

- **Customer Jobs:** 1-2 main + 3-5 supporting.
- **Pains:** 3-5 broken-leg pains.
- **Gains:** 3-5 high-value gains.
- **Pain Relievers:** 1:1 with locked Pains (no orphans).
- **Gain Creators:** 1:1 with locked Gains (no orphans, multi-tag allowed).
- **Products & Services:** 1-3 bundle items (the offering shape, not features).

If you bring 30 candidate Pains, the agent's job is to help you cluster and prune to 3-5 dominant ones.

### Core stance

- **One segment or persona at a time.** Sequential, not parallel. The agent waits for your answer to "persona or segment?" before doing anything.
- **Hard gates between every step.** Phase 1 must be accepted before Phase 2. Each Phase 2 substep must be accepted before the next. You can stop at any gate.
- **Tables, not paragraphs.** Rows are prioritized; columns are fields.
- **Pain Relievers and Gain Creators are features; Products & Services is the bundle.** The agent must not confuse these levels.
- **Every claim has a verbatim source quote.** A Pain without a quote is a `Hypothesis` (added, labeled, not deleted). The Hypothesis discipline is a guidepost, not a wall.
- **The agent does not invent.** It structures what you provide.
- **The agent does not draft a UVP.** UVP is downstream of Kano, your job.
- **The agent does not run prioritization.** You pick the framework, then run it.

## When to use

- You have interview transcripts, persona docs, or observation notes to structure into a full VPC
- You want to map Pains to Pain Relievers and Gains to Gain Creators
- You want to define a Products & Services bundle mapped to Customer Jobs
- You want to run a VPC workshop with a team or solo
- You want to choose a prioritization framework (Kano, RICE, MoSCoW, ICE) for the next step

Triggers: "value proposition canvas", "VPC", "customer jobs pains gains", "Pain Relievers", "Gain Creators", "Products and Services", "JTBD canvas", "build a value proposition", "map research to a value prop", "pick a prioritization framework".

## When NOT to use

- One-line marketing copy or UVP drafting (use a copy skill). The skill produces the VPC; the user writes the UVP.
- Financial modeling, pricing, unit economics (use a finance skill).
- User research execution — the skill plans research, it does not conduct interviews.
- Feature prioritization — that is the chosen framework's skill (e.g., `kano-model-strategist`).
- Full go-to-market strategy (use a GTM skill).
- A user who has no research base and no intention of gathering one.

## The output: `vpc-result.md`

The workshop produces a single Markdown artifact:

```
vpc-result.md
├─ 1. Customer Segment / Persona      (one sentence + behavioral profile)
├─ 2. Customer Profile (Phase 1)      (Jobs, Pains, Gains tables, all evidence-anchored)
├─ 3. Value Map (Phase 2)             (Pain Relievers, Gain Creators, Products & Services)
├─ 4. Framework Selection (Phase 2.5) (Kano / RICE / MoSCoW / ICE / custom)
├─ 5. Workshop log
├─ 6. Evidence log
├─ 7. Dalsza lektura
├─ 8. Open Questions
├─ 9. What the agent did NOT do       (UVP, prioritization, roadmap — out of scope)
└─ 10. Workshop end
```

The full template is in `references/methodology-vpc.md`, Section 6.

## Compatibility

- **Tested with:** Claude Sonnet 4.5 (Claude Code), Claude Sonnet 4.5 (opencode), MiniMax-m3
- **Designed for:** Claude Code, Codex, VS Code, OpenCode, Cursor, GitHub Copilot
- **Composes with:** `socratic-dialogue` (validation, not extraction), `kano-model-strategist` (the **next step** after the skill finishes), `legible-agent-output` (every user-facing string the agent emits)
- **No MCP, no external dependencies, no network access at runtime**

## What's inside

```
value-proposition-canvas/
├── README.md                       ← this file
├── SKILL.md                        ← what the agent loads (frontmatter + Phase 1/2/2.5 + Quality Checklist)
├── ATTRIBUTION.md                  ← source citations and license chain
├── SYNCHRONIZATION.md              ← source-of-truth ↔ public copy mapping
├── LICENSE                         ← MIT
├── references/
│   ├── methodology-vpc.md          ← 74 KB: 7 progressive-disclosure layers + Section 0 (GOOB) + Section 5 (Scope Boundary) + Section 6 (Gold Standard v2.0 template) + 2 appendices
│   └── canvas-examples/
│       └── webvan-anti-pattern.md  ← negative example: what happens without Phase 1 acceptance gates
└── examples/
    ├── research-ingestion.md       ← Use Case 1: user has data → full v2.0 pipeline (Phase 1 + Phase 2 + Phase 2.5)
    └── research-collection.md      ← Use Case 2: no data → research plan → same v2.0 pipeline
```

## Quick orientation for first-time users

If you have never run a VPC before:

1. Read `SKILL.md` end-to-end (it is short — 30 KB).
2. Read `examples/research-ingestion.md` to see the full Phase 1 → Phase 2 → Phase 2.5 pipeline in a familiar domain.
3. Run the workshop against your own research. Start with the persona-vs-segment question and let the agent structure your data.

If the workshop stalls at "I don't have evidence":

1. Read `examples/research-collection.md` for the full research plan template.
2. Run the 5-8 interviews + 1-2 shadowing sessions + forum mining. Come back with data.

If the agent is producing "Value Proposition" or "best supporting features":

1. That's a scope violation. The skill ends at framework selection. UVP and ranking are downstream.
2. Re-read SKILL.md "Scope Boundary" section. The agent must stop at Phase 2.5.

## Sources

- **Osterwalder, A., Pigneur, Y., Smith, A. (2014).** *Value Proposition Design.* Wiley. — The VPC itself.
- **Strategyzer.** https://www.strategyzer.com — Canonical steward of the canvas.
- **Interaction Design Foundation (2024).** *The Value Proposition Canvas.* — Pain and Gain category taxonomies, the two rules for gains.
- **Blank, S. (2013).** *The Four Steps to the Epiphany.* — Customer Development, GOOB.
- **Christensen et al. (2016).** *Know Your Customers' Jobs to Be Done.* HBR.
- **Gothelf, J., Seiden, J. (2016).** *Lean UX.* O'Reilly. — Three-level outcome.
- **Hunt, V. (2016).** *The Product Taster / Sprint to Market.* — Pain-Driven Design.
- **Ries, E. (2011).** *The Lean Startup.* Crown Business. — Build Trap.
- **Perri, M. (2018).** *Escaping the Build Trap.* O'Reilly.
- **Kano, N. (1984).** *Attractive Quality and Must-be Quality.* — The Kano Model.

Full attribution in `ATTRIBUTION.md`.

## Status

- **v2.2** — Current. Adds the Co-creation discipline: the agent proposes, the user decides, with an explicit wait at every gate (no auto-picked file paths, no auto-filled rows, no auto-ranked features).
- **v2.1** — Added the multi-file output structure (`vpc-result.md` + `shadow-backlog.md` + `value-proposition.md`).
- **v2.0** — Full VPC with Phase 1 + Phase 2 + Phase 2.5, tables as primary output, number rules, soft rigor, context window management, explicit acceptance gates.
- **Pending:** Path B eval (`EVIDENCE.md`) after first real workshop.

## License

MIT — see the `LICENSE` file in this directory. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisekstudio/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
