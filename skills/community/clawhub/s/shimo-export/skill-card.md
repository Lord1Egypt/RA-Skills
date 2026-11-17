## Description:

Shimo Export helps agents authenticate to shimo.im, browse and search Shimo files and team spaces, and export documents in formats such as Markdown, PDF, Word, Excel, PowerPoint, XMind, and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[navyum](https://clawhub.ai/user/navyum)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents working with Shimo documents use this skill to search, browse, and export personal or team-space files. It supports both single-document and batch export workflows when a valid Shimo session credential is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Shimo session credentials and can access account, file metadata, team spaces, and exported document contents.

Mitigation: Install only if granting that access is acceptable, prefer a short-lived SHIMO_COOKIE value, never paste cookie values into conversation, and keep credential storage out of source control.

Risk: Broad batch exports can expose large amounts of personal or team-space document content.

Mitigation: Prefer scoped keyword or folder exports, avoid all-files exports unless explicitly needed, and write exports only to controlled directories.

Risk: The browser proxy login flow intercepts a session cookie locally and is called out by the security evidence as risky until replaced or hardened.

Mitigation: Use the proxy only on a trusted local machine or set a short-lived credential manually through the environment, then remove the credential after use.

Risk: Downloaded export files may contain sensitive Shimo document contents.

Mitigation: Handle exported files according to the user's data classification requirements and delete local copies when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/navyum/skills/shimo-export)
- [Export API Reference](artifact/export/references/api.md)
- [File Management API Reference](artifact/file-management/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Natural-language summaries, JSON script results, and exported document files such as Markdown, PDF, DOCX, XLSX, PPTX, XMind, and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create single-file or batch exports in a user-selected output directory; requires a valid SHIMO_COOKIE credential.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
