## Description: <br>
Uses the Z-Image lightweight text-to-image API to generate images from prompts, sizes, or aspect ratios, while avoiding image editing, OCR, and video generation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runninghcm](https://clawhub.ai/user/runninghcm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate text-to-image requests through the Z-Image API, including poster, cover, illustration, product, and Chinese or English text-in-image prompts. It normalizes requested aspect ratios into supported sizes, validates required parameters, and controls the exact number of API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API usage are sent to the Z-Image provider. <br>
Mitigation: Avoid confidential prompts and install only when the provider is trusted for the intended use case. <br>
Risk: The helper scripts can store the API key in plaintext at ~/.config/z-image/.env. <br>
Mitigation: Prefer a session-scoped X_API_KEY or a dedicated revocable key, and remove or rotate the key when it is no longer needed. <br>
Risk: Repeated generation requests can consume API quota or expose more prompt data than intended. <br>
Mitigation: Confirm the requested count before execution and run only the number of API calls requested by the user. <br>


## Reference(s): <br>
- [z-image API Guide](references/api-guide.md) <br>
- [Z-Image API endpoint](https://agent.mathmind.cn/minimalist/api/tywx/zImage) <br>
- [ClawHub skill page](https://clawhub.ai/runninghcm/zimage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with shell commands and structured API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce one or more Z-Image API calls according to the requested count; uses prompt and size parameters and requires an x-api-key.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
