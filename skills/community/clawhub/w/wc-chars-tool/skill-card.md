## Description:

Counts characters from standard input for a minimal text length check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need a simple character count for text supplied through stdin, such as checking basic content length limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises file input, option flags, CJK-only counts, grapheme counts, JSON output, and detailed breakdowns that are not supported by the current artifact.

Mitigation: Use the skill only as a minimal stdin-based character counter unless a future release implements and validates those modes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text integer count, with Markdown guidance and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current evidence supports stdin-based character counting only; advertised file input, option flags, CJK-only counts, grapheme counts, JSON output, and detailed breakdowns are not supported.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
