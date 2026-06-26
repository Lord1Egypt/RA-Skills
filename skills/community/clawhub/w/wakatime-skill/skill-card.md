## Description: <br>
Query WakaTime coding statistics for time ranges, projects, languages, categories, editors, and machines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensoul](https://clawhub.ai/user/chensoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to retrieve read-only WakaTime coding activity summaries and breakdowns from WakaTime cloud for status reports, time review, and project analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Providing a WakaTime API key allows the skill to retrieve account coding activity. <br>
Mitigation: Set WAKATIME_API_KEY only in the local agent environment, avoid sharing it in prompts or logs, and rotate the key if exposed. <br>
Risk: Returned WakaTime statistics may reveal private project names, machines, editors, dependencies, and work patterns. <br>
Mitigation: Review outputs before sharing and limit queries to the needed date range, project, branch, or timezone. <br>
Risk: Debug output can expose request URLs and query parameters related to projects or branches. <br>
Mitigation: Use debug mode only during troubleshooting and avoid sharing debug logs that contain sensitive activity details. <br>


## Reference(s): <br>
- [WakaTime API Reference](references/wakatime-api.md) <br>
- [WakaTime Developers](https://wakatime.com/developers) <br>
- [WakaTime Summaries API](https://wakatime.com/developers#summaries) <br>
- [ClawHub WakaTime Skill](https://clawhub.ai/chensoul/wakatime-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WAKATIME_API_KEY. Queries are read-only against WakaTime cloud, and returned statistics may include private project, machine, editor, dependency, and work-pattern information.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
