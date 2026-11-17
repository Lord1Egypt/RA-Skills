## Description:

Operate WordPress installs through WP-CLI for inspection, core maintenance, plugin and theme management, users, options, content, media, cron, database tasks, and multisite-aware administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to inspect and administer WordPress installations through WP-CLI when shell, SSH, or node-local access is available. It helps choose command families, attach appropriate global flags, and stage higher-risk maintenance work with read-first checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WP-CLI write operations such as updates, imports, search-replace, and user or content changes can affect a live WordPress site.

Mitigation: Review commands before execution, perform a read-first inspection, export the database before import or replacement work, and use dry-run options where available.

Risk: Inspection output can expose site configuration and account-role information.

Mitigation: Treat inspection results as sensitive operational data and avoid sharing them outside the intended administrative context.

Risk: The security summary notes a minor disclosure gap around listing WordPress users.

Mitigation: Confirm that user listing output is necessary for the task and handle user identifiers and role data as sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/skills/wordpress-wp-cli-admin)
- [Command Families](references/command-families.md)
- [Global Flags And Safety](references/global-flags-and-safety.md)
- [WP-CLI commands index](https://developer.wordpress.org/cli/commands/)
- [WP-CLI handbook](https://make.wordpress.org/cli/handbook/)
- [WP-CLI global parameters](https://developer.wordpress.org/cli/commands/#global-parameters)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and references to helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WP-CLI command proposals and inspection-script output that should be reviewed before write operations.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
