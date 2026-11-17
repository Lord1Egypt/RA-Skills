## Description:

A high-trust lead qualification and appointment booking agent for realtors that prevents MLS hallucinations via ThumbGate grounding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate agents and teams use this skill to qualify buyer, seller, and renter leads, ground listing discussion in verified MLS or sheet data, and route appointments or handoffs into their CRM and calendar workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can log personal lead data and behavioral scores to a CRM without clear consent or data limits.

Mitigation: Use it only with a configured privacy notice and consent flow, restrict CRM writes to necessary fields, and define retention and deletion procedures.

Risk: Free-form lead conversations may contain sensitive information that should not be broadly synced or retained.

Mitigation: Avoid syncing free-form sensitive conversation content and use authenticated, least-privilege CRM and calendar integrations.

Risk: Real estate lead workflows can raise Fair Housing, Do Not Call, legal, and negotiation concerns.

Mitigation: Keep the artifact's Fair Housing, DNC, legal-disclaimer, and human-handoff rules enabled and review them before deployment.

## Reference(s):

- [Real Estate Lead Pilot on ClawHub](https://clawhub.ai/igorganapolsky/skills/real-estate-lead-pilot)
- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown skill instructions with lead-handling rules and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CRM lead fields, behavioral scores, appointment details, handoff prompts, and compliance disclaimers.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
