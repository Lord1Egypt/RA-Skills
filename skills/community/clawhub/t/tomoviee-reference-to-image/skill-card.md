## Description: <br>
Generate images from a reference image using Tomoviee Image-to-Image API (`tm_reference_img2img`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation workflow authors use this skill to call Tomoviee's image-to-image API for reference-based image editing, style transfer, and subject-preserving transformations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, optional callback URLs, and task metadata are sent to Wondershare/Tomoviee for processing. <br>
Mitigation: Use non-sensitive prompts and images, avoid private or regulated content, and review the provider's terms before production use. <br>
Risk: API credentials and generated Basic authorization tokens are sensitive, and the token helper prints the token to stdout. <br>
Mitigation: Use dedicated revocable API credentials and avoid running token generation in CI logs, shared terminals, or other recorded sessions. <br>
Risk: Callback URLs can disclose internal endpoints or receive generated-task metadata. <br>
Mitigation: Use purpose-built public callback endpoints and avoid internal, secret-bearing, or privileged callback URLs. <br>


## Reference(s): <br>
- [Tomoviee Image-to-Image API Reference](references/image_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>
- [Tomoviee API docs (global)](https://www.tomoviee.ai/doc/ai-image/image-to-image.html) <br>
- [Tomoviee developer portal (global)](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API docs (mainland)](https://www.tomoviee.cn/doc/ai-image/image-to-image.html) <br>
- [Tomoviee developer portal (mainland)](https://www.tomoviee.cn/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell examples; API responses may include JSON task metadata and generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an asynchronous task workflow with polling; generated assets are returned by the Tomoviee/Wondershare service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
