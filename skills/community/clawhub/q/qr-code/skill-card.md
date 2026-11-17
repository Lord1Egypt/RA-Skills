## Description:

Generate and read QR codes from text, URLs, screenshots, or image files, with support for PNG/JPG images and configurable generation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omar-khaleel](https://clawhub.ai/user/omar-khaleel)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to generate QR code image files from supplied text or URLs and to decode QR payloads from user-provided images or screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions may drift across environments, which can affect reproducibility.

Mitigation: Install the Python dependencies in a virtual environment and pin versions for controlled deployments.

Risk: Packaged script locations may differ from the documented command paths.

Mitigation: Adjust command paths to the artifact root or provide wrappers before using the documented examples.

Risk: Decoded QR payloads can contain untrusted text or URLs.

Mitigation: Review decoded content before opening links or passing payloads into other systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omar-khaleel/skills/qr-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the QR reader]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG image files for generated QR codes and may return decoded QR payloads as text or JSON.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
