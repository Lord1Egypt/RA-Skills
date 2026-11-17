---
title: "Prepare clean Codex-only upstream branch or diff summary"
status: done
priority: P1
owner: Cody
repo: openai-codex-private / wip-ldm-os-private
created: 2026-05-06
---

# Remote Control Codex-Only Upstream Branch

## Problem

Remote Control co-presence is proven in WIP dogfood, but the OpenAI-facing artifact must be Codex-only.

The current working system spans several WIP components:

- patched WIP Codex;
- Remote Control daemon;
- hosted relay;
- Kaleidoscope browser UI;
- product tickets and security review notes.

That full product stack is not the upstream patch.

The upstreamable question is narrower:

```text
Can Codex App Server expose a stable peer-client surface for the live TUI thread?
```

Before opening an OpenAI PR, we need either:

- a clean Codex-only branch; or
- a clean diff summary if an issue should come first.

This artifact must not mix WIP relay code, Kaleidoscope UI code, private tickets, or product security notes into the Codex contribution.

## Scope

Prepare a Codex-only upstream-prep artifact that includes only the Codex-side pieces needed to explain or propose the integration surface.

Likely Codex-side pieces:

- TUI-owned App Server control socket or equivalent peer-client attachment point.
- External App Server client initialization over the live TUI-owned server.
- Live thread event fanout for multiple subscribers.
- MCP environment injection for current `CODEX_THREAD_ID` and `CODEX_THREAD_NAME`, if needed for the current-session tool path.
- Focused tests proving an external peer can initialize, resume the live thread, and receive events.
- Notes on any remaining limitations, such as one global socket or auth shape.

Explicitly exclude:

- WIP hosted relay implementation.
- WIP daemon protocol implementation.
- Kaleidoscope or browser UI code.
- iOS app plans.
- private product tickets.
- private security-review findings.
- WIP install and release pipeline details.

## Expected Output

Produce one of these artifacts:

1. Preferred: a clean branch in the Codex fork based on upstream `main`, containing only Codex-side changes.
2. Acceptable first step: a clean Markdown diff summary suitable for an OpenAI issue, with file-level Codex changes and tests.

The branch or summary should answer:

- What is the use case?
- Why App Server is the right integration layer.
- What currently prevents peer clients from using the live TUI thread.
- What the patch changes.
- What tests prove.
- What remains intentionally WIP-only.
- What question we want OpenAI to answer before a formal PR.

## Acceptance

- Artifact is based on upstream OpenAI Codex, not private fork `main`.
- Artifact contains only Codex-side changes or Codex-side summary.
- No `ai/` files are included.
- No WIP relay, daemon, Kaleidoscope, or iOS code is included.
- Tests or validation commands are listed.
- Known limitations are listed honestly.
- The artifact can be linked from an OpenAI issue without exposing private WIP product notes.
- The OpenAI-facing framing is "working proof plus request for intended direction," not "please merge the whole WIP product."

## Result

Prepared in:

```text
ai/product/plans-prds/codex-remote-control/2026-05-06--codex--openai-upstream-app-server-peer-client-packet.md
```

The packet identifies the clean Codex-only candidate branch:

```text
wipcomputer/openai-codex-private:cc-mini/app-server-multi-listener
```

It is based on `upstream/main`, has head commit `9c1f151193`, and the inspected diff touches only:

```text
codex-rs/app-server/src/request_processors/thread_lifecycle.rs
codex-rs/app-server/tests/suite/v2/connection_handling_websocket.rs
codex-rs/core/src/codex_thread.rs
```

The packet also records the separate current-thread MCP environment branches as optional follow-up, not part of the first App Server peer-client issue.

The clean OpenAI-facing issue draft is:

```text
ai/product/plans-prds/codex-remote-control/2026-05-06--codex--openai-app-server-peer-client-issue-draft.md
```

## Non-Goals

- Do not publish the issue before the architecture diagram and demo artifact are ready.
- Do not open an upstream PR before the branch has been reviewed for scope.
- Do not conflate PR #13 with the full upstream patch.
- Do not claim broad product readiness.
- Do not block WIP Remote Control dogfood on this upstream artifact.

## Related

- `2026-05-06--codex--remote-control-upstream-architecture-diagram.md`
- `2026-05-05--codex--wip-codex-fork-upstream-hygiene.md`
- `2026-05-05--codex--remote-control-patched-codex-install-path.md`
