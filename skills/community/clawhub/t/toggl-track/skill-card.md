## Description:

Helps agents manage Toggl Track time entries, projects, clients, and tags through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams tracking work can ask an agent to find or manage their Toggl Track time entries, projects, clients, and tags. With separate approval, they can set up scheduled or event-driven actions through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account or changing Toggl Track records can grant access or alter business data.

Mitigation: Confirm the intended account and scope before connecting; start with read-only requests and obtain explicit approval for each write or deletion.

Risk: Hosted functions, triggers, and destinations can run persistently or forward account data.

Mitigation: Approve each automation only after reviewing its resource, payload, destination URL, and ongoing behavior.

Risk: Authentication credentials and API results can expose sensitive account information.

Mitigation: Keep credentials out of commands, logs, and destinations; share only the response fields needed for the task.

## Reference(s):

- [Toggl Track API documentation](https://engineering.toggl.com/docs/)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [ClawHub Toggl Track release](https://clawhub.ai/byungkyu/skills/toggl-track)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with command and code examples; API results where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and authorization for the connected Toggl Track account.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
