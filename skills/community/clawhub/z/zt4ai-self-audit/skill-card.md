## Description: <br>
Zero Trust security audit support for AI agent workspaces, skills, and configurations, including prompt injection risk, credential exposure, excessive privilege, behavioral manipulation, and integrity drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanarchytan](https://clawhub.ai/user/tanarchytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review agent skills, workspace files, permissions, trust boundaries, network egress, and integrity baselines before relying on an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scans and audit reports may expose workspace paths, skill names, and security findings. <br>
Mitigation: Treat generated reports and integrity baselines as sensitive, review them before sharing, and store them only in approved workspace memory. <br>
Risk: Broad filesystem and network checks can inspect local agent workspaces or test outbound connectivity. <br>
Mitigation: Run the commands deliberately, review scope before broad checks, and constrain use to owned workspaces and approved endpoints. <br>
Risk: Integrity baselines become trust anchors and can mislead users if regenerated before reviewing unexpected changes. <br>
Mitigation: Investigate changed, missing, or new files before updating a baseline after installs or skill modifications. <br>


## Reference(s): <br>
- [Risk Classification Guide](references/risk-classification.md) <br>
- [Per-Skill Audit Checklist](references/audit-checklist.md) <br>
- [Action Tiers - Graduated Trust Model](references/action-tiers.md) <br>
- [ZT4AI Audit Report Template](references/report-template.md) <br>
- [Caging the Agents (arXiv:2603.17419)](https://arxiv.org/abs/2603.17419) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown audit guidance with shell command blocks and structured report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce audit reports and integrity baselines in workspace memory when the user runs the suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
