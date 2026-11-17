## Description:

ZenTao CLI helps agents query and maintain ZenTao products, projects, requirements, tasks, and bugs, including status transitions, progress summaries, installation, configuration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catouse](https://clawhub.ai/user/catouse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and project-management operators use this skill to run ZenTao CLI commands for reading, updating, and summarizing ZenTao work items and related project records. It is also used to install, configure, authenticate, and troubleshoot the CLI in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide write, delete, bulk update, and status-transition operations that change ZenTao business records.

Mitigation: Use it only with intended ZenTao sites and accounts, confirm the authorized object set before destructive or bulk changes, require explicit delete confirmation such as --yes where applicable, and verify results after writes.

Risk: Credential exposure or unintended account selection could give the agent access beyond the user's intent.

Mitigation: Do not collect passwords or tokens in chat, avoid reading or printing credential files or environment variables, and verify the selected site and account with a scoped read-only query when needed.

Risk: CLI help, fields, actions, and minimum server versions can differ from the installed CLI or ZenTao server.

Mitigation: Check local command help and server compatibility before requests, report unsupported-version errors clearly, and use only supported equivalent queries when a direct action is unavailable.

Risk: Partial pages, local filters, or batch partial failures can lead to incomplete summaries or incorrect success claims.

Mitigation: Use JSON output for programmatic work, paginate when complete counts are required, separate success, failed, and skipped batch results, and query uncertain write outcomes before retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catouse/skills/zentao-cli)
- [Publisher profile](https://clawhub.ai/user/catouse)
- [ZenTao CLI repository](https://github.com/easysoft/zentao-cli.git)
- [ZenTao official site](https://www.zentao.net/)
- [Output, filtering, and statistics reference](artifact/references/data-output.md)
- [Writes, status transitions, and batch operations reference](artifact/references/writes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ZenTao CLI commands, status summaries, parsed JSON results, error explanations, and verification steps.]

## Skill Version(s):

0.3.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
