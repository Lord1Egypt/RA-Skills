# Research Paper Figure Skill Factory

Version: 1.0.1

This guide is a two-layer Skill Factory:

1. Build a specialized figure-making skill for a chosen paper-figure class from lawful source acquisition, full-feasible local PDF coverage, structured figure/caption evidence, taxonomy, and skill-package testing.
2. Use that generated specialized skill to design, generate, review, and integrate concrete figures for arbitrary target papers of that class.

## Core Rules

- First trigger only shows the plan; no analysis or image generation.
- B1-B9 are the Skill Builder layer.
- P1-P9 are the generated Figure Production layer.
- Generated specialized skills must mark every step as `TEXT_ONLY` or `IMAGE_ONLY`.
- Text and image generation must never be combined in one response.
- ChatGPT web uses Create image through ChatGPT Images 2.0.
- Codex uses `$imagegen` first; if unavailable, use ChatGPT Images 2.0 API or another approved image-generation API.
- SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, and code-rendered images are forbidden as visual outputs or fallbacks.
- Full-feasible local corpus coverage is required before production-grade generated skill locking when many relevant PDFs exist.

## v1.0.1 Candidate-Image Bridge

Generated figure-making skills must not stop at text candidates. After any multi-option text decision, they must include:

1. `TEXT_ONLY` candidate-board setup.
2. `IMAGE_ONLY` generation/display of 4-6 candidate images or schematic candidates, normally 6.
3. `TEXT_ONLY` candidate review, recording the image batch and asking the user to select, revise, combine, or request another board.

Generated skill tests must fail if a workflow jumps from 4-6 text candidates, layout/style-axis setup, or prompt alternatives directly to final prompt, final image, caption, or text-only locking unless the user explicitly skipped image candidates.
