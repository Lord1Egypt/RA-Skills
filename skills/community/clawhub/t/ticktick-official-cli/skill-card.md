## Description:

Uses official Dida365 OAuth and Open API access to manage projects and tasks, including querying, creating, updating, completing, and deleting items without a third-party OAuth relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superowenx](https://clawhub.ai/user/superowenx)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to authenticate with Dida365 and manage task and project workflows through official API-backed shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials and tokens can expose sensitive Dida365 tasks or projects if local config files or command output are shared.

Mitigation: Restrict permissions on ~/.config/ticktick-official, avoid including token-bearing output in logs or transcripts, and revoke exposed tokens immediately.

Risk: Delete commands can permanently change projects or tasks in the connected Dida365 account.

Mitigation: Require explicit user approval before running project or task delete commands.

Risk: Using a non-official API base URL could send account credentials or task data to an unintended endpoint.

Mitigation: Use only the official Dida365 API base URL unless the user has explicitly verified an alternative endpoint.

## Reference(s):

- [Dida365 Open API](references/dida365-openapi.md)
- [Dida365 Developer Center](https://developer.dida365.com/manage)
- [Dida365 Open API Base URL](https://api.dida365.com/open/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or table CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local OAuth setup instructions and Dida365 API response data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
