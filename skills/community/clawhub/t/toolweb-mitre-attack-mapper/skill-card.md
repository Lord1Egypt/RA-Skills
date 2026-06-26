## Description: <br>
Maps attacker behavior text or uploaded security report files to MITRE ATT&CK techniques, tactics, detection guidance, mitigation recommendations, ATT&CK Navigator layer data, and threat actor associations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and threat intelligence teams use this skill to map incident narratives, SIEM alerts, threat reports, and related files to MITRE ATT&CK techniques and tactics. It helps generate technique IDs, confidence scores, detection guidance, mitigation recommendations, and actor associations for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security reports, logs, or incident details may be sent to an external provider. <br>
Mitigation: Use the skill only with authorization, redact secrets, customer data, internal hostnames, and active investigation details before upload, and use a dedicated revocable API key. <br>
Risk: Mapped techniques, confidence scores, detections, mitigations, and actor associations may be incomplete or incorrect. <br>
Mitigation: Have a qualified security analyst review the results before using them for investigation, reporting, detection engineering, or response decisions. <br>
Risk: API keys used with the ToolWeb endpoint could be exposed through prompts, logs, or shared command examples. <br>
Mitigation: Keep API keys out of shared transcripts and repositories, scope them to this use case where possible, and rotate or revoke them after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-mitre-attack-mapper) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ToolWeb MCP server](https://hub.toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to send text or uploaded security files to ToolWeb's external API and return ATT&CK mappings, detections, mitigations, Navigator layer details, and actor associations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
