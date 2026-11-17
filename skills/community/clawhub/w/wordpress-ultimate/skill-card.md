## Description:

TinkerClaw WordPress lets an agent manage a WordPress site through guarded REST API scripts that draft content by default and require explicit flags for publishing or administrative changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and content teams use this skill to let an agent draft, edit, organize, and publish WordPress content through explicit consent-gated commands. It is also useful for controlled site administration tasks such as plugin, theme, user, and settings changes when the operator grants the required admin flag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured agent receives powerful access to the target WordPress site, including content, media, comments, users, settings, plugins, and themes within the chosen account's permissions.

Mitigation: Use the least-privileged WordPress user available, keep WP_READONLY=1 for browsing-only work, and set WP_ALLOWED_HOSTS to the intended site.

Risk: Plugin or theme installation and activation can execute code on the WordPress site.

Mitigation: Treat WP_ALLOW_ADMIN=1 as explicit approval for site-level changes and grant it only for a reviewed, specific command.

Risk: Publishing, media uploads, content edits, trashing, and moderation can affect what visitors see.

Mitigation: Require WP_ALLOW_PUBLISH=1 on the specific call after reviewing the content or file that will become visible.

## Reference(s):

- [WordPress REST API Quick Reference](artifact/references/wp-api-reference.md)
- [SEO Patterns for WordPress Content](artifact/references/seo-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/globalcaos/skills/wordpress-ultimate)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require WordPress connection settings and may require per-call WP_ALLOW_PUBLISH, WP_ALLOW_ADMIN, or WP_READONLY flags.]

## Skill Version(s):

1.4.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
