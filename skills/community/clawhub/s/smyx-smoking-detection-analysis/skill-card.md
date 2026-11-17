## Description:

Analyzes images, videos, and video streams for suspected smoking behavior and returns detection reports, alerts, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Public-space managers and operations teams use the skill to review submitted images or video for suspected smoking and to retrieve prior detection reports. Results support smoking-control management and should be considered alongside the organization's review procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service may send an API secret as account-registration data.

Mitigation: Have the publisher correct credential handling before use, and avoid processing sensitive footage until this is addressed.

Risk: Footage may be uploaded even when the --export-env-only option is used.

Mitigation: Do not treat that option as a no-upload guarantee. Confirm permission to upload the media and review the provider's retention terms first.

Risk: The --api-url option may not redirect processing to the expected service.

Mitigation: Do not rely on this option to redirect processing; verify the processing destination before sending footage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-smoking-detection-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured detection results and reports in JSON or Markdown, with alert and report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis results are for smoking-control management reference; follow organizational procedures for decisions.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
