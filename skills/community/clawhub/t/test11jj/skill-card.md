## Description:

Manage Trello boards, lists, and cards via the Trello REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjcloud](https://clawhub.ai/user/hjcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Trello board data and prepare Trello card management commands for listing, creating, moving, commenting on, and archiving cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trello API tokens can expose sensitive account access if copied into logs, shared terminals, chats, or tickets.

Mitigation: Use a dedicated Trello token with the narrowest practical scope and avoid exposing expanded credential-bearing URLs.

Risk: Create, move, comment, and archive commands can modify Trello board data when the wrong board, list, or card ID is used.

Mitigation: Verify all board, list, and card IDs before running any modifying command.

Risk: High request volume may hit Trello API rate limits.

Mitigation: Pace repeated requests and retry only after Trello rate limits reset.

## Reference(s):

- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello API key setup](https://trello.com/app-key)
- [ClawHub skill page](https://clawhub.ai/hjcloud/skills/test11jj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
