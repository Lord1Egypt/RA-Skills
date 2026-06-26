## Description: <br>
Generate and edit images with Recraft through RunAPI for one-off CLI tasks or SDK integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route Recraft image generation, upscaling, background removal, and image-editing requests through the RunAPI CLI or SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on RUNAPI_API_KEY or a saved RunAPI CLI login, which are sensitive credentials. <br>
Mitigation: Keep API keys and saved CLI credentials out of prompts, logs, generated files, and version control; rotate credentials if exposed. <br>
Risk: Image prompts, source images, or edited outputs may be sent to an external RunAPI/Recraft service. <br>
Mitigation: Review RunAPI and Recraft terms, pricing, rate limits, and data handling before sending private or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-recraft) <br>
- [RunAPI Recraft homepage](https://runapi.ai/models/recraft) <br>
- [RunAPI Recraft model overview, pricing, and rate limits](https://runapi.ai/models/recraft.md) <br>
- [RunAPI Recraft provider comparison](https://runapi.ai/providers/recraft.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Recraft crisp upscale variant](https://runapi.ai/models/recraft/crisp-upscale.md) <br>
- [Recraft remove background variant](https://runapi.ai/models/recraft/remove-background.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include RunAPI CLI commands, request-file guidance, asynchronous polling steps, authentication guidance, and SDK package references.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
