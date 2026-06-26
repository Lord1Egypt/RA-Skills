## Description: <br>
Guides agents using the npx corp CLI to manage corporate formation, governance, cap tables, finance, documents, tax, compliance, agents, and work items on TheCorporation platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansonkd](https://clawhub.ai/user/hansonkd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and operator agents use this skill to set up and operate corporate entities through TheCorporation CLI, including formation, governance approvals, equity workflows, finance tasks, document handling, compliance tracking, and agent work loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide legally or financially significant corporate actions, including formation, signing, equity, payroll, payment, tax, and autonomous-agent operations. <br>
Mitigation: Review every proposed command before execution, use dry-run where available, and get legal or financial review before taking binding or high-impact actions. <br>
Risk: Commands may affect the wrong workspace or entity, or expose sensitive local corporate data. <br>
Mitigation: Verify the active workspace, entity, and hosting mode with context commands before writes, and protect the local ~/.corp/data directory. <br>


## Reference(s): <br>
- [TheCorporation.ai Form and Operate on ClawHub](https://clawhub.ai/hansonkd/thecorporation-form-and-operate) <br>
- [TheCorporation mono repository](https://github.com/thecorporationai/thecorporation-mono) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI command sequences, flags, setup modes, context checks, and review guidance before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
