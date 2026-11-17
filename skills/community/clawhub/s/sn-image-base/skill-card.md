## Description:

Base-layer skill for the SenseNova-Skills project, providing low-level APIs for image generation, image recognition with VLMs, and text optimization with LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and upper-layer skills use this base layer to call configured image generation, image editing, image recognition, and text optimization backends without adding preprocessing logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, and API keys may be sent to configured external providers.

Mitigation: Install only if the publisher is trusted, keep API keys in local secret management, and restrict provider base URLs to approved endpoints.

Risk: The skill includes risky transport and dependency choices, including an option to disable TLS verification.

Mitigation: Avoid using --insecure, pin dependencies in deployment, and review network configuration before allowing automated use.

Risk: One image backend disables model safety thresholds.

Mitigation: Review or remove the Nano Banana safetySettings override before upper-layer skills call the backend automatically.

## Reference(s):

- [sn-image-base API Specification](references/api_spec.md)
- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-image-base)
- [SenseNova platform](https://platform.sensenova.cn/)
- [SenseNova Token Plan](https://platform.sensenova.cn/token-plan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON command output; generated and edited images are saved as files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation and editing return output file paths; recognition and text optimization return model text, with JSON mode adding status, runtime, model, base URL, and interface type.]

## Skill Version(s):

2026.9.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
