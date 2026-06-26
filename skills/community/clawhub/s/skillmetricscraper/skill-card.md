## Description: <br>
Tracks trending ClawHub skills, stores metrics snapshots, ranks movers and rockets, and generates weekly Markdown reports and voice-ready video scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ademczuk](https://clawhub.ai/user/ademczuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and ecosystem analysts use this skill to monitor ClawHub skill trends, preserve time-series metrics, and produce weekly summaries or scripts for reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public ClawHub, social, and GitHub data and persists analytics outputs locally. <br>
Mitigation: Run it only where local report, JSON, text, and SQLite outputs are expected, and review output locations and retention before scheduled use. <br>
Risk: The skill may use authenticated services, Docker access, and an external X search helper. <br>
Mitigation: Provide least-privilege credentials only for intended modes, and review or disable Docker bridge behavior and X_SEARCH_SCRIPT before running in sensitive environments. <br>
Risk: Broad triggers and cron or hourly setup can collect data or generate reports more often than intended. <br>
Mitigation: Enable only the needed triggers and schedules, and monitor snapshot and report jobs when automation is configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ademczuk/skillmetricscraper) <br>
- [ClawHub public skills API](https://clawhub.ai/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, text scripts, JSON metrics data, SQLite snapshots, and terminal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local report, script, JSON, and SQLite files; script generation depends on configured API credentials.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
