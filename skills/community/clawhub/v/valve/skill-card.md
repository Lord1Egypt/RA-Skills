## Description:

Valve is presented as a valve sizing and selection tool, but the inspected artifact functions as a local command-line record manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to add, list, search, remove, export, and summarize local records stored under ~/.valve. Do not rely on it for engineering valve sizing or selection decisions without independent validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is labeled as a valve sizing tool, while the inspected artifact behaves as a local record manager.

Mitigation: Treat outputs as record-management results only and validate any valve sizing or selection work with an appropriate engineering tool.

Risk: The skill stores arbitrary entries under ~/.valve and supports remove and export operations.

Mitigation: Set VALVE_DIR to a controlled directory, avoid storing sensitive data, and back up records before removal or export workflows.

Risk: Security evidence flags unsafe input handling in the config command.

Mitigation: Avoid the config command until key and value handling are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/valve)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output, JSONL records, and optional JSON or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local records in ~/.valve by default; VALVE_DIR can change the data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
