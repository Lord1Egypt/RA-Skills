## Description:

Share one local file through a public download URL or QR code using CNB uploads by default, with 3-day retention and immediate manual deletion, or an optional TryCloudflare tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steinvenic](https://clawhub.ai/user/steinvenic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users share a selected local file through a public download link or QR code, either by uploading it to CNB or by serving it through a temporary tunnel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default uploads begin immediately and expose the selected file through a public link without access control.

Mitigation: Confirm the file is approved for public sharing and encrypt sensitive files before upload.

Risk: Tunnel mode may expose other files in the same folder, not just the selected file.

Mitigation: Avoid --cf until the server is fixed to serve only the selected file.

Risk: The CNB upload path uses an embedded shared bearer token with broad remote asset authority.

Mitigation: Review before installing; the publisher should rotate or remove the token and use scoped, short-lived upload and delete authority.

## Reference(s):

- [ClawHub qshare release](https://clawhub.ai/steinvenic/skills/qshare)
- [qshare source repository (server-resolved provenance)](https://github.com/steinvenic/qshare)
- [qshare package on PyPI](https://pypi.org/project/qshare/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and a public file URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can display a QR code. Kept CNB uploads have a default three-day retention; tunnel links expire or stop with the tunnel.]

## Skill Version(s):

0.1.1 (source: ClawHub release; package files declare 0.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
