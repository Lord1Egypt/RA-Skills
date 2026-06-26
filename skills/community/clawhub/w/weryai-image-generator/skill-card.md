## Description: <br>
Generate WeryAI images from text prompts or reference images through the WeryAI image APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images from prompts, transform reference images, inspect WeryAI model capabilities, and check generation status with bounded polling and paid-run awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected reference images, and explicitly provided local image files can be sent to WeryAI for processing. <br>
Mitigation: Prefer public HTTPS image URLs or dry-run previews first, and do not provide sensitive local files. <br>
Risk: Custom WERYAI_BASE_URL or WERYAI_MODELS_BASE_URL values can redirect API traffic to another host. <br>
Mitigation: Keep the default WeryAI hosts unless the replacement host is fully trusted. <br>
Risk: Real submit and wait workflows can create paid generation tasks and are not idempotent. <br>
Mitigation: Confirm model, prompt, image count, aspect ratio, and resolution before paid submission; use status checks for existing tasks instead of resubmitting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weryai-developer/weryai-image-generator) <br>
- [WeryAI Image Generation Models](references/api-models.md) <br>
- [WeryAI Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command results, with user-facing image links or rendered images when generation completes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, batch IDs, task status, image URLs, balance details, model settings, and errors; default polling is bounded to 300 seconds.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
