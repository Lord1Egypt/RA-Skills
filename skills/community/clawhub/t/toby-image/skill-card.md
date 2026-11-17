## Description:

Run local ComfyUI workflows via the HTTP API, including default, file-based, or raw JSON workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to have an agent edit ComfyUI workflow JSON, queue local image-generation jobs, download model weights when requested, and return generated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent modify and execute local ComfyUI workflows.

Mitigation: Review workflow JSON before execution and run only workflows from trusted sources.

Risk: The model downloader can contact arbitrary model URLs and write files under ~/ComfyUI.

Mitigation: Use trusted HTTPS model sources, verify destination paths, and avoid --overwrite unless replacement is intentional.

Risk: The downloader may install and execute pget from an external release path.

Mitigation: Prefer --no-pget when reviewing or operating in restricted environments.

Risk: Bundled workflow assets may contain unexpected sensitive prompts.

Mitigation: Inspect bundled workflow prompts before use and remove or replace prompts that are not appropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-image)
- [ComfyUI project](https://github.com/comfyanonymous/ComfyUI.git)
- [pget downloader](https://github.com/replicate/pget)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, edited workflow JSON, helper-script JSON status, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local ComfyUI server and Python 3; workflow outputs are saved under the local ComfyUI output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
