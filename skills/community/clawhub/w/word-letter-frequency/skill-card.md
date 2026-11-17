## Description:

Count how many times each letter appears in a word or short phrase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmusjune](https://clawhub.ai/user/simmusjune)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to calculate per-character frequencies for a word or short phrase and summarize the result as text, a table, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute its bundled local Python script when counting letters.

Mitigation: Review the bundled script and file hashes before deployment, and run it with normal least-privilege controls.

Risk: Letter counts can differ when case sensitivity or non-alphabetic characters are handled differently.

Mitigation: State the counting options used in user-facing responses, especially when punctuation, digits, or uppercase letters are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmusjune/skills/word-letter-frequency)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with optional plain-text table or compact JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default behavior lowercases input and ignores non-alphabetic characters unless flags request case-sensitive or non-alphabetic counting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
