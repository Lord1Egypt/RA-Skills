## Description:

Prepares Xiaohongshu image-and-text posts and short videos in the creator portal using EasyPost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gybin02](https://clawhub.ai/user/gybin02)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill to prepare image-and-text posts or short videos for Xiaohongshu. It fills a draft for review by default, and can publish when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external EasyPost tool is not included in this package, so its source cannot be assessed from these files.

Mitigation: Verify the source of EasyPost before use.

Risk: Publishing can make account content public before the user has reviewed the selected account, media, and text.

Mitigation: Use the fill workflow to review and adjust the draft in the browser; publish with --yes only when explicitly requested.

## Reference(s):

- [Xiaohongshu Upload on ClawHub](https://clawhub.ai/gybin02/skills/xiaohongshu-upload)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON task configurations and shell commands with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image-and-text or short-video task configurations; fill drafts for review, with publishing available only on explicit request.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
