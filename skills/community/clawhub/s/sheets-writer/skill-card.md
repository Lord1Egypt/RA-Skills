## Description:

Google Sheets Data Writer. Use when the user wants to append rows, update cells, or automate spreadsheet data pipelines against a pre-configured target sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to configure PortEden authentication, identify a target Google Sheet, append new rows, update specific cells, and verify spreadsheet writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PortEden CLI dependency and persisted credentials can access Google Drive resources available to the authenticated account.

Mitigation: Install only from a trusted or reviewed source, use a dedicated Google account or profile limited to the required spreadsheet workspace, and remove persisted credentials when finished.

Risk: Cell write operations can overwrite existing spreadsheet data and cannot be undone from the CLI.

Mitigation: Prefer append for new rows, read target ranges before multi-cell writes, and require explicit confirmation of the range and values before overwriting cells.

Risk: Untrusted values may be interpreted as spreadsheet formulas when written to cells.

Mitigation: Use raw-value writes for user, agent, or external inputs and read the range back after writing to verify the stored values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/porteden/skills/sheets-writer)
- [PortEden homepage](https://porteden.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash command examples and JSON or CSV value examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact JSON command output flags for read and info operations when appropriate.]

## Skill Version(s):

1.0.8 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
