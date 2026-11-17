---
name: ui-doctor
description: Audits an existing app's UI for consistency and layout/state-sync bugs (e.g. a sidebar that collapses but siblings don't adjust, or icons disappearing entirely instead of just their labels), responsive breakpoint failures, accessibility gaps, performance issues, and — for chat/workspace apps — message bubble, markdown/table/code-block rendering, and input control quality — then fixes them in code with evidence-based verification (not assumed-working fixes). Always verifies the project's actual installed library versions against current official docs, and checks for build/dev-server cache staleness before re-diagnosing a fix that "didn't work." Trigger when the user reports UI that "looks off," components out of sync, layout breaking at certain sizes, a fix that doesn't seem to have taken effect, or asks for a UI audit/review/health-check. For designing a new system from scratch, use `design-system-architect` instead (this skill uses its state-matrix/token definitions as audit criteria when present).
---

# UI Doctor

A diagnostic and repair skill for UI that has already been built but doesn't hold together — components that don't stay synchronized (the classic case: sidebar collapses, but the main content area doesn't resize because it isn't reading the same state), layouts that break at certain widths, accessibility gaps, and performance problems. This is not a design-creation skill — it examines existing code, finds root causes, and fixes them.

## Relationship to your other UI skills

- **`design-system-architect`**: defines what "correct" looks like (token system, component state matrix, breakpoint/mode strategy) *before* or *during* building. If that skill's output exists in the project (e.g. a documented state matrix or token file), `ui-doctor` audits against it directly instead of inventing its own standard.
- **`frontend-design` / `frontend-design-mega`**: govern aesthetic direction and style catalog. `ui-doctor` does not second-guess visual style choices — it only flags structural/functional/consistency problems, not "this color is boring."

If none of the above exist in the project yet, `ui-doctor` still works — it falls back to general industry standards (see `references/audit-checklist.md`) rather than requiring them as a prerequisite.

## Process

### Step 1 — Identify the actual stack and versions (mandatory, every audit)

Before diagnosing anything, read the project's dependency manifest (`package.json` + lockfile, or equivalent) to find the **exact installed versions** of the relevant libraries (Tailwind, React/Next/Vue, the component kit, state management library). Never assume a version from memory.

### Step 2 — Verify current official docs for those exact versions (mandatory, every audit)

For every library identified in Step 1, web-search and check the current official documentation/changelog for that version — do this every time, not from cached knowledge, since APIs and recommended patterns shift between versions (e.g. Tailwind's config approach changed substantially between major versions; a fix that's correct for one version can be actively wrong or deprecated for another). Read `references/framework-verification.md` for how to do this efficiently without re-verifying things that haven't changed. Cite what you find when it affects a diagnosis or fix (per normal citation rules — paraphrase, don't quote docs verbatim beyond short fragments).

### Step 3 — Reproduce and localize the reported symptom

For a reported bug (e.g. "sidebar collapses but sibling doesn't adjust"), don't just patch the symptom you're told about — find the **shared state boundary** that's broken. Read `references/layout-state-sync.md` first: state-synchronization bugs are almost always a "duplicate source of truth" problem (two components each holding their own copy of what should be one shared value), not a CSS problem, even though they present visually. Also check `references/common-bug-signatures.md` — many reported symptoms match one of a small set of recurring patterns (element disappearing instead of just its label, a child sizing fix neutralized by an unfixed parent, a fix that didn't actually take effect due to cache staleness), and recognizing the pattern is faster than re-deriving root cause from first principles every time.

### Step 4 — Run the full audit checklist

Read `references/audit-checklist.md` and go through every category even if the user only reported one symptom — the reported bug is often a symptom of a broader pattern (e.g. if the sidebar has a duplicate-state bug, other collapsible/toggleable components in the same codebase likely share the same anti-pattern). Categories: layout & state synchronization, responsive breakpoint behavior, accessibility (WCAG 2.2 AA), and performance.

### Step 5 — Fix directly, with root-cause framing

Since the fix-mode here is auto-fix (not report-only):
- Fix the root cause (the broken shared-state boundary), not just the visible symptom — a patch that hides the symptom at one breakpoint without fixing the underlying state model will resurface elsewhere.
- Explain, briefly, *why* it was broken (one or two sentences: "the sidebar width was tracked as separate local state in two components instead of one shared source") before showing the fix — this is what makes the fix trustworthy rather than a black-box patch.
- Preserve the project's existing token/state-matrix conventions if `design-system-architect` output exists; don't introduce a parallel styling approach.

### Step 6 — Verify with evidence, not by assuming the fix took effect

This is the step most likely to be skipped under time pressure, and skipping it is the single most common cause of "I fixed it" turning out to be false. Do not declare a fix verified based on reasoning about what the code *should* do — confirm it with concrete evidence:

- **Re-read the actual file after editing it** (not from memory of what you just wrote) to confirm the change is present exactly where expected, and that no other rule in the cascade overrides it (check for a more specific selector, a later-loaded stylesheet, or a conflicting utility class still present alongside the new one).
- **Trace the full property chain for layout fixes**: if the fix is "make main content full-width," verify every ancestor from the element up to the layout root doesn't have a competing fixed-width, `max-width`, or `inline-block`/`inline-flex` sizing that would constrain it regardless of the child's own `flex-grow`/`w-full`. A child fix is neutralized by an unfixed parent constraint — this exact failure mode (fix applied to the wrong level of the tree) is extremely common and easy to miss by inspecting only the component that was reported broken.
- **Check for build/dev-server cache staleness** before concluding a fix didn't work or re-diagnosing from scratch: see `references/framework-verification.md` for cache/HMR gotchas per tool (Vite, Next.js, Tailwind JIT). A correct fix that isn't visible yet is a different problem than an incorrect fix, and misdiagnosing one as the other wastes the next several iterations.
- **State exactly what changed**: file path, the specific property/selector/state variable, old value → new value. A fix report that only describes the symptom fixed ("sidebar now works") without naming the concrete code change is not verifiable by the user and is a sign the fix itself may not have been precisely targeted.
- Walk through every breakpoint, state (open/closed, loading/error/empty), and light/dark mode if applicable — a fix verified only in the exact scenario reported is not fully verified.

If, after this, you cannot produce concrete evidence the fix took effect — say so plainly rather than reporting success. Read `references/common-bug-signatures.md` for a catalog of exact failure patterns (including "fix applied but symptom unchanged") worth checking against.

### Step 6.5 — Conversational/chat UI audit (when applicable)

If the app under audit is a chat/agent/workspace interface, also read `references/conversational-ui-audit.md` and audit message bubbles, markdown/table/code-block rendering, and the chat input control against it — these have their own recurring failure patterns distinct from general layout/state bugs (e.g. markdown tables rendering as literal pipe-and-dash text, code blocks with no copy affordance, an input control that doesn't auto-resize or communicate its own states). Skip this step for non-chat apps.

### Step 7 — Report

Summarize findings as a short audit report: what was broken (root cause, not just symptom), what else was found while auditing broadly, what was fixed, and anything flagged but not auto-fixed (e.g. something needing a design decision from the user rather than a pure bug fix).
