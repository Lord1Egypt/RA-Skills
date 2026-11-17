## Description:

Generates Xiaohongshu-style cover images for social media posts and article artwork, with setup, balance, and history commands through the xhscover CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Xiaohongshu-style and social media cover images from short cover text, and to check xhscover credit balance or generation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm CLI that handles credentials and user-provided cover text.

Mitigation: Install only after reviewing the xhscover package, and prefer a pinned, reviewed version or lockfile-managed install before entering an API key or sending private text.

Risk: Cover prompts and API credentials are sent to xhscover.cn for processing.

Mitigation: Use the skill only when the user intends to use that service and accepts its data handling.

## Reference(s):

- [Xhs Cover Skill on ClawHub](https://clawhub.ai/xwchris/skills/xhs-cover)
- [xhscover website](https://xhscover.cn)
- [xhscover npm package](https://www.npmjs.com/package/xhscover)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text, Guidance]

**Output Format:** [Markdown with inline shell commands and generated cover image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses npx xhscover to set up access, generate covers, check balance, and view history.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
