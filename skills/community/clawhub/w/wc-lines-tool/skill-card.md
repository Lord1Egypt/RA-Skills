## Description:

Count lines, blank lines, code lines, and comment lines in text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to count lines in text streams for code statistics, log sizing, and document analysis. The packaged script evidence supports a simple stdin total-line counter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises file input, JSON output, threshold checks, blank-line counts, code-line counts, and comment-line counts that are not implemented by the bundled script.

Mitigation: Treat the release as a simple stdin total-line counter unless updated; test any advertised option before using it in automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/wc-lines-tool)
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text line count from the bundled script; markdown guidance may include command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads stdin and prints the number of input lines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
