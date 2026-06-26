# Changelog

All notable changes to the SELF-DISCOVER Skill.

## [1.0.0] - 2026-05-20

### Added
- Core SELF-DISCOVER pipeline: SELECT → ADAPT → IMPLEMENT
- 8 seed reasoning modules with descriptions
- 4 depth levels (Level 0-3, auto-selected by task complexity)
- Inline discovery templates for platforms without file access
- Platform auto-detection at skill load time
- Task-type classification for module selection
- Convergence rules (max 3 composition iterations)
- Cost control strategy (0-40% token overhead by depth)
- Ready-to-use discovery prompt templates per depth level
- 14 platform compatibility with installation instructions
- Benchmark report (20 questions, 5 categories, +24.6% improvement)
- Before/After examples in README

### References Added
- Zhou et al. (2024) — SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
- Yao et al. (2023) — Tree of Thoughts
- Wang et al. (2023) — Plan-and-Solve Prompting
- Yasunaga et al. (2024) — Large Language Models as Analogical Reasoners
- Shinn et al. (2023) — Reflexion
- Madaan et al. (2023) — Self-Refine
