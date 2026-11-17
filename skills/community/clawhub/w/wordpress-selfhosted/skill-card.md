## Description:

Manage a self-hosted WordPress site through SSH/WP-CLI or the WordPress REST API for drafting, publishing, updating, deleting, formatting, and optimizing posts or pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to let an agent manage content on a configured self-hosted WordPress installation. It is intended for posts and pages on LXC, VPS, or bare-metal WordPress deployments, not WordPress.com-hosted sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can exercise high-impact control over the configured WordPress site, including publishing, updating, and deleting content.

Mitigation: Use a least-privilege WordPress account, scope the skill to a specific site, and review publish/delete actions before execution.

Risk: The documented REST API flow uses a curl credential pattern that can expose a WordPress application password to local process observers.

Mitigation: Avoid that pattern in shared or monitored environments; prefer SSH/WP-CLI or safer secret handling, and use a dedicated revocable application password.

Risk: First SSH connections rely on trust-on-first-use host key handling by default.

Mitigation: Pre-populate known_hosts where possible and reserve disabled host-key checking for isolated, trusted CI environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddygk/skills/wordpress-selfhosted)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and WordPress content snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary local and remote HTML files for content transfer; the artifact directs cleanup after use.]

## Skill Version(s):

1.0.3 (source: server release evidence, released 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
