## Description: <br>
File-based weekly planning system (TOML) with inbox capture, time-block scheduling, weekly review, and optional calendar publishing (Google Calendar via gogcli or .ics export). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to capture tasks, plan and time-block a week, roll over unfinished work, complete weekly reviews, and optionally publish time blocks to a calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initializer can delete a chosen target folder when run with --force. <br>
Mitigation: Use --force only after confirming the target is exactly the planner folder intended for replacement. <br>
Risk: Calendar sync can update or delete managed events in the configured calendar. <br>
Mitigation: Run dry-run first, sync only to a dedicated planner calendar, and apply changes only after reviewing the planned actions. <br>
Risk: Planner files may contain private notes and schedule details. <br>
Mitigation: Keep planner notes private and use .ics export when direct calendar access is not desired. <br>


## Reference(s): <br>
- [Weekly Planner Skill Page](https://clawhub.ai/tristanmanchester/weekly-planner) <br>
- [Weekly Planner schema](references/PLANNER_SCHEMA.md) <br>
- [Calendar publishing](references/CALENDAR_SYNC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline TOML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and edits plain-text planner files; optional calendar output is Google Calendar sync actions or .ics files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
