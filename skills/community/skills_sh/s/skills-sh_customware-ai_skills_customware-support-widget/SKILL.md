---
name: customware-support-widget
description: Use this skill when adding, placing, configuring, or fixing the Customware support chat widget in the Customware React Router client-only SPA template. It covers root.tsx/root document script loading, route/layout placement, required org/project ids, bubble versus full mode, optional metadata and style options, page-operation support, and constraints for MITB-style code generation.
---

# Customware Support Widget

Use this skill when the Customware React Router client-only SPA template needs a Customware support chat entry point.

The widget is a third-party browser custom element. In this template, load the widget script in `root.tsx` or the equivalent React Router root file/component where the HTML document structure is defined, and render `<customware-chat>` only in the route or layout where support should appear. The widget owns its Shadow DOM UI, chat runtime, service calls, tool badges, speech input, and page-operation behavior.

For all React code examples, script loading patterns, JSX typing, bubble/full mode examples, metadata, and style options, read [references/component-usage.md](references/component-usage.md).

## What It Offers

- A support chat UI as `<customware-chat>`.
- `chat-bubble` mode for a floating launcher/dialog.
- `full` mode for a sidebar, rail, drawer, or split-pane chat region.
- Optional visitor metadata through the `meta` DOM property.
- Optional sizing/customization through `styleOptions` or `style-options`.
- Tool-backed support behavior: read domain/context, list tasks, create tasks, and operate the visible page.
- Page operation for user requests like filling forms, selecting options, clicking buttons, replacing values, or submitting visible UI.

## When To Use

- Add support chat to the Customware React Router client-only SPA template.
- Place a floating support launcher in an app shell.
- Place support chat as a full embedded panel in a layout region.
- Allow the support agent to help with visible app UI, such as filling a form on behalf of the user.
- Update an existing support widget placement or styling.

For the exact React implementation patterns, use [references/component-usage.md](references/component-usage.md).

## When Not To Use

- Do not use this skill for server-side rendering work. The target template is client-only React Router SPA mode.
- Do not use this skill to build a custom chat UI.
- Do not use this skill to iframe the widget.
- Do not use this skill to call support chat endpoints directly.
- Do not use this skill for non-template React apps or non-React apps unless explicitly asked.
- Do not use this skill if `orgId` or `projectId` cannot be determined. Fail the task with a clear reason that the required Customware org/project id is missing.

## Non-Negotiables

- Always render the real custom element: `<customware-chat>`.
- Always pass both `org-id` and `project-id`.
- If either id is unavailable, fail the task with a clear missing-id reason instead of rendering placeholders or asking follow-up questions.
- Load `https://app.customware.ai/support-widget/customware-chat.js` once from `root.tsx` or the template's equivalent React Router root document shell unless an existing app-level loader already does this.
- Do not pass task ids, domain ids, user ids, API tokens, session tokens, auth cookies, or secrets into the component.
- Use `meta` only for optional visitor identity: `email` and/or `name`.
- Use wrapper CSS, `styleOptions`, or `style-options` for sizing. Do not use the native DOM `style` property as widget configuration.
- Tool calls are compact status badges, not buttons.
- Page operation is handled inside the widget. Do not add custom click/fill/page-control handlers around it.
- Do not hardcode page-operation prompts or values into the host app. The user must type the request into the widget.

## Implementation Workflow

1. Read [references/component-usage.md](references/component-usage.md).
2. Confirm the React app has `orgId` and `projectId`.
3. Choose the mode:
   - `chat-bubble` for a floating support launcher/dialog.
   - `full` for an embedded rail, drawer, split pane, or fixed chat region.
4. Add the script tag in `root.tsx` or the React Router root file/component that defines the HTML document `<head>`, unless it already exists.
5. Add JSX custom element typings in a `.d.ts` file when the template does not already know `<customware-chat>`.
6. Render `<customware-chat>` with `org-id` and `project-id` in the specific route or layout that needs support.
7. Set optional `meta` and `styleOptions` through a typed React ref when needed.
8. For full mode, ensure the wrapper/component has a concrete height and internal scrolling belongs to the widget.
9. For bubble mode, ensure the wrapper is not clipped and has an appropriate `z-index`.
10. Validate the resulting React code syntactically and with `npm run check` when available.

Use [references/component-usage.md](references/component-usage.md) for complete code examples for each mode.

## MITB Agent Constraints

- Do not assume access to Playwright, screenshots, browser DevTools, or visual testing.
- Do not claim that the widget was visually tested.
- Do not write user-facing status reports inside the generated app.
- Validate by code inspection, TypeScript/compile checks, and ensuring the generated React Router/Vite code follows the examples in [references/component-usage.md](references/component-usage.md).
- If runtime ids are unavailable during generation, fail the task with a clear missing-id reason. If ids are expected to load asynchronously at runtime, gate the component behind `orgId && projectId` so it never renders with placeholders.

## Do Not Do

- Do not create an iframe integration.
- Do not rebuild or restyle the widget internals in React.
- Do not reach into Shadow DOM or depend on internal class names.
- Do not expose tool calls as clickable UI controls.
- Do not call the support chat API or page-operation API directly from the host app.
- Do not add fallback embed modes.
- Do not store secrets, access tokens, private payloads, or auth/session data in widget attributes.
- Do not pass arbitrary user/profile objects into `meta`; pass only optional `email` and `name`.
- Do not set a fixed height only on an imagined internal message list. Size the whole full-mode host region.
- Do not place bubble mode inside clipped or transformed containers unless that behavior is intentional.
