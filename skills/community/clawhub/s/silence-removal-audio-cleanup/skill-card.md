## Description:

Remove dead air, pauses, and filler words from video and audio timelines with automatic music ducking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and editors use this skill to tighten spoken-word audio and video by removing pauses and filler words, balancing dialogue, and ducking music. They provide an edit request and media through a configured Levea integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media is processed by Levea and may be exposed through public URLs.

Mitigation: Use only media you are comfortable sharing with Levea and exposing through public URLs.

Risk: An exposed Levea API key could allow unauthorized use.

Mitigation: Protect the API key and supply it through the integration's configuration.

Risk: Requested edits may proceed without a review pause.

Mitigation: Enable requirePlanApproval when you want to review proposed edits before they proceed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/brajendrak00068/skills/silence-removal-audio-cleanup)
- [Levea editing service](https://livecore.ai/)
- [Levea API endpoint](https://api.livecore.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Video]

**Output Format:** [Tool calls with JSON status and verification responses; completed exports are MP4 videos.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edits may run asynchronously or pause for plan approval.]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
