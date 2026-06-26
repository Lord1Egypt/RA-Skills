## Description: <br>
Generate/edit images via Tuzi API (default), Google Gemini, OpenAI, DashScope, Replicate. Text-to-image + image-to-image editing; 1K/2K/4K resolution. Use for image create/modify/edit requests incl. --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljquan](https://clawhub.ai/user/ljquan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to generate new images or edit existing images through supported third-party image providers. It supports draft-to-final workflows with selectable provider, model, input image, and 1K/2K/4K resolution options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, API keys, proxy settings, and input images may be sent to selected third-party image providers. <br>
Mitigation: Use only trusted provider and proxy settings, avoid sensitive prompts or images, and protect API keys in environment files and command arguments. <br>
Risk: Untrusted input image paths or .tuzi-skills environment files can affect how the skill reads files and routes API traffic. <br>
Mitigation: Run the skill from trusted project directories, avoid untrusted --input-image paths, and review any local .tuzi-skills/.env file before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ljquan/tuzi-nano-banana) <br>
- [Tuzi API](https://api.tu-zi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG image files with terminal status text and saved-path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key for the selected provider; supports optional input images, provider/model selection, and 1K, 2K, or 4K resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
