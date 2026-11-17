## Description:

TG Cam Skill helps agents list bound cameras, capture current snapshots, review events and event images, and check online status and battery level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

External users with configured TG camera credentials use this skill to inspect available cameras, request snapshots, review camera events and images, and check device status or battery level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists sensitive camera API credentials for later use.

Mitigation: Keep openclaw.json private, avoid sharing or committing it, and rotate the camera API key if exposure is suspected.

Risk: The skill can expose home surveillance snapshots, event images, event history, and device status.

Mitigation: Install only if the user trusts the camera service and is comfortable granting access to camera images, events, and status.

Risk: Ambiguous device requests could retrieve information from the wrong camera.

Mitigation: Confirm the target device from the device list before making snapshot, event, online-status, or battery requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyfinec/skills/tg-cam-api)
- [Publisher profile](https://clawhub.ai/user/flyfinec)
- [Camera service API base](https://skill.webcamapp.cc)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries with image references and concise status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include camera snapshot or event image content when the service returns an image URL.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
