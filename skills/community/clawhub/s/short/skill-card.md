## Description: <br>
Generate FLUX images through the inference.sh CLI, including text-to-image, image-to-image, LoRA fine-tuning, and custom style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihai2582424632-droid](https://clawhub.ai/user/lihai2582424632-droid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to generate, transform, and iterate on FLUX images from prompts or source images through inference.sh CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and authenticating an external inference.sh CLI before use. <br>
Mitigation: Install only if the inference.sh provider is trusted, prefer manual installation with checksum verification, and log in with the intended account. <br>
Risk: Prompts and image URLs may be sent to an external image-generation provider. <br>
Mitigation: Avoid sending private prompts or private image URLs unless the provider's data handling and billing terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lihai2582424632-droid/short) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Image Generation Example](https://inference.sh/docs/examples/image-generation) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>
- [CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent to call inference.sh apps; generated image assets are produced by the external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
