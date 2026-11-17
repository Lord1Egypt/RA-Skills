## Description:

Viral Video Studio helps agents analyze short-form video references, reverse-engineer viral structure, and produce scripts, AI image prompts, posting calendars, and monetization roadmaps for TikTok, Instagram Reels, and YouTube Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieluong](https://clawhub.ai/user/eddieluong)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content operators use this skill to turn a reference short-form video or channel idea into a reusable content workflow, including viral analysis, character development, image prompts, editing guidance, posting plans, and monetization planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper workflow may fetch user-provided social-video URLs and create local temporary media, frame, and subtitle files.

Mitigation: Run the helper in an isolated account or private temporary directory, delete generated media after analysis, and avoid shared locations for sensitive inputs.

Risk: Reference videos may be private, copyrighted, or otherwise unsuitable for reuse.

Mitigation: Use only videos the user has permission to analyze and reuse, and review generated concepts to avoid copying protected creative expression.

Risk: Downloaded media paths are predictable under /tmp and could expose content on shared systems.

Mitigation: Prefer a private temp directory or isolated runtime and remove /tmp/tiktok-ref.*, /tmp/tiktok-frame-*.jpg, and /tmp/tiktok-sub* files after use.

## Reference(s):

- [Character Sheet Template](assets/character-sheet-template.md)
- [TikTok Channel Setup Guide](references/channel-setup.md)
- [Character Bible - TikTok Channel Identity](references/character-bible.md)
- [TikTok Monetization Roadmap](references/monetization.md)
- [30-Day TikTok Posting Calendar](references/posting-calendar.md)
- [AI Image Prompt Templates for TikTok](references/prompt-templates.md)
- [Script Templates for TikTok Content Factory](references/script-templates.md)
- [Trend-Riding Playbook](references/trend-riding.md)
- [Video Generation Tools - Comparison and Workflow](references/video-generation-tools.md)
- [Viral Video Analysis Framework](references/viral-analysis.md)
- [ClawHub skill page](https://clawhub.ai/eddieluong/skills/viral-video-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown reports, prompt templates, shell command snippets, and step-by-step production guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local temporary video, frame, and subtitle files created by the helper script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
