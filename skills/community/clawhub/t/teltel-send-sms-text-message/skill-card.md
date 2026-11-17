## Description:

Send SMS text messages via TelTel (teltel.io) using the REST API (api.teltel.io). Includes bulk send, delivery report, and bulk sms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teltel-call-center](https://clawhub.ai/user/teltel-call-center)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent prepare and run TelTel SMS sends for individual recipients or bulk recipient lists after the TelTel account, sender, and API key are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution sends recipient phone numbers and message content to TelTel and may incur account charges.

Mitigation: Use dry-run first, require explicit user approval for live sends and bulk sends, and avoid sending sensitive message content unless the user confirms it is appropriate.

Risk: Exposure of TELTEL_API_KEY could allow unauthorized SMS sends from the TelTel account.

Mitigation: Keep TELTEL_API_KEY in the approved secret store or environment, do not echo it in prompts or logs, and verify TELTEL_BASE_URL is trusted before execution.

## Reference(s):

- [TelTel homepage](https://www.teltel.io/)
- [TelTel API base URL](https://api.teltel.io/v2)
- [ClawHub skill page](https://clawhub.ai/teltel-call-center/skills/teltel-send-sms-text-message)
- [Publisher profile](https://clawhub.ai/user/teltel-call-center)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run output for URL and payload preview; live runs send SMS through TelTel and may return parsed JSON or raw response text.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
