## Description:

Relight a still image by changing lighting setup, color temperature, direction, or mood on RunComfy through the runcomfy CLI, using Qwen Edit 2509 Relight LoRA by default and identity-preserving edit endpoints as fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and image-production teams use this skill to generate RunComfy CLI guidance for relighting still images while preserving subject identity, pose, framing, and product appearance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path can execute a mutable, unpinned npm CLI package, including automatic npx execution.

Mitigation: Use a pinned and locally locked RunComfy CLI version, verify package provenance or checksums where available, and avoid automatic latest-version execution in production workflows.

Risk: Images, prompts, and outputs are sent to and processed by RunComfy services.

Mitigation: Use the skill only when that data handling is acceptable, avoid submitting sensitive images without approval, and review token and output storage locations before use.

Risk: Authentication depends on RUNCOMFY_TOKEN or local RunComfy token configuration.

Mitigation: Store tokens in controlled environments, avoid logging secrets, and rotate credentials if they are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/relight)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)
- [Qwen Edit 2509 Relight LoRA](https://www.runcomfy.com/models/qwen/qwen-edit-2509/lora/relight?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)
- [Qwen Image collection](https://www.runcomfy.com/models/collections/qwen-image?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)
- [Best image editing models collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)
- [RunComfy trainer](https://www.runcomfy.com/trainer?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)
- [RunComfy ComfyUI workflows](https://www.runcomfy.com/comfyui-workflows?utm_source=clawhub&utm_medium=skill&utm_campaign=relight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on still-image relighting through the runcomfy CLI and model-specific prompt routing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
