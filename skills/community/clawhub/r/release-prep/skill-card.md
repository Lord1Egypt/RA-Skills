## Description:

Deep code audit, documentation sync, and release preparation for Python packages before publishing to PyPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morozsm](https://clawhub.ai/user/morozsm)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to audit Python packages before release, align documentation with code, prepare changelog and version updates, and publish to PyPI when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix and release modes can make repository edits, update changelog or version files, and create commits or tags.

Mitigation: Use audit mode for read-only review, and request fix or release mode only after reviewing the proposed changes.

Risk: Release mode includes a PyPI publishing step.

Mitigation: Require explicit user confirmation before publishing and review the release summary before upload.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and release guidance, with optional repository file changes and shell commands for fix or release modes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default audit mode is read-only; fix and release modes may modify files, create commits or tags, and prepare package publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
