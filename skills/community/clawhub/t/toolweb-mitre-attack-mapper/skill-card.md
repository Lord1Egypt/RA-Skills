## Description:

Maps threat descriptions, incident reports, or security observations to MITRE ATT&CK techniques, tactics, detection guidance, mitigations, and threat actor associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners and developers use this skill to submit attacker behavior text or security report files and receive mapped MITRE ATT&CK techniques, tactics, detection guidance, mitigation recommendations, Navigator layer output, and threat actor associations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive security reports, incident details, SIEM exports, or threat intelligence files may be sent to an external ToolWeb API.

Mitigation: Submit only data you are authorized to share, redact secrets and unnecessary internal details, and review the provider's privacy, retention, and deletion terms before use.

Risk: API credentials are required for requests to the external service.

Mitigation: Use a revocable, scoped API key and rotate or revoke it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-mitre-attack-mapper)
- [Publisher Profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd)
- [ToolWeb](https://toolweb.in)
- [ToolWeb API Portal](https://portal.toolweb.in)
- [ToolWeb MCP Server](https://hub.toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [ToolWeb RapidAPI Profile](https://rapidapi.com/user/mkrishna477)
- [ToolWeb YouTube Channel](https://youtube.com/@toolweb-009)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with multipart/form-data curl examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include technique IDs, tactics, confidence scores, detection guidance, mitigation recommendations, Navigator layer data, and threat actor associations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
