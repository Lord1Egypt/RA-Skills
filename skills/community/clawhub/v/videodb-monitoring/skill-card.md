## Description:

Screen recording capabilities. Generate stream URLs, search recordings, get transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omgate234](https://clawhub.ai/user/omgate234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to record agent work sessions, generate playable VideoDB stream URLs, and optionally search recordings or retrieve summaries and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record the user's screen and possible system audio and send captured content to VideoDB.

Mitigation: Use it only when screen recording is intentional, avoid sensitive sessions, and confirm VideoDB storage, deletion, and access controls before use.

Risk: The monitor can run as a detached background recorder without a clear per-task stop or consent workflow.

Mitigation: Confirm how to stop the monitor process before starting it and check the running state after each recording task.

Risk: Generated stream or player URLs may expose recorded activity to anyone with access to the link.

Mitigation: Share recording links only with intended recipients and avoid generating links for private, regulated, or confidential work without consent and retention controls.

Risk: The VideoDB API key is required for operation and is stored in OpenClaw configuration or environment variables.

Mitigation: Store the API key only in approved configuration, avoid exposing it in transcripts or logs, and rotate it if it may have been shared.

## Reference(s):

- [VideoDB Console](https://console.videodb.io)
- [VideoDB Monitoring on ClawHub](https://clawhub.ai/omgate234/skills/videodb-monitoring)
- [Publisher profile](https://clawhub.ai/user/omgate234)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and generated recording or player URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return VideoDB stream URLs, player page URLs, search results, activity summaries, or audio transcripts depending on the requested command.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
