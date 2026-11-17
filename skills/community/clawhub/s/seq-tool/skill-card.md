## Description:

Generate sequences of numbers with configurable start, end, and increment values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate simple numeric ranges for numbered lists, loop inputs, and range-based commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented options for formatting, separators, padding, and decimal sequences may not match the bundled script behavior.

Mitigation: Verify required command forms before relying on them, and treat the bundled implementation as an integer-only start, end, and step sequence helper unless updated evidence proves broader support.

Risk: Invalid or missing numeric arguments can cause command failures instead of producing a sequence.

Mitigation: Validate integer arguments before invoking the skill in automated workflows.

## Reference(s):

- [Seq Tool release page](https://clawhub.ai/dinghaibin/skills/seq-tool)
- [dinghaibin publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integer sequence output from the bundled local script; documented formatting, separator, padding, and decimal options may require verification before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
