---
title: "Kaleidoscope shadcn/Radix foundation audit"
status: open
priority: P0
owner: Cody
repo: kaleidoscope-private
created: 2026-05-06
---

# Kaleidoscope Shadcn/Radix Foundation Audit

## Problem

Remote Control UI work is starting to use shadcn/Radix-style component references. That is the right direction, but shadcn-style components should render with correct spacing, shape, and proportions out of the box inside Kaleidoscope.

If a semantically correct component or pattern looks wrong, we should not keep hand-tuning each instance. That usually means the app foundation is incomplete, mismatched, or being overridden:

- Tailwind reset/preflight is not active or is loaded in the wrong order.
- Global CSS is missing, duplicated, or imported from the wrong root.
- Required shadcn CSS variables/tokens are absent.
- Tailwind v4 setup is being treated like Tailwind v3.
- `cn()` / `clsx` / `tailwind-merge` is missing or not wired.
- Component variants are ad hoc instead of predictable.
- Parent containers are adding layout, font, line-height, padding, transform, or zoom styles that distort primitives.
- Legacy global CSS is overriding spacing, borders, or line-height.

This has already shown up during the Remote Control loader work. The center `Syncing` state was being hand-tuned while trying to match a shadcn spinner-badge reference. That debugging loop should become a foundation audit, not repeated one-off visual edits.

## Current Evidence

Observed in `kaleidoscope-private` during Remote Control UI dogfood:

- `web/src/app/globals.css` imports Tailwind v4 with `@import "tailwindcss";`.
- `web/src/app/layout.tsx` imports `./globals.css`.
- Only minimal theme variables are defined today: `--background` and `--foreground`.
- No normal shadcn token set is present yet, such as `--border`, `--input`, `--ring`, `--muted`, `--muted-foreground`, `--primary`, or `--secondary`.
- No shared `cn()` helper was found for shadcn-style components.
- No `clsx` / `tailwind-merge` setup was found in the app package.
- Local Remote Control primitives currently include `Skeleton` and `Spinner`, but they are not backed by a documented component foundation.
- Remote Control has a large amount of inline style layout, which may hide or distort component defaults when shadcn-style primitives are introduced.

This does not mean the existing Remote Control page is wrong. It means the app is not yet clearly shadcn-compatible, so shadcn-referenced components may render differently than the docs or examples.

## Principle

Do not hand-tune every shadcn-style component until it looks right.

Fix the app's design-system foundation so shadcn-style primitives render correctly by default.

Use shadcn/Radix as component and behavior references, but keep all runtime code first-party and committed locally unless a dependency is explicitly reviewed.

## Scope

Audit and normalize the foundation needed for shadcn/Radix-style components in Kaleidoscope:

- Tailwind v4 setup;
- preflight/reset behavior;
- global CSS import order;
- shadcn-compatible CSS variables and tokens;
- local `cn()` helper using `clsx` and `tailwind-merge`, if dependencies are approved;
- local component primitive structure;
- variant conventions;
- parent layout rules that distort primitives;
- legacy global CSS overrides.

## Expected Work

1. Inspect the live and source CSS pipeline:
   - `globals.css`;
   - `layout.tsx`;
   - Tailwind v4 config or CSS-first setup;
   - PostCSS config;
   - any legacy global CSS files;
   - component import paths.
2. Create a small internal component demo or test surface that renders a minimal primitive set:
   - Button;
   - Badge;
   - Spinner;
   - Skeleton;
   - Separator.
3. Compare rendered spacing and proportions against shadcn reference behavior.
4. Inspect computed styles for incorrect spacing:
   - font-size;
   - line-height;
   - padding;
   - gap;
   - height;
   - box-sizing;
   - border;
   - background;
   - parent font and layout styles.
5. Fix the foundation before tuning individual Remote Control components.
6. Document the local shadcn-style rules for Kaleidoscope components.

## Acceptance

- Tailwind preflight/reset behavior is verified active in Kaleidoscope.
- Global CSS is imported once at the correct root.
- Tailwind v4 setup is documented and coherent.
- shadcn-compatible CSS variables/tokens exist for the primitives we use, or the ticket explicitly documents why a token is intentionally omitted.
- A local `cn()` helper exists and works with `clsx` + `tailwind-merge`, or the ticket explicitly documents the approved alternative.
- A minimal internal component demo/test surface renders Button, Badge, Spinner, Skeleton, and Separator.
- Those primitives render with expected spacing and proportions without per-instance hacks.
- Parent layout and legacy global CSS rules that distort component spacing are identified and fixed or documented.
- Remote Control can use those primitives without re-debugging the Tailwind/shadcn foundation every time.

## Non-Goals

- Do not redesign Remote Control in this ticket.
- Do not change Remote Control relay, daemon, E2EE, App Server, or thread routing behavior.
- Do not install a paid UI catalog or make `shadcn.io` a runtime dependency.
- Do not add third-party scripts, fonts, analytics, or CDN assets.
- Do not migrate the app away from Next.js, React, TypeScript, or Tailwind.
- Do not use this ticket to solve transcript hydration, Stop state, or mobile safe-area behavior.

## Related Tickets

- `2026-05-06--codex--remote-control-chat-ui-baseline.md`
- `2026-05-05--codex--remote-control-ui-cleanup.md`
- `2026-05-05--codex--remote-control-web-transcript-fidelity.md`
- `2026-05-05--codex--remote-control-web-status-line.md`
- `2026-05-06--codex--remote-control-mobile-composer-safe-area.md`
