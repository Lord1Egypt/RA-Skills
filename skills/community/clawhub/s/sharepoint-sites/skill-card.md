## Description: <br>
Microsoft SharePoint and OneDrive integration with managed OAuth for managing sites, lists, libraries, files, folders, permissions, content types, and SharePoint operations via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and site administrators use this skill to work with SharePoint and OneDrive content through ClawLink-managed Microsoft OAuth, including site discovery, list and library operations, file workflows, permissions, sharing links, search, and site management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to the connected Microsoft account and can access SharePoint and OneDrive resources available to that account. <br>
Mitigation: Use a least-privileged Microsoft account where possible and review requested Microsoft permissions during OAuth connection. <br>
Risk: The skill supports write, delete, sharing-link, and permission-change operations that can alter content or access controls. <br>
Mitigation: Confirm the target resource and intended effect before writes, deletes, sharing-link creation, or permission changes. <br>


## Reference(s): <br>
- [ClawHub SharePoint Skill](https://clawhub.ai/hith3sh/sharepoint-sites) <br>
- [ClawLink Dashboard](https://claw-link.dev/dashboard?add=sharepoint) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [Microsoft Graph SharePoint API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint) <br>
- [Microsoft Graph List Resource](https://learn.microsoft.com/en-us/graph/api/resources/list) <br>
- [SharePoint Permissions](https://learn.microsoft.com/en-us/sharepoint/how-to-set-up-and-configure-sharepoint-add-ins) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include SharePoint and OneDrive operational guidance, ClawLink setup commands, and JSON-style parameters for live tool calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
