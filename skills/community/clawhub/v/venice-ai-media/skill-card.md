## Description: <br>
Generate, edit, and upscale images; create videos from images via Venice AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhannah](https://clawhub.ai/user/nhannah) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI assistants use this skill to generate media assets, edit or upscale source images, and create short image-to-video outputs through Venice AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source images, and generated media are sent to Venice AI. <br>
Mitigation: Avoid submitting sensitive photos, documents, audio, or private prompt text unless Venice AI's data handling is acceptable for the use case. <br>
Risk: Image and video generation can spend Venice API credits, especially longer or higher-resolution video jobs. <br>
Mitigation: Use a dedicated revocable Venice API key, monitor credit usage, and use quote mode before expensive video generation. <br>
Risk: Embedding EXIF metadata can expose prompt text or generation details when images are shared. <br>
Mitigation: Avoid --embed-exif for sensitive prompts or strip metadata before distributing generated images. <br>


## Reference(s): <br>
- [Venice AI](https://venice.ai) <br>
- [Venice API settings](https://venice.ai/settings/api) <br>
- [ClawHub skill page](https://clawhub.ai/nhannah/venice-ai-media) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with shell command examples and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media scripts print MEDIA lines for agent attachment; use VENICE_API_KEY for authenticated Venice API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
