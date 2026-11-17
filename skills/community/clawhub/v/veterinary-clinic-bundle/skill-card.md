## Description:

Veterinary Clinic Bundle provides VetClaw, a set of veterinary clinic automation skills for scheduling, records, client follow-up, clinic operations, triage support, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Veterinary clinic owners, clinicians, assistants, and operators use this bundle to automate front desk, appointment, client communication, records, inventory, reporting, and pet-care knowledge workflows while keeping clinical decisions with veterinary professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle handles sensitive clinic, owner, and pet medical information.

Mitigation: Use it only in a controlled local or test environment until explicit consent, retention policies, and data-handling controls are in place.

Risk: Weak access controls may expose clinic workflows or stored records.

Mitigation: Add authentication, role-based authorization, random server-side sessions, and endpoint restrictions before broader deployment.

Risk: External AI processing may be under-disclosed to users.

Mitigation: Disclose DeepSeek or other external AI use, provide a local-only mode where needed, and redact prompts before sending sensitive content to external services.

Risk: Untrusted rendered text and dependency drift can increase application risk.

Mitigation: Use safe text rendering instead of innerHTML and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/skills/veterinary-clinic-bundle)
- [Publisher profile](https://clawhub.ai/user/daimingvip-a11y)

## Skill Output:

**Output Type(s):** [text, json, markdown, configuration, guidance]

**Output Format:** [Natural-language responses, JSON records, structured reports, workflow text, and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can contain sensitive clinic, owner, and pet medical information.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
