## Description: <br>
SharePoint API integration via Microsoft Graph with managed OAuth for accessing SharePoint sites, lists, document libraries, and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make authenticated Microsoft Graph requests through Maton for SharePoint document management, list operations, site discovery, file handling, sharing, and permissions workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton-managed OAuth and MATON_API_KEY to access and modify SharePoint content. <br>
Mitigation: Protect MATON_API_KEY like a password and use the least-privileged SharePoint account practical. <br>
Risk: Write and sharing operations can change files, lists, folders, or permissions in the connected SharePoint account. <br>
Mitigation: Confirm the target resource, intended effect, audience, link scope, and expiration or revocation plan before approving write or sharing operations. <br>


## Reference(s): <br>
- [Microsoft SharePoint Sites API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint) <br>
- [Microsoft Graph DriveItem API](https://learn.microsoft.com/en-us/graph/api/resources/driveitem) <br>
- [Microsoft Graph List API](https://learn.microsoft.com/en-us/graph/api/resources/list) <br>
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline HTTP examples, shell commands, Python snippets, JavaScript snippets, and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
