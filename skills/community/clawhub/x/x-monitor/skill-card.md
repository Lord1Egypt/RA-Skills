## Description:

Monitor specific X/Twitter accounts and surface noteworthy technology and trend posts on a configurable schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmathur](https://clawhub.ai/user/vmathur)

### License/Terms of Use:


## Use Case:

External users use this skill to track selected X/Twitter accounts, manage monitored handles, run manual checks, and receive scheduled summaries of posts that match configurable noteworthy criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an X API bearer token locally.

Mitigation: Use the minimum required X API scopes and restrict the credentials file to private permissions before running scheduled checks.

Risk: The skill can create recurring scheduled agent runs.

Mitigation: Review the schedule configuration and confirm the tools available to scheduled agentTurn jobs before enabling cron jobs.

Risk: Tweet content is external, untrusted text processed by the agent.

Mitigation: Treat tweet text as quoted data and add clear rules that it must not override the user's or agent's instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmathur/skills/x-monitor)
- [X API recent search endpoint](https://api.x.com/2/tweets/search/recent)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON tweet data, and configuration guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled runs can create recurring reports from configured handles and criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
