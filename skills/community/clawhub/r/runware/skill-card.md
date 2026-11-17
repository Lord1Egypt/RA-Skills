## Description:

Generate images and videos through the Runware API, including text-to-image, image-to-image, upscaling, text-to-video, and image-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[26medias](https://clawhub.ai/user/26medias)

### License/Terms of Use:


## Use Case:

Developers and creative teams use this skill to generate, transform, upscale, and animate visual media from prompts or selected source images using Runware-hosted models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected image files, and generation parameters are sent to Runware.

Mitigation: Avoid sending sensitive prompts or local images unless they are intended for Runware processing.

Risk: API keys can be exposed through command-line history when passed as arguments.

Mitigation: Use the RUNWARE_API_KEY environment variable instead of the --api-key command-line option.

Risk: Generation cost varies by model and request settings.

Mitigation: Review Runware pricing, monitor reported costs, and choose model, count, duration, and resolution settings deliberately.

## Reference(s):

- [Runware](https://runware.ai)
- [Runware Models](https://runware.ai/models)
- [Runware Pricing](https://runware.ai/pricing)
- [ClawHub Skill Page](https://clawhub.ai/26medias/skills/runware)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Generated image or video files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Runware API key; video generation is asynchronous and may incur model-dependent costs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
