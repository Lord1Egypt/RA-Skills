---
name: sports-digest
description: Rolling multi-sport digest skill that tracks current storylines, recent results, upcoming fixtures/events, injuries/availability, and standings across a chosen sports portfolio while keeping a compact context file current.
version: 1.0.2
---

# Sports Digest 

Prepare a concise, factual sports digest for **{{recipient_name}}** and keep the rolling context file current.

Use this skill when the goal is not to cover every sports headline, but to answer: **what actually changed for this audience’s teams and competitions since the last digest, and what should they know next?**

This skill works best when paired with:

- a rolling context file: `SPORTS_CONTEXT.md`
- a clearly defined sports scope
- a recurring cadence such as 3x weekly or weekly

## When to use this skill

Use it when you want:

- a recurring digest for specific teams, leagues, tours, or competitions
- continuity across runs instead of starting from scratch every time
- coverage that balances recent results, upcoming events, injuries, standings, and major storylines
- one digest that can mix team sports and event-based sports cleanly

## When not to use this skill

Do **not** use it when you want:

- full box-score recaps for every game or match
- betting picks or gambling advice
- instant live-play updates during an event
- broad all-sports news unrelated to the selected teams or competitions
- archived historical writeups that grow forever over time

## Setup

- **Context file**: `SPORTS_CONTEXT.md` in this skill directory
- **Schedule**: {{schedule_description}}
- **Delivery**: {{delivery_channel}} → {{recipient_name}}
- **Scope**:
{{scope_bullets}}

## Inputs to customize

- `{{recipient_name}}` — person, team, or audience receiving the digest
- `{{schedule_description}}` — cadence and timezone, e.g. `Monday, Thursday, Saturday at 8am ET via cron`
- `{{delivery_channel}}` — e.g. `Telegram`, `email`, `Slack DM`, `Notion`, `Discord`
- `{{scope_bullets}}` — bullet list of teams, leagues, competitions, or sports to cover
- `{{digest_title}}` — optional digest title, e.g. `Sports Digest`, `Weekend Sports Pulse`
- `{{emoji_prefix}}` — optional emoji cluster for the title line
- `{{section_specs}}` — ordered list of sections with labels and coverage targets
- `{{special_rules}}` — sport- or audience-specific reporting priorities
- `{{tone_notes}}` — optional voice/style cues for the final writeup
- `{{time_window}}` — optional lookback guidance, e.g. `since last digest`, `last 3 days`

## Core workflow

1. Read `SPORTS_CONTEXT.md` first so the digest continues the current story instead of starting cold.
2. Search each team, league, tour, or sport separately.
3. Cover only information sourced in the current session.
4. Update `SPORTS_CONTEXT.md` by replacing stale information rather than appending an archive.
5. Deliver one clean digest message.

## Coverage model

### For team sports
Focus on:
- latest result(s)
- next fixture(s)
- injuries / absences / lineup changes
- standings or playoff / table implications
- roster moves, transfer news, or major off-field developments

### For soccer / football clubs
Also look for:
- manager or tactical changes
- transfer updates
- cup / league / European competition context
- relegation / qualification / title-race implications when relevant

### For motorsport, golf, and other event-based sports
Focus on:
- most recent event result(s)
- next scheduled event
- championship / points / FedExCup / ranking context if relevant
- penalties, withdrawals, injuries, suspensions, qualifying context, or key field changes
- major narrative shifts that matter for the next event

## Search guidance

Useful searches include:
- `[team] news [current month year]`
- `[team] latest result`
- `[team] next game`
- `[team] injury report`
- `[club] transfer news`
- `[league] standings`
- `[driver/team] latest result`
- `[series] standings`
- `[tournament] leaderboard`
- `[tour/player] news`
- `[sport] upcoming schedule`

## Accuracy rules

- Only report scores, standings, and results that were actually sourced in the current session.
- Never infer a result because an event should have finished by now.
- If a result is not confirmed, say the event is upcoming or in progress.
- Keep uncertainty explicit rather than smoothing it over.
- If sources conflict, prefer the most direct and current report, and keep the wording careful.

## Updating SPORTS_CONTEXT.md

Treat `SPORTS_CONTEXT.md` as rolling memory, not an archive.

Keep it focused on what is still useful for the *next* digest:

- latest confirmed results
- next upcoming fixtures/events
- active injuries / absences / lineup concerns
- current standings / points / competition context
- a few live storylines that still matter

Do not let it grow endlessly.

When updating:
- replace outdated fixtures and results
- remove stale injuries or obsolete narratives
- preserve only current context that helps the next run
- keep the file roughly stable in size
- update the `Last updated` line when making meaningful changes

## Output format

Use this structure:

```text
{{emoji_prefix}} {{digest_title}} — [today's date]

{{formatted_sections}}
```

Example section format:

```text
{{section_emoji}} {{section_label}}: [2-5 punchy factual sentences]
```

## Recommended section planning

A good mixed-sport digest often works well with sections like:

- 🦅 Eagles — NFL / Philadelphia Eagles
- ⚾️ Phillies — MLB / Philadelphia Phillies
- 🔵 Everton — Premier League / Everton FC
- 💜 Fiorentina — Serie A / ACF Fiorentina
- 🏎️ F1 — Formula 1
- ⛳️ Golf — PGA Tour, DP World Tour, majors

Keep club teams separate when storyline continuity matters. It is fine to keep whole-sport sections like F1 and golf at a higher level.

But use whatever section structure best matches `{{section_specs}}`.

## Style constraints

- Keep it tight, factual, and current.
- Prioritize what changed and what’s next.
- Avoid padding with generic sportswriter filler.
- Prefer clear consequences over vague hype.
- Follow tone notes: `{{tone_notes}}`

## Success criteria

A good digest should:

- feel continuous from the prior digest
- give the reader the minimum they need to stay current
- balance recent results with what’s next
- stay accurate under uncertainty
- avoid becoming a bloated archive or recap dump