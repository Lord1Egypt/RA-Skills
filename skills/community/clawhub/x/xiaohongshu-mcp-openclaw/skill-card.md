## Description:

Enables agents to query Xiaohongshu/Rednote notes, retrieve note details and comments, and summarize engagement metrics through an MCP-based workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitterccc](https://clawhub.ai/user/glitterccc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Xiaohongshu/Rednote content, fetch note details and comments, and produce normalized summaries of likes, comments, authors, and note text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and runtime scripts install or run unpinned external executables.

Mitigation: Review setup scripts and pin or verify dependency versions before running on a sensitive machine.

Risk: The optional service installer can create a background service that starts across sessions.

Mitigation: Avoid service_install.sh unless persistent background operation is intentional, and review the service definition before enabling it.

Risk: The QR login flow may open local files or URLs automatically.

Mitigation: Set XHS_QR_AUTO_OPEN=0 when automatic file or URL opening is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glitterccc/skills/xiaohongshu-mcp-openclaw)
- [README](artifact/README.md)
- [Field Mapping](artifact/references/field-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local QR-code file paths, MCP query results, summarized note metrics, and next-step commands.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
