## Description: <br>
Onboarding wizard for retail digital employee agents that guides businesses through a 12-step setup to configure a fully operational AI store assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail business owners, managers, and operations teams use this skill to configure a store assistant agent across systems inventory, data import, role selection, knowledge validation, channel setup, permissions, testing, launch, and ongoing improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup may touch live retail systems, channel credentials, and operational automation. <br>
Mitigation: Use test or least-privilege API credentials, store secrets only as environment or secret-manager references, and confirm channel activation before launch. <br>
Risk: Retail data imports can include customer PII or sensitive business records. <br>
Mitigation: Avoid uploading raw customer PII, prefer anonymized aggregates or CRM references, and review what is saved in agent memory. <br>
Risk: Launch and continuous-improvement steps can activate channels or scheduled jobs before the business is ready. <br>
Mitigation: Use the built-in confirmation checkpoints, pre-launch test score, and explicit review of cron jobs and alert thresholds before going live. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fangwei-frank/retail-agent-setup) <br>
- [Step 01 - System Inventory](references/step-01-systems.md) <br>
- [Step 02 - Data Infrastructure Assessment](references/step-02-data-infra.md) <br>
- [Step 03 - Data Import and Auto-Structuring](references/step-03-data-import.md) <br>
- [Step 04 - Role Selection](references/step-04-role-select.md) <br>
- [Step 05 - Skills Configuration](references/step-05-skills-config.md) <br>
- [Step 06 - Knowledge Base Validation](references/step-06-knowledge.md) <br>
- [Step 07 - Digital Employee Persona](references/step-07-persona.md) <br>
- [Step 08 - Channel Integration](references/step-08-channels.md) <br>
- [Step 09 - Permissions and Escalation](references/step-09-permissions.md) <br>
- [Step 10 - Pre-Launch Testing](references/step-10-test.md) <br>
- [Step 11 - Launch and Handoff](references/step-11-handoff.md) <br>
- [Step 12 - Continuous Improvement](references/step-12-iterate.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and optional Python script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step artifacts saved to agent memory and asks for confirmation before continuing between setup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
