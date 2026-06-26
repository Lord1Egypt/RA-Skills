## Description: <br>
Generate or edit images with Volcengine Seedream (Doubao), including text-to-image, image-to-image, multi-reference fusion, sequential generation, PNG output, prompt optimization, web search, and streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberkurry](https://clawhub.ai/user/cyberkurry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate, edit, and combine images through the Volcengine Doubao-Seedream API from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and generated-image requests are sent to Volcengine. <br>
Mitigation: Use this skill only for content approved for Volcengine processing, and avoid sensitive or regulated material unless the deployment has explicit approval. <br>
Risk: The skill requires a Volcengine API key. <br>
Mitigation: Provide credentials through VOLC_API_KEY when possible, avoid hardcoding keys, and do not pass keys in shell history where that is prohibited. <br>
Risk: The optional web search mode can send prompt context for external lookup. <br>
Mitigation: Enable --web-search only when current-information retrieval is acceptable for the prompt and use case. <br>
Risk: Setup instructions rely on installing uv from an external source. <br>
Mitigation: Verify the uv installation method from a trusted source before running installer commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cyberkurry/seedream-volcengine) <br>
- [Seedream Reference](references/REFERENCE.md) <br>
- [Volcengine Seedream API documentation](https://www.volcengine.com/docs/82379/1541523) <br>
- [Volcengine Seedream tutorial](https://www.volcengine.com/docs/82379/1824121) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated image URLs or base64 image payloads from the Volcengine API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URL responses are valid for 24 hours; base64 output is available when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
