## Description:

Send files to users in chat by creating temporary public download links via an aitun tunnel for generated documents, images, reports, and code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to deliver generated files to a chat user by hosting a local file temporarily and sharing a browser-accessible download link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-line remote script installers can execute unreviewed code.

Mitigation: Install aitun only through a trusted, reviewed package source and avoid remote script installers unless they have been independently reviewed.

Risk: Serving a directory through a public tunnel can expose unintended local files.

Mitigation: Before sharing, place only the intended file in a dedicated temporary directory, bind the server to loopback when possible, and shut down the tunnel immediately after download.

Risk: Temporary public download links can expose sensitive data if used for secrets, credentials, or private content.

Mitigation: Use this skill only for non-sensitive files and do not share files containing secrets or credentials.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/sendfile)
- [ClawHub package metadata](https://clawhub.ai/ctz168/sendfile)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and a temporary public download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary public links are intended for non-sensitive files and should be shut down after download.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
