## Description:

Standardized workspace directory layout for multi-agent OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaixi](https://clawhub.ai/user/zaixi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to standardize OpenClaw workspace layout, place generated files under files/ subdirectories, audit layout drift, and optionally apply workspace organization fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fix script can move broad workspace content and may follow symlinks outside the intended workspace boundary.

Mitigation: Run the audit and dry-run workflow first, inspect every proposed move, and do not run apply.py --execute on untrusted or symlink-heavy workspaces unless containment checks, explicit confirmation, exclusions, and rollback or journaling are in place.

## Reference(s):

- [Directory Layout Reference](references/layout.md)
- [ClawHub skill page](https://clawhub.ai/zaixi/skills/workspace-org)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run workspace migration guidance and compliance-audit commands.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
