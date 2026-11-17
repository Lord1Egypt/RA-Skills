## Description:

将 2026 FIFA 世界杯赛程按北京时间同步到私密飞书日历，并为关注球队比赛设置提前提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kekenana272](https://clawhub.ai/user/kekenana272)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview, create, or delete Feishu calendar events for the 2026 FIFA World Cup schedule, including private visibility, free busy status, and focus-team reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can globally install an unpinned external Feishu CLI through npm.

Mitigation: Install and verify a pinned lark-cli version separately before using the skill, or review the package before running doctor --install-cli.

Risk: The skill can create or delete real Feishu calendar data when --execute is used.

Mitigation: Run preview commands first, review the planned sync or delete output, and use --execute only after confirming the target calendar and match selection.

Risk: The bundled schedule may become stale if FIFA updates match times or knockout-stage teams.

Mitigation: Recheck the official FIFA schedule before important matches and update references/fwc2026-schedule.json when official data changes.

## Reference(s):

- [Schedule Data Notes](references/data-notes.md)
- [2026 FIFA World Cup Schedule Data](references/fwc2026-schedule.json)
- [FIFA Official Match Schedule PDF](https://digitalhub.fifa.com/m/1be9ce37eb98fcc5/original/FWC26-Match-Schedule_English.pdf)
- [ClawHub Skill Page](https://clawhub.ai/kekenana272/skills/world-cup-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON calendar-event previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is the default; Feishu writes and deletions require an explicit --execute flag.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
