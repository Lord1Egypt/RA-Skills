## Description:

Count words, lines, and characters in a file. Outputs a single summary line. Use when the user wants to know how long a file is or count words in a document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and other users can ask an agent to count the lines, words, and byte-sized character count for a local text file when they need a quick length summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads whichever local file path the user supplies.

Mitigation: Run it only on files the user intends to inspect and avoid passing sensitive files unless counting them is necessary.

Risk: The reported BYTES value may be mistaken for a true Unicode character count.

Mitigation: Treat the character count as a byte count unless the implementation or documentation is updated to use Unicode-aware counting.

## Reference(s):

- [Word Count on ClawHub](https://clawhub.ai/jinwangmok/skills/word-count)
- [Publisher profile](https://clawhub.ai/user/jinwangmok)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text count summary with file path, line count, word count, byte count, and status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local file path and the wc command; byte counts may differ from true Unicode character counts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
