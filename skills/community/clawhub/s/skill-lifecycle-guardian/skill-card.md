## Description:

Skill Guardian monitors OpenClaw skill workspaces for new or changed skills, checks for functional overlap, generates or updates user guides, refreshes the guide index, and can notify administrators when changes are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathemkingh](https://clawhub.ai/user/nathemkingh)

### License/Terms of Use:

MIT-0

## Use Case:

Administrators and skill maintainers use this skill to maintain an inventory of installed OpenClaw skills, detect new or changed SKILL.md files, identify overlapping functionality, and keep user-facing guide files current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled scans can broadly read installed skill files and update persistent registry, guide, README, and notification outputs.

Mitigation: Install only when an administrator-level autonomous skill inventory service is intended, restrict scanned directories, and run scheduled agents with least privilege.

Risk: Scanned skill contents may influence generated guide and README output.

Mitigation: Treat scanned SKILL.md content as untrusted data and review generated guides and README changes before relying on them.

Risk: The security guidance identifies insufficient path containment in guardian-check.sh.

Mitigation: Fix the path containment logic and pin or verify the approved SKILL.md hash before each scheduled run.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets, JSON configuration examples, generated guide files, README updates, and concise Chinese status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent registry, user guide, README, and notification outputs inside the configured OpenClaw workspace.]

## Skill Version(s):

2.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
