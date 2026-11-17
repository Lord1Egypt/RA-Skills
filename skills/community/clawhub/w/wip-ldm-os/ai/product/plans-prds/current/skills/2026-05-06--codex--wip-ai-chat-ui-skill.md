---
title: "Create reusable WIP AI Chat UI skill"
status: open
priority: P1
owner: Cody
repo: new skill repo
created: 2026-05-06
---

# Create Reusable WIP AI Chat UI Skill

## Problem

WIP now has enough repeated AI chat UI work that each coder should not rediscover the same frontend stack choices from scratch.

Current active surfaces include:

- Codex Remote Control web;
- Kaleidoscope private web;
- future WIP mobile and desktop AI chat surfaces;
- future iOS companion planning, even when the iOS implementation is native.

The team has aligned on a clear frontend model:

```text
Behavior primitives: Radix UI by default
Component recipe: shadcn/ui style local components
Theme and visual style: Tailwind classes, CSS variables, spacing, color, radius
Icons: lucide-react
AI chat UX reference: assistant-ui
Backend/protocol: WIP-owned
```

This should become a reusable skill so agents can consistently build WIP chat interfaces without copying proprietary apps, adding hosted services, or guessing component patterns.

## Decision

Create a reusable skill named:

```text
wip-ai-chat-ui
```

This should be a general WIP skill, not a Remote Control-only ticket and not a Kaleidoscope-only ticket.

Current repo shape:

```text
private working repo: repos/wip-inc-private-only
skill source path: design/skills/wip-ai-chat-ui/
public package: @wipcomputer/wip-ai-chat-ui
```

Use the WIP Inc private working repo for the source because this is design guidance for agents, not app runtime UI. Publish the skill as a public npm package so LDM OS can install it onto Codex and other agent surfaces. Kaleidoscope and Codex Remote Control are the first real consumers, but the skill itself belongs with WIP's design language and agent guidance.

Do not place this under `repos/ldm-os/components/`. This is not a product runtime component package.

Do not place this under `repos/ldm-os/apps/kaleidoscope-private/web/src/components/`. Actual React UI components belong there, but this skill is not a component. It tells agents how to build components correctly.

Do not create a standalone React component library for this slice. Also do not assume this needs to be open source. This is WIP internal design guidance unless Parker explicitly decides to publish it later.

Packaging decision: Parker approved shipping the skill from the private working repo as the public npm package `@wipcomputer/wip-ai-chat-ui`. The npm tarball is public. Private repo planning files are not.

## Skill Trigger

The skill should trigger when an agent is asked to:

- build or revise a WIP AI chat UI;
- implement Remote Control transcript, composer, loading, status, or activity UI;
- apply shadcn/ui component patterns to WIP apps;
- choose between Radix, Base UI, shadcn/ui, Tailwind, lucide-react, or assistant-ui;
- convert "make it like ChatGPT or Claude" into a defensible open-source component plan.

## Core Instructions To Encode

The skill should teach agents:

- use shadcn/ui docs as the component reference;
- use assistant-ui as the AI chat UX reference;
- use Radix-backed primitives where behavior matters;
- use lucide-react for icons;
- use Tailwind and CSS variables for WIP visual identity;
- build or copy local source components into the app, do not rely on hosted UI services;
- keep WIP's own backend and protocol;
- do not adopt Assistant Cloud, Vercel AI provider routing, hosted analytics, hosted auth, or third-party persistence by default;
- do not scrape private apps;
- do not copy proprietary code, private assets, exact branding, or hidden implementation details;
- use open-source patterns for standard chat UI behavior.

## Component Guidance

The skill should distinguish simple visual components from behavior-heavy components.

Use local React and Tailwind for simple visual pieces:

- Button;
- Badge;
- Card;
- Separator;
- Skeleton;
- Spinner;
- message bubble;
- composer shell;
- status line;
- activity row.

Use Radix-backed shadcn patterns for behavior-heavy pieces:

- Dialog;
- Sheet;
- Tooltip;
- Popover;
- Dropdown Menu;
- Select;
- Tabs;
- Command;
- Toast or Sonner-style notifications, after the app chooses its notification surface.

Base UI can be mentioned as an acceptable alternative primitive family, but Radix should be the default unless the project has already chosen Base UI.

## Semantic Component Rule

The skill should explicitly teach that shadcn component names are references, not permission to use the wrong semantic component.

Agents should ask:

- What is the semantic role of this UI element?
- Is the chosen component meant for that role?
- Is this a global component decision or a local usage decision?
- Is the shadcn reference showing the visual target, behavior, interaction pattern, spacing, or literal component API?

When Parker points to a shadcn example or screenshot, separate visual reference from component implementation. Preserve the visible target: size, spacing, hierarchy, and behavior. Do not blindly copy the nearest component name.

Example:

- `Badge` is for compact metadata labels such as `Beta`, `Online`, `P1`, or `New`.
- A centered hydration/loading state is not a badge.
- A centered hydration/loading state should use `Spinner` plus a dedicated local `StatusPill`, `LoadingPill`, or `SyncingPill`.

Avoid this loop:

```text
Badge is too tight -> tweak Badge globally -> still wrong -> unrelated badges change too
```

Preferred fix:

```text
Keep Spinner reusable.
Keep Badge for actual metadata labels.
Create a local StatusPill or SyncingPill for centered loading states.
Do not mutate global component variants to solve one local use case.
```

The skill should tell agents to prefer local wrappers or local components when a one-off state needs different spacing, size, or visual weight. Global component variants should change only when the whole product's component contract changes.

## Remote Control First Consumer

Remote Control should be the first validation surface.

The skill should help agents implement these existing tickets consistently:

- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-chat-ui-baseline.md`;
- `ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-web-transcript-fidelity.md`;
- `ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-app-server-event-rendering.md`;
- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-activity-hydration.md`;
- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-slash-command-controls.md`;
- `ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-web-status-line.md`;
- `ai/product/bugs/codex-remote-control/2026-05-06--codex--remote-control-mobile-composer-safe-area.md`.

Remote Control's backend must remain:

```text
browser -> hosted relay -> local daemon -> Codex App Server -> live Codex TUI thread
```

The skill must not tell agents to replace that with a web model provider call.

## References

The skill can include these public references:

- `https://ui.shadcn.com/docs/components`;
- `https://ui.shadcn.com/docs/components/radix/spinner`;
- `https://ui.shadcn.com/docs/components/radix/skeleton`;
- `https://ui.shadcn.com/docs/components/radix/separator`;
- `https://www.assistant-ui.com/docs/architecture`;
- `https://www.assistant-ui.com/docs/ui/tabs`;
- `https://www.assistant-ui.com/docs/ui/file`;
- `https://github.com/assistant-ui/assistant-ui`;
- `https://www.radix-ui.com/primitives/docs/overview/introduction`;
- `https://lucide.dev/icons/`.

Do not require a paid service or remote MCP to use the skill.

## Suggested Skill Shape

```text
wip-ai-chat-ui/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── stack.md
    ├── components.md
    ├── remote-control.md
    └── anti-patterns.md
```

Keep `SKILL.md` concise. Put longer examples in `references/`.

Do not create extra README files inside the skill folder unless the repo itself needs one. The skill should follow Codex skill packaging guidance.

## Acceptance

- A reusable `wip-ai-chat-ui` skill exists.
- The skill can be installed by Codex agents through LDM OS from `@wipcomputer/wip-ai-chat-ui`.
- The npm tarball includes all four referenced files: `references/stack.md`, `references/components.md`, `references/anti-patterns.md`, and `references/remote-control.md`.
- The npm tarball excludes `ai/`, `_trash/`, `_sort/`, `.env`, `.worktrees/`, and `node_modules/`.
- The skill has clear trigger metadata.
- The skill tells agents to use shadcn/ui component references, assistant-ui chat UX references, Radix primitives, lucide-react icons, and WIP-owned Tailwind styling.
- The skill separates primitive behavior from component recipes and visual theme.
- The skill includes the semantic component rule: choose the component by role, not by a visually similar name.
- The skill warns against mutating global component variants to solve one local layout problem.
- The skill tells agents not to adopt hosted runtime services by default.
- The skill tells agents not to scrape proprietary apps or copy private UI/code/assets.
- The skill gives concrete guidance for Spinner, Skeleton, Separator, Tooltip, Sheet, Dialog, message list, composer, status line, and activity rows.
- The skill references Remote Control as the first validation surface, but it is reusable across WIP products.
- A coder can use the skill to implement a Remote Control UI ticket without re-litigating the frontend stack.

## Non-Goals

- Do not implement the Remote Control UI pass in this ticket.
- Do not install new UI dependencies into Kaleidoscope in this ticket.
- Do not make shadcn.io, Assistant Cloud, Vercel services, or any paid UI catalog part of WIP runtime infrastructure.
- Do not choose Base UI as the default primitive family unless a product repo explicitly opts in.
- Do not create a proprietary-app clone.
