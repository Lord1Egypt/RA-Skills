## Description:

Generate UUIDs (v4) and short random IDs from the command line. Use when you need a unique identifier for files, records, test fixtures, or correlation IDs and want a zero-dependency one-liner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate UUIDs and short random IDs for files, records, test fixtures, logs, and correlation IDs without adding dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Short random IDs are convenient but are not collision-proof at scale.

Mitigation: Use UUID v4 for stronger uniqueness needs, or increase entropy and check for collisions before storing short IDs in systems with many generated values.

Risk: The Linux /proc UUID command is platform-specific.

Mitigation: Use the Python uuid.uuid4() fallback when the Linux kernel-provided UUID path is unavailable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local command snippets for UUID v4 generation, short URL-safe random IDs, and batch UUID generation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
