## Description:

Manage Trello boards, lists, and cards via the Trello REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjcloud](https://clawhub.ai/user/hjcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Trello REST API commands for listing boards, lists, and cards and for creating, moving, commenting on, or archiving cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trello API credentials may be exposed because commands place the API key and token in command-line URLs.

Mitigation: Use a dedicated Trello token with the narrowest practical access, avoid shell tracing or verbose command logging, and revoke the token if exposure is suspected.

Risk: The skill can prepare commands that create, move, comment on, or archive Trello cards.

Mitigation: Review the proposed Trello action and target board, list, or card before execution, especially in shared or production workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjcloud/skills/testjeff)
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello API key setup](https://trello.com/app-key)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
