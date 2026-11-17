## Description:

Report or filter repeated lines in sorted text. Use for deduplication, frequency counting, and data cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to remove duplicate lines or count repeated lines while preparing sorted text data for cleanup, inspection, or shell-style data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented -d, -u, -i, and output-file behaviors are not implemented by the inspected script.

Mitigation: Use only the implemented file/stdin input and count or global deduplication behavior, or verify compatibility before relying on documented uniq-style options.

Risk: The inspected script treats non-adjacent duplicate lines as duplicates, which differs from adjacent-line-only uniq behavior.

Mitigation: Install only when global deduplication or counting is acceptable for the workflow, and test representative input before using it in data-cleanup pipelines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/uniq-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell examples and plain-text command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tool reads local text input from a file or standard input and writes deduplicated or counted lines to standard output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
