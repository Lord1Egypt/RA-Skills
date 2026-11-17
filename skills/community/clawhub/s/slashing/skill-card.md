## Description:

Slashing presents itself as blockchain slashing analysis but provides a shell-based local record manager with status, add, list, search, remove, export, stats, and config commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users may use this skill as a command-line local record manager for adding, listing, searching, removing, exporting, and configuring entries. The security evidence says it should not be relied on for blockchain slashing analysis unless the purpose mismatch is resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised blockchain slashing-analysis purpose does not match the observed local note and configuration manager behavior.

Mitigation: Install only when a local record manager is intended, and do not use it as a source of blockchain slashing analysis until the purpose mismatch is corrected.

Risk: The skill writes persistent local data, supports deletion, and can export files from stored entries.

Mitigation: Run it in a controlled workspace, set SLASHING_DIR explicitly when isolation is needed, and review exported files before sharing or committing them.

Risk: The security guidance warns against untrusted values in configuration or CSV export workflows because shell escaping issues remain.

Mitigation: Avoid feeding untrusted input to config, add, search, or export workflows until escaping and validation are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/slashing)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples; command output is plain text and exports JSONL or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local state under $SLASHING_DIR or ~/.slashing and can create slashing-export.json or slashing-export.csv in the working directory.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
