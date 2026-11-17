## Description:

Transfers credentials between networked and air-gapped devices using QR codes as an optical channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifehackjohn](https://clawhub.ai/user/lifehackjohn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate QR codes from credentials for air-gapped devices and to decode credential QR codes from images. It is intended for controlled credential transfer workflows where network transfer is unavailable or undesired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords can be exposed through shell history, stdout, chat logs, browser state, temporary files, or displayed QR codes.

Mitigation: Use only in physically controlled settings, avoid real passwords in shell commands or prompts, redact credential output, and prefer short-lived or one-time credentials.

Risk: Generated QR images and captured images may persist after use.

Mitigation: Delete generated or captured images immediately after the credential transfer is complete.

Risk: The offline HTML generator keeps the password field value after QR generation in the current artifact.

Mitigation: Clear the browser form and close the page after use, and avoid relying on browser state as a secret channel.

## Reference(s):

- [QR Password ClawHub page](https://clawhub.ai/lifehackjohn/skills/qr-password)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; QR image files and decoded JSON credential objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated QR images and decoded credentials should be treated as sensitive and removed or redacted after use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
