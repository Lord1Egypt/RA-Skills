# Codebase Report — Standard Structure

Read this in `full` scan mode, or when the user asks for a **repository
report** ("docs for the repo", "onboarding guide", "write up how this codebase
works"). A bare "a report" (weather, sales, ...) is out of scope — this page
only activates in repository context. A Codebase Report is **conclusions + diagrams +
source evidence + notes** — not a pile of images. Every section answers one
question; every claim either carries evidence or is visibly flagged.

## Section Template

| # | Section | Answers | Diagram (usual pick) |
|---|---|---|---|
| 1 | Overview | What is this, who runs it, what's the shape? | 1 `archmap` tier overview |
| 2 | Modules | What are the parts and their jobs? | 1 `archmap` per subsystem (only if >4 modules) or mind map |
| 3 | Dependencies | Who depends on whom, and how heavily? | Sankey weighted by imports/bytes, or `archmap` + `main` edges |
| 4 | Execution | How does a request/task flow through? | `seq` for the golden path; `lifecycle` for state machines |
| 5 | Data Flow | Where does data originate, transform, persist? | Sankey (volumes) or `dataflow` DFD |
| 6 | Database | What's stored, keyed by what? | `erd` (tables/views + cardinalities) |
| 7 | Entry Points | Where do requests/commands come in? | Flowchart (`/draw/mermaid`) of CLI/API/bootstrap |
| 8 | External Services | What third parties does it call? | `archmap` `ext` tier detail or a table + small map |
| 9 | Risks | What structural problems exist? | Bullets + 1 diagram only if it clarifies (cycle → `archmap` with `dash` back-edge) |

Skip sections that don't apply (a library has no DB; a CLI has no request
lifecycle). A good report has 3–6 sections, not 9 by force.

## Per-Section Shape

```markdown
### 4. Execution
<2-4 sentence conclusion: the golden path, in plain language>

![Request lifecycle](<draw-url>)
- <bullet: what to notice in the diagram>
- <bullet: coupling / failure mode>

Evidence: verified 6 · inferred 1 — `api→service` is inferred (factory lookup).
```

- Conclusion first, diagram second, judgment bullets third, evidence line last.
- The evidence line per section feeds the global quality report.

## Assembly

1. Run the mode-appropriate scans once; reuse the IR inventory across sections
   (one scan, many diagrams — see `references/repository-ir.md`).
2. Validate every URL (`bash scripts/validate.sh <urls…>`) before delivery.
3. Deliverables, in increasing permanence:
   - Chat: sections as Markdown + image embeds (default, zero writes).
   - `bash scripts/build_html.sh "Repo Report" repoviz-report.html '<json>'` —
     one section per diagram; pass `ev` so each section gets its evidence table;
     print-to-PDF friendly.
   - `bash scripts/inject_readme.sh README.md '<json>'` — keep the Overview +
     Execution diagrams living in the repo between reports.
4. Close with the global quality report (counts across all sections).

## Budget & Limits

- Whole report ≤ ~60 diagram nodes total (3–6 diagrams × ~12 nodes). A repo that
  needs more is a repo that needs subsystems — link, don't cram.
- Every section's diagram respects the single-diagram guardrail
  (~15–20 nodes) from `SKILL.md`.
- Token order: manifests → tree → entry points → per-section evidence files.
  Never bulk-read; the report is only as trustworthy as its evidence discipline.

## Anti-Patterns

- Don't pad: a section with nothing to say should be absent, not verbose.
- Don't narrate the picture ("as you can see…") — conclusions add what the
  diagram cannot show.
- Don't bury risks: if you found a cycle or a god-module, it leads the Risks
  section with its evidence, not a footnote.
