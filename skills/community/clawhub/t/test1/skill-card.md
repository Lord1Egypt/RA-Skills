## Description:

Manage Trello boards, lists, and cards via the Trello REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and update Trello boards, lists, cards, and comments from an agent workflow using Trello REST API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trello API keys and tokens can grant broad live account access and may be exposed through command history, process listings, shell tracing, or logs.

Mitigation: Use a dedicated token with the least access practical and avoid running commands in environments that capture command URLs or environment values.

Risk: Create, move, comment, and archive commands change live Trello data.

Mitigation: Confirm the target board, list, card, and requested operation before executing state-changing commands.

## Reference(s):

- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello API key and token page](https://trello.com/app-key)
- [ClawHub skill page](https://clawhub.ai/chaunceyliu/skills/test1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq plus Trello API key and token environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
