## Description:

Formats finalized Markdown drafts into Xiaohongshu-ready notes, supports reviewed semi-automated publishing, and guides post-publication performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-ke](https://clawhub.ai/user/little-ke)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing operators use this skill to transform completed Markdown drafts into Xiaohongshu content packages, prepare publishing JSON, coordinate user-confirmed semi-automated posting, and review post-publication metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unaudited external or local xhs_publish.cjs script and an unpinned Playwright installation.

Mitigation: Review the script before installation, use a trusted source, pin dependencies with a lockfile, and keep browser automation dependencies current.

Risk: The publishing workflow operates an authenticated Xiaohongshu browser session and can prepare public-posting automation.

Mitigation: Require explicit user confirmation before running publish commands and final confirmation inside the browser before any post is submitted.

Risk: Generated formatting, title, tag, or analysis guidance can introduce factual errors or misleading publishing recommendations.

Mitigation: Keep the editorial review gate, verify previews before publishing, and route factual errors back to the content creation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-ke/skills/xiaohongshu-publish-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce title options, formatted Xiaohongshu body text, tag plans, image guidance, publishing JSON, command invocations, publishing previews, and performance review guidance.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
