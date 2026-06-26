## Description: <br>
Generate, edit, and compose images using Gemini models, including logos, posters, icons, banners, photo edits, and multi-image compositions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyan](https://clawhub.ai/user/wangyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create, edit, or combine images through Gemini-compatible image models, then save and send the resulting image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Gemini API credentials and can load shared .env files. <br>
Mitigation: Use a dedicated Gemini key, prefer a skill-local .env with only GEMINI_* values, and avoid placing unrelated secrets in shared environment files. <br>
Risk: Prompts and input images are sent to the configured API provider or custom endpoint. <br>
Mitigation: Install only if you trust the publisher, dependencies, and provider, and do not submit private images or sensitive prompts to untrusted endpoints. <br>


## Reference(s): <br>
- [API Formats Reference](references/api-formats.md) <br>
- [Project Homepage](https://github.com/wangyan/wangyan-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Generated image files with terminal status text and an IMAGE_PATH line for agent delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and GEMINI_BASE_URL; supports optional input images, aspect ratio, resolution, quality, style, model, API format, timeout, and output directory settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
