## Description:

Routes video region-edit requests through the RunComfy CLI to remove, clean up, or replace regions across frames using Wan 2-7 Edit-Video by default, with Lucy Edit Restyle and Seedream 4-0 Edit-Sequential alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through prompt-driven video inpainting on RunComfy, including object removal, watermark cleanup, region replacement, and selection of more precise ComfyUI workflows when CLI endpoints are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned third-party RunComfy CLI.

Mitigation: Install the CLI only from a trusted source, pin the package version where possible, and avoid unattended npx execution.

Risk: The RunComfy CLI uses local credentials or a RUNCOMFY_TOKEN environment variable.

Mitigation: Use a revocable least-privilege token and keep token files or environment variables out of shared logs and artifacts.

Risk: Video URLs and prompts are submitted to RunComfy for media-editing workflows.

Mitigation: Submit only user-provided media and prompts that the user is comfortable sending to RunComfy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/video-inpainting)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting)
- [Wan 2-7 Edit-Video](https://www.runcomfy.com/models/wan-ai/wan-2-7/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting)
- [Seedream 4-0 Edit-Sequential](https://www.runcomfy.com/models/bytedance/seedream-4-0/edit-sequential?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting)
- [RunComfy ComfyUI Workflows](https://www.runcomfy.com/comfyui-workflows?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting)
- [Wan Models Collection](https://www.runcomfy.com/models/collections/wan-models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides model selection and RunComfy CLI invocation; generated media is downloaded by the CLI to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
