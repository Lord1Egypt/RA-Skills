---
name: core-arch-upkeep-routing
description: Route every repo to a canonical arch-* skill and upgrade architecture via arch-upkeep.
---

# Map Architecture to `arch-*` Skills via `arch-upkeep`

Every project should map cleanly to one or more canonical `arch-*` skills, and `arch-upkeep` is the orchestrator that keeps architectures aligned and upgraded.

## Usage

1. **Detect current architecture**
   - Use `@skills/arch-upkeep` to classify the repo:
     - Monorepo (`arch-tsdown-monorepo`)
     - Single TS library (`arch-tsdown`)
     - CLI (`arch-tsdown-cli`)
     - unplugin library (`arch-unplugin`)
     - Web extension + Vue (`arch-webext-vue`)
     - VS Code extension (`arch-vscode`)
2. **Choose target `arch-*` skill(s)**
   - Pick the primary architecture that best matches the desired end state.
   - If mixed (e.g. monorepo with CLI + libs), combine `arch-tsdown-monorepo` with per-package skills.
3. **Plan incremental migration**
   - Follow `arch-upkeep`’s recommended order:
     - Normalize layout.
     - Migrate build to tsdown (where applicable).
     - Align test/lint/CI and release.
4. **Treat mismatches as upgrade opportunities**
   - If the current shape does not match any `arch-*` cleanly:
     - Do **not** pile on more ad-hoc config.
     - Use `arch-upkeep` to plan a series of PRs that move towards the chosen starter architecture.

## Key Points

- There should always be a clear answer to “which `arch-*` skill describes this repo/package?”.
- `arch-upkeep` is the router/orchestrator; concrete details live in each `arch-*` skill.
- Architecture drift is a signal to run an upkeep pass, not to add more custom scripts.

<!--
Source references:
- Internal hairy global preference: "Architecture must map to `arch-*` skills"
- @skills/arch-upkeep
-->

