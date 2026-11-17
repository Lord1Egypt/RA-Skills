## Description:

Create, extract, list, and compress tar archives with format support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, inspect, compare, verify, search, and extract tar archives from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports unsafe tar handling that can let crafted archives overwrite files or create command-execution risk.

Mitigation: Use only trusted archives and file arguments, avoid filenames beginning with dashes, and extract into a disposable directory until the script adds explicit option terminators and archive-entry validation.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installing or deploying it and apply the scanner guidance as the authoritative operating constraint.

## Reference(s):

- [Tar skill on ClawHub](https://clawhub.ai/bytesagain1/skills/tar)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide use of a bundled shell script that emits command-line status text and archive listings.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
