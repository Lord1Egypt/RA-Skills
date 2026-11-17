## Description:

Write and publish WeChat Official Account articles end-to-end with AI, or take an existing draft straight into the skill's built-in formatting and draft-box publishing flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, adapt, format, preview, and send WeChat Official Account articles to a draft box through the YouMind workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create drafts in the linked WeChat Official Account.

Mitigation: Review generated content and account targeting before running publish actions, and validate the WeChat connection before first use.

Risk: Markdown image references can lead to local image files being uploaded during publishing.

Mitigation: Use trusted Markdown sources and inspect or sanitize local image paths before publishing.

Risk: Changing the YouMind base URL could route publishing and upload traffic away from the official service.

Mitigation: Keep the base URL set to the official HTTPS YouMind endpoint unless a trusted deployment is explicitly approved.

Risk: Optional external design-skill installation expands the trust boundary.

Mitigation: Install optional companion skills only after separately reviewing and trusting their source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/youmind-wechat-article)
- [YouMind OpenAPI Document](references/openapi-document.md)
- [CLI Reference](references/cli-reference.md)
- [Pipeline](references/pipeline.md)
- [Runtime Rules](references/runtime-rules.md)
- [WeChat Constraints](references/wechat-constraints.md)
- [Publishing Guidelines](shared/PUBLISHING.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, generated article files, HTML previews, and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article drafts, HTML previews, generated image assets, and WeChat draft-box entries when configured.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
