## Description:

Provides camera device lookup, current snapshots, event history, event images, online status, and battery checks for authorized webcam devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect authorized webcam devices, retrieve current snapshots, review event history and images, and check online status or battery after identifying the correct device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private camera device data, snapshots, event history, and event images.

Mitigation: Install and run it only when that camera access is intended, and verify the publisher and device scope before use.

Risk: The skill instructs the agent to store camera API credentials in local configuration when credentials are provided in chat.

Mitigation: Prefer a protected secret store or out-of-band credential setup, and define clear credential deletion and rotation procedures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyfinec/skills/webcam)
- [Webcam Skill API Base](https://skill.webcamapp.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Images]

**Output Format:** [Markdown summaries with concise device, event, status, battery, snapshot, or event image results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return image content for snapshots or event images; avoids exposing raw API keys or signed image URLs by default.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
