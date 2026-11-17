## Description:

Generate FLUX image-generation requests with inference.sh CLI commands for text-to-image, image-to-image, LoRA fine-tuning, and custom styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihai2582424632-droid](https://clawhub.ai/user/lihai2582424632-droid)

### License/Terms of Use:


## Use Case:

Developers, creators, and operators use this skill to ask an agent for inference.sh CLI commands that generate or transform images with FLUX models and related image tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start installer executes remote code that may change over time.

Mitigation: Review the installer source first, or use a version-pinned manual install and verify the downloaded binary against published checksums.

Risk: Optional related-skill commands use unpinned npx installers.

Mitigation: Avoid those optional commands unless the supply chain is trusted and versions are pinned or otherwise verified.

Risk: Prompts and image URLs submitted to image-generation services may contain sensitive information.

Mitigation: Do not submit confidential prompts, private image URLs, credentials, or personal data unless the service and use case have been approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihai2582424632-droid/skills/short)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Image Generation Example](https://inference.sh/docs/examples/image-generation)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may include remote CLI installation, login, model app runs, and user-supplied prompt or image URL inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
