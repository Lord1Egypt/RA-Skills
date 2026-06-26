## Description: <br>
Provides a daily morning brief with the current date, week number, China public-holiday countdowns, and week, month, and year progress percentages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxseller](https://clawhub.ai/user/foxseller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents or users who want a scheduled daily status message use this skill to generate a morning brief with date context, China holiday countdowns, and time-progress reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external public holiday-data source, so generated holiday countdowns can be unavailable or stale if that source changes. <br>
Mitigation: Monitor or review the upstream data source and confirm holiday output before relying on it for time-sensitive workflows. <br>
Risk: The release relies on npm dependencies without evidence of a reviewed lockfile. <br>
Mitigation: Install with pinned dependency versions or a reviewed lockfile to improve reproducibility. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/foxseller/wakeup-niuma) <br>
- [China holiday calendar data source](https://github.com/lanceliao/china-holiday-calender) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text daily brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled cron execution; writes a local yearly holiday cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
