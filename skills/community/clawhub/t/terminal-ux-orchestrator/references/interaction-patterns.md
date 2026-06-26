# Interaction Patterns

Pick patterns that match the task instead of forcing a full-screen TUI everywhere.

## 1. Command-first execution

Use when tasks are repeatable, scriptable, and well-specified by flags or config.

Good for:

- automation
- CI usage
- batch operations
- expert users who know the workflow

Enhance with:

- strong `--help` output
- examples
- explicit defaults
- structured success and error output

## 2. Prompt or confirm flow

Use when the user needs light guidance or confirmation before running an action.

Good for:

- setup flows
- destructive confirmations
- choosing one option from a short list
- collecting a few fields interactively

Avoid for long or highly branched workflows.

## 3. Wizard

Use when the task has a fixed order, dependencies between steps, or validation at each stage.

Good for:

- project initialization
- deployment setup
- multi-step creation flows

Requirements:

- explicit step count or progress
- back and cancel behavior
- validation before advancing
- clear summary before commit

## 4. Selector or list browser

Use when users choose among dynamic resources.

Good for:

- environments
- services
- files
- jobs
- history items

Requirements:

- clear focus state
- search or filtering when the list is long
- visible key hints
- empty-state messaging

## 5. Table or grid view

Use when side-by-side comparison matters.

Good for:

- status dashboards
- resource inventories
- job listings
- diff-like summaries

Avoid if width constraints make columns unreadable. Prefer a list with detail panels or drill-down views in narrow layouts.

## 6. Multi-panel TUI

Use only when persistent context is genuinely valuable.

Good for:

- monitoring
- browsing plus detail inspection
- workflows where selection and detail must stay visible together

Requirements:

- stable focus model
- consistent pane responsibilities
- resize-aware layout
- obvious quit, back, and refresh actions

## 7. Streaming log or progress view

Use when work is long-running and users need confidence that the tool is alive.

Requirements:

- immediate acknowledgement of start
- progress or heartbeat
- explicit completion or failure state
- summary after completion

## Pattern Selection Rule

If two patterns could work, prefer the simpler one unless the richer pattern clearly improves speed, confidence, or error recovery.
