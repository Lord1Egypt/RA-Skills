## Description:

TG Cam Claw lets an agent list bound camera devices, fetch current snapshots, review camera events and event images, and report device online status or battery level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate ClawHub-bound camera integrations: list available devices, request current snapshots, inspect event history and event images, and check online state or battery after confirming the target device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access camera devices, event history, snapshots, and private spaces through long-lived credentials.

Mitigation: Install only when the publisher and camera service are trusted, and confirm user intent before requesting or displaying sensitive images.

Risk: Camera API credentials may be pasted into chat or persisted in local configuration.

Mitigation: Treat TIVS_API_KEY like a password, store credentials only in protected secret storage, avoid echoing them in responses, and rotate them if they may have been exposed.

Risk: Signed image URLs or event images may disclose private camera media if shared directly.

Mitigation: Use complete signed URLs only for retrieval, avoid exposing raw image URLs by default, and present only the image or concise event summary needed for the user's request.

## Reference(s):

- [TG Cam Claw ClawHub listing](https://clawhub.ai/flyfinec/skills/tg-cam-claw)
- [Camera Skill API base URL](https://skill.webcamapp.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown summaries with API request guidance, JSON configuration examples, and image retrieval results when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIVS_CLI_ID and TIVS_API_KEY credentials; avoids exposing raw API keys or long raw JSON responses.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
