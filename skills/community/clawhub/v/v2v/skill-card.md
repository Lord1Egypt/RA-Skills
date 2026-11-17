## Description:

Placeholder skill for video-to-video workflows on skills.video. Use when the user is asking about v2v generation and the concrete API contract has not been implemented yet.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[skills-video](https://clawhub.ai/user/skills-video)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this placeholder when asking about video-to-video generation before a verified v2v API contract is available. It should steer users toward provider-specific documentation instead of inventing undocumented endpoints, payloads, or video-edit parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the placeholder for an implemented v2v workflow.

Mitigation: State clearly that no verified v2v endpoint, payload template, helper command, or polling flow is available yet.

Risk: Incorrect provider-specific API calls could result from guessed video input fields or edit parameters.

Mitigation: Require verified model-specific OpenAPI or documentation before describing request structure, upload semantics, or edit controls.

## Reference(s):

- [ClawHub V2V Skill Page](https://clawhub.ai/skills-video/skills/v2v)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains that v2v support is not implemented yet and directs users to verified model- or provider-specific documentation before making API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
