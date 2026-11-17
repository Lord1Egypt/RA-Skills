## Description:

Generate QR code for Wi-Fi credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and other users use this skill to generate a QR code that lets phones join a Wi-Fi network without manually typing the password.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wi-Fi passwords and generated QR codes can expose network access if logged, shared, or displayed publicly.

Mitigation: Avoid using real passwords in logged commands, avoid screen sharing generated QR codes, and rotate the Wi-Fi password if exposure is suspected.

Risk: The skill depends on the external qrencode binary installed through the system package manager.

Mitigation: Install qrencode only from a trusted package source and confirm the binary is available before using the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires qrencode and handles Wi-Fi credentials that should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
