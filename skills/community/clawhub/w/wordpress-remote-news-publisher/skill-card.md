## Description:

Automates news article creation and publishing to remote WordPress via SSH and WP-CLI, including image handling and SEO metadata integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promoweb](https://clawhub.ai/user/promoweb)

### License/Terms of Use:

MIT

## Use Case:

Publishers, site operators, and automation developers use this skill to generate source-grounded news articles, prepare cover images, and publish drafts or posts to a remote WordPress site through SSH and WP-CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH automation can modify a live WordPress site.

Mitigation: Treat the install as review-required, use a dedicated non-root SSH user and key, and validate configuration before enabling scheduled publishing.

Risk: The provided SSH examples disable host key verification and include an allow-root example.

Mitigation: Enable SSH host key verification and remove any --allow-root usage before deployment.

Risk: Shared temporary files and remote command argument handling can create conflicts or unsafe publishing behavior.

Mitigation: Use private per-run temporary files, validate numeric IDs, and fix remote command argument handling before cron-based operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/promoweb/skills/wordpress-remote-news-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON article data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article, media, and state files before issuing remote WordPress publishing commands.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
