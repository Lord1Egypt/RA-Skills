## Description:

将结构化品牌内容转化为今日头条通俗场景化文章草稿，辅助填写供用户人工审核发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

B2B teams, founders, and content operators use this skill to turn structured brand assets into Toutiao-ready drafts, titles, summaries, cover prompts, micro-posts, keywords, and a pre-publication checklist. It can also assist with local visible-browser draft entry while leaving final review and publishing under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Toutiao content may contain inaccurate claims, exaggerated marketing language, or platform-inappropriate framing.

Mitigation: Review all generated content with the publish checklist before saving or publishing.

Risk: Browser automation can create account or platform-policy risk if extended beyond draft entry.

Mitigation: Run only in a normal user account, keep the browser visible, do not bypass verification, and leave final save or publish actions to the user.

Risk: The example script's file handling and dependencies may need hardening before operational use.

Mitigation: Pin Playwright versions and tighten file path checks so the script reads only resolved files inside the intended output/toutiao directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljseeking/skills/toutiao-geo-draft-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, prompt-guided text outputs, and an example Python Playwright script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft content for human review; the browser automation example uses a visible browser and does not publish automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
