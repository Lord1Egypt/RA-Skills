## Description:

Maintains workspace documentation hygiene by organizing markdown sprawl, refreshing indexes, archiving stale snapshots, and producing dry-run cleanup candidate lists without deleting files automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houseofjuici](https://clawhub.ai/user/houseofjuici)

### License/Terms of Use:


## Use Case:

Developers and workspace maintainers use this skill to run a reversible documentation cleanup cycle: audit archive retention, refresh documentation indexes, move stale status and progress files into archive buckets, and produce deletion-candidate reports for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled audit script writes to a hardcoded personal archive path and could overwrite an unintended writable report file.

Mitigation: Review the script before installation, change the archive root to the intended workspace, and harden report creation with temporary files, symlink checks, and refusal to overwrite existing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houseofjuici/skills/workspace-maintenance)
- [Publisher profile](https://clawhub.ai/user/houseofjuici)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated report or manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow is non-destructive by design and requires human review before any deletion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
