## Description:

Quark helps agents operate Quark Drive through a Python CLI for QR login, file listing and search, uploads, downloads, sharing, transfer-save, delete, and batch-upload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imeiming](https://clawhub.ai/user/imeiming)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to manage Quark Drive files, folders, shares, and transfers from agent workflows. It is suited for account-scoped file operations such as listing, uploading, downloading, deleting, sharing, cancelling shares, saving shared resources, and batch uploading directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Quark account cookies can grant account access if exposed or stored insecurely.

Mitigation: Use an isolated environment, prefer QUARK_COOKIE, protect or remove ~/.hermes/skills/cloud-drive/quark/config.json, and clear stored cookies when they are no longer needed.

Risk: Batch upload can unintentionally copy broad local directories or secrets into Quark Drive.

Mitigation: Review source directories before upload, use skip and size filters, and avoid broad paths such as ~/.hermes unless secrets have been checked.

Risk: Share, delete, clear, permanent-share, and confirmation-bypass actions can expose or remove cloud-drive data.

Mitigation: Confirm target paths and share settings before execution, and use confirmation bypass only after the operation has been reviewed.

## Reference(s):

- [ClawHub Quark Release Page](https://clawhub.ai/imeiming/skills/quark-drive)
- [Quark Drive QR Login Flow](references/auth.md)
- [Quark Drive Upload API Notes](references/upload-api.md)
- [Quark Drive Share and Transfer-Save API](references/share-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Python CLI actions against Quark Drive; outputs depend on account state, credentials, network access, and the selected command.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
