## Description:

Generates images and short videos with Volcengine Doubao APIs, including Seedream text-to-image, image-to-image, sequential image generation, and Seedance text-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goodgooddayhi](https://clawhub.ai/user/goodgooddayhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to call Volcengine Doubao services from an agent workflow for prompt-driven image generation, reference-image editing, multi-image generation, and short video creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External Volcengine API calls require ARK_API_KEY and may incur usage costs.

Mitigation: Install and run only with an intended Volcengine key, and review prompts, model choices, and generation parameters before execution.

Risk: The video workflow reads a shared workspace .env file and may import unrelated secrets into the runtime environment.

Mitigation: Use a workspace .env containing only the credentials needed for this skill, or run in an isolated workspace without unrelated secrets.

Risk: Returned media URLs are downloaded without host allowlisting or size limits.

Mitigation: Prefer explicit filenames in a controlled output directory and review generated media downloads in a constrained environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goodgooddayhi/skills/volcengine-doubao-image-gen)
- [Volcengine Ark Console](https://console.volcengine.com/ark)
- [Volcengine Ark Images Generations API](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY; outputs generated image or video files to user-selected filenames or generated local paths.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
