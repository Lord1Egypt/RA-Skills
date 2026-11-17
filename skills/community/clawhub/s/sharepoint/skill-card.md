## Description:

Helps agents access SharePoint sites, lists, document libraries, and files through Microsoft Graph using a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to find and manage SharePoint sites, lists, and files, and to set up approved SharePoint automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected account can expose sensitive SharePoint content within its granted permissions.

Mitigation: Review Microsoft and Maton scopes, use the narrowest connection needed, and prefer read-only access.

Risk: Writing, deleting, or sharing content can change access or cause data loss.

Mitigation: Confirm the specific target and effect with the user before each write, delete, or share action.

Risk: Trigger destinations can keep forwarding future event data until removed.

Mitigation: Require separate approval for each destination, verify its recipient and event scope, and remove it when no longer needed.

## Reference(s):

- [ClawHub SharePoint skill](https://clawhub.ai/byungkyu/skills/sharepoint)
- [Maton](https://maton.ai)
- [Microsoft Graph SharePoint sites](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint)
- [Microsoft Graph drive items](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [Microsoft Graph lists](https://learn.microsoft.com/en-us/graph/api/resources/list)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell, JSON, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and list operations are preferred; changes and new connections require user confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
