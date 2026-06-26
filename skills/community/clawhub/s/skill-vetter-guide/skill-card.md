## Description: <br>
Guide for vetting third-party OpenClaw skills before installation using the Skill Vetter security protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibesparkingai](https://clawhub.ai/user/vibesparkingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review third-party OpenClaw skills before installation, produce standardized vetting reports, audit installed skills, and establish a vet-before-install practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Templates can persistently change future agent behavior by adding mandatory vetting rules to AGENTS.md. <br>
Mitigation: Review the exact AGENTS.md target path and proposed diff before applying changes, and keep clear rollback steps. <br>
Risk: Automated audit prompts can schedule recurring cron jobs and write audit files without enough confirmation. <br>
Mitigation: Approve the cron entry, output directory, execution context, and removal steps before scheduling automated audits. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/vibesparkingai/skill-vetter-guide) <br>
- [Vetting Report Template](references/report-template.md) <br>
- [Audit Report Template](references/audit-template.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Vetting Report Template (zh-CN)](references/report-template.zh-CN.md) <br>
- [Audit Report Template (zh-CN)](references/audit-template.zh-CN.md) <br>
- [Prompt Templates (zh-CN)](references/prompt-templates.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown reports, checklist guidance, configuration instructions, and prompt templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes English and zh-CN source and template variants.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
