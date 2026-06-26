# Master Workflow

Version: 1.0.1

This skill is a two-layer Skill Factory.

- **Skill Builder layer (B1-B9):** build, test, patch, package, and lock a reusable specialized figure-making skill for one research-paper figure class.
- **Figure Production layer (P1-P9):** after a generated specialized skill is locked, use it to produce concrete figures for arbitrary target papers of that figure class.

## Workflow Table

| Code | Layer | Mode | Name | Output |
|---|---|---|---|---|
| S0 | Startup | STARTUP_PLAN_ONLY (TEXT_ONLY) | Startup confirmation gate | Full plan only |
| B1 | Skill Builder | TEXT_ONLY | Target figure class and skill objective | Figure-class brief |
| B2 | Skill Builder | TEXT_ONLY | Literature goal and corpus plan | Corpus plan and inclusion rules |
| B3 | Skill Builder | TEXT_ONLY | Lawful literature acquisition and local corpus artifact | PDFs/manifests/acquisition report |
| B4 | Skill Builder | TEXT_ONLY | Evidence extraction from corpus | Paper cards, figure/caption inventory, evidence map |
| B5 | Skill Builder | TEXT_ONLY | Evidence-backed taxonomy | Taxonomy and lineage |
| B6 | Skill Builder | TEXT_ONLY | Specialized skill blueprint | Workflow, state schema, prompt/style/review rules |
| B7 | Skill Builder | TEXT_ONLY | Generate specialized skill | Skill package files |
| B8 | Skill Builder | TEXT_ONLY | Test and patch specialized skill | Test report and patched files |
| B9 | Skill Builder | TEXT_ONLY | Lock generated skill | Locked slug/version/scope/limitations |
| P1 | Figure Production | TEXT_ONLY | Target-paper material intake | Material status |
| P2 | Figure Production | TEXT_ONLY | Figure need diagnosis and routing | Subtype candidates + default recommendation |
| P3 | Figure Production | TEXT_ONLY | Reader effect and 4-6 text candidate schemes | Text candidates + required visual-candidate next action |
| P4 | Figure Production | TEXT_ONLY | Visual candidate board setup | Board brief: count, varied axis, fixed content, route |
| P5 | Figure Production | IMAGE_ONLY | Visual candidate board generation | 4-6 image/schematic candidates, normally 6 |
| P6 | Figure Production | TEXT_ONLY | Candidate review and direction lock | Recorded image batch + selected/revised direction |
| P7 | Figure Production | TEXT_ONLY | Final image brief construction | Formal prompt/image brief |
| P8 | Figure Production | IMAGE_ONLY | Formal figure candidate generation | Formal image batch only |
| P9 | Figure Production | TEXT_ONLY | Review and paper text package | Critique, caption, legend, body text, handoff |

## Mandatory Candidate-Image Bridge

The generated production workflow must not stop at text candidates. After any text reply that presents multiple schemes, subtypes, layouts, styles, metaphors, density levels, or prompt alternatives:

1. The first recommended next prompt must ask the user to generate/display multiple candidate images or schematic candidates, normally 6.
2. The next workflow step must be a `TEXT_ONLY` candidate-board setup step unless all setup fields were already confirmed by the user.
3. The following generation step must be `IMAGE_ONLY` and must generate/display 4-6 candidates, normally 6.
4. The next `TEXT_ONLY` step must record the generated image batch and ask the user to select, revise, or request another board.

Skipping this bridge is allowed only when the user explicitly says to stay text-only or skip image candidates. Record that as `visual_candidate_board_skipped_by_user: true`.

## Startup Table Requirement

The startup reply must show S0, B1-B9, and P1-P9 as separate rows. Every row must label `TEXT_ONLY`, `STARTUP_PLAN_ONLY (TEXT_ONLY)`, or `IMAGE_ONLY`. The startup reply is a plan only and must not analyze or generate images.

## Builder Gate Chain

Use this gate chain for production-grade generated skills:

- B3 complete for B4: `local_corpus.ready_for_extraction: true`
- B4 complete for B5: `extracted_evidence.ready_for_taxonomy: true`
- B5 complete for B6-B7: `evidence_lineage.evidence_lineage_complete: true`

If many local PDFs are available, process all accessible relevant PDFs as far as feasible and record candidate/accessible/processed/skipped counts and skipped reasons. Small samples are limited/pilot evidence unless the user accepts the limitation.

## Rendering Boundary

P5 and P8 are `IMAGE_ONLY`. They must contain only generated images/artifacts. Do not prepend a plan or append explanation. P4, P6, P7, and P9 are `TEXT_ONLY` and must not generate images in the same response.

ChatGPT web uses Create image through ChatGPT Images 2.0. Codex uses `$imagegen` first; if unavailable, use ChatGPT Images 2.0 API or another approved image-generation API. Do not substitute SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, or code-rendered images.
