## Description:

Manage a user-provided QingLong panel through its REST API for cron jobs, environment variables, scripts, dependencies, subscriptions, logs, and system operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nnnnzs](https://clawhub.ai/user/nnnnzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent administer their own self-hosted QingLong panel, including scheduled tasks, environment variables, scripts, dependencies, subscriptions, logs, and selected system actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad administrative control over a QingLong panel.

Mitigation: Install it only when agent administration is intended, list resources before changes, confirm destructive actions, and grant only the QingLong API scopes needed for the task.

Risk: The skill relies on long-lived QingLong API credentials and cached bearer tokens.

Mitigation: Use HTTPS, restrict API access to trusted hosts, avoid showing tokens in shared logs, and rotate the client secret if it may have been exposed.

Risk: System, dependency, and script scopes can enable high-impact operations on the target panel.

Mitigation: Avoid granting system, dependencies, or scripts scopes unless they are required for the intended workflow.

## Reference(s):

- [QingLong Skill Setup Guide](references/setup.md)
- [QingLong API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/nnnnzs/skills/qinglong-skills)
- [QingLong upstream project](https://github.com/whyour/qinglong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, QINGLONG_URL, QINGLONG_CLIENT_ID, and QINGLONG_CLIENT_SECRET.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
