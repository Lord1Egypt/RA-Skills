## Description:

Enable WordPress superpowers for OpenClaw. Your Developer, Content Manager, Author, Security Specialists, Contributor, Subscriber and Admin and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm1lf](https://clawhub.ai/user/realm1lf)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners, developers, and operators use this skill to guide an OpenClaw agent through WordPress content, media, plugin, theme, WooCommerce, Elementor, REST, and wp-content work on an existing site. It supports REST-based workflows by default, with optional WP-CLI and file-level workflows when the environment is configured for them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended companion plugin installation can pull unpinned external code before granting powerful WordPress access.

Mitigation: Review the companion plugin source and dependencies before installation, preferably from a pinned commit or release.

Risk: WordPress credentials, WP-CLI, media upload, and plugin-file tools can have broad site impact if enabled on production.

Mitigation: Start on staging, use a dedicated least-privilege WordPress application-password user, allow only required tools, and keep backups with a clear rollback path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realm1lf/skills/wordpress-expert)
- [Metadata OpenClaw homepage](https://github.com/realM1lF/openclaw-wordpress-tool)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Before install: trust, credentials, and blast radius](references/PRE_INSTALL_AND_TRUST.md)
- [Connect WordPress to OpenClaw](references/CONNECTING.md)
- [Tools: decision tree](references/TOOLING.md)
- [Safety and defaults](references/SAFETY.md)
- [Plugin development under OpenClaw](references/PLUGIN_DEV_PLAYBOOK.md)
- [Reference index](references/OVERVIEW.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WordPress REST, WP-CLI, plugin file, and configuration guidance depending on the user's allowed tools and site setup.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
