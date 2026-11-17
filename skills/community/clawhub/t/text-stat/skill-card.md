## Description:

Count words, characters, lines, and estimate reading time for any text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and other external users can use this skill to quickly measure line count, word count, character count, and estimated reading time for a provided text file or piped input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided files or pasted text to compute counts, which may expose sensitive content through local command execution or output.

Mitigation: Run it only on text the user explicitly selects and avoid sensitive files unless count output is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text statistics and Markdown usage guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads only the file or text stream explicitly provided by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
