## Description:

Upload files such as images, PDFs, and documents to tmpfiles.org and produce temporary download links for sharing through messaging platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to upload a user-selected file to tmpfiles.org and return a temporary public download link, especially when direct upload to a messaging platform is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files are publicly accessible while active.

Mitigation: Confirm the exact file path before upload and avoid confidential documents, private screenshots, or other sensitive files.

Risk: Anyone with a generated link may access the file until it expires.

Mitigation: Share links only with intended recipients and use the workflow for short-lived, non-sensitive transfers.

## Reference(s):

- [Tmpfiles Upload ClawHub Page](https://clawhub.ai/turbos7/skills/tmpfiles-upload)
- [tmpfiles.org upload API endpoint](https://tmpfiles.org/api/v1/upload)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, bash, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces temporary public download links; users should avoid uploading confidential or private files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
