## Description: <br>
VetClaw is a veterinary clinic automation bundle with AI-assisted workflows for reception, scheduling, medical-record support, client follow-up, clinic operations, and business reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Veterinary clinic owners, veterinarians, assistants, and operators use this skill bundle to automate front-desk intake, appointment scheduling, reminders, client communication, record lookup, reporting, inventory support, and clinic knowledge workflows. Clinical, financial, messaging, and report-generating outputs should be reviewed by qualified staff before action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive client, pet, medical, appointment, conversation, inventory, and business data may be stored or processed by the skill. <br>
Mitigation: Use explicit client consent, data minimization, encryption, access controls, retention limits, and documented deletion procedures before clinic deployment. <br>
Risk: External LLM processing may transmit prompts that contain clinic, client, pet, or medical context when an API key is configured. <br>
Mitigation: Disable external LLM calls unless disclosed and approved, or redact sensitive fields and restrict providers through a reviewed data-processing agreement. <br>
Risk: Unauthenticated API endpoints and conversation-history access can expose operational or personal information. <br>
Mitigation: Require authentication, authorization, session isolation, audit logging, and network controls before exposing the service beyond a trusted local environment. <br>
Risk: Clinical, financial, messaging, and report-generating workflows can produce incorrect or inappropriate outputs if used without review. <br>
Mitigation: Require qualified staff confirmation before diagnosis-related guidance, treatment decisions, charges, outbound messages, inventory actions, or generated reports are acted on. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/daimingvip-a11y/veterinary-clinic-bundle) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Workflow examples](artifact/examples/workflow_flows.md) <br>
- [Sample conversations](artifact/examples/sample_conversations.md) <br>
- [Clinic configuration template](artifact/config/vet-config.yaml) <br>
- [Veterinary knowledge base](artifact/config/vet-knowledge-base.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Configuration, Guidance] <br>
**Output Format:** [Agent responses, structured JSON records, workflow guidance, report text, templates, and configuration-backed recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or retrieve client, pet, appointment, conversation, inventory, and report data depending on deployment configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and application code state 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
