## Description: <br>
Automatically generates daily standup reports from Git commits, task updates, chat messages, and calendar events, with Scrum, Kanban, template, and channel delivery support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, scrum masters, and team leads use this skill to draft individual or team standup reports from work activity and share them through workplace channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request broad access to repositories, task trackers, chat, and calendars to assemble standup reports. <br>
Mitigation: Review configured data sources and scopes before installation, use least-privilege tokens, and avoid workspace-wide access where narrower permissions are available. <br>
Risk: The skill can post generated reports to Slack, Teams, Feishu, DingTalk, or email, which may expose sensitive work or personal information. <br>
Mitigation: Require manual review before posting reports, keep automated redaction enabled, and limit destination channels to the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/standup-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown standup reports and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May aggregate configured workplace activity sources and prepare reports for selected destination channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
