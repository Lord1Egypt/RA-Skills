## Description: <br>
Operate WordPress installs through WP-CLI for inspection, core maintenance, plugin and theme management, users, options, content, media, cron, database tasks, and multisite-aware administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and WordPress operators use this skill to inspect WordPress installations, choose the correct WP-CLI command family, and perform maintenance or administration tasks with read-first checks and safer write-operation practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WP-CLI commands can change live WordPress code, users, options, content, or database state. <br>
Mitigation: Inspect first, confirm the target path and URL, export the database before destructive work, and use dry-run options when available. <br>
Risk: Remote or automated execution can run against the wrong environment if target context is ambiguous. <br>
Mitigation: Use explicit --path, --url, --user, and --ssh values as needed, verify the target before write operations, and keep credentials or SSH keys out of skill folders. <br>


## Reference(s): <br>
- [Command Families](references/command-families.md) <br>
- [Global Flags And Safety](references/global-flags-and-safety.md) <br>
- [WP-CLI Commands Index](https://developer.wordpress.org/cli/commands/) <br>
- [WP-CLI Handbook](https://make.wordpress.org/cli/handbook/) <br>
- [WP-CLI Global Parameters](https://developer.wordpress.org/cli/commands/#global-parameters) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command suggestions should be reviewed against the target WordPress install before execution.] <br>

## Skill Version(s): <br>
0.5.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
