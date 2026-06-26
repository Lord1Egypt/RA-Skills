## Description: <br>
Create, manage, and track QR codes using the QRdex.io REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastienb](https://clawhub.ai/user/sebastienb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use QRdex to create, list, inspect, update, delete, and download QR codes through the QRdex.io API, including URL, email, telephone, SMS, WhatsApp, and WiFi QR code workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a QRdex.io account using QRDEX_API_KEY, including creating, updating, deleting, and downloading QR code assets. <br>
Mitigation: Use a revocable API key with the least account access available, keep it in the environment rather than prompts or files, and rotate it if exposed. <br>
Risk: Update and delete actions operate on QR code IDs and can affect existing team QR codes. <br>
Mitigation: Confirm the target QR code ID and intended operation before running update or delete commands. <br>
Risk: QR payloads and scan tracking can expose sensitive data such as WiFi passwords, phone numbers, messages, destinations, or scan activity. <br>
Mitigation: Avoid storing sensitive QR payloads or enabling tracking unless that storage and exposure are acceptable for the account and use case. <br>


## Reference(s): <br>
- [QRdex API Reference](references/API_REFERENCE.md) <br>
- [QRdex API Base URL](https://qrdex.io/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/sebastienb/qrdex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, Python CLI usage, JSON API examples, and SVG file download instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses QRDEX_API_KEY for authenticated QRdex.io requests and may produce QR metadata, command output, JSON responses, or downloaded SVG files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
