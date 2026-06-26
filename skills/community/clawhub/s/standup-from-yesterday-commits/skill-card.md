## Description: <br>
Generates a 30-second Slack-ready standup update from yesterday's GitHub commits, PR activity, reviews, and Jira tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabgpt](https://clawhub.ai/user/rabgpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill before daily standup to gather their recent GitHub and Jira activity and synthesize it into concise yesterday, today, and blockers bullets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Standup drafts may expose GitHub or Jira work details if posted to the wrong Slack workspace, channel, or audience. <br>
Mitigation: Preview the message, confirm the destination and audience, and redact sensitive repository or ticket details before posting. <br>
Risk: Scheduled or automatic posting can share recurring updates without a fresh review. <br>
Mitigation: Avoid auto-posting unless the workspace, channel, audience, and preview behavior have been intentionally approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rabgpt/standup-from-yesterday-commits) <br>
- [Implexa homepage](https://implexa.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Slack mrkdwn with yesterday, today, and blockers sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise bullets intended for a roughly 30-second standup update; each bullet should be 12 words or fewer.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
