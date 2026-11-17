---
title: "Remote Control should show current Codex session title and UUID"
status: open
priority: P1
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Session Title Freshness

## Problem

Remote Control currently shows:

```text
Untitled Codex session
<threadId>
```

That is acceptable only when the Codex thread truly has no title. The product contract is that the Remote Control page identifies the exact session by both user-facing title and UUID.

Parker expects rename/title state to make the target obvious. If a session has been renamed, the browser should show that title, not a stale title or generic fallback.

## Expected Behavior

Remote Control must always have a small top bar. This applies on mobile and desktop.

Header:

```text
<Codex session title>
<thread UUID>
```

Fallback only when no title exists:

```text
Untitled Codex session
<thread UUID>
```

If the session is renamed:

- next page load must show the new title,
- live title update is nice if App Server emits it, but not required before the next load,
- routing still uses UUID, never title.

Top bar behavior:

- The top bar stays anchored to the top of the Remote Control viewport.
- The chat transcript scrolls underneath the top bar.
- The bottom composer stays independent of the top bar.
- If the thread has a session name, show that title as the primary top-bar label.
- If the thread has no session name, show `Untitled Codex session` as the primary top-bar label.
- The thread UUID remains the routing identity and must be available from the top bar.
- On mobile, tapping the title area should reveal or toggle the UUID so Parker can confirm exactly which thread is attached.
- The top bar should be very small and functional. Do not turn it into a large page header or marketing surface.
- The top bar must not be removed as part of mobile chat cleanup.

## Likely Implementation

Use App Server thread metadata through the daemon:

- on attach or hydration, read the thread title/name from `thread/read`, `thread/resume`, or the loaded thread object,
- send it in the existing `session.attached` response or a new explicit metadata message,
- keep the browser header title primary and UUID secondary.

Do not guess by most-recent session.

Do not use title as a routing key unless the user explicitly supplied a unique title to the MCP launcher.

## Acceptance

- A thread with a title shows that title in the browser header.
- UUID remains visible below or beside the title.
- A truly untitled thread shows `Untitled Codex session`.
- Mobile has a small top bar even in the compact chat view.
- Tapping the mobile title area reveals or toggles the UUID.
- The top bar remains anchored at the top while transcript content scrolls underneath it.
- The top bar does not scroll away with chat messages.
- Refresh preserves correct title.
- Rename followed by reload shows the new title.
- The Remote Control URL remains `/codex-remote-control/<threadId>`.

## Non-Goals

- Do not build a session picker.
- Do not build an alias registry.
- Do not replace UUID routing with title routing.
