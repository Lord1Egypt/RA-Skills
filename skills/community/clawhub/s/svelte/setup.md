# Setup — Svelte

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Svelte rewards precision: the reactivity model is small, and almost every bug is a violation of one of its rules rather than a mystery. Diagnose from the symptom, name the rule, give the fix in the user's own syntax mode. Be direct, and do not rewrite a working Svelte 4 codebase into runes unless the user asked.

## How To Load Preferences

1. Read `~/Clawic/data/svelte/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `syntax_mode: runes`, `kit_project: true`, `deployment_adapter: auto`, `package_manager: npm`, `styling: scoped-css`, `typescript: true`, `experimental_features: false`, `check_threshold: error`.
3. Detect rather than ask where the project itself answers the question: `svelte.config.js` names the adapter, the lockfile names the package manager, `package.json` names the Svelte and Kit versions, and any `$state`/`export let` in `src/` reveals the syntax mode. What the code says wins over a stale config value; record the correction.
4. Read `~/Clawic/data/svelte/memory.md` for prior context (project shape, recurring pain points). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about stack, conventions, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a syntax mode, adapter, package manager, styling approach, or TypeScript stance → update the matching key in `~/Clawic/data/svelte/config.yaml`.
- User expresses a habit or stance (naming conventions, validation library, whether the app must work without JavaScript, how strictly to treat a11y warnings, unit-vs-e2e balance, tolerance for experimental APIs, how much explanation they want) → record it under the relevant preference area (conventions, stack, progressive enhancement, accessibility posture, testing strategy, risk posture, budgets, output format, proactivity) in `~/Clawic/data/svelte/memory.md`.
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track the project shape (Svelte-only vs SvelteKit, versions, adapter), the migration state of a mixed codebase, recurring pain points, and their stance in the preference areas above (explanation depth belongs to `output format`) — but only from what they actually reveal.
