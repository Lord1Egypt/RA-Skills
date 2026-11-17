## Description:

Generate and read QR codes from text, URLs, screenshots, and image files, with PNG/JPG support and configurable generation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omar-khaleel](https://clawhub.ai/user/omar-khaleel)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to create QR codes from provided content and decode QR codes from local images or screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies or missing native QR decoding libraries can change behavior or fail at runtime.

Mitigation: Install the skill in a controlled Python environment with pinned dependency versions and the required platform zbar components.

Risk: Decoded QR payloads may contain misleading links, commands, or other untrusted text.

Mitigation: Inspect decoded output before acting on it, prefer JSON output for unfamiliar QR codes, and do not open links or run commands solely because a QR payload suggests them.

## Reference(s):

- [Advanced QR Intelligence on ClawHub](https://clawhub.ai/omar-khaleel/skills/qr-code-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, PNG file outputs, and optional JSON decode results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated QR codes are written as image files; decoded QR payloads should be treated as untrusted text.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
