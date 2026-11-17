## Description:

Generate videos using local AI models (ComfyUI/Stable Video Diffusion) and auto-publish to social media platforms. Supports text-to-video, image-to-video, batch processing, and automated posting to Twitter, LinkedIn, Instagram, TikTok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[954215110](https://clawhub.ai/user/954215110)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and developers use this skill to set up local AI video generation workflows and prepare or automate publishing of generated videos across social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated public posting can publish unintended videos, captions, or hashtags through connected social accounts.

Mitigation: Review generated videos, captions, and selected platforms before posting; use manual approval or dry-run behavior before connecting production accounts.

Risk: The skill asks for social-media posting credentials without enough least-privilege setup guidance.

Mitigation: Use scoped test credentials where possible, store secrets outside shared files, rotate keys after testing, and avoid real account keys until setup safeguards are confirmed.

Risk: The posting script describes platform uploads but its platform API integrations are placeholders.

Mitigation: Confirm actual platform implementation and error handling before relying on the script for scheduled or production posting.

## Reference(s):

- [Video Prompt Guide](references/prompt-guide.md)
- [ComfyUI](https://comfyui.org)
- [ClawHub Skill Page](https://clawhub.ai/954215110/skills/video-generator-auto-post)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, command examples, configuration snippets, and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local video files, model setup steps, platform-specific caption guidance, and social-media credential names.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
