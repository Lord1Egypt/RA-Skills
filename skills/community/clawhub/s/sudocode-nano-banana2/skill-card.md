## Description: <br>
Generate or edit images with Sudocode's nano-banana2 remote image service through a bundled API client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengy983](https://clawhub.ai/user/shengy983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate images from text prompts or edit local images by sending the prompt and optional image to Sudocode's remote service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional input images, and the API key are sent to the configured remote endpoint. <br>
Mitigation: Install only if you trust Sudocode and the configured SUDOCODE_BASE_URL; keep the default endpoint unless you intentionally control the alternative. <br>
Risk: Credentials may be persisted to ~/.openclaw/.env when the initializer is used. <br>
Mitigation: Protect the environment file, use a revocable API key, and rotate or revoke the key if it is exposed. <br>
Risk: Generated image files and per-run logs are written near the selected output path. <br>
Mitigation: Choose the output location deliberately and review generated files and logs before sharing them. <br>
Risk: Sensitive prompts or input images may be processed by a remote service. <br>
Mitigation: Avoid sending confidential, personal, or regulated content unless that use has been approved for the configured endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shengy983/sudocode-nano-banana2) <br>
- [Sudocode registration and account portal](https://sudocode.us) <br>
- [Default Sudocode API endpoint](https://sudocode.run) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated image files with text logs and Markdown-style operating guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUDOCODE_IMAGE_API_KEY; optional SUDOCODE_BASE_URL selects the remote endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
