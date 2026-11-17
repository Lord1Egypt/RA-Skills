## Description:

Drive a zero-to-first-test-payment UPI onboarding workflow with explicit readiness checks: provider selection, sandbox setup, credentials, webhook validation, test matrix, go-live gates, and incident rollback planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product, operations, finance, and compliance teams use this skill to coordinate UPI payment launch readiness from first setup through sandbox validation, gate review, incident planning, and go/no-go approval.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Payment rules, authentication requirements, and provider onboarding terms may change before production launch.

Mitigation: Verify current RBI, NPCI, and selected PSP or aggregator requirements before go-live approval.

Risk: Local launch memory or evidence files could accidentally collect credentials, customer PII, or live payment secrets.

Mitigation: Keep secrets in an approved secret manager and exclude credentials, customer PII, and live payment secrets from local memory and evidence files.

Risk: A team could enable production traffic without complete gate evidence, rollback testing, or reconciliation sign-off.

Mitigation: Require dated evidence and approver names for all go-live gates, including rollback readiness and finance reconciliation review.

## Reference(s):

- [UPI Go Live Checklist release page](https://clawhub.ai/anugotta/skills/upi-go-live-checklist)
- [RBI Digital Payment Authentication Directions](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898)
- [Setup first-use checklist](setup.md)
- [Project memory template](memory-template.md)
- [Provider matrix starter template](provider-matrix.md)
- [Go-live gates](go-live-gates.md)
- [Launch playbook](launch-playbook.md)
- [Incident runbook](incident-runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown checklists, status summaries, templates, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include owner and due-date fields for missing launch tasks and mark blockers explicitly.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
