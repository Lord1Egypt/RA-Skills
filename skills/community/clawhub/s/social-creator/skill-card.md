## Description:

Creates high-engagement Chinese social media copy and 3:4 HTML cover pages for platforms such as Xiaohongshu, Douyin, and WeChat Channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javastarboy](https://clawhub.ai/user/javastarboy)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and marketing teams use this skill to research AI-tool topics, draft short Chinese social posts with hashtags and interaction prompts, and generate screenshot-ready HTML cover pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped user-provided or web-sourced text, which may execute JavaScript when opened.

Mitigation: Review generated HTML before opening or sharing it, and escape inserted text or add a restrictive Content Security Policy before trusted reuse.

Risk: The workflow writes files to a fixed OpenClaw workspace output folder and may open that folder automatically.

Mitigation: Run the skill in a workspace where this output path is expected, and inspect generated files before publishing or distributing them.

## Reference(s):

- [Copywriting Guide](artifact/references/copywriting-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/javastarboy/skills/social-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance plus generated single-file HTML cover pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write copywriting.md and cover-*.html files for each requested social post.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
