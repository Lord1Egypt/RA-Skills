## Description:

Read-only Trello planner using the official Trello Boards API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomas-mikula](https://clawhub.ai/user/tomas-mikula)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with a read-scoped Trello token to inspect Trello boards, open cards, overdue work, and basic board health signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Trello token can expose board data visible to that token, including board names and card metadata.

Mitigation: Use a read-only token with the shortest practical expiration and restrict the token to accounts or workspaces appropriate for this skill.

Risk: Default board selection and broad board enumeration may surface data from an unintended Trello board.

Mitigation: Pass an explicit board_id when using the skill for sensitive workspaces.

Risk: Credential-bearing Trello URLs can leak key or token values if copied into logs, tickets, or chat.

Mitigation: Avoid sharing full Trello URLs that include key or token query parameters.

Risk: Advertised optimization, search, and capacity features are broader than the implementation evidence supports.

Mitigation: Treat generated planning and optimization output as lightweight guidance until the implementation is updated and reviewed.

## Reference(s):

- [Atlassian Trello Boards REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)
- [Atlassian Trello Actions REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)
- [Trello API Key](https://trello.com/app-key)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON status object with board metrics, overdue-card counts, planner insights, and health status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Trello API credentials and performs read-only requests to api.trello.com.]

## Skill Version(s):

1.0.8 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
