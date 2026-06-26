# Release Checklist - v1.0.1

## Factory Package

- [x] `SKILL.md` has name, description, MIT-0 license, version 1.0.1, and OpenClaw metadata.
- [x] `VERSION` is 1.0.1.
- [x] `metadata.json` is valid JSON and says 1.0.1.
- [x] `agents/openai.yaml` says 1.0.1.
- [x] Startup workflow lists S0, B1-B9, and P1-P9.
- [x] Skill Builder layer remains specialized-skill-first.
- [x] Full-feasible local PDF coverage policy remains active.
- [x] Strict text/image separation remains active.
- [x] ChatGPT web Create image / ChatGPT Images 2.0 route remains active.
- [x] Codex `$imagegen` first route remains active.

## Generated Skill Candidate-Image Bridge

Before any generated specialized figure-making skill can be locked, verify:

- [ ] Production workflow includes P1-P9 or a stricter equivalent.
- [ ] P3 or equivalent produces 4-6 text candidates, normally 6.
- [ ] After text candidates, the first recommended next prompt asks to generate/display candidate images or schematic candidates, normally 6.
- [ ] P4 or equivalent is a `TEXT_ONLY` visual candidate-board setup step.
- [ ] P5 or equivalent is an `IMAGE_ONLY` candidate-board generation step.
- [ ] P6 or equivalent is a `TEXT_ONLY` candidate-review/selection step.
- [ ] The workflow does not move from text candidates directly to final prompt, formal image generation, caption, or text-only lock unless the user explicitly skips image candidates.
- [ ] State footer includes `visual_candidate_board_status`, `candidate_image_batch_id`, and `selected_visual_candidate`.
- [ ] The next text reply after `IMAGE_ONLY` generation records the generated image batch.
- [ ] Examples include startup, text candidates, candidate-board setup, image-only candidate board, and candidate review.
- [ ] Rendering route uses ChatGPT web Create image / ChatGPT Images 2.0 and Codex `$imagegen` first.
- [ ] SVG/Mermaid/TikZ/Graphviz/HTML-CSS/canvas/matplotlib/code-rendered visual fallbacks are forbidden.
