## Description:

Generate QR codes for URLs, text, WiFi credentials, contact cards, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardodpanda](https://clawhub.ai/user/leonardodpanda)

### License/Terms of Use:


## Use Case:

Developers, operators, marketers, and event teams use this skill to generate scannable QR code examples for links, WiFi credentials, vCards, locations, app downloads, and batch QR workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WiFi QR codes encode network passwords in a form that can be recovered by anyone who can scan the image.

Mitigation: Use WiFi QR codes only for guest or intentionally shared networks and avoid publishing private credentials.

Risk: Generated code depends on third-party Python packages and writes image files to disk.

Mitigation: Install dependencies in an isolated Python environment and review output paths before running generated scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardodpanda/skills/qr-code-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce QR image files when the generated Python examples are run by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
