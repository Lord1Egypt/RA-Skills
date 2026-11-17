## Description:

Provides step-by-step automation for uploading files through agent-browser CLI, with fallback strategies, path normalization, and upload verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m1ss-cell](https://clawhub.ai/user/m1ss-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser-based file uploads when they have an explicit destination page and local file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to arbitrary web pages without built-in destination limits.

Mitigation: Use it only with an explicit destination page and exact file path, and require confirmation before upload.

Risk: Sensitive files could be uploaded if the agent is given a secret, credential, private document, or untrusted destination.

Mitigation: Avoid using it for sensitive files or untrusted sites unless allowlists and sensitive-file checks are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m1ss-cell/skills/upload-file)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and a Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an explicit destination URL and file path; uses agent-browser CLI for browser actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
