## Description:

Generates QR codes locally for text, URLs, WiFi connections, and vCard business cards, with optional custom PNG output paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyangabel](https://clawhub.ai/user/ouyangabel)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create QR code PNG files for websites, arbitrary text, WiFi sharing, and digital business cards without relying on an external API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WiFi QR codes encode the network password and can expose it through saved PNG files, shell history, terminal logs, or shared images.

Mitigation: Treat WiFi QR outputs as secrets, store them only where intended recipients can access them, and remove command history or generated files when they are no longer needed.

Risk: Dependency installation can affect the local Python or operating-system environment.

Mitigation: Install dependencies in a virtual environment where possible and avoid sudo-based package installation unless the OS repository and environment are trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated QR codes are PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are saved locally, with a default output path of ~/qrcode_output.png when no path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
