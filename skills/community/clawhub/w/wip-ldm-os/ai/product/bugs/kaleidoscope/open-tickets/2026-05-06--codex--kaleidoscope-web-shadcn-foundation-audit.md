---
title: "Kaleidoscope web shadcn foundation should render components correctly by default"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-06
---

# Kaleidoscope Web Shadcn Foundation Audit

## Problem

Kaleidoscope web is starting to use shadcn-style UI references for Codex Remote Control and future WIP chat surfaces.

The baseline expectation is:

```text
If we use a shadcn/Radix component pattern correctly, it should render correctly out of the box.
```

If spacing, proportions, or component shape are wrong, the answer should not be repeated one-off class tweaking. It may mean Kaleidoscope's Tailwind/shadcn foundation is incomplete, mismatched, or being overridden.

This surfaced while trying to match a compact shadcn-style `Spinner + Updating` pill. The implementation kept drifting through local class changes even though the intended component shape should have been straightforward.

The loader bug is a symptom. The system question is:

```text
Does Kaleidoscope web have a valid shadcn-compatible styling foundation?
```

## Expected Behavior

Kaleidoscope web should support shadcn-style local components without every component needing manual rescue.

Baseline components should have correct spacing and proportions:

- Button;
- Badge;
- Spinner;
- Skeleton;
- Separator;
- Tooltip;
- Sheet or Dialog, if behavior primitives are added;
- simple status/loading pill built from Spinner plus local layout.

The app can and should use WIP visual identity, but the foundation should be coherent.

## Audit Checklist

Check the actual Kaleidoscope web app:

- Tailwind reset/preflight is active.
- Global CSS is imported once and in the right root layout.
- Tailwind v4 setup is coherent and not mixed with v3 assumptions.
- CSS variables and theme tokens exist where shadcn-style components expect them.
- `cn()` helper exists if shadcn-style components need class merging.
- `cn()` uses `clsx` and `tailwind-merge` or an equivalent local helper.
- `tailwind-merge` is current enough for the Tailwind version in use.
- Custom CSS lives in the right cascade layer and does not leak into component internals.
- Parent containers are not adding unexpected gap, padding, line-height, font-size, zoom, transform, or box constraints.
- Legacy global styles are not overriding button, span, div, p, h*, line-height, margin, padding, or box-sizing in ways that distort components.
- Radix portal components have a sane z-index/portal strategy if Dialog, Popover, Select, or Dropdown are added.

## Diagnostic Surface

Add a private/internal component reference surface if needed.

It can be a dev-only route, story page, or local test fixture that renders:

- Button variants;
- Badge variants;
- Spinner alone;
- Spinner plus compact status pill;
- Skeleton row/card placeholders;
- Separator;
- Tooltip or Dialog if installed.

The point is not to ship a public gallery. The point is to verify the foundation before polishing product surfaces.

## Acceptance

- The ticket has an implementation report that says whether Kaleidoscope's current Tailwind/shadcn foundation is valid.
- A minimal reference surface or equivalent screenshot evidence exists for baseline components.
- Baseline shadcn-style components render with sane default spacing and proportions.
- If a component renders incorrectly, the root cause is identified in one of:
  - Tailwind reset/preflight;
  - global CSS import;
  - Tailwind v4/v3 mismatch;
  - missing CSS variables;
  - missing or broken `cn()` helper;
  - class merge issue;
  - parent container distortion;
  - global CSS override;
  - portal/z-index issue.
- The compact loading/status pill matches the shadcn-style reference proportions without global component hacks.
- No global Badge variant is mutated to solve one local loading state.
- No product protocol, daemon, relay, or Codex App Server behavior changes.
- Codex Remote Control still passes the current smoke path after any foundation fix.

## Non-Goals

- Do not redesign Kaleidoscope.
- Do not implement the whole Remote Control UI pass here.
- Do not add Assistant Cloud, Vercel AI provider routing, hosted analytics, hosted auth, or third-party persistence.
- Do not create a shared React component package.
- Do not make WIP design guidance public.
- Do not keep hand-tuning individual components before proving the foundation.

## Related

- `ai/product/plans-prds/current/skills/2026-05-06--codex--wip-ai-chat-ui-skill.md`
- `ai/product/bugs/installer/2026-05-06--codex--ldm-install-wip-design-skills-all-surfaces.md`
- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-chat-ui-baseline.md`
- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-mobile-composer-safe-area.md`
