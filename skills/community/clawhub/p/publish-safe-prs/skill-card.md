## Description:

Prepare, sanitize, publish, and verify public GitHub issues, pull requests, review comments, release notes, bug reports, logs, screenshots, and test evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jumpunder](https://clawhub.ai/user/jumpunder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert private debugging context into sanitized public GitHub contributions, run deterministic privacy and secret preflight checks, and verify public artifacts after publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A sanitized contribution can still expose private context through secrets, identifiers, local paths, logs, screenshots, metadata, or unique combinations of details.

Mitigation: Provide only the intended draft and deny-term files to the preflight scanner, replace private context with synthetic examples, review every evidence surface, and manually inspect the final public artifact.

Risk: Public GitHub writes, comments, uploads, pushes, and edits are external actions that may preserve history or notifications even after correction.

Mitigation: Require separate explicit user authorization before the first public write, fetch and rescan the published artifact immediately, and avoid claiming complete erasure after any exposure.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner exits 0 when no configured pattern matches, 1 when likely private material is found, and 2 when scanning cannot complete.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
