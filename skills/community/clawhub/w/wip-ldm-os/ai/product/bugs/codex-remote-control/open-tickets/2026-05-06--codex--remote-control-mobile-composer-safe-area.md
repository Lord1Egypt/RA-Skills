---
title: "Remote Control mobile composer must stay above browser chrome"
status: open
priority: P0
owner: Cody
repo: wip-ldm-os-private / kaleidoscope-private
created: 2026-05-06
---

# Remote Control Mobile Composer Safe Area

## Problem

The Remote Control mobile composer is too low on iPhone Safari and Chrome. The input and Send button can sit underneath or behind the browser bottom bar, which makes testing unreliable.

This is blocking dogfood. Parker cannot reliably type into the Remote Control page when the bottom input is partially hidden or the chat cannot scroll enough to expose it.

## Current Evidence

Observed on mobile browser screenshots from 2026-05-06:

- iPhone Safari shows the composer partly hidden behind the browser bottom toolbar.
- Chrome has the same bottom input risk.
- The message list does not leave enough scrollable bottom padding for the composer plus browser safe area.
- The composer should be locked above the browser bar, not pushed below the viewport.
- The chat should remain scrollable above the composer.

Related existing UI ticket:

- `2026-05-05--codex--remote-control-ui-cleanup.md`

This ticket is narrower and higher priority because it blocks mobile dogfood.

## Expected Behavior

Remote Control mobile layout must keep the composer usable at all times:

- input and Send button are always visible,
- composer is fixed or sticky to the bottom of the app viewport,
- composer sits above iOS Safari and Chrome bottom browser chrome,
- composer uses `env(safe-area-inset-bottom)` or equivalent safe-area handling,
- message list scrolls independently above the composer,
- final message can scroll above the composer instead of hiding behind it,
- keyboard open and keyboard closed states both remain usable.

## Visual Target

Use the existing Remote Control bottom composer style. This ticket is not a request to redesign the full chat UI.

- rounded message input,
- blue circular or rounded Send button,
- compact spacing,
- no desktop-style outer margins on the mobile composer,
- no extra footer or explanatory text,
- no new decorative treatment.

The mobile composer should be full-width for the phone layout, with only the small functional padding needed for the input, Send button, and safe area.

Unified visual polish can happen later after the core Remote Control flows are stable. Do not expand this ticket into a broader style pass.

## Likely Implementation

Fix the mobile viewport and layout contract:

- use a real app-height variable or dynamic viewport unit such as `100dvh`,
- reserve bottom space for composer height plus safe-area inset,
- keep the transcript container scrollable with bottom padding matching composer height,
- position composer with `bottom: env(safe-area-inset-bottom)` or equivalent,
- avoid desktop-style fixed-width margins on the mobile bottom composer,
- test both iPhone Safari and iPhone Chrome.

Be careful with iOS browser behavior: `100vh` can include hidden or visible browser chrome in ways that place fixed elements too low.

## Acceptance

- On iPhone Safari, input and Send button are fully visible with keyboard closed.
- On iPhone Chrome, input and Send button are fully visible with keyboard closed.
- With the keyboard open, the input remains reachable and typing works.
- The message list scrolls behind or above the composer without hiding the latest messages.
- The bottom of the transcript has enough padding that the final `turn complete` or final chat bubble can be scrolled above the composer.
- The composer never overlaps the iOS browser bottom bar.
- The composer keeps the existing bottom input style, but spans the mobile width appropriately.
- Desktop layout remains usable.

## Non-Goals

- Do not solve transcript hydration here.
- Do not solve raw event rendering here.
- Do not solve model/status-line metadata here.
- Do not do a unified visual redesign here.
- Do not touch relay, daemon, App Server, E2EE, or security logic.
