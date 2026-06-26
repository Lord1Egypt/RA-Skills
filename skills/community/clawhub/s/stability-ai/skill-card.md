## Description: <br>
Generate high-quality images via Stability AI API (SDXL, SD3, Stable Image Core). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative users use this skill to generate image files and matching metadata from text prompts through the Stability AI API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Stability AI and may also be stored in local metadata. <br>
Mitigation: Avoid submitting sensitive prompts and review generated metadata before sharing output files. <br>
Risk: API_HOST can redirect requests to a custom endpoint. <br>
Mitigation: Leave API_HOST unset or point it only to a trusted HTTPS endpoint compatible with the Stability AI API. <br>
Risk: The output directory automatically retains only the most recent 20 generated images and removes older image and metadata files. <br>
Mitigation: Store important generated images outside the auto-cleanup output directory. <br>
Risk: The skill installs and uses Python dependencies for network requests, environment loading, and image processing. <br>
Mitigation: Use a reviewed or pinned Python environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1999AZZAR/stability-ai) <br>
- [Publisher profile](https://clawhub.ai/user/1999AZZAR) <br>
- [Model and parameter reference](references/models.md) <br>
- [Stability AI API host](https://api.stability.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line output with local image file paths and JSON metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images use png, jpg, jpeg, or webp format; metadata records prompt, model, generation settings, seed, and API version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
