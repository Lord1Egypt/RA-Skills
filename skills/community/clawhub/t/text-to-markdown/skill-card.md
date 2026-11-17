## Description:

纯文本格式预处理工具，自动插入换行、拆分长段落，为后续 AI/LLM 生成 Markdown 提供结构化输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cizixiu](https://clawhub.ai/user/cizixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to prepare Chinese plain text for Markdown conversion by inserting line breaks, splitting long paragraphs, and preserving the original wording before an AI/LLM adds final Markdown structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example command includes a local Windows path that may not match the user's environment.

Mitigation: Review and adapt the script path before running the command.

Risk: The preprocessing script reads an input file and can write an output file.

Mitigation: Provide only intended text files and choose an output path that will not overwrite important content.

## Reference(s):

- [IMA note examples](references/examples.md)
- [Markdown format specification](references/markdown-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or preprocessed plain text with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original wording while changing line breaks and paragraph structure.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
