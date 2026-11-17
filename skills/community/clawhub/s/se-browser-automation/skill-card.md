## Description:

Browser automation patterns and best practices for OpenClaw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boris148](https://clawhub.ai/user/boris148)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to navigate web applications, fill forms, interact with iframe-heavy SPAs, handle login flows, and troubleshoot browser snapshots and screenshots in OpenClaw-managed browsers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents through login flows that involve credentials or two-factor codes.

Mitigation: Use only accounts the operator controls or is authorized to access, and provide credentials or 2FA codes only through approved secure channels.

Risk: Screenshots, snapshots, or logs from automated browsing can expose secrets or account contents.

Mitigation: Avoid retaining browser artifacts that show sensitive data, and redact or discard screenshots and logs before sharing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with command-style browser actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; guidance covers browser navigation, snapshots, screenshots, iframe handling, login flows, and SPA troubleshooting.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
