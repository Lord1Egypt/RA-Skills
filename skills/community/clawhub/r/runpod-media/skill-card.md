## Description: <br>
Generate images from text, edit images with text instructions, animate images to video, and generate video from text via RunPod public AI endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ItamarCoh3n](https://clawhub.ai/user/ItamarCoh3n) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to create, edit, animate, and deliver AI-generated media through RunPod endpoints from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call arbitrary RunPod endpoints, including endpoints outside the known registry. <br>
Mitigation: Prefer known registry endpoints and review any custom endpoint before use. <br>
Risk: Prompts and local media may be sent to remote RunPod endpoints and local files may be uploaded through Cloudflare R2 presigned URLs. <br>
Mitigation: Avoid private media or sensitive prompts unless remote processing is acceptable, and use dedicated, narrowly scoped RunPod and Cloudflare R2 credentials. <br>
Risk: The artifact includes a direct Telegram Bot API curl fallback for media delivery. <br>
Mitigation: Do not use the Telegram curl fallback unless the bot token, chat ID handling, and delivery path are trusted. <br>


## Reference(s): <br>
- [Runpod Media on ClawHub](https://clawhub.ai/ItamarCoh3n/runpod-media) <br>
- [ItamarCoh3n ClawHub Profile](https://clawhub.ai/user/ItamarCoh3n) <br>
- [RunPod API Settings](https://www.runpod.io/console/user/settings) <br>
- [RunPod Hub Playground](https://console.runpod.io/hub/playground/{type}/{endpoint-id}) <br>
- [Google Nano Banana 2 Edit RunPod Playground](https://console.runpod.io/hub/playground/image/google-nano-banana-2-edit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image, video, or audio files may be saved locally and delivered through the active channel.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
