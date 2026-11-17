## Description:

Create, manage, and track QR codes using the QRdex.io REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastienb](https://clawhub.ai/user/sebastienb)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to create, list, update, delete, download, and track QR codes through the QRdex.io REST API, including URL, email, telephone, SMS, WhatsApp, and WiFi QR code types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR payloads and the QRDEX_API_KEY are sent to QRdex.io when API operations are performed.

Mitigation: Use the skill only when QRdex.io is trusted with the submitted QR data and keep the API key scoped and protected.

Risk: The skill can update or soft-delete QR codes when those actions are requested.

Mitigation: Confirm target QR code identifiers and intended changes before allowing update or delete operations.

Risk: Scan analytics may be enabled through track_scans.

Mitigation: Set track_scans deliberately when scan tracking is not desired.

## Reference(s):

- [QRdex API Reference](references/API_REFERENCE.md)
- [QRdex ClawHub Skill Page](https://clawhub.ai/sebastienb/skills/qrdex)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python CLI usage, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke QRdex.io API operations that create, update, soft-delete, list, or download QR code resources when the user supplies credentials and requests those actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
