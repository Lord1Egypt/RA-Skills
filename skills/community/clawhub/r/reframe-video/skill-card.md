## Description:

Convert a video to a new aspect ratio without cropping the subject by extending the scene edges with model-generated content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to adapt finished video clips for different social, feed, or delivery aspect ratios while preserving the subject. The skill guides collection of the source video, target canvas, extension prompt, source placement, and model schema checks before running video inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends the selected video and prompt to an external video-generation provider.

Mitigation: Confirm the user is comfortable sharing the media and prompt with the provider before running the job.

Risk: Video reframing may incur per-second generation costs.

Mitigation: Check current pricing through the related model or run skill before submitting inference jobs.

Risk: Model availability, supported resolutions, and request schema can change.

Mitigation: Verify the model is live and inspect the current schema before calling video inference.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/runware/skills/reframe-video)
- [runware Publisher Profile](https://clawhub.ai/user/runware)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with API parameters and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides asynchronous video inference, model schema confirmation, source positioning, target canvas selection, and prompt refinement.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
