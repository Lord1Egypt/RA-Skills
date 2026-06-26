## Description: <br>
OpenClaw skill for sending and retrieving SMS messages via the VoIP.ms API (no Bitwarden dependency). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccormier](https://clawhub.ai/user/ccormier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send SMS messages from a VoIP.ms DID and retrieve recent SMS messages through the VoIP.ms API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with VoIP.ms credentials can send SMS messages from the configured account. <br>
Mitigation: Use a dedicated SMS-only VoIP.ms API sub-account and verify the destination and message before sending. <br>
Risk: Retrieved SMS messages can contain private or sensitive data. <br>
Mitigation: Treat retrieved SMS output as private data and limit access to users and agents that need it. <br>
Risk: Using main VoIP.ms admin credentials would increase account impact if credentials are exposed. <br>
Mitigation: Avoid main admin credentials and provide only the required API environment variables for the task. <br>


## Reference(s): <br>
- [VoIP.ms REST API endpoint](https://voip.ms/api/v1/rest.php) <br>
- [ClawHub skill page](https://clawhub.ai/ccormier/voipms-sms) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOIPMS_API_USERNAME and VOIPMS_API_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and openclaw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
