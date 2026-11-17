## Description:

Creates creator-style UGC ad video plans and Runware video-generation requests for direct-to-camera testimonials, product demos, unboxings, or faceless voiceover cuts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to prepare short social ad videos with a native UGC structure, including script or audio selection, presenter or faceless format, platform orientation, captions, and model request parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad generation may send scripts, recordings, photos, and background images to external generation services.

Mitigation: Use only media and URLs that are acceptable to expose to the provider or intended audience, and avoid private personal data in ad assets.

Risk: UGC ads can include misleading claims, testimonials, metrics, or reviews if unsupported content is supplied.

Mitigation: Use only exact, user-supplied claims and review copy, and verify proof points before generating the final cut.

## Reference(s):

- [UGC ad worked recipes](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/ugc-ad)

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces async video-generation request guidance; the external generation result is typically a video URL.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
