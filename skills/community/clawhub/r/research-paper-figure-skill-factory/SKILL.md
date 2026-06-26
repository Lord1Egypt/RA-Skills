---
name: research-paper-figure-skill-factory
license: MIT-0
description: "Use when the user wants a research-paper figure Skill Factory: build, patch, package, or use reusable specialized paper-figure-making skills from lawful literature/corpus evidence. Generated skills must use a specialized-skill-first workflow, full-feasible local PDF coverage where available, startup-plan-only first replies, strict text/image turn separation, ChatGPT web Create image / ChatGPT Images 2.0 rendering, Codex $imagegen-first rendering, sample-image transfer rules, all-step/current-position state footers, and a mandatory text-candidate to visual-candidate-board to image-only candidate generation to selection workflow after every multi-option figure decision."
metadata:
  display_name: Research Paper Figure Skill Factory
  version: "1.0.1"
  author: OpenAI
  tags: research-figure, paper-figure, figure-skill-builder, figure-skill-factory, scientific-illustration, figure-taxonomy, meta-skill, image-prompt, imagegen, chatgpt-images-2, clawhub, openclaw, visual-style, figure-studio
  compatibility: ChatGPT web, Codex, OpenClaw, ClawHub marketplace. Requires image-generation capability for rendering.
  openclaw:
    skillKey: research-paper-figure-skill-factory
---

# Research Paper Figure Skill Factory

This skill is a two-layer research-paper figure Skill Factory.

1. **Skill Builder layer:** build or patch a reusable specialized figure-making skill for one paper-figure class by acquiring lawful source material, extracting figure evidence, building a taxonomy, generating the skill package, testing it, and locking it.
2. **Figure Production layer:** after a specialized skill is locked, use that generated skill to design, compare, render, review, and integrate concrete figures for arbitrary target papers of the same figure class.

## Non-Negotiable Contract

### First Trigger

On first trigger, output only a startup plan. Do not analyze a paper, build a taxonomy, create candidate schemes, draft prompts, or generate images. The first reply is `STARTUP_PLAN_ONLY (TEXT_ONLY)`.

If the first user message asks for images, record the request as pending only. The first reply must not call Create image, `$imagegen`, an image API, or include image artifacts.

### Specialized-Skill-First Builder Rule

The normal route is:

`figure-class goal -> corpus plan -> lawful acquisition/local corpus -> evidence extraction -> taxonomy -> specialized skill blueprint -> generated specialized skill -> tests/patches -> locked skill -> target-paper production`.

Do not jump from source papers directly to one concrete figure unless the user explicitly chooses a full production fast-track. If fast-tracking, record the skipped builder steps and fallback skill/taxonomy.

### Full-Feasible Corpus Rule

When local PDFs, a paper index, or retrieval manifests exist, enumerate the full relevant candidate set and process as many accessible relevant PDFs as feasible. A small sample can support only a limited/pilot/fallback lock unless the user explicitly accepts that limitation. Representative rendered pages are audit aids only, not the corpus size.

### Mandatory Candidate-Image Bridge

Every generated specialized figure-making skill must include a hard workflow bridge after any multi-option text decision:

1. `TEXT_ONLY` candidate text turn: present 4-6 text candidates, normally 6.
2. `TEXT_ONLY` visual candidate setup turn: define candidate count, varied axis, fixed elements, rendering route, and what the user should compare.
3. `IMAGE_ONLY` candidate-board turn: generate/display 4-6 candidate images or schematic candidates, normally 6.
4. `TEXT_ONLY` candidate-review turn: record the previous image batch, compare candidates, recommend one direction, and ask the user to select, revise, or request another board.

This bridge is mandatory after candidate schemes, subtype choices, layout choices, style choices, metaphor choices, density choices, and prompt alternatives. The generated skill must not move directly from 4-6 text candidates to final prompt construction, final image generation, caption writing, or text-only locking unless the user explicitly says to skip image candidates and stay text-only. If skipped, record `visual_candidate_board_skipped_by_user: true`.

Generated skill lock/test must fail if:

- the workflow lacks a dedicated visual candidate setup step;
- the workflow lacks a dedicated `IMAGE_ONLY` candidate-board step before direction lock;
- examples show text candidates followed directly by final prompt or final image generation;
- the state footer cannot record `visual_candidate_board_status`, `candidate_image_batch_id`, and `selected_visual_candidate`;
- multi-option next prompts do not ask the user to generate/display multiple candidate images or schematic candidates, normally 6.

### Strict Text/Image Separation

Every response is exactly one modality:

- `TEXT_ONLY`: planning, intake, diagnosis, candidate text, candidate-board setup, prompt writing, critique, status, and next prompts.
- `IMAGE_ONLY`: image generation only. No prose, captions, critique, prompt text, or state footer.

If a reply emits any visible text, it must not generate images in the same response. If the user confirms generation and state is sufficient, the next assistant response may be `IMAGE_ONLY` only.

### Rendering Route

For candidate boards, draft candidates, final diagrams, and revisions:

1. ChatGPT web must use **Create image** through **ChatGPT Images 2.0**.
2. Codex must use the `$imagegen` skill first.
3. If `$imagegen` is unavailable in Codex, use ChatGPT Images 2.0 API or another approved image-generation API.
4. Native bitmap outputs such as PNG, JPG, JPEG, and WebP are allowed when produced by the approved image route.
5. Do not use SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported figures as candidate images, draft images, final visuals, or fallbacks.

### Reference Images

Generated specialized skills must support optional sample/reference images. If the user provides multiple images, ask which attributes to borrow from each image: style, layout, panel rhythm, density, content-detail level, labels, color semantics, callout grammar, or negative-reference constraints.

### Every Text Reply

Every `TEXT_ONLY` reply from this factory and from generated specialized skills must include:

- `当前执行计划`
- substantive work for the current step
- `默认推荐`
- `当前状态与产物`
- `下一步你可以这样问`

The state footer must list all steps plus the current position and the response mode of every step. The first copyable next prompt must use:

`请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：...`

Always include:

`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

## Skill Builder Workflow

| Step | Layer | Mode | Purpose | Output |
|---|---|---|---|---|
| S0 | Startup | STARTUP_PLAN_ONLY (TEXT_ONLY) | Show the complete two-layer plan only | Startup plan |
| B1 | Skill Builder | TEXT_ONLY | Define target figure class and generated skill goal | Figure-class brief |
| B2 | Skill Builder | TEXT_ONLY | Define corpus scope, venues, keywords, and lawful acquisition route | Corpus plan |
| B3 | Skill Builder | TEXT_ONLY | Acquire or organize open/user-authorized PDFs and manifests | Local corpus + retrieval manifest |
| B4 | Skill Builder | TEXT_ONLY | Extract paper cards, captions, figure inventory, labels, and visual observations | Evidence artifacts |
| B5 | Skill Builder | TEXT_ONLY | Build evidence-backed figure-class taxonomy | Taxonomy + lineage |
| B6 | Skill Builder | TEXT_ONLY | Convert taxonomy into specialized skill blueprint | Blueprint |
| B7 | Skill Builder | TEXT_ONLY | Generate specialized skill package | Skill folder/package |
| B8 | Skill Builder | TEXT_ONLY | Test and patch startup, state, candidate-board, rendering, and prompt behavior | Test report + patches |
| B9 | Skill Builder | TEXT_ONLY | Lock generated skill for reusable production | Locked skill with version/scope |

## Required Generated Figure-Production Workflow

Every generated specialized figure-making skill must use this expanded production workflow, or a stricter equivalent with the same mandatory candidate-image bridge:

| Step | Mode | Purpose | Output |
|---|---|---|---|
| P1 | TEXT_ONLY | Intake target-paper material, target slot, constraints, and optional sample images | Material status |
| P2 | TEXT_ONLY | Diagnose figure need and multi-label subtype routing | Subtype candidates + default route |
| P3 | TEXT_ONLY | Define reader effect and produce 4-6 text candidate schemes, normally 6 | Text candidates + required visual-candidate next action |
| P4 | TEXT_ONLY | Set up visual candidate board: candidate count, varied axis, fixed content, route, comparison criteria | Candidate-board brief |
| P5 | IMAGE_ONLY | Generate/display 4-6 candidate images or schematic candidates, normally 6 | Image candidates only |
| P6 | TEXT_ONLY | Record the image batch, compare candidates, recommend one, and lock or revise direction | Selected/revised visual direction |
| P7 | TEXT_ONLY | Build final content architecture and formal image brief/prompt for the selected direction | Final image brief |
| P8 | IMAGE_ONLY | Generate formal figure candidate or revision batch through the approved image route | Formal image candidates only |
| P9 | TEXT_ONLY | Review, refine, caption, legend, body insertion, and handoff text | Final paper text package |

Rules for this workflow:

- P3 must not ask the user to choose only from text as the primary route. Its first recommended next prompt must be to generate/display 6 candidate images or schematic candidates.
- P4 is required before P5 unless the immediately preceding user message already confirms the board count, varied axis, fixed elements, and rendering route.
- P5 is not a final figure stage. It is a visual selection stage.
- P6 must happen after P5 and must record the image batch before any final prompt or caption work.
- P7/P8 may only occur after a direction is selected or the user explicitly requests a formal generation despite unresolved candidates.
- Any generated skill may add more domain-specific steps, but it must not remove P4/P5/P6 or collapse them into a mixed text+image response.

## Generated Skill Package Requirements

Generated specialized skills must include the candidate-image bridge in:

- `SKILL.md`
- `metadata.json`
- `agents/openai.yaml`
- `references/workflow-and-state-contract.md`
- `references/visual-style-and-board-protocol.md`
- `references/prompt-generation-policy.md`
- `templates/state-footer-template.md`
- `templates/figure-brief-template.md`
- `templates/prompt-template.md`
- examples, especially startup, text-candidate, visual-board setup, image-only board, and candidate-review examples
- release checklist and starter prompts

The release checklist must include a failing test for the exact bug this patch fixes: “after 4-6 text candidates or layout/style-axis setup, the generated skill still has no separate candidate-image generation step.”

## Reference Loading Order

Load references as needed:

1. `references/master-workflow.md`
2. `references/generated-specialized-skill-output-spec.md`
3. `references/generated-skill-multi-candidate-policy.md`
4. `references/visual-first-decision-board-protocol.md`
5. `references/startup-plan-step-output-map.md`
6. `references/planning-state-and-navigation-contract.md`
7. `references/prompt-generation-and-rendering-policy.md`
8. `references/strict-text-image-turn-separation-policy.md`
9. `templates/specialized_skill_blueprint_template.md`
10. `templates/state_footer_template.md`

## Version Note

Version 1.0.1 makes the candidate-image bridge mandatory in generated figure-making skills. A generated skill must no longer stop at text candidates, layout/style axis decisions, or visual-board suggestions; it must provide explicit steps for candidate-board setup, image-only generation of multiple candidates, and text-only candidate review/selection.
