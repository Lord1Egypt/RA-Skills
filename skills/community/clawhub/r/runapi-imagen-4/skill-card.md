## Description: <br>
Generate and edit images with Imagen 4 through RunAPI. Use when the user asks an agent to create, edit, or transform images with Imagen 4. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image generation, editing, and transformation requests through RunAPI's Imagen 4 service. It supports one-off CLI workflows and SDK-oriented application integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and inputs are sent to a third-party cloud service. <br>
Mitigation: Use the skill only when RunAPI transmission is intended, and avoid regulated data, proprietary prompts, sensitive images, or secrets in request files. <br>
Risk: API credentials can be exposed through shell history, logs, or checked-in files. <br>
Mitigation: Prefer runapi login or secure environment management, and avoid pasting RUNAPI_API_KEY values into commands, logs, or committed configuration. <br>


## Reference(s): <br>
- [Imagen 4 model overview, pricing, and rate limits](https://runapi.ai/models/imagen-4.md) <br>
- [RunAPI Imagen 4 homepage](https://runapi.ai/models/imagen-4) <br>
- [Google provider comparison](https://runapi.ai/providers/google.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Imagen 4 variant](https://runapi.ai/models/imagen-4/imagen-4.md) <br>
- [Imagen 4 Fast variant](https://runapi.ai/models/imagen-4/fast.md) <br>
- [Imagen 4 Ultra variant](https://runapi.ai/models/imagen-4/ultra.md) <br>
- [Imagen 4 Pro image-to-image variant](https://runapi.ai/models/imagen-4/pro-image-to-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward RunAPI CLI usage for one-off tasks and SDK usage for application integration.] <br>

## Skill Version(s): <br>
0.2.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
