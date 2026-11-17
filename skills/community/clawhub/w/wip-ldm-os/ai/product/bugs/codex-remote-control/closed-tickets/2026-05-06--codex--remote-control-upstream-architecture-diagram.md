---
title: "Create OpenAI-facing Remote Control architecture diagram"
status: done
priority: P1
owner: Kay
repo: wip-ldm-os-private / openai-codex-private
created: 2026-05-06
---

# Remote Control Upstream Architecture Diagram

## Problem

Remote Control co-presence now works end to end, but the upstream story needs one clean diagram before opening an OpenAI issue.

The important point is not "WIP built a phone UI." The important point is:

```text
Codex App Server is the right shared surface for peer clients that need to attach to the live TUI thread.
```

Without a diagram, the story can be confused with:

- a second Codex runner;
- rollout-file polling;
- direct SQLite/session-index mutation;
- hosted relay authority over Codex state;
- a WIP product request instead of a Codex App Server integration question.

The diagram should make the trust and ownership boundaries visible in 10 seconds.

## Desired Diagram

Create one OpenAI-facing architecture diagram with this shape:

```text
Codex TUI
   |
   v
Codex App Server
   |
   v
WIP daemon
   |
   v
WIP relay
   |
   v
browser / iOS client
```

The diagram must annotate:

- Codex runs locally on the user's machine.
- The TUI and daemon attach to the same live App Server thread.
- The daemon is a peer client, not a second Codex runner.
- The relay transports encrypted frames, but is not the authority over Codex runtime state.
- The browser or iOS client mirrors the Codex thread, not terminal pixels.
- The Codex-side patch lives at the App Server and live event fanout layer.
- WIP-specific hosted relay and app UI are outside the proposed OpenAI surface.

## Acceptance

- A diagram artifact exists in the Remote Control product docs or upstream-prep docs.
- The diagram shows `TUI -> App Server -> daemon -> relay -> browser`.
- The diagram labels Codex-owned components separately from WIP-owned components.
- The diagram labels local trust boundary versus hosted relay boundary.
- The diagram makes clear that App Server is the proposed upstream integration surface.
- The diagram does not include private implementation details, internal ticket names, or security-review notes.
- The diagram is suitable to attach or link from an OpenAI issue.
- The diagram can be understood without reading the full Remote Control product docs.

## Result

Prepared in:

```text
ai/product/plans-prds/codex-remote-control/2026-05-06--codex--openai-upstream-app-server-peer-client-packet.md
```

The packet includes a Mermaid diagram with Codex-owned and WIP-owned boundaries, local runtime versus hosted transport boundaries, and issue-ready wording that frames App Server as the proposed peer-client surface.

The clean OpenAI-facing issue draft is:

```text
ai/product/plans-prds/codex-remote-control/2026-05-06--codex--openai-app-server-peer-client-issue-draft.md
```

## Non-Goals

- Do not document every WIP relay endpoint.
- Do not document Kaleidoscope implementation details.
- Do not imply OpenAI should adopt WIP's hosted relay.
- Do not include private repo paths or private ticket references.
- Do not include speculative iOS app architecture.

## Related

- `2026-05-05--codex--wip-codex-fork-upstream-hygiene.md`
- `2026-05-05--codex--remote-control-app-server-spike.md`
- `2026-05-05--codex--remote-control-regression-contract.md`
