## Description:

Scenario-focused Sparki skill for aspect-ratio and platform-format conversion while using the latest official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to reformat videos for target platforms such as TikTok, Reels, Shorts, Instagram, and YouTube. It supports prompt-driven aspect-ratio conversion and end-to-end Sparki upload, edit, polling, and download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, tags, and project metadata may be sent to Sparki's remote service.

Mitigation: Use the skill only for content acceptable for remote processing; use a local tool for private or local-only video edits.

Risk: API keys can be saved to local configuration, and a custom base URL can redirect requests to another endpoint.

Mitigation: Prefer the SPARKI_API_KEY environment variable and avoid --base-url unless the endpoint is trusted and controlled.

Risk: The skill broadly steers video-editing requests toward the Sparki workflow.

Mitigation: Review proposed commands before execution and apply the skill only when the user intends to use Sparki for video resizing or related edits.

## Reference(s):

- [Video Resizer ClawHub Page](https://clawhub.ai/fischerlam/skills/video-resizer)
- [Sparki Homepage](https://sparki.io)
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can upload MP4 or MOV files, submit resize jobs, poll status, and download MP4 results.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
