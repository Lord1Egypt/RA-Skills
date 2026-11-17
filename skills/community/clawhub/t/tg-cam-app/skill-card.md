## Description:

TG Cam App helps an agent query bound camera devices, capture current snapshots, retrieve event records and images, and check device online status and battery level through the webcamapp.cc service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent inspect their authorized camera devices, summarize recent camera events, show event images, generate app links, and report device status or battery information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access bound camera devices and retrieve device images or event data through the webcamapp.cc service.

Mitigation: Install and use it only for camera devices the user intends to expose to the agent through their TIVS credentials.

Risk: Snapshot requests actively capture a new camera image and may create storage or traffic cost.

Mitigation: Ask explicitly before taking snapshots and avoid repeated captures unless the user requests them.

Risk: TIVS credentials stored for the skill grant access to the camera service.

Mitigation: Treat TIVS_CLI_ID and TIVS_API_KEY as sensitive values and do not echo the API key in chat or logs.

## Reference(s):

- [TG Cam App ClawHub listing](https://clawhub.ai/flyfinec/skills/tg-cam-app)
- [webcamapp.cc skill API base](https://skill.webcamapp.cc)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and concise text with camera images or app links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided TIVS credentials and avoids exposing raw API keys or long raw JSON responses.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
