---
title: "Align .github-private org profile with Speedrun agent-readable thesis"
status: open
priority: P0
owner: unassigned
repo: .github-private
created: 2026-05-17
---

# Align .github-private Org Profile With Speedrun Agent-Readable Thesis

## Problem

The Speedrun application is making a direct claim that WIP Computer can be inspected by agents:

```text
Point your own AI at https://wip.computer and https://github.com/wipcomputer, then ask what WIP Computer does.
The fact that the application can verify itself is part of the product thesis.
```

That claim only works if the public GitHub org profile returns the same story as the application when a reviewer or their AI reads it.

The current `.github-private/profile/README.md` is useful as an inventory, but it is too much of a component catalog for this moment. It opens with older wording:

```text
We build AI agent infrastructure. Identity, memory, sovereignty.
```

It then lists many tools, deprecated repos, unreleased components, utilities, and project-contributor notes before the reader gets a crisp answer to what WIP Computer is building now.

For Speedrun, the org profile needs to act as a map, not a museum.

## Desired Outcome

Update `.github-private` so `https://github.com/wipcomputer` is aligned with the application and the new public homepage.

The canonical thesis for this surface:

```text
WIP Computer gives people one portable memory, persistent identity, and human-in-the-loop permission layer across every AI they use.
```

The profile should make the core problem obvious:

- every major AI company is building its own agent universe;
- none of those universes are connected;
- people still copy-paste context between tools;
- memory, identity, permission, and agent coordination are fragmented;
- WIP Computer is building the connective layer.

## Required Changes

### 1. Rewrite the org profile README top section

Target file:

```text
/Users/lesa/wipcomputerinc/repos/wip-web/.github-private/profile/README.md
```

Recommended shape:

```markdown
# WIP Computer

We build the memory, identity, and permission layer for AI agents.

Every major AI company is building its own agent universe. None of them are connected. People copy-paste context between tools, lose memory every session, and reauthorize the same trust decisions everywhere.

WIP Computer is building the missing layer: portable memory, persistent identity, agent-to-agent coordination, and human-in-the-loop control across every AI a person uses.

## What to inspect first

- **LDM OS**: operating layer for AI agents. Identity, memory, Bridge, extensions, and boot sequence.
- **Memory Crystal**: cross-session, cross-harness, cross-model AI memory.
- **Codex Remote Control**: drive local Codex CLI sessions from your phone, including local-model workflows.
- **Dream Weaver Protocol**: memory consolidation for agents with bounded context.
- **WIP AI DevOps Toolbox**: release, license, repo, and safety tools for AI-native software teams.

The repo set is meant to be inspectable by humans and AI agents. Point any AI at this org and ask what WIP Computer does.
```

Keep the profile short. Do not reproduce the full component catalog above the fold.

### 2. Do not add a scripted AI-inspection prompt

Do not add a block like:

```markdown
## For AI agents

Answer these questions...
```

The Speedrun claim is stronger if an evaluating AI can inspect the org naturally and synthesize the answer. A founder-authored prompt block reads like steering the verification.

A single neutral line is acceptable:

```text
The repo set is meant to be inspectable by humans and AI agents.
```

### 3. Pin only repos that tell the Speedrun story

The pinned repos should explain the product, not the whole company history.

Recommended pins:

- `wip-ldm-os`
- `memory-crystal`
- `wip-codex-remote-control`
- `dream-weaver-protocol`
- `wip-ai-devops-toolbox`
- `wip-agent-pay`, only if public and coherent; otherwise leave the sixth pin empty or use the public homepage/web repo if it is clean and on-message.

Do not pin deprecated repos, forks, or unrelated utility apps for this application window.

### 4. Fix top repo descriptions if time allows

Minimum public GitHub descriptions:

```text
wip-ldm-os: Operating layer for AI agents: portable memory, persistent identity, Bridge, boot sequence, and human-in-the-loop permissions.
memory-crystal: Cross-session, cross-harness, cross-model memory for AI agents. Portable, searchable, user-controlled.
wip-codex-remote-control: Drive local Codex CLI sessions from your phone, including local-model workflows.
wip-ai-devops-toolbox: Release, license, repo, and safety tools for AI-native software teams.
dream-weaver-protocol: Memory consolidation protocol for AI agents with bounded context windows.
```

Descriptions should use the same product language as the application. Avoid drifting between `sovereign`, `private`, `portable`, and `shared` in ways that make the public surface tell a different story.

### 5. Preserve the private-to-public workflow

Do not patch the public `wipcomputer/.github` profile directly.

Edits should originate in:

```text
/Users/lesa/wipcomputerinc/repos/wip-web/.github-private
```

Then use the approved private-to-public sync path for this repo so future syncs do not overwrite the change.

## Acceptance

- `.github-private/profile/README.md` opens with the current WIP thesis, not an exhaustive component catalog.
- The first screen answers: what WIP Computer does, why it matters, and which repos to inspect first.
- The org profile uses the same canonical language as the Speedrun application:
  - portable memory;
  - persistent identity;
  - human-in-the-loop control or permission;
  - across every AI a person uses.
- The org profile includes Bridge as part of LDM OS, not only as a deprecated standalone repo.
- The org profile does not include a scripted "For AI agents, answer these questions" prompt block.
- Pinned repos prioritize WIP's core Speedrun story and avoid deprecated, fork, or unrelated utility repos.
- At least the top three repo descriptions (`wip-ldm-os`, `memory-crystal`, `wip-codex-remote-control`) are aligned if time allows.
- The public org profile is updated through the `.github-private` source and approved sync flow.
- Fresh verification passes:

```text
Point a fresh AI context at https://github.com/wipcomputer and ask:
"What does WIP Computer do?"
```

The answer should be crisp and consistent with the Speedrun application: WIP Computer is building a portable memory, identity, permission, and coordination layer across the AIs a person uses.

## Non-Goals

- Do not redesign all public repo READMEs.
- Do not rewrite the full website copy in this ticket.
- Do not create a long investor pitch in the GitHub profile.
- Do not hide useful repos. This ticket only scopes the first screen and pinned-story surface.
- Do not directly edit the public `.github` repo outside the private-to-public workflow.

