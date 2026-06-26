## Description: <br>
WP Multitool helps agents audit WordPress site health, diagnose performance and database issues, and propose or run WP-CLI optimization and configuration commands with confirmation for write operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcindudekdev](https://clawhub.ai/user/marcindudekdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, WordPress site administrators, and operations teams use this skill to inspect WordPress health, database bloat, autoload pressure, slow queries, frontend optimization state, and related configuration. It can also guide confirmed WP-CLI cleanup and configuration actions for sites the user is authorized to administer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WordPress admin-level WP-CLI commands can delete database rows, optimize tables, change wp-config.php, and modify plugin options. <br>
Mitigation: Run the skill only on WordPress sites the user is authorized to administer, take a database backup before destructive changes, and require explicit confirmation before every write command. <br>
Risk: The security review notes a plugin activation command that is not clearly declared or confirmation-gated like other site-changing actions. <br>
Mitigation: Treat `wp plugin activate wp-multitool` as a write operation and require explicit user confirmation before running it. <br>
Risk: Read-only diagnostics can still expose site metadata, environment details, and performance information. <br>
Mitigation: Use diagnostic output only for the user's immediate review and avoid logging, storing, or transmitting site data. <br>


## Reference(s): <br>
- [WP Multitool Homepage](https://wpmultitool.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/marcindudekdev/skills/wp-multi-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/marcindudekdev) <br>
- [Author Website](https://marcindudek.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with WP-CLI command blocks and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WP-CLI. Write operations require explicit user confirmation, and backups are recommended before destructive database changes.] <br>

## Skill Version(s): <br>
1.5.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
