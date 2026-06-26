## Description: <br>
Audits and safely cleans Ubuntu 24.04 and WSL system junk, caches, logs, temporary files, and unused local tool artifacts outside /mnt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenzheke](https://clawhub.ai/user/shenzheke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit disk usage and reclaim storage on Ubuntu/WSL systems while preserving /mnt, project files, Docker data, and active shared runtimes unless explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands can remove caches, apt metadata, logs, temporary files, and orphaned tool residues that may still be useful. <br>
Mitigation: Review audit output first, keep /mnt and project files out of scope, and require explicit confirmation before extended cleanup or permanent deletion. <br>
Risk: Docker cleanup can remove images, containers, volumes, or builder cache if used too broadly. <br>
Mitigation: Only run Docker cleanup when explicitly requested, inspect Docker usage first, and choose the least destructive prune command that matches the request. <br>
Risk: Hard-coded /root and Ubuntu/WSL paths may not match every environment. <br>
Mitigation: Confirm the target environment uses the intended paths before running scripts or deleting files. <br>


## Reference(s): <br>
- [Cleanup Targets](references/targets.md) <br>
- [Orphaned Tool Patterns](references/orphaned-tool-patterns.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/shenzheke/ubuntu-wsl-system-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and cleanup summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes audit findings, cleaned targets, preserved areas, estimated reclaimed space, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
