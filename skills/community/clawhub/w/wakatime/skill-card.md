## Description: <br>
WakaTime API integration with managed OAuth for retrieving coding statistics, productivity metrics, language and editor usage, and daily summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect WakaTime coding activity, project time, language and editor breakdowns, goals, insights, and daily summaries from chat through a managed OAuth connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read privacy-sensitive WakaTime analytics, including project names, machine names, coding activity, and workplace patterns. <br>
Mitigation: Scope agent requests to the specific project, date range, or metric needed, and avoid sharing returned data that exposes private clients, machines, or activity patterns. <br>
Risk: OAuth scopes may be insufficient for summaries or goals, causing partial or failed responses. <br>
Mitigation: Reconnect the WakaTime account through ClawLink when scope-related errors occur, and request only the scopes needed for the intended read-only analysis. <br>
Risk: Coding time values returned by the API may differ from WakaTime dashboard totals. <br>
Mitigation: Treat API results as operational analytics and verify important totals against the WakaTime dashboard before using them for reporting. <br>


## Reference(s): <br>
- [ClawHub WakaTime Skill](https://clawhub.ai/hith3sh/wakatime) <br>
- [WakaTime API Docs](https://wakatime.com/developers) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command snippets, tool-call examples, and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only WakaTime API access through managed OAuth; results can include privacy-sensitive project, machine, editor, language, and activity-pattern data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
