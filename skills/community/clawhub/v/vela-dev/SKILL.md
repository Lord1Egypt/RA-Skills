---
name: vela-dev
description: Build, edit, debug, and package Xiaomi Vela JS quick apps for wearable devices such as Xiaomi Band 10. Use when the user asks to create a Vela 快应用, modify `.ux` pages, fix `npx aiot build` errors, adapt UI for 手环屏幕, or package/send `.rpk` apps. Covers project scaffolding, manifest/app/config creation, Vela component/event/style constraints, and iterative build-debug loops.
---

# Vela Dev

Use this skill when working on Xiaomi Vela JS wearable quick apps.

## What this skill is for

- Create a new Vela quick app from scratch
- Edit existing `.ux` pages
- Fix build errors from `npx aiot build`
- Adapt UI for Xiaomi Band / Watch screens
- Package an `.rpk` for delivery

## Workflow

1. Identify whether the user wants a **new app** or edits to an **existing Vela project**.
2. If new, scaffold the minimum required files:
   - `src/manifest.json`
   - `src/app.ux`
   - `src/config-watch.json`
   - at least one page like `src/pages/<name>/index.ux`
3. Prefer a **single-page app with internal state switching** unless the app clearly benefits from router-based multi-page navigation.
4. Build with:
   - `cd <project> && npx aiot build`
5. If build fails, inspect the exact error and patch surgically.
6. Only send/package the `.rpk` after a successful build.

## Xiaomi Band / Vela constraints

Read `references/vela-notes.md` when you need practical constraints and common fixes.

Important defaults:
- Xiaomi Band 10 uses a **212x520 跑道屏** style layout.
- Frontend apps should feel **foreground-first**: quick open, quick action, quick exit.
- Avoid overstuffed home screens. Prefer vertical lists/cards.
- Symbol glyph buttons like `↺` `⏸` `▶` `⏭` may not render reliably on device; prefer plain Chinese text.
- When in doubt, choose larger touch targets and fewer simultaneous actions.

## Build/debug loop

After each meaningful edit:
- Run `npx aiot build`
- If needed, filter logs with grep for `success|error|Error`
- Fix the reported file/line first before changing anything else

Common failure classes are documented in `references/vela-notes.md`.

## Event/style rules

Read `references/ux-gotchas.md` when build errors point to template/event/CSS issues.

Key reminders:
- Vela event handlers are strict; avoid unsupported template expression forms in `onclick`
- Broken CSS blocks can produce `UxLoader` / `Unexpected }`
- Prefer simple, explicit structure over clever templating

## Project template

If the user asks for a fresh app, copy or adapt files from `assets/template/`.

## Deliverables

Typical successful output includes:
- working project folder
- successful `npx aiot build`
- generated `.rpk` path from `dist/`

## When to read extra files

- For practical Vela constraints and prior lessons: read `references/vela-notes.md`
- For template/event/style pitfalls: read `references/ux-gotchas.md`
- For official documentation entry points and what to consult: read `references/docs-map.md`
- For a reusable end-to-end implementation/debug loop: read `references/dev-workflow.md`
- For fresh project scaffolding: inspect `assets/template/`

## Documentation-backed behavior

When you need authoritative confirmation:
1. Start with `references/docs-map.md`
2. Open the matching official doc page
3. Apply the smallest viable change
4. Rebuild immediately

Prefer official docs for:
- component capability questions
- feature API availability
- project structure uncertainty
- framework/lifecycle questions

Prefer local reference notes for:
- previously observed build pitfalls
- Band 10-specific practical constraints
- project patterns that already worked here
