## Description: <br>
Fetch productivity data from RescueTime when the user asks about screen time, productivity score, app usage, time tracking, how they spent their day or week, or reports on computer activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rusynandriy](https://clawhub.ai/user/rusynandriy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and productivity-focused developers use this skill to ask an agent for RescueTime activity reports, daily summaries, productivity breakdowns, and app or category usage analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A RescueTime API key can expose productivity-report access if it is committed, logged, or shared. <br>
Mitigation: Keep the key out of source control and shared logs, and redact it before sharing transcripts or screenshots. <br>
Risk: Detailed activity reports can reveal sensitive work habits, app usage, websites, documents, or time patterns. <br>
Mitigation: Request only the date ranges and report dimensions needed, and redact detailed activity results before sharing. <br>


## Reference(s): <br>
- [RescueTime API key management](https://www.rescuetime.com/anapi/manage) <br>
- [RescueTime analytic data endpoint](https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=activity) <br>
- [RescueTime daily summary feed](https://www.rescuetime.com/anapi/daily_summary_feed?key=API_KEY) <br>
- [ClawHub skill page](https://clawhub.ai/rusynandriy/rescuetime) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RescueTime API key supplied outside source control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
