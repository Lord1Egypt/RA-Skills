# Framework & Library Verification

Mandatory pre-audit step: confirm exact versions in use and check them against current official documentation, every audit, before diagnosing or fixing anything. This exists because a fix that's correct for one major version of a library can be actively wrong, deprecated, or unidiomatic for another — and library best practices shift often enough that memory/training data should not be trusted as current.

## 1. Identify exact versions first

Read the project's manifest and lockfile, not just the manifest's version *range*:

- `package.json` dependencies show a requested range (e.g. `"tailwindcss": "^4.0.0"`); the **lockfile** (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) shows the actually-installed version. Always check the lockfile — a project can be "on Tailwind 4" per package.json but still resolve to an early patch version with different behavior.
- Note the exact version for: CSS framework (Tailwind, etc.), UI component kit (shadcn/ui, Radix, MUI, etc.), the frontend framework itself (React/Next/Vue/Svelte), and any state-management library in use.

## 2. Search official docs for that specific version, not "the library" in general

- Query pattern: `"<library name> <exact major.minor version> docs"` or `"<library name> changelog <version>"` — specific enough to land on the right version's documentation, not a generic marketing page.
- For libraries with major breaking changes between versions (Tailwind's config approach changed substantially across major versions; component libraries frequently rename props or restructure APIs), explicitly check whether the pattern you're about to recommend or use in a fix is the current-version idiom or a carried-over pattern from an older version that happens to still compile/run without error (silently-working-but-deprecated is the dangerous case, not the one that throws an error).
- Check the library's official changelog/release notes for the versions between what's likely in training data and what's actually installed, if there's a gap — don't assume nothing relevant changed just because the API surface looks similar.

## 3. What to do when docs and installed behavior disagree

- If the project's code uses a pattern that current official docs mark deprecated (but not yet removed) — flag it in the audit report as a forward-compatibility risk, and prefer the current-recommended pattern in the fix, unless doing so would require a larger migration than the reported bug warrants (in that case, fix the immediate bug with the existing pattern, but explicitly note the deprecation for a separate follow-up rather than silently ignoring it).
- If official docs are ambiguous or the search doesn't turn up a clear current answer, say so plainly in the audit report rather than presenting a guess as verified — this keeps the audit trustworthy.

## 4. Cache and HMR staleness — check before re-diagnosing a fix that "didn't work"

Before concluding a fix is wrong and iterating again, rule out that you're looking at stale output — this is a distinct failure mode from an incorrect fix, and confusing the two wastes cycles (see `references/common-bug-signatures.md`, signature #1 and #4).

- **Vite**: HMR generally handles component edits well, but changes to `vite.config.*`, `tailwind.config.*`, PostCSS config, or environment files often require a full dev-server restart to take effect — HMR silently not picking these up looks identical to "the fix didn't work." If a fix touches any config file, restart the dev server before judging the result.
- **Next.js**: check `.next/` cache staleness after config or dependency changes — `rm -rf .next` followed by a fresh `next dev` (or `next build`) is a legitimate diagnostic step. Also distinguish dev-mode-only artifacts (React strict-mode double-invoking effects, more verbose hydration warnings) from actual bugs — a warning that only appears in dev mode isn't necessarily the root cause of a production-visible bug.
- **Tailwind (v3 content-scanning / v4 auto-detection)**: a class that's dynamically constructed in code (e.g. `` `text-${color}-500` ``) is invisible to Tailwind's static analysis and gets purged even though it's "correct" in source — this looks exactly like "the style didn't apply" but is actually a class-detection issue, not a CSS specificity or logic bug. Check whether any newly-added class is built dynamically before assuming the fix itself is wrong.
- **Browser cache**: for CSS/asset changes verified via a manually-refreshed browser tab, rule out a stale cached stylesheet with a hard refresh before concluding a fix failed.

## 5. Efficiency note

Not every audit needs to re-verify every library from scratch if a very recent verification (same conversation, same versions) already happened — but do re-verify whenever: the library/version wasn't checked yet in this session, meaningful time has passed, or the fix being considered touches an area (config format, breaking-change-prone API) where version sensitivity is high. When in doubt, check — a stale assumption here produces confidently-wrong fixes, which is worse than a moment's extra search.
