## Description: <br>
Secure SharePoint file operations and Office document intelligence via Microsoft Graph API with certificate authentication, Sites.Selected permissions, and Office/PDF text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, search, read, upload, edit, and manage files in a configured SharePoint document library, including extracting text from Office and PDF documents for downstream AI work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, upload, edit, delete, check out, check in, and create organization edit links for SharePoint files. <br>
Mitigation: Use a dedicated Entra app with Sites.Selected, grant only the minimum site-level permission needed, and require human review for upload, delete, checkout, checkin, edit, and organization edit-link creation. <br>
Risk: Certificate credentials and optional passwords grant access to the configured SharePoint site if exposed. <br>
Mitigation: Protect the certificate and optional password, keep secrets out of logs, rotate credentials when needed, and install dependencies with the lockfile. <br>
Risk: Incorrect site or drive configuration could expose or modify unintended SharePoint content. <br>
Mitigation: Validate SP_SITE_ID and optional SP_DRIVE_ID before use and prefer a dedicated SharePoint site with least-privilege access. <br>


## Reference(s): <br>
- [ClawHub release: SharePoint by altf1be](https://clawhub.ai/Abdelkrim/sharepoint-by-altf1be) <br>
- [Publisher profile: Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>
- [Skill homepage](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint) <br>
- [Microsoft SharePoint](https://www.microsoft.com/en-us/microsoft-365/sharepoint/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output from the SharePoint CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SP_TENANT_ID, SP_CLIENT_ID, SP_CERT_PATH, and SP_SITE_ID; optional SP_DRIVE_ID, SP_CERT_PASSWORD, and SP_MAX_FILE_SIZE.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
