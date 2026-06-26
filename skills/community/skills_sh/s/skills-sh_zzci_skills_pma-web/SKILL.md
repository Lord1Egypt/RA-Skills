---
name: pma-web
description: Frontend implementation guide for PMA-managed React 19 + TypeScript + Vite 8 SPA projects. Defaults to a single-app layout (the right choice for a Rust/Go service that ships a UI); promotes to a Bun monorepo only when multiple apps or shared packages exist. UI is hard-locked to shadcn/ui (base-nova) + `@base-ui/react` — Radix and other UI ecosystems (MUI / Mantine / Chakra / Ant Design / Headless UI / Ariakit / NextUI / …) are forbidden. Covers required quality gates, file-based type-safe routing with TanStack Router, state conventions (TanStack Query + Zustand), Tailwind CSS v4 patterns, Vitest 4 testing, dual-channel theming, i18n, nsl-based dev integration with backend services, and delivery rules for frontend applications. Use when implementing, scaffolding, or reviewing a React/Vite SPA or internal-tool frontend in a PMA repo.
---

# Web Frontend Implementation Guide

Use this skill together with `/pma`. `/pma` controls workflow, approval, and task tracking; this guide defines the implementation baseline after work is approved.

Keep this entry file lean. Load only the reference packs needed for the current task.

## Scope

For PMA-managed SPA and internal-tool frontend projects using:

- React 19 + TypeScript + Vite 8
- TanStack Router for file-based type-safe routing
- TanStack Query for server state
- Zustand for UI-only client state
- shadcn/ui (base-nova style) with `@base-ui/react` primitives and Tailwind CSS v4 — this is the **only** allowed UI ecosystem; Radix UI and other component libraries are forbidden (see `references/baseline.md` *UI Library Policy*)

Single-app layout is the default. Reach for a Bun monorepo only when the repo really hosts multiple apps or shared packages — a single SPA bolted onto a Rust or Go service does not need workspaces.

Not for SSR-first sites, content sites, or non-PMA projects.

## Loading Order

1. Always load `references/baseline.md` first.
2. Load `references/routing-and-ui.md` when touching route structure, providers, theming, Tailwind, or shadcn/ui.
3. Load `references/runtime-and-data.md` when touching API integration, query state, i18n, Vite config, or the frontend-side dev script. For the full nsl protocol (registration patterns, `--strip`, `NSL_PORT`, fallback) load `/pma references/dev-environment.md`.
4. Load `references/review.md` when touching release checks, tests, accessibility, or security-sensitive UI behavior.

## Quick Routing

- New app setup or repo restructuring (single-app vs monorepo): `references/baseline.md`
- Router, layouts, providers, entrypoint, shadcn, Tailwind, theme: `references/routing-and-ui.md`
- HTTP client, query client, i18n, Vite config, frontend nsl invocation: `references/runtime-and-data.md` (full nsl protocol → `/pma references/dev-environment.md`)
- Lint, typecheck, build, test, accessibility, UI security review: `references/review.md`

## Reference Packs

- `references/baseline.md`
  Stack defaults, quality gates, workspace layout, conventions, and baseline scripts.
- `references/routing-and-ui.md`
  TanStack Router layout, provider composition, entry point, shadcn/ui, Tailwind v4, and theming.
- `references/runtime-and-data.md`
  Query client, HTTP layer, state boundaries, i18n, Vite config, and the frontend-side nsl invocation. Full nsl protocol lives in `/pma references/dev-environment.md`.
- `references/review.md`
  Verification gates and the accessibility and security review checklist for UI changes.

If the project intentionally diverges from these defaults, keep the divergence explicit in the proposal and match the repository's existing patterns consistently.
