## Description:

Generate images from text, edit images with text instructions, animate images to video, and generate video from text via RunPod public AI endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itamarcoh3n](https://clawhub.ai/user/itamarcoh3n)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate or edit images, create videos from prompts, animate source images, and list or call supported RunPod media endpoints from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media may be sent to RunPod and local inputs may be temporarily uploaded to Cloudflare R2.

Mitigation: Use only approved media, avoid sensitive inputs, and confirm that RunPod and R2 handling meets the deployment's data policy before use.

Risk: The skill includes a Telegram delivery fallback that reads Telegram credentials.

Mitigation: Review or remove the Telegram fallback before deployment unless Telegram delivery is explicitly required and credential access is scoped.

Risk: The generic endpoint caller can use arbitrary endpoint IDs, which may send data to endpoints outside the vetted registry.

Mitigation: Prefer the included endpoint registry and require review before using or adding custom endpoint IDs.

## Reference(s):

- [Runpod Media ClawHub Release](https://clawhub.ai/itamarcoh3n/skills/runpod-media)
- [RunPod API Settings](https://www.runpod.io/console/user/settings)
- [Google Nano Banana 2 Edit Endpoint](https://console.runpod.io/hub/playground/image/google-nano-banana-2-edit)
- [Endpoint Registry](artifact/scripts/endpoints.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, configuration notes, endpoint metadata, and generated image or video file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved as local image or video files; endpoint calls may also return JSON when no media URL is found.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
