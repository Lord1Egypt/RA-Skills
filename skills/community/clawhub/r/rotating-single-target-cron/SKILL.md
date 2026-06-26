---
name: rotating-single-target-cron
description: Create or update recurring chat cron jobs that choose exactly one @ID from a configured list on each run, avoid repeating the previous target, persist the last-picked target in a workspace state file, and post one single-target message to chat. Use when a user wants rotating daily/weekly mentions, story prompts, wake-up messages, teasing copy, or any other one-person-at-a-time scheduled content instead of group-wide output.
---

# Rotating Single Target Cron

## Overview

Use this skill to build or maintain cron jobs that rotate across a roster of @IDs.
Each run should pick exactly one target, avoid the immediately previous target when alternatives exist, update a state file, and send only one final message.

## Workflow

### 1. Confirm the shape of the job

Default assumptions for this pattern:
- one recurring cron job
- one message per run
- one selected @ID per run
- fixed roster unless the user asks to edit it
- current chat as delivery target unless the user specifies another destination
- last-picked target stored in a workspace file under `memory/`

Ask only for missing essentials:
- roster of @IDs
- schedule and timezone
- message style or prompt brief
- whether this is a new job or an update to an existing one

### 2. Prepare state

Create or maintain a plain text state file in the workspace.
Recommended naming:

```text
memory/<job-slug>-last-target.txt
```

State rules:
- store exactly one line: `@ID` or `none`
- if the file is missing, empty, or contains an ID no longer in the roster, treat it as `none`
- when migrating an existing job, seed the file from the most recent known target if reliable; otherwise initialize it to `none`

### 3. Write a strict cron payload

The scheduled prompt should instruct the runtime to do this sequence:
1. read the state file
2. determine the previous target
3. pick exactly one target from the configured roster
4. avoid the previous target whenever another valid choice exists
5. overwrite the state file with the newly chosen target
6. output only the final chat message

Keep the payload strict about output shape.
Unless the user says otherwise, include these rules:
- mention the chosen `@ID` naturally near the beginning
- do not mention the other configured IDs in the same message
- keep the output public-chat safe
- do not add explanations, labels, or meta commentary

### 4. Create or update the cron job

For a new job:
- create the state file first
- add the cron job with `sessionTarget="isolated"`
- default delivery to the current chat
- use a short descriptive name tied to the behavior

For an update:
- patch the existing job in place
- update schedule, roster, payload, and name as needed
- do not create duplicates when the user is clearly editing an existing rotation

### 5. Test only on request

In active group chats, do not trigger a live run unless the user explicitly asks.
If the user asks to test:
- warn briefly that the test will post to the chat
- run the cron job immediately
- remember that the state file will advance after the test

### 6. Handle common edits safely

Common edits:
- change the time
- change the roster
- swap the writing style or content brief
- switch from multi-target message mode to rotating single-target mode
- change word-count or tone constraints

When converting an older multi-target job into this pattern, initialize or repair the state file so the first rotated run starts cleanly.

## Prompt skeleton

Use this as the base structure and replace placeholders with the user's style/content requirements.

```text
Send exactly one message to the current chat every day at <HH:MM> (<TZ>).

Roster: <@id list>
State file: memory/<job-slug>-last-target.txt

You must follow these rules exactly:
1. Before generating anything, read the state file. If the file does not exist, is empty, or contains an ID not in the roster, treat the previous target as "none".
2. Randomly select exactly one person from the roster as the only target for this run.
3. Never pick the same target as last time when any other valid option exists.
4. After choosing the target, immediately overwrite the state file with that target's @ID.
5. Do not mention any other IDs from the roster in the final output.
6. Output only the final chat message. Do not add explanations, titles, labels, or commentary.
7. Mention the selected @ID naturally near the beginning of the message.
8. Follow these content requirements exactly:
<content brief and style constraints>
```

## References

Read `references/examples.md` when you need ready-made prompt patterns for common variants such as heartbreak stories, wake-up copy, teasing posts, or fortune-style rotations.

## Checklist

Before finishing, verify:
- only one active cron job handles this rotation
- schedule matches the user's request
- roster matches the user's request exactly
- state file uses a relative workspace path under `memory/`
- prompt forbids repeating the immediately previous target
- prompt forbids mentioning other configured IDs in the same output unless the user explicitly wants that
- delivery target is correct
- live testing happened only if the user requested it
