## Description:

Stata Skill helps agents execute Stata commands and do-files, install ado packages, read Stata help, inspect data files, and review execution logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sepinetam](https://clawhub.ai/user/sepinetam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents working with Stata use this skill to inspect datasets, create or run do-files, install needed ado packages, troubleshoot commands, and read execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask agents to run unpinned third-party tooling and install mutable ado packages from SSC, GitHub, or Net sources, which can affect local data and analysis results.

Mitigation: Use a pinned, reviewed version of stata-mcp, avoid arbitrary Net or unreviewed GitHub ado sources, and run Stata work with only the filesystem and data access needed for the task.

Risk: Executing Stata do-files or package installation commands may change local files, logs, or analysis outputs.

Mitigation: Review proposed commands and do-files before execution, use controlled working directories, and inspect logs after each run.

## Reference(s):

- [Stata-MCP Documentation](https://docs.statamcp.com)
- [Stata-MCP OpenClaw Skill Setup](https://docs.statamcp.com/skills/openclaw)
- [Stata-MCP FAQ](https://docs.statamcp.com/faq)
- [Stata-MCP GitHub Repository](https://github.com/statamcp/stata-mcp)
- [Publisher Stata-MCP GitHub Repository](https://github.com/sepinetam/stata-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Stata workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Stata CLI commands, do-file guidance, package installation steps, dataset inspection guidance, and log review instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
