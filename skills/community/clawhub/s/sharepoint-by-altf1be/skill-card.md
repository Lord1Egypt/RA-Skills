## Description:

Secure SharePoint file operations and Office document intelligence via Microsoft Graph API - certificate auth, Sites.Selected, read/write Word (mammoth), Excel (exceljs), PowerPoint (jszip), PDF (pdf-parse).

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT

## Use Case:

Developers and employees use this skill to browse, read, upload, search, edit, and manage files in a tightly scoped SharePoint document library through Microsoft Graph. It is useful for extracting text from Office and PDF documents so an agent can summarize, reformat, or prepare follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create organization-wide edit links for SharePoint files.

Mitigation: Install it only for a tightly scoped SharePoint site and review or disable the edit-link command when tenant policy requires user-specific or view-only links.

Risk: Office and PDF parsing may process untrusted SharePoint content with limited resource controls.

Mitigation: Keep document parsing isolated, enforce file size limits, and update dependencies before using the skill on untrusted files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdelkrim/skills/sharepoint-by-altf1be)
- [Microsoft SharePoint](https://www.microsoft.com/en-us/microsoft-365/sharepoint/)
- [Publisher Profile](https://clawhub.ai/user/abdelkrim)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SharePoint tenant, app, certificate, and site identifiers; default file size limit is 50 MB.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
