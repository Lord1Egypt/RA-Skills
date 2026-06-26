## Description: <br>
Manages skill distribution and visibility across AI agents using a two-layer, two-dimension Universal Skill Manager with syncing and scope control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulk-yin](https://clawhub.ai/user/hulk-yin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to synchronize skill availability across multiple agent platforms, manage universal or agent-specific scope, and audit which skills each agent can load. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change which skills multiple agents load. <br>
Mitigation: Inspect ~/.skills/agents.yaml and each skill's meta.yaml before running synchronization or migration commands. <br>
Risk: Automatic sync and migration behavior may expose unreviewed skills broadly when universal scope is used. <br>
Mitigation: Use --dry-run first, avoid universal scope for unreviewed skills, and back up agent skill directories before migration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hulk-yin/skill-manager-usm) <br>
- [ClawHub Distribution Notes](artifact/references/clawhub_distribution.md) <br>
- [USM Metadata Schema](artifact/references/meta_schema.md) <br>
- [Naming Conflict Discussion](artifact/references/naming_conflict.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent changes to local skill directories and symlinks when synchronization or migration scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
