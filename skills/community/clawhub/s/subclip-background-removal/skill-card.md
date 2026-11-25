## Description:

Remove the background from an existing Subclip MediaPanel image locally by default or from video through the credit-backed cloud workflow, then preserve or replace the exact timeline item with the editable result. Use for requests to cut out a subject, make an image transparent, or remove a video background; do not use for generating unrelated new media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Subclip users and their agents use this skill to remove backgrounds from an existing image or video and update the matching timeline item with the editable result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and an incomplete scan because one local reference could not be resolved.

Mitigation: Consider the incomplete scan coverage when deciding whether to install.

Risk: Video background removal uses account credits.

Mitigation: Check available credits before submitting a video operation and stop if the credit check fails.

Risk: Video matting may be less effective for objects, animation, or complex transparent materials than for people and talking-head footage.

Mitigation: Review the result and use people-focused footage when reliable subject separation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prosamik/skills/subclip-background-removal)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Image and video media]

**Output Format:** [Subclip timeline edits and image/video assets, with concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image results are transparent PNGs; video results include one editable color-key effect.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
