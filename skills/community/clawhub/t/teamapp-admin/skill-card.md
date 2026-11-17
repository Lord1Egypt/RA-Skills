## Description:

Use when interacting with TeamApp club admin JSON endpoints on teamapp.com to create/read/update News articles and Schedule events, and to resolve Team and Access Group IDs needed for visibility, roster, and targeting fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thed000d](https://clawhub.ai/user/thed000d)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and club administrators use this skill to operate TeamApp club admin JSON endpoints for news, schedule events, teams, and access groups. It supports authenticated API calls, ID resolution, payload construction, notification controls, and verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live TeamApp admin sessions and may expose credentials or session files.

Mitigation: Use a low-privilege TeamApp account where possible, keep TA_AUTH_TOKEN out of shared logs, and clear temporary cookie and CSRF files after use.

Risk: The skill can make unintended administrative changes, including publishing content, notifying users, changing teams or access groups, and using archive or delete endpoints.

Mitigation: Require explicit confirmation before write, notification, team/access-group, archive, or delete operations, then verify changes by reloading the relevant list endpoint.

Risk: Passing a non-TeamApp URL to the wrapper could send TeamApp session credentials to the wrong host.

Mitigation: Only pass trusted teamapp.com URLs to the wrapper.

## Reference(s):

- [TeamApp Admin JSON API Map](references/api-map.md)
- [TeamApp home](https://www.teamapp.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and form-field examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TeamApp authentication cookie and routes API requests through the provided wrapper.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
