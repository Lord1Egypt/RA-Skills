---
name: yoooclaw-daily-morning-brief-en
description: Used when the user needs to organize a general morning report from the notifications of the day or the most recent period; typical trigger sentences: 'Help me publish a morning report', 'What important information and to-dos are there today', 'Help me organize the key messages and things to follow in the morning', 'Summarize recent notifications into a morning report', 'Help me organize the morning report'.
---

# Daily Morning Brief

The input is usually a JSON array of notifications, and the sources may be a mix of team groups, projects, private chats, calendar reminders, system notifications, platform messages, and life noise.

Users set three types of attention dimensions through the installation pop-up window:
- Who to pay attention to: direct superiors, key colleagues, customers, partners, family members or others who need priority response.
- What to pay attention to: key items such as project name, customer name, document name, version name, activity name, project name, etc.
- Which groups and applications to follow: Feishu, WeChat, email, calendar, GitHub, DingTalk, project management tools, etc.

The goal is to explain in a morning paper:
- Key information
- Today's to-do
- Missed items
- Things to follow up on
- Matters to be decided

## Workflow

1. To query notifications within a specified time range, use exec to execute:
If the user does not provide the corresponding time, query notifications from yesterday to the current time:
```text
command: openclaw ntf search --from start time --to end time
yieldMs: 30000
```
Example:
```text
command: openclaw ntf search --from 2026-03-01T00:00:00+08:00 --to 2026-03-09T23:59:59+08:00
yieldMs: 30000
```
2. It is strictly prohibited to reuse old results, and all queries must be re-queried.
3. Read the user's settings of who to follow, what to follow, and which groups and applications to follow; if the user does not provide it, identify possible items of interest from the current request.
4. Filter the results for information that has an impact on today, and ignore advertisements, promotions, pure chatter, repeated reminders, and life-related notifications without clear action value.
5. Increase the priority of messages that hit "Who to Follow", "What to Follow" and "Which Groups and Applications to Follow". Even if the content is short, check whether it contains progress, risks, reminders, pending confirmation or implicit to-dos.
6. Merge multiple messages on the same matter and summarize them according to the latest progress, without stacking the original texts one by one.
7. Identify and label four categories of to-dos:
- Missed: items that have expired, not been responded to, not confirmed, not processed, or may be missed.
- What should be followed up: Matters that already have context but lack the next step.- Decision-making: Matters that require the user or person in charge to judge, make decisions, make choices, or give clear opinions.
- What must be done today: There are clear deadlines for today, meetings for today, delivery for today, or matters that will affect the progress of the day.
8. Extract the clear date, period, and deadline for time messages; the relative time needs to be calculated based on the `timestamp` of the notification.
9. Try to retain key entities such as responsible person, object, project name, meeting name, client name, file name, etc.
10. If the information is sparse and key changes and to-dos are not clearly defined, output copywriting and do not forcibly make up matters.

## Output requirements

The output is session text, no file is generated. Default structure:

```text
🌅 Today’s morning news (YYYY-MM-DD)

One Sentence Overview: Use 1 sentence to describe whether there were key changes, major pressure points, or overall smoothness today.

1. Key information
  1. Name of the matter: key facts, latest progress, scope of impact
  2. ...

2. Today’s to-do
  【Missed】...
  [Time to follow up]...
  【Decision to be made】...
  【Must do today】...

3. Risks and reminders
  Only list reminders that may affect delivery, relationships, scheduling, approvals, meetings, or decision-making quality; otherwise write "no obvious risk yet."
```

If there is not enough valid information, it must output:

```text
🌅 Today’s morning news (YYYY-MM-DD)

No key changes today, good morning.
```

## Information filtering rules

- Who to follow, what to follow, which groups and applications to follow set by the user are the highest priority clues. Related messages must be read, merged and judged for action value first.
- News related to items of concern does not necessarily have to be output; morning reports will only be entered when there are new developments, risks, to-dos, decisions, deadlines, reminders or context changes.
- Prioritize the retention of information that will affect today's schedule, project advancement, interpersonal collaboration, customer communication, approval decisions, and delivery quality.
- Content that has been reminded, @user, named, requested for confirmation, or requested for reply multiple times in the group chat should be given a higher priority.
- Content with clear deadlines, meeting times, approval times, and delivery times must be entered into to-do or reminder.
- Completed items are only kept if they can reduce repeated follow-up or explain the current status.
- Life notifications are only retained when they will affect the schedule of the day, such as traffic delays, medical appointments, important express delivery, and family emergencies.

## To-do judgment rules

- The deadline has passed but no evidence of completion or reply has been seen, and it is classified as [Missed].
- The other party raises questions, urges, needs supplementary materials, and waits for confirmation, which is classified as [this follow-up].
- Involving program selection, budget, scheduling conflicts, whether to participate, whether to publish, and whether to agree, these are classified as [Decisions to be made].
- Things that need to be attended, submitted, replied, confirmed, prepared or delivered today are classified as [Must Do Today].- When the same matter meets multiple categories at the same time, put it into the most urgent category and explain the reason in the entry.

## Decision Criteria

- Don’t keep a running account, and give priority to outputting information that can change actions.
- You can write "may need confirmation" when there is no clear evidence, but do not write speculation as fact.
- When the same matter is updated before and after, the latest status shall prevail, while retaining key historical conditions, such as deadlines or requirements of the other party.
- To-dos must be written as executable actions, and empty expressions such as "pay attention to it" and "process it" should be avoided.
- When the data is sparse, it is better to output detailed copy instead of generating meaningless morning reports just to make up the structure.

## Output style

- The information density is high, suitable for reading quickly in the morning and starting action.
- Tone soberly, concisely, and directly.
- Key information + Today’s to-dos must be prioritized, and background explanations should be kept simple.
