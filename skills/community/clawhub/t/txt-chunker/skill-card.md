## Description:

Splits large text files into smaller chunks by line count for easier processing of logs, datasets, or documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to split large local text files, such as logs, datasets, and long documents, into smaller line-count-based chunks that are easier for agents or downstream tools to process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Existing files with the same numbered output prefix can be overwritten.

Mitigation: Choose a unique output prefix or run the tool in a controlled output directory before splitting files.

Risk: The tool reads the provided local file path and writes chunk files to the local workspace.

Mitigation: Run it only on text files intended for splitting and review the working directory before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/txt-chunker)

## Skill Output:

**Output Type(s):** [shell commands, text, files]

**Output Format:** [Markdown guidance with shell command examples and local text chunk files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes numbered UTF-8 .txt files using the selected output prefix.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
