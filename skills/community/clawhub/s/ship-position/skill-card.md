## Description:

Gets the latest vessel position from the HiFleet position API after a HiFleet user token is configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleiwang](https://clawhub.ai/user/charleiwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up a vessel's latest position by MMSI and present key AIS-derived details such as vessel name, update time, latitude, longitude, speed, course, destination, and status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a HiFleet user token and documents passing it as a URL query parameter, which can expose the token through chat transcripts, logs, traces, errors, or shared diagnostics.

Mitigation: Store the token in a protected environment variable or secret manager, avoid pasting real tokens into chat or completed URLs, and redact usertoken values from logs, traces, errors, and shared diagnostics.

Risk: Broad activation terms may trigger the skill for general location or vessel questions that are outside the intended HiFleet API use case.

Mitigation: Confirm that the request is for a vessel-position lookup and validate that the user supplied a 9-digit MMSI before making the API call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charleiwang/skills/ship-position)
- [HiFleet position API endpoint](https://api.hifleet.com/position/position/get/token)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text with vessel-position fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid HiFleet user token and a 9-digit MMSI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
