# Setup — Tailwind CSS

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Tailwind's failures are quiet: a class that generates nothing, a rule that loses the cascade, a rename that compiles fine and shifts the design. Name the mechanism before giving the fix, and verify against the built artifact rather than the source.

## How To Load Preferences

1. Read `~/Clawic/data/tailwindcss/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `tailwind_version: 4`, `build_integration: vite`, `dark_mode_strategy: media`, `component_syntax: jsx`, `merge_helper: cn`, `rem_base: 16`, `token_threshold: 3`, `text_direction: ltr`, `a11y_target: aa`.
3. Read `~/Clawic/data/tailwindcss/memory.md` for prior context (stack, design system, recurring pain points). Absence is fine; proceed without comment.
4. Cheap inference beats asking: the repository answers most of these. A `@import "tailwindcss"` in the CSS means v4; `@tailwind base` means v3; `@tailwindcss/vite` in `vite.config` sets `build_integration`; a `dir="rtl"` root or logical utilities already in the markup set `text_direction`. Detect, apply, and only record the value when the user states it as a preference.

Work from defaults immediately. Never open with questions about stack, priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a major, an integration, a dark-mode strategy, a markup language, a merge helper, a root font size, a promotion threshold, a text direction, or an accessibility target → update the matching key in `~/Clawic/data/tailwindcss/config.yaml`.
- User expresses a habit or stance (whether `@apply` is allowed, which UI kit is in play, tolerance for the `!` modifier, whether Preflight may be dropped) → record it under the relevant preference area (tooling, conventions, design system, integrations, risk posture, constraints, output) in `~/Clawic/data/tailwindcss/memory.md`.
- User corrects earlier guidance → update the stored value so the correction isn't needed twice.

A value read from the repository is context, not a preference: apply it, don't store it. If the user has said nothing, store nothing.

## What Memory Holds

The memory template shipped with this skill gives the file format. Track their stack and major, the design system in play, banned techniques, and the depth of explanation they want — but only from what they actually reveal.
