## Description:

Audit and safely clean Ubuntu 24.04 system junk, caches, logs, temp files, and unused local tool artifacts outside /mnt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenzheke](https://clawhub.ai/user/shenzheke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit disk usage and reclaim Ubuntu or WSL storage through conservative cache, log, temp-file, package-cache, and orphaned-tool cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup scripts can delete root-level cache, package-list, log-retention, npm, and temporary data.

Mitigation: Review the planned cleanup first, default to the safe cleanup path, preserve /mnt and project files, and require explicit approval for Docker or more aggressive cleanup.

Risk: Second-round orphaned-tool scans can print private configuration or workspace lines when broad or sensitive search terms are used.

Mitigation: Use narrow tool names, review scan output before sharing it, and avoid broad or sensitive terms that could expose private configuration content.

## Reference(s):

- [Cleanup Targets](references/targets.md)
- [Orphaned Tool Patterns](references/orphaned-tool-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/shenzheke/skills/ubuntu-wsl-system-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and cleanup summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports inspected directories, cleaned items, preserved areas, estimated reclaimed space, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
