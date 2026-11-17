## Description:

Regex Tool helps agents match, extract, and replace text patterns using regular expressions for validation, parsing, and pattern-based extraction tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to test regex patterns against supplied text, extract matches, and perform regex-based replacements for validation, parsing, and redaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very complex regular expressions can hang or consume heavy CPU when run against large inputs.

Mitigation: Run complex or untrusted patterns only in environments with time or resource limits, and test on small inputs before larger data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/regex-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and text output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print matched text, capture groups, positions, replacement output, invalid-pattern errors, or no-match status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
