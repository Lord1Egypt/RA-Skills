## Description: <br>
Read, manage, share, upload, and download OneDrive files via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to give an agent command-line access to OneDrive, OneDrive for Business, and SharePoint document libraries for browsing, file transfer, metadata inspection, sharing, and permission management through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses broad Microsoft Graph permissions and persistent OAuth credentials that can provide read/write access to OneDrive and SharePoint content. <br>
Mitigation: Use a dedicated Microsoft app registration, grant the narrowest scopes that fit the task, isolate the runtime, protect ~/.onedrive-mcp/config.json and credentials.json, and revoke the app or refresh tokens when no longer needed. <br>
Risk: Commands can delete, move, upload, share, invite, revoke, or target non-default drives. <br>
Mitigation: Review the exact command, drive prefix, item identifiers, recipients, and sharing scope before execution; prefer read-only or test accounts for exploration. <br>
Risk: The bootstrap path can make unrelated host-level changes. <br>
Mitigation: Avoid the bootstrap script unless those changes are acceptable, or remove the openclaw process stop, /root permission change, and bashrc edit before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trendex/trendex-onedrive) <br>
- [Microsoft Graph OneDrive overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive) <br>
- [DriveItem resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem) <br>
- [Large file upload](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession) <br>
- [Sharing concepts](https://learn.microsoft.com/en-us/graph/api/resources/sharing) <br>
- [Microsoft Graph OneDrive API Reference](references/api-reference.md) <br>
- [OAuth Scopes and Permissions](references/permissions.md) <br>
- [OneDrive Manual Setup Guide](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, code, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read, create, modify, delete, share, invite, revoke, upload, and download cloud files according to the configured Microsoft Graph token and scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
