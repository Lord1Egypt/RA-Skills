## Description: <br>
Push high-risk ClawVault security events and daily security reports through OpenClaw agent messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martin2877](https://clawhub.ai/user/martin2877) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators and developers using ClawVault use this skill to configure OpenClaw delivery, send high-risk alerts, and generate daily security reports from local dashboard data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw delivery can forward alerts to external communication channels if configured. <br>
Mitigation: Send a test message first and confirm the configured agent, session, channel, and reply target route only to trusted destinations. <br>
Risk: Optional input previews or file paths can expose sensitive operational details in notifications. <br>
Mitigation: Keep verbose fields disabled unless the destination is trusted and the workflow requires those details. <br>
Risk: The skill stores alert configuration, state, process IDs, and logs on the local machine. <br>
Mitigation: Keep ~/.ClawVault/openclaw-alerts/ local and out of source control or shared archives. <br>


## Reference(s): <br>
- [ClawVault homepage](https://github.com/tophant-ai/ClawVault) <br>
- [ClawHub skill page](https://clawhub.ai/martin2877/tophant-clawvault-openclaw-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Human-readable command output, JSON status/report output, and redacted OpenClaw notification messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local configuration, daemon state, deduplication state, and logs under ~/.ClawVault/openclaw-alerts/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
