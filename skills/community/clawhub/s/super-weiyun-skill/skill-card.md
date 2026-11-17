## Description:

This skill helps an agent manage Tencent Weiyun cloud storage, including account authentication, uploads, downloads, sharing, file operations, space management, and recycle-bin actions through a Python CLI and SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate Tencent Weiyun file management from an agent workflow or Python environment. Typical tasks include logging in with QR code or cookies, uploading and downloading files or folders, creating share links, checking storage usage, and managing recycle-bin recovery or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tencent Weiyun account cookies and can save them locally.

Mitigation: Prefer QR login, avoid passing cookies on the command line, restrict access to cookies.json, and delete saved cookies after use.

Risk: Downloads, recursive folder downloads, and overwrite options can write or replace local files.

Mitigation: Download only from trusted Weiyun folders, choose explicit destination paths, and review --overwrite before running commands.

Risk: Delete, permanent delete, recycle-bin clearing, and share-link operations can expose or remove cloud files.

Mitigation: Review target paths, share settings, and destructive flags before execution, especially for permanent deletion and public sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-weiyun-skill)
- [Tencent Weiyun](https://www.weiyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON-style operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local files such as downloaded content, uploaded file manifests, QR code images, and cookies.json when the user runs the provided commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
