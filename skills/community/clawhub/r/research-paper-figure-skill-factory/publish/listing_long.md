# Research Paper Figure Skill Factory

Research Paper Figure Skill Factory builds reusable, evidence-backed, class-specific figure-making skills for scientific papers, then uses those generated skills for concrete target-paper figures.

The factory supports lawful literature/source acquisition, full-feasible local PDF coverage where available, structured figure/caption extraction, multi-label figure taxonomy, specialized skill generation, skill testing, packaging, and concrete figure production.

Version 1.0.1 adds a hard candidate-image bridge for generated figure-making skills:

- after 4-6 text candidates, usually 6, the generated skill must not ask the user to choose only from text as the primary route;
- it must include a `TEXT_ONLY` visual candidate-board setup step;
- it must then generate/display 4-6 candidate images or schematic candidates, usually 6, in a separate `IMAGE_ONLY` turn;
- it must then return to `TEXT_ONLY` to record the image batch and ask the user to select, revise, combine, or request another board;
- generated skill release tests must fail if this bridge is missing.

Rendering route is strict: ChatGPT web uses Create image through ChatGPT Images 2.0; Codex uses `$imagegen` first and falls back only to ChatGPT Images 2.0 API or another approved image-generation API. Native PNG/JPEG/WebP outputs from that route are allowed. SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, and code-rendered images are forbidden as candidate, draft, final, or fallback visuals.
