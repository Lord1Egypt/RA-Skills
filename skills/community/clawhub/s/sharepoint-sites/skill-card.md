## Description:

Microsoft SharePoint and OneDrive integration with managed OAuth. Manage sites, lists, libraries, files, folders, permissions, content types, and SharePoint operations via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to connect an agent to SharePoint and OneDrive through ClawLink-managed OAuth, then discover sites, manage lists and document libraries, work with files and folders, and perform permissions or content operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external plugin that handles Microsoft OAuth and SharePoint requests.

Mitigation: Review the ClawLink plugin and OAuth consent before installing, and install only if the hosted third-party integration is acceptable for the environment.

Risk: The connected account may expose broad SharePoint write, delete, sharing, and permission operations.

Mitigation: Use an account with the minimum SharePoint permissions needed, and confirm every write, delete, sharing, or permission-changing action before execution.

## Reference(s):

- [ClawHub SharePoint Skill](https://clawhub.ai/hith3sh/skills/sharepoint-sites)
- [Microsoft Graph SharePoint API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint)
- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-in/set-up-a-sharepoint-add-in-development-environment)
- [SharePoint Permissions](https://learn.microsoft.com/en-us/sharepoint/how-to-set-up-and-configure-sharepoint-add-ins)
- [Working with Lists and List Items](https://learn.microsoft.com/en-us/graph/api/resources/list)
- [Sharing and Permissions in SharePoint](https://learn.microsoft.com/en-us/graph/api/resources/permission)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, OAuth connection, SharePoint operation guidance, and confirmation guidance for write or permission-changing actions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
