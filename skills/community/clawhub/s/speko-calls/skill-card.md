## Description:

Place and monitor outbound AI phone calls through Speko.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speko](https://clawhub.ai/user/speko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to place, monitor, and retrieve reports for outbound AI phone calls through Speko when dialing has been explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound calls can ring real recipients, incur cost, and cannot be recalled after connection.

Mitigation: Require explicit per-call confirmation of the E.164 number and purpose, check local destination time, and stop after one call unless the user authorizes additional numbers one at a time.

Risk: The Speko platform key enables higher-impact dialing operations and could be exposed through logged shell commands.

Mitigation: Use the key only from an approved environment variable, keep it least-privileged and rotated, and avoid pasting it directly into commands or logs.

Risk: Unsafe call-ID handling in status and report examples could alter request URLs or expose credentials.

Mitigation: Validate call IDs as UUIDs and quote the full URL before running status or report commands.

Risk: Call reports and structured data can include dialed phone numbers, transcripts, cost, and other sensitive call details.

Mitigation: Apply redaction and retention controls to reports, transcripts, structured data, and logs before sharing or storing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/speko/skills/speko-calls)
- [Speko publisher profile](https://clawhub.ai/user/speko)
- [Speko API base URL](https://api.speko.dev/v1)
- [Speko phone numbers endpoint](https://api.speko.dev/v1/phone-numbers)
- [Speko phone session endpoint](https://api.speko.dev/v1/sessions/phone)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and SPEKO_PLATFORM_API_KEY; outputs may include call status, reports, transcripts, and cost fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
