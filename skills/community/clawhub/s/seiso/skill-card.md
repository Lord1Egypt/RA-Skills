## Description:

Unified media generation gateway for agents. Discover tools dynamically, choose API key or x402 auth, invoke image/video/audio/music/3D/training tools, and handle queue jobs reliably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legendarylibr](https://clawhub.ai/user/legendarylibr)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover Seisoai media-generation tools, select API-key or x402 authentication, invoke image, video, audio, music, 3D, and training tools, and manage queued jobs reliably.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face swap, voice cloning, lip sync, and motion-transfer tools can be misused with real people's likenesses or voices without consent.

Mitigation: Use the skill only with media the user has rights and consent to process, and require an explicit confirmation or refusal step for these requests.

Risk: API-key and x402 payment flows can expose credentials or create unintended billable calls.

Mitigation: Keep credentials scoped, use only current caller credentials, monitor billable calls, and avoid reusing stale x402 signatures.

## Reference(s):

- [Seisoai homepage](https://seisoai.com)
- [ClawHub skill page](https://clawhub.ai/legendarylibr/skills/seiso)
- [ClawHub publisher profile](https://clawhub.ai/user/legendarylibr)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown with API endpoint lists and JSON/HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes queue polling, error handling, authentication selection, and agent-scoped safety guidance.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
