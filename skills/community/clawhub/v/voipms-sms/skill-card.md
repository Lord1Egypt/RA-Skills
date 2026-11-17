## Description:

OpenClaw skill for sending and retrieving SMS messages via the VoIP.ms API (no Bitwarden dependency).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccormier](https://clawhub.ai/user/ccormier)

### License/Terms of Use:


## Use Case:

Developers and operators with VoIP.ms accounts use this skill to send SMS messages from a DID and retrieve recent SMS messages through the VoIP.ms API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS contents and reusable VoIP.ms API credentials can be exposed through request URL logs or terminal output.

Mitigation: Use a dedicated VoIP.ms SMS-only sub-account, avoid sending highly sensitive messages, treat command output as sensitive, prefer POST-body parameters if the API supports them, and rotate credentials if full request URLs may have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccormier/skills/voipms-sms)
- [VoIP.ms API endpoint](https://voip.ms/api/v1/rest.php)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output is JSON or raw API text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOIPMS_API_USERNAME and VOIPMS_API_PASSWORD environment variables; SMS contents and API responses may be sensitive.]

## Skill Version(s):

1.0.1 (source: server release metadata and openclaw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
