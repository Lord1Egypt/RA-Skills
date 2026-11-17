## Description:

A Chinese-language Sparki skill for reframing videos into platform-friendly aspect ratios such as 9:16, 1:1, and 16:9.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking creators, social media operators, and agents use this skill to upload a local video, request a target aspect ratio, and receive a resized Sparki-generated output for Reels, Shorts, TikTok, Instagram, YouTube, or similar distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and prompts are sent to the third-party Sparki service.

Mitigation: Use the skill only when the user intends to use Sparki, and avoid sensitive or private videos unless the service is trusted for that content.

Risk: The setup command can save a Sparki API key in local OpenClaw configuration.

Mitigation: Prefer SPARKI_API_KEY for temporary credentials and protect any saved local configuration.

Risk: Downloaded result URLs and file sizes are not tightly validated by the skill.

Mitigation: Treat generated downloads as untrusted files, use an explicit output path when possible, and review the result before redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/video-resizer-zh)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload link](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads MP4 or MOV inputs, creates Sparki edit tasks, and can download generated MP4 results to a local output path.]

## Skill Version(s):

1.0.12 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
