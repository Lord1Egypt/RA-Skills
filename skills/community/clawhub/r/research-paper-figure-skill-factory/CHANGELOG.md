# Changelog

## 1.0.1 - 2026-05-05

- Added a mandatory candidate-image bridge for generated figure-making skills.
- Expanded generated Figure Production workflow from P1-P7 to P1-P9.
- Added required P4 `TEXT_ONLY` visual candidate-board setup, P5 `IMAGE_ONLY` candidate-board generation, and P6 `TEXT_ONLY` candidate review/selection.
- Required generated skills to fail lock/tests if they move from 4-6 text candidates directly to final prompt, final image generation, caption writing, or text-only locking.
- Updated metadata, agent rules, master workflow, output spec, startup map, state footer template, and blueprint template.

## 1.0.0 - 2026-05-05

- Renamed and repositioned the package as `research-paper-figure-skill-factory`.
- Reset the public skill version to `1.0.0`.
- Required full-feasible-corpus coverage for generated specialized figure-making skills.
- Required first/startup replies to be text-only and no-image.
- Required every generated figure-making skill step to mark `TEXT_ONLY` or `IMAGE_ONLY`.
- Required every generated skill text footer to list all steps and current position.
- Required multi-option text replies to recommend multiple candidate images or schematic boards as the next action.
- Clarified rendering routes: ChatGPT web uses Create image through ChatGPT Images 2.0; Codex uses `$imagegen` first and falls back only to ChatGPT Images 2.0 API or another approved image-generation API.
