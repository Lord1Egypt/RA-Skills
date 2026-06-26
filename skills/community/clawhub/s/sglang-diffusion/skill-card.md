## Description: <br>
Generate images using a local SGLang-Diffusion server with an OpenAI-compatible image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangyukunok](https://clawhub.ai/user/jiangyukunok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate image files from text prompts through a local or trusted SGLang-Diffusion server. It supports common image-generation options such as size, negative prompts, denoising steps, guidance scale, seed, server URL, output path, and optional API key configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional credentials are sent to the configured SGLang-Diffusion server. <br>
Mitigation: Use only a local or trusted server and prefer the SGLANG_DIFFUSION_API_KEY environment variable instead of passing API keys directly on the command line. <br>
Risk: Generated image files are written to local storage. <br>
Mitigation: Choose an appropriate output path and review generated files before sharing or retaining them. <br>


## Reference(s): <br>
- [SGLang Project](https://github.com/sgl-project/sglang) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiangyukunok/sglang-diffusion) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and saved image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script writes a PNG image locally and prints a MEDIA path for supported chat providers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
