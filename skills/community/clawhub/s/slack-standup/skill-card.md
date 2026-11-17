## Description:

Automates Slack daily standups by prompting updates, compiling responses, and posting summaries on a set schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allanwei](https://clawhub.ai/user/allanwei)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and developers use this skill to automate asynchronous Slack standups, send reminders, collect status updates, and post formatted summaries to a chosen Slack channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships risky credential handling, including a packaged hardcoded Slack bot token value.

Mitigation: Use a newly created, least-privileged Slack bot token from a secure environment variable, remove or replace the packaged token value, and rotate any token that may have been exposed.

Risk: The test path can make live Slack posts.

Mitigation: Treat /standup test and script test mode as live posting; test only in a dedicated channel or workspace unless the package is changed to dry-run.

Risk: The setup guidance includes broad Slack scopes such as chat:write.public and channels:read.

Mitigation: Avoid chat:write.public and channels:read unless the workspace use case truly requires them; start with least-privileged Slack scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allanwei/skills/slack-standup)
- [Slack Bot Setup](artifact/references/SETUP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and Slack message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Slack API calls that post messages when its scripts are run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
