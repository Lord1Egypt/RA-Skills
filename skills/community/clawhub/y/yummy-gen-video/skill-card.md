## Description: <br>
Use when the user wants to generate a video with Gemini Veo through yummycli, including text-to-video, image-to-video, and reference-image-guided generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yummysource](https://clawhub.ai/user/yummysource) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to translate video-generation requests into validated yummycli commands for Google Gemini Veo, including text prompts, starting images, and up to three reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GEMINI_API_KEY and an external CLI. <br>
Mitigation: Install and authenticate yummycli only in environments where using @yummysource/yummycli and a Gemini API key is approved. <br>
Risk: Prompts and selected image files may be sent to Google Veo for cloud video generation. <br>
Mitigation: Avoid confidential prompts or private images unless provider processing is intentional and permitted. <br>
Risk: Incorrect model, duration, resolution, image count, or output extension can cause command validation failures. <br>
Mitigation: Validate requested parameters against the skill's compatibility rules before running yummycli, and retry only with corrected arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yummysource/yummy-gen-video) <br>
- [Publisher profile](https://clawhub.ai/user/yummysource) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yummycli, the yummy-shared skill, and GEMINI_API_KEY; generated video output is an MP4 file path returned by the CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
