## Description:

Generate and save images when the user requests TokenHot. Check model parameters, inspect a local job, or recover its output without generating again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokenhot](https://clawhub.ai/user/tokenhot)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers can generate GPT Image 2 images through TokenHot, check supported model parameters, inspect local generation jobs, and recover saved results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image generation contacts TokenHot and is billed per generation; the workflow uses the TOKENHOT_API_KEY credential.

Mitigation: Send only content authorized for TokenHot, keep the key in the local environment, and check the applicable rate and price cap before generation.

Risk: ClawScan reports a benign result with medium confidence, but its analysis covered only two of three components and one script was analyzed partially.

Mitigation: Review and scan the incompletely assessed code before installation; treat the benign verdict as limited by the stated coverage.

Risk: A local job receipt can contain a temporary signed image link.

Mitigation: Keep job files local and restrict access to them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/tokenhot/skills/tokenhot-models)
- [TokenHot model catalog](https://tokenhot.ai/models)
- [GPT Image 2 model reference](https://docs.tokenhot.ai/main/gpt-image-2)
- [TokenHot OpenClaw guide](https://docs.tokenhot.ai/openclaw)
- [OpenClaw environment help](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Image files, JSON job records, Guidance]

**Output Format:** [Locally saved PNG, JPEG, GIF, WebP, or AVIF images, with JSON job status and recovery information]

**Output Parameters:** [One image per job; GPT Image 2 with a supported size]

**Other Properties Related to Output:** [Image generation is billed by TokenHot; a job may be inspected or its existing result downloaded again.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
