## Description: <br>
Redraw image content using Tomoviee Image Redrawing API (`tm_redrawing`) through the Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`) for inpainting, localized replacement, object removal, or mask-based image edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call Tomoviee/Wondershare image redrawing APIs for prompt-guided image edits, optional mask-controlled redrawing, and polling for generated image results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are sent to Tomoviee/Wondershare for third-party processing. <br>
Mitigation: Use the skill only with approved content, avoid sensitive or regulated images unless authorized, and confirm Tomoviee/Wondershare is acceptable for the intended workflow. <br>
Risk: Public image URLs, private network URLs, or callback URLs can expose data or internal services. <br>
Mitigation: Prefer short-lived public image URLs, avoid internal or private URLs, and review callback destinations before execution. <br>
Risk: The authentication helper prints a Basic auth token that could be captured in logs or shared terminals. <br>
Mitigation: Use a dedicated API key, keep generated tokens out of logs, and rotate credentials if a token is exposed. <br>


## Reference(s): <br>
- [Tomoviee Image APIs](references/image_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>
- [Tomoviee Developer Portal (Global)](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API Docs (Global)](https://www.tomoviee.ai/doc/) <br>
- [Tomoviee Developer Portal (Mainland)](https://www.tomoviee.cn/developers.html) <br>
- [Tomoviee API Docs (Mainland)](https://www.tomoviee.cn/doc/) <br>
- [Wondershare OpenAPI Gateway](https://openapi.wondershare.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API task IDs, polling guidance, and image result URL handling for Tomoviee redrawing workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
