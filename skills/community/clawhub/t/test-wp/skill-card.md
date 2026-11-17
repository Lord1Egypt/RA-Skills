## Description:

Automatically publish Markdown articles to WordPress blog via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainco2008](https://clawhub.ai/user/rainco2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to publish Markdown posts, drafts, categories, tags, and featured images to a configured WordPress site through the REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled credentials or JWT material may be exposed or reusable.

Mitigation: Treat any included WordPress credentials as compromised, revoke them, and configure fresh least-privilege credentials through environment variables or a secret store.

Risk: Test, diagnostic, or fixed-target scripts may authenticate to or modify an unintended WordPress site.

Mitigation: Review target URLs and commands before execution, disable fixed-target scripts unless needed, and require explicit confirmation before publish, update, delete, media, category, or tag operations.

Risk: Publishing automation can make incorrect or unintended content public.

Mitigation: Use draft status for validation, inspect rendered Markdown and metadata before publishing, and run changes with a WordPress account limited to the minimum required permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainco2008/skills/test-wp)
- [Publisher profile](https://clawhub.ai/user/rainco2008)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute WordPress REST API publishing, listing, media, category, tag, test, setup, and diagnostic workflows when used with configured credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
