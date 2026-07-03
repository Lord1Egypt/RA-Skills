## Description: <br>
FDE helps an agent guide Forward Deployed Engineers through a 12-step enterprise AI deployment workflow for mapping business processes, identifying AI nodes, producing a deployment plan, and building a knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongfangxun](https://clawhub.ai/user/kongfangxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Forward Deployed Engineers, enterprise IT staff, and CIO teams use this skill to guide an agent through enterprise AI deployment discovery, planning, handoff, and post-deployment checks. The skill helps capture enterprise context, classify workflow nodes, generate workflow configuration, and package deployment and knowledge-base deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer scripts can change local agent configuration and target-device setup. <br>
Mitigation: Review the installer scripts before execution, verify file writes and overwrites, confirm whether persistent services are installed, and document uninstall or rollback steps. <br>
Risk: The deployment workflow can produce inaccurate plans if enterprise context or workflow-node details are incomplete. <br>
Mitigation: Require human confirmation of the enterprise profile, technical environment, five workflow-node elements, cost assumptions, and handoff checklist before deploying AI nodes. <br>
Risk: Knowledge-base and audit outputs may store or publish enterprise operational details. <br>
Mitigation: Confirm what data is stored in the knowledge base and webhook/audit outputs, restrict access to the enterprise-approved platform, and review sensitive content before sharing. <br>


## Reference(s): <br>
- [FDE deployment manual](artifact/FDE.md) <br>
- [FDE toolkit README](artifact/README.md) <br>
- [12-step workflow template](artifact/workflow/template.yaml) <br>
- [FDE agent role templates](artifact/agents/templates.md) <br>
- [n8n-workflows reference](https://github.com/Zie619/n8n-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce deployment plans, workflow.yaml configuration, knowledge-base documents, checklists, and operational handoff guidance.] <br>

## Skill Version(s): <br>
0.99.4 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
