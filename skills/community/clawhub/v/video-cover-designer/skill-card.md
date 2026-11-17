## Description:

Assists Chinese-language short-video creators with cover copy, layout ideas, color palettes, popular-cover element analysis, and platform-specific sizing and style suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huajianjiu000](https://clawhub.ai/user/huajianjiu000)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to turn a video topic or script into Chinese cover-title ideas, layout guidance, color palettes, and platform-specific cover recommendations for Douyin, Kuaishou, WeChat Channels, Bilibili, and similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python helper may fail when generating composition suggestions because it references platform configuration outside the helper function's local scope.

Mitigation: Review and test the helper before relying on scripted output; pass platform sizing data into the composition helper or otherwise fix the undefined reference.

Risk: Outputs are oriented to Chinese-language short-video cover ideation and may not satisfy non-Chinese localization needs.

Mitigation: Confirm the target language and platform requirements before use, and add explicit localization controls if the skill is adapted for other markets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huajianjiu000/skills/video-cover-designer)
- [Source skill documentation](artifact/SKILL.md)
- [Bundled cover designer helper](artifact/scripts/cover_designer.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured headings, lists, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language cover design recommendations, including titles, subtitles, tags, color palettes, layout suggestions, element priorities, and platform sizing notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
