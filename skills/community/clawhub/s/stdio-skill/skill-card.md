## Description:

Stdio Skill provides a local MCP stdio server for a filesystem-backed inbox, tmp, and outbox workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[safatinaztepe](https://clawhub.ai/user/safatinaztepe)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to pass files through a local inbox, tmp, and outbox workflow over an MCP stdio server without interpreting file formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The filesystem boundary may not match the documented workspace boundary.

Mitigation: Use only in a contained environment and prefer a fixed version that stores data under the intended project directory.

Risk: Local file operations can overwrite or delete files when overwrite or delete tools are used.

Mitigation: Keep sensitive files away from the inbox, tmp, and outbox directories and require explicit review before overwrites or deletes.

Risk: Large base64 payloads can be inefficient or difficult to review.

Mitigation: Prefer path-based handling and move operations for large files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/safatinaztepe/skills/stdio-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with MCP tool calls and JSON text results containing paths, file listings, base64 file content, and file operation status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File reads and writes use base64 payloads; large files should be handled by path or move operations when possible.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
