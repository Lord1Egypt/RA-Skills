## Description:

Helps agents manage Trello boards, lists, cards, labels, and members through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using Trello can ask an agent to inspect and manage project boards, lists, cards, labels, and members. With separate user approval, they can also set up Maton-hosted functions and triggers for automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trello writes or new connections could change data or grant unintended access.

Mitigation: Confirm each write and new connection with the user; review OAuth scopes and use the least privilege needed.

Risk: Long-lived API keys or exposed credentials could permit unauthorized access.

Mitigation: Prefer the Maton CLI OAuth flow and avoid exposing or storing credentials in commands, files, or trigger destinations.

Risk: Hosted functions and persistent triggers can keep acting or forwarding event data after setup.

Mitigation: Review and confirm automations and destinations before enabling them; remove unused functions and triggers.

## Reference(s):

- [Trello skill on ClawHub](https://clawhub.ai/byungkyu/skills/trello-api)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Trello REST API: boards](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and user authorization for Trello access.]

## Skill Version(s):

1.2.5 (source: ClawHub release; skill frontmatter states 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
