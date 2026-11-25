## Description:

Generate persistent cloud video with Subclip AI from text and model-supported image or video references. Use for new clips and generative edits of existing footage, including FLUX Video Edit. Ordinary trimming and reframing use native timeline tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create new cloud video clips or generatively edit existing footage in Subclip AI. It helps select a currently available model, provide supported source media, and import completed video into the project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video generation can involve high-impact settings that require user confirmation.

Mitigation: Generate only after the user authorizes the exact model and settings; ask for confirmation when material settings are missing or change.

Risk: Media may be sent to external services, and the release has no privacy disclosure covering that handling.

Mitigation: Before submitting media, make its external processing clear and avoid sending sensitive media unless the user has authorized it.

## Reference(s):

- [Model selection and pricing](references/model-selection.md)
- [Subclip Video Generation on ClawHub](https://clawhub.ai/prosamik/skills/subclip-video-generation)

## Skill Output:

**Output Type(s):** [API Calls, Video, Guidance]

**Output Format:** [Video generation tool calls with concise user-facing guidance; completed video is imported into the project.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio stays with its video unless the user requests audio extraction.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
