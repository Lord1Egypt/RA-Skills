## Description: <br>
将 2026 FIFA 世界杯赛程同步到飞书日历，支持按北京时间预览、创建或删除私密日程，并为关注球队设置提前提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kekenana272](https://clawhub.ai/user/kekenana272) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preview and synchronize the 2026 FIFA World Cup schedule into a Feishu/Lark calendar with private visibility, free busy status, and configurable reminders for selected teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar permissions allow the local Feishu/Lark CLI to create or delete calendar data. <br>
Mitigation: Review preview output first, grant only the needed calendar scopes, and use --execute only after confirming the intended changes. <br>
Risk: The helper can attempt a global npm install of @larksuite/cli when requested. <br>
Mitigation: Install @larksuite/cli manually when preferred, or review the doctor --install-cli path before allowing a global npm install. <br>
Risk: World Cup fixture times and knockout-stage placeholders may change after the bundled data extraction. <br>
Mitigation: Recheck the official FIFA schedule before important syncs or before updating placeholder knockout matches. <br>
Risk: Delete commands can remove generated World Cup events or the whole target calendar when executed. <br>
Mitigation: Run delete commands without --execute first and confirm the matched calendar, match IDs, and event list before deleting. <br>


## Reference(s): <br>
- [FIFA 2026 match schedule PDF](https://digitalhub.fifa.com/m/1be9ce37eb98fcc5/original/FWC26-Match-Schedule_English.pdf) <br>
- [Schedule data notes](references/data-notes.md) <br>
- [2026 FIFA World Cup schedule JSON](references/fwc2026-schedule.json) <br>
- [ClawHub skill page](https://clawhub.ai/kekenana272/world-cup-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON preview output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode is the default; calendar writes and deletions require the user to add --execute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
