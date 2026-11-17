## Description:

Generates short-video scripts, hooks, titles, outlines, storyboards, calls to action, series plans, and performance review guidance for platforms such as Douyin, Kuaishou, YouTube Shorts, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to draft platform-specific short-video scripts, opening hooks, titles, shot guidance, subtitles, music cues, and CTA copy. It also supports lightweight content planning and video performance review prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled script can read or overwrite Markdown files outside its storage folder when save or show names are untrusted.

Mitigation: Use trusted names for save and show operations, review generated paths before use, and add path validation before deployment.

Risk: The skill can keep local history of script topics without clear disclosure.

Mitigation: Avoid entering sensitive topics, disclose or disable local logging, and clear local history where required.

Risk: Generated output may include unsolicited publisher branding.

Mitigation: Review generated scripts before publication and remove branding that is not appropriate for the intended channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/admirobot/skills/tvdr-video-script)
- [examples.md](artifact/examples.md)
- [tips.md](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with script sections, hooks, outlines, storyboard cues, tags, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local template-based content; no external API key is required by the artifact evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
