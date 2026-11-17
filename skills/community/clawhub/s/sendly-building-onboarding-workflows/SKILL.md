---
name: building-onboarding-workflows
description: "Builds, reviews, and troubleshoots Sendly workflow automations such as welcome, drip, and onboarding email series; new workflows are created disabled. Use when the user asks to 'build a welcome series for new signups', 'create a drip campaign', 'set up an onboarding email sequence', 'what does this workflow do', 'why isn't my onboarding workflow running', 'change the delay before the second email', or wants to automate lifecycle emails."
---

# Sendly onboarding workflow

Turn a plain-language brief into a multi-step workflow, and explain or fix existing ones. A live workflow sends real email to every contact who triggers it, so turning one on needs the user's explicit yes.

## Connecting and calling the tools

Every tool in this skill comes from the `sendly` MCP server, the Sendly connector, and is written here as `sendly:<tool>`.

- **Tools listed by name:** call them directly, for example `sendly:list_contacts`.
- **Only `sendly:search_tools` and `sendly:execute_typescript` listed (Code Mode, the default):** call `sendly:search_tools` first, then call each tool inside `sendly:execute_typescript` as `external_<tool>` (for example `external_list_contacts`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `sendly:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Sendly and approves that scope.
- **No `sendly` tools at all:** Sendly is not connected yet. Install the Sendly power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `sendly:list_workflows`, `sendly:get_workflow`: existing workflows and their full definition (trigger and steps).
- `sendly:get_workflow_status`: whether a workflow is enabled, its step count, and its execution count.
- `sendly:list_workflow_executions`: individual runs, to see where contacts stopped.
- `sendly:list_events`: recent events, to check the trigger event actually arrives.
- `sendly:list_templates`: templates the email steps can use.
- `sendly:create_workflow`: create a workflow from a structured spec. Created with `enabled: false` by default.
- `sendly:clone_workflow`: copy an existing workflow as a starting point.
- `sendly:edit_workflow`: change a workflow's step graph.
- `sendly:update_workflow`: change a workflow's settings. Step changes go through `sendly:edit_workflow`.
- `sendly:manage_workflow`: change a workflow's state. Read its description for the actions it accepts.

## Workflow

1. For a new workflow, restate the brief as a trigger and a numbered list of steps (for example: on `member.signup` send Welcome, wait 3 days, send Nudge). Confirm it with the user.
2. Call `sendly:list_templates` and map each email step to a template. Point out steps that have no template yet.
3. Call `sendly:create_workflow` (or `sendly:clone_workflow` from a similar one). Leave it disabled. Report its id and steps.
4. For an existing workflow, call `sendly:get_workflow_status` and `sendly:get_workflow`, and describe the trigger and each step in plain words.
5. If it is not sending: check it is enabled, call `sendly:list_events` to see whether the trigger event is arriving, and call `sendly:list_workflow_executions` to see where runs stop. Report the first cause you find.
6. To change steps, show the before and after, get an explicit yes, then call `sendly:edit_workflow`.
7. To turn a workflow on, say that it will start sending real email to every contact who triggers it from now on, get an explicit yes, then make the change.

## Rules

- Never enable a workflow, or change one that is already enabled, without an explicit yes in this turn.
- Workflows refuse a `from` address that is not on a verified domain. If that happens, offer the `checking-email-deliverability` skill.
- `sendly:edit_workflow`, `sendly:manage_workflow`, and `sendly:delete_workflow` are annotated destructive, and `sendly:update_workflow` can change what a live workflow sends. Call each only after an explicit yes naming the workflow.
- Confirm the workflow by name before `sendly:delete_workflow`.
