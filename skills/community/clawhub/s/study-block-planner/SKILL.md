---
name: study-block-planner
description: Build a realistic, conflict-free study plan from a user-provided schedule, tasks, and available time.
---

# Study Block Planner

Use this skill when the user provides fixed commitments and tasks and asks how to fit the work into a day or another planning window. This skill works from information the user provides; it does not read a calendar, create events, or modify files.

## Gather the inputs

Use the schedule, available planning window, task names, durations, deadlines, and priorities given by the user. If the user has not supplied enough information to make a useful plan, ask only for the missing details that would change the result. Do not invent commitments, deadlines, or task durations.

If the user asks for a quick draft despite missing durations, state a reasonable duration estimate for each affected task and label it as an assumption. Invite the user to correct those estimates.

## Build the plan

1. Keep fixed commitments at their stated times. Do not move or overlap them.
2. Treat only the gaps the user identifies as available time as schedulable.
3. Schedule tasks with nearer deadlines or higher stated priority first. For tasks with equal priority, use the order the user gave unless they request another rule.
4. Fit each task into a contiguous block at least as long as its stated or clearly labeled estimated duration. Do not silently split a task into smaller blocks.
5. Leave a 10-minute transition buffer between different activities when the available window permits. If the user specifies a different buffer, use theirs.
6. If a task cannot fit, leave it unscheduled and explain why. Never overbook the planning window to make everything appear to fit.
7. Use the user's time zone. If it is unknown and affects interpretation, ask or label the time zone assumption.

## Respond

Start with a short summary of whether all tasks fit. Then show a chronological table with the time, activity, and a brief reason for placement. List unscheduled tasks and any assumptions after the table. Keep the plan practical and concise.

Do not claim to have checked a calendar or saved the plan. The result is a proposal based solely on the information in the conversation.

## Example request

“Plan 1:00–5:00 PM. Fixed: class 2:00–3:00. Tasks: problem set (90 minutes, due tomorrow, high priority), reading (45 minutes, no deadline). Use 10-minute transitions.”
