## Description: <br>
Generate and edit images with Seedream through RunAPI. Use when the user asks an agent to create, edit, or transform images with Seedream. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Seedream image generation or editing requests through RunAPI, using the CLI for one-off work and SDKs for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or image inputs may be sent to the external RunAPI Seedream service. <br>
Mitigation: Review RunAPI terms, pricing, rate limits, and data-handling expectations before using private or sensitive content. <br>
Risk: The skill can use RunAPI authentication through an API key or saved CLI login. <br>
Mitigation: Protect RUNAPI_API_KEY and local CLI credentials, and review authentication handling before deployment. <br>


## Reference(s): <br>
- [RunAPI Seedream model documentation](https://runapi.ai/models/seedream.md) <br>
- [RunAPI Seedream homepage](https://runapi.ai/models/seedream) <br>
- [ByteDance provider comparison](https://runapi.ai/providers/bytedance.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Seedream 4.5 text-to-image](https://runapi.ai/models/seedream/4.5-text-to-image.md) <br>
- [Seedream 4.5 edit](https://runapi.ai/models/seedream/4.5-edit.md) <br>
- [Seedream 5 lite text-to-image](https://runapi.ai/models/seedream/5-lite-text-to-image.md) <br>
- [Seedream 5 lite image-to-image](https://runapi.ai/models/seedream/5-lite-image-to-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code guidance] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RunAPI CLI commands, authentication guidance, JSON request-file guidance, and SDK package references.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
