## Description:

Generates Xiaohongshu-style social media cover images from user-provided text and supports balance and history checks through the xhscover CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Xiaohongshu-style cover images for posts, articles, and social media content, or to check xhscover account balance and generation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use runs the latest xhscover npm CLI package, which can change after review.

Mitigation: Pin or preinstall a trusted xhscover package version before using the skill.

Risk: The skill sends the user's API key and cover text to xhscover.cn for processing.

Mitigation: Use the skill only when the user trusts the xhscover npm package and xhscover.cn service with that data.

## Reference(s):

- [XhsCover website](https://xhscover.cn)
- [xhscover npm package](https://www.npmjs.com/package/xhscover)
- [xhscover CLI repository](https://github.com/xwchris/xhscover-cli)
- [Xhs Cover Skill on ClawHub](https://clawhub.ai/xwchris/skills/xhs-cover-skill)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated image files from the xhscover CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 3:4, 9:16, 1:1, and 16:9 aspect ratios; requires Node.js 18+ and npx.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
