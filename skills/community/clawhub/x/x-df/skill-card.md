## Description:

Enhanced `df` combines disk usage and mount information with CSV, TSV, TUI, raw, and numeric output modes plus filesystem type detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to inspect local disk usage and mount information, select machine-readable or interactive output, and compose df-style data into shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external x-cmd tool.

Mitigation: Install only when x-cmd is already trusted for the target environment, as recommended by the security guidance.

Risk: Disk and mount output can reveal local filesystem names, mount paths, capacity, and inode details.

Mitigation: Use the skill in trusted sessions and avoid sharing generated output when storage layout or path information is sensitive.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of an installed x-cmd module and may surface local filesystem, mount, capacity, and inode information.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
