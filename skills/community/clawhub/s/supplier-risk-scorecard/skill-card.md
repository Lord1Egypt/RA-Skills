## Description:

Use this skill when a supply chain analyst, procurement manager, or sourcing team needs to assess a supplier's risk profile, producing a scored five-dimension risk scorecard, a Low/Medium/High/Critical tier rating, and a prioritized mitigation action plan for procurement review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain analysts, procurement managers, and sourcing teams use this skill to assess supplier risk during onboarding, periodic review, triggered reassessment, or risk-tiered supplier ranking. It guides intake, evidence collection, five-dimension scoring, risk-tier calculation, mitigation planning, and evidence-gap logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier financials, audits, sanctions checks, and employee-related materials can contain confidential or regulated information.

Mitigation: Use only authorized, business-relevant excerpts and redact unnecessary personal data, secrets, credentials, and regulated information before using the skill.

Risk: Missing supplier evidence can make risk scores assumption-based and less reliable.

Mitigation: Flag every assumption explicitly, log evidence gaps, and do not present assumed scores as evidence-backed conclusions.

Risk: A sanctioned supplier or confirmed material regulatory violation may require immediate business escalation.

Mitigation: Escalate the overall tier to Critical and recommend review by legal and procurement leadership before further action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/supplier-risk-scorecard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown scorecard with tables, ranked risk flags, recommended actions, and evidence gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses five weighted supplier-risk dimensions, maps scores to Low/Medium/High/Critical tiers, and escalates Critical or High conditions under stated rules.]

## Skill Version(s):

0.1.2 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
