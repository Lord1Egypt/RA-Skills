---
name: coverage-loop
description: Defines the coverage loop and what counts as a major module when generating skills from a repo.
---

# Coverage Loop and Major Modules

When creating skills from a repo (create-skills-from-repo), the agent must loop until no **major modules** are missing. This reference defines how to run the loop and what “major” means.

## The Loop

1. **Review** — Compare `skills/<skills-name>/references/` and `SKILL.md` to the repo’s documented surface (docs tree, README, nav/sidebar).
2. **Identify** — List topics that are present in the repo but not yet covered by any reference file, and that qualify as “major” (see below).
3. **Supplement** — For each such topic, add a reference file and update `SKILL.md`.
4. **Decide** — If no major topics remain uncovered, exit the loop; otherwise repeat from step 1.

## What Counts as a Major Module

**Include (major):**

- **Core concepts** — Central ideas, data model, or architecture the project is built on (e.g. “stores”, “components”, “routing”).
- **Primary APIs / surface** — Main entry points, config, and APIs that agents or users use routinely (e.g. main CLI commands, core composables, config schema).
- **Main feature areas** — Documented feature sets that are first-class in the docs (e.g. “plugins”, “testing”, “deployment”).
- **Integration points** — How the project integrates with the rest of the stack (e.g. “Nuxt module”, “Vite plugin”, “CLI usage”).

**Exclude (not major for the loop):**

- **Get-started / install** — Installation, “quick start”, or “hello world” unless they encode non-obvious conventions.
- **Changelog / migration** — Version history or migration guides (unless the user explicitly asked for them).
- **Narrow edge cases** — Rare options or scenarios that are not in the main nav or README.
- **Content agents already know** — General programming or tooling knowledge that is not specific to this project.

## When to Stop

- Stop when every major area from the repo’s **main documentation structure** (nav/sidebar/top-level README sections) is covered by at least one reference, and there are no obvious “missing chapter” gaps.
- Do **not** require coverage of every subpage or every paragraph; aim for coherent, agent-usable coverage of the main surface.
- If in doubt, one more loop to add one clearly missing major topic is fine; then stop and let the user ask for “more” if needed.

## Practical Check

Before exiting the loop, ask:

- “If an agent had only these references and SKILL.md, could it reliably use this project’s main features and APIs?”  
- “Is there a clear section in the repo’s docs that has no corresponding reference?”  

If the answer to the first is yes and the second is no, the loop is complete.
