## Description:

WordPress site health audit, performance optimization, database cleanup, autoload tuning, slow query detection, wp-config management, image size control, frontend speed fixes, and server diagnostics. Combines 19 optimization and control modules into a single paid plugin (Pro $79/year single-site, $199/year or $499 lifetime unlimited). The diagnostic commands in this skill work on any WordPress 5.8+ site without the plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress site owners and developers use this skill to inspect site health, performance, database state, and WP Multitool monitoring data through WP-CLI. They can use its suggested cleanup and configuration commands after confirming each write operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup and configuration commands can delete WordPress data or change site behavior.

Mitigation: Get user confirmation before every write operation and export a database backup before cleanup.

Risk: The included SQL examples use the default wp_ table prefix and may fail on sites with a custom prefix.

Mitigation: Check the site's prefix with `wp db prefix` and substitute it in the SQL before running queries.

## Reference(s):

- [WP Multitool](https://wpmultitool.com)
- [ClawHub skill release](https://clawhub.ai/marcindudekdev/skills/wp-multi-tool)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Guidance, Configuration instructions]

**Output Format:** [Markdown with inline SQL and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require user confirmation.]

## Skill Version(s):

1.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
