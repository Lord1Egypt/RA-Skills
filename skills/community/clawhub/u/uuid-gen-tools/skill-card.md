## Description:

Generate UUIDs in versions v1, v4, and v5 with options for count, namespace, name, and output format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate one or more UUIDs for identifiers, including random v4, time-based v1, and namespace-based v5 values with selectable output formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUID v1 can expose timestamp and node metadata.

Mitigation: Use UUID v4 for privacy-sensitive identifiers unless v1 metadata disclosure is acceptable.

Risk: Very large bulk generation requests may produce oversized output because no documented maximum is present.

Mitigation: Keep requested counts bounded until a maximum count or streaming output behavior is documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/uuid-gen-tools)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text UUID values, with optional newline-separated bulk output and inline shell commands when explaining usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports v1, v4, and v5 UUID generation; output may be standard, uppercase, no-dashes, or URL-safe.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
