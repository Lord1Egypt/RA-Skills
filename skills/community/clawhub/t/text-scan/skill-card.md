## Description:

text-scan helps agents quickly find and score relevant lines with surrounding context in local text files using keyword and phrase matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search notes, logs, Markdown files, and other local text documents for relevant lines before deciding whether to read full file context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning very large files or unbounded stdin may consume substantial memory because the script reads input into memory.

Mitigation: Use bounded files where practical, limit result counts, and avoid unbounded stdin for very large inputs.

Risk: The --output option can overwrite the specified output file.

Mitigation: Choose output paths deliberately and avoid pointing --output at important existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigas/skills/text-scan)
- [Publisher profile](https://clawhub.ai/user/indigas)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, brief line summaries, or JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include line numbers, relevance scores, matched terms, and surrounding context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
