## Description:

Serves spec-driven development workflow tools via MCP for adding tasks, planning iterations, tracking completion, and reviewing quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to record spec tasks, sprint plans, progress updates, review notes, reminders, priorities, and weekly retrospectives in local text logs from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow notes are stored as plaintext under the user's home directory and may contain sensitive project data.

Mitigation: Do not enter passwords, tokens, confidential customer data, regulated information, or other sensitive material into logged entries.

Risk: CSV exports can carry unsafe spreadsheet content if entries include formulas or command-like values.

Mitigation: Review exported CSV files before opening them in spreadsheet software, and sanitize values that begin with formula-triggering characters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/spec-workflow-mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores workflow entries as local plaintext logs and can export collected entries as json, csv, or txt.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
