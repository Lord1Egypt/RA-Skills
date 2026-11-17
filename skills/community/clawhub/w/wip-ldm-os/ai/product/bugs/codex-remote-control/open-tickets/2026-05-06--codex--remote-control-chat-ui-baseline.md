---
title: "Remote Control Chat UI Baseline From Assistant UI Patterns"
status: open
priority: P1
owner: Cody
repo: kaleidoscope-private
created: 2026-05-06
---

# Remote Control Chat UI Baseline From Assistant UI Patterns

## Problem

Remote Control now works well enough that the remaining web UI work should stop being hand-recreated from screenshots.

The page is a modern AI chat surface:

- transcript history;
- user messages;
- streaming assistant messages;
- composer;
- mobile safe area;
- Stop while running;
- reconnect and hydration;
- lightweight status diagnostics.

These are solved UI patterns in the React + Next.js + Tailwind + TypeScript ecosystem. We should use those patterns as references while preserving WIP's own Remote Control backend and security model.

## Decision

Use assistant-ui/shadcn-style chat interfaces as the primary behavior reference for Remote Control web.

Use Vercel Chatbot as a secondary structure reference for Next.js + React + TypeScript + Tailwind project patterns.

Build WIP's own frontend and backend. Do not adopt their backend, provider, hosted services, analytics, auth, persistence, or AI SDK model-call path.

Remote Control's backend remains:

```text
browser -> hosted relay -> local daemon -> Codex App Server -> live Codex TUI thread
```

The UI reference stack is compatible with our current web stack:

```text
React + Next.js + Tailwind + TypeScript
```

assistant-ui/shadcn patterns can be used in a Next.js app. Vercel Chatbot is also a Next.js app. They are compatible references. The question is not "which backend do we copy?" The question is "which chat UI behaviors and component patterns teach us what users expect?"

The product decision is to build our own implementation. Templates and component libraries are references, not dependencies that define the product.

## References

- assistant-ui shadcn template: `https://www.shadcn.io/template/assistant-ui-assistant-ui`
- Vercel Chatbot template: `https://vercel.com/templates/next.js/chatbot`
- Vercel Chatbot repo: `https://github.com/vercel/chatbot`
- assistant-ui repo: `https://github.com/assistant-ui/assistant-ui`

Important distinction:

- Official shadcn/ui style means copy-owned component code in our repo.
- `shadcn.io` is a separate paid service on top of the ecosystem. We should not depend on paying for it or routing development through it. It can be useful as a public catalog reference, but it must not become runtime product infrastructure or a required development dependency.

## Expected Behavior

Remote Control web should behave like a production chat client:

- Composer is anchored and comfortable on desktop and mobile.
- Mobile safe area is respected in Safari and Chrome.
- Return behavior matches platform expectations.
- Send button is explicit on mobile.
- Stop button replaces or accompanies send while a turn is running.
- Transcript scroll behavior is stable.
- History hydration and live streaming hand off without duplicates.
- User messages render once as user bubbles.
- Codex output renders as assistant messages.
- Status diagnostics are visually secondary.
- Raw protocol JSON is hidden outside debug mode.
- Markdown/code output is readable when present.
- Accessibility and keyboard behavior are not afterthoughts.

## Implementation Boundary

Allowed:

- Read assistant-ui and Vercel Chatbot patterns.
- Adapt lessons from component structure, state handling, composer behavior, scroll behavior, and visual hierarchy.
- Use shadcn-style copy-owned components if reviewed and committed into our repo.
- Keep the existing `kaleidoscope-private` Next.js app.
- Add focused UI dependencies only after explicit review.

Not allowed:

- Do not adopt Vercel AI SDK provider routing.
- Do not send Remote Control messages through a model provider API from the web app.
- Do not add Vercel-hosted storage, analytics, auth, or gateway services.
- Do not make `shadcn.io` or any third-party service a runtime dependency.
- Do not load third-party scripts, fonts, analytics, or CDN assets in the Remote Control page.
- Do not change the relay, E2EE, daemon, or App Server protocol as part of this UI baseline.
- Do not require a paid third-party UI catalog or MCP subscription to build or maintain the product.

## Relationship To Existing Tickets

This ticket is the baseline/reference decision for the broader UI pass.

Related implementation tickets:

- `2026-05-05--codex--remote-control-ui-cleanup.md`
- `2026-05-05--codex--remote-control-web-transcript-fidelity.md`
- `2026-05-05--codex--remote-control-app-server-event-rendering.md`
- `2026-05-05--codex--remote-control-web-status-line.md`
- `2026-05-06--codex--remote-control-mobile-composer-safe-area.md`
- `2026-05-05--codex--remote-control-refresh-hydration.md`
- `2026-05-05--codex--remote-control-stop-shared-state.md`

This ticket should guide those fixes. It should not replace their acceptance criteria.

## Acceptance

- Remote Control web UI has a named baseline: assistant-ui/shadcn-style chat behavior.
- Vercel Chatbot is documented as a structure reference, not a backend reference.
- The implementation keeps WIP's Remote Control protocol intact.
- The implementation is WIP-owned: backend, protocol, and product-specific frontend state remain ours.
- The normal page loads only first-party runtime assets.
- User, assistant, status, streaming, Stop, hydration, and mobile composer behavior are aligned with modern AI chat interfaces.
- Existing co-presence remains green:
  - browser to TUI;
  - TUI to browser;
  - multi-browser fanout;
  - refresh/rejoin;
  - Stop scoped to the attached thread.

## Non-Goals

- Do not implement the UI pass in this ticket.
- Do not install `shadcn.io` MCP in this ticket.
- Do not make `shadcn.io` MCP or any paid UI catalog a required workflow.
- Do not choose a new backend.
- Do not migrate away from Next.js in this ticket.
- Do not move wallet, token custody, or password-like secrets into the web app.
