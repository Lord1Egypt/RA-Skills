## Description:

WeChat Official Account Manager - Automatically generate articles, images, SEO optimization, and data analysis. Supports end-to-end operations from topic selection to publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, self-media operators, enterprise account teams, and personal bloggers use this skill to plan, generate, optimize, analyze, and prepare WeChat Official Account content for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure WeChat account credentials, including an app secret.

Mitigation: Install only in an isolated Python environment, pin and review dependencies, and keep the WeChat secret out of committed configuration files.

Risk: The skill advertises publishing automation and multi-platform synchronization, which could publish incorrect content or affect the wrong account.

Mitigation: Require explicit confirmation of the target account, platform, content, schedule, and cancellation or rollback path before publishing or syncing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/wechat-mp-assistant-chen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include content outlines, SEO suggestions, image prompts, analytics guidance, dependency installation commands, and WeChat account configuration examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
