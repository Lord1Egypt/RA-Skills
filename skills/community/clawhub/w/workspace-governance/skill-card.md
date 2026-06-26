## Description: <br>
A methodology-first workspace governance skill for AI agents that focuses on principles, decision framework, and safe execution patterns instead of fixed directory templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars2003](https://clawhub.ai/user/mars2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to plan workspace cleanup, auditing, archiving, and project setup with clear boundaries, rollback checkpoints, and confirmation gates before risky file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cleanup plans may include moves or deletes that affect user files. <br>
Mitigation: Review the dry-run plan before approving file operations, and require explicit confirmation for delete and bulk-move actions. <br>
Risk: Using a broad workspace root can expose more files than intended to scanning or governance actions. <br>
Mitigation: Confirm the intended workspace boundary first, and avoid broad roots such as a home directory unless that scope is intentional. <br>
Risk: Ambiguous files can be misclassified when the agent lacks enough context. <br>
Mitigation: Mark ambiguous items as pending user decisions and block non-interactive execution instead of auto-approving changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mars2003/workspace-governance) <br>
- [Governance Manual](references/Governance-Manual.md) <br>
- [Chinese Governance Manual](references/治理手册.zh-CN.md) <br>
- [Minimal Governance Run Example](examples/minimal-governance-run.md) <br>
- [Interoperability Tools](tools/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown plans, tables, logs, configuration snippets, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run plans, pending-decision lists, rollback checkpoints, and governance logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
