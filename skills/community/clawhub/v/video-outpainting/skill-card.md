## Description:

Guides agents to extend a video's spatial canvas with RunComfy CLI workflows, including aspect-ratio conversion and environment generation beyond the original frame while preserving central action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and media automation agents use this skill to prepare RunComfy video outpainting jobs that expand footage for new aspect ratios or wider framing. It helps choose between the CLI-accessible Wan 2-7 Edit-Video path and RunComfy ComfyUI workflows when seam quality is important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a third-party CLI installer or executor that may be unpinned.

Mitigation: Prefer a pinned and reviewed @runcomfy/cli version before use, especially in automated agent runs.

Risk: RunComfy API tokens may be exposed through environment variables or local configuration.

Mitigation: Keep RUNCOMFY_TOKEN scoped and protected, and ensure local token files remain private.

Risk: Source video URLs are sent to RunComfy and may include unintended or untrusted media.

Mitigation: Only process video URLs explicitly provided for the outpainting task and review outputs for prompt divergence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/video-outpainting)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting)
- [Wan 2-7 Edit-Video model](https://www.runcomfy.com/models/wan-ai/wan-2-7/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting)
- [LTX 2-3 outpainting ComfyUI workflow](https://www.runcomfy.com/comfyui-workflows/ltx-2-3-outpainting-in-comfyui-spatial-frame-expansion-workflow?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting)
- [RunComfy video model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunComfy CLI invocation patterns, authentication guidance, model-routing advice, and workflow links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
