## Description:

VetClaw Bundle provides veterinary clinic automation skills for front desk intake, appointment scheduling, records, follow-up, client communication, reporting, and operations workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Veterinary clinic operators, clinicians, assistants, and operations teams use this bundle to automate clinic conversations and workflows such as intake, booking, reminders, triage routing, records lookup, pricing, reports, inventory, and client follow-up. Clinical decisions and medical actions should remain under licensed veterinary review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle handles sensitive clinic, customer, pet, medical, and business data through unauthenticated network APIs.

Mitigation: Run only on private localhost or behind real authentication until authorization, session ownership, XSS protection, retention controls, and privacy notices are fixed; do not use real records before those controls are in place.

Risk: Configured third-party LLM integration can share clinic or customer data outside the deployment boundary.

Mitigation: Use explicit consent, data minimization, and an approved provider configuration before sending production conversations or records to an external LLM.

Risk: Veterinary triage and medical guidance can be mistaken for diagnosis or treatment direction.

Mitigation: Keep clinical decisions and medical actions under licensed veterinary review and use the automation for routing, reminders, documentation, and support workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/skills/vetclaw-bundle)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Workflow examples](artifact/examples/workflow_flows.md)
- [Sample conversations](artifact/examples/sample_conversations.md)
- [Clinic configuration template](artifact/config/vet-config.yaml)
- [Veterinary knowledge base](artifact/config/vet-knowledge-base.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with JSON-like records, reports, Python handlers, configuration snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local clinic records and may call configured third-party LLM, SMS, WeChat, phone, payment, or database services when deployed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
