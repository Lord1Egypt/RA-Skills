## Description:

Researches a company for a sales call and prepares a ten-stage PDF brief covering account context, buyer concerns, discovery questions, objections, a battle card, and follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericgonzalez](https://clawhub.ai/user/ericgonzalez)

### License/Terms of Use:

MIT-0

## Use Case:

Sales representatives use this skill to prepare for a company-specific call, turning sourced account research into a PDF brief with discovery questions, a battle card, and a draft follow-up email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated briefs and optional seller profiles can retain confidential customer or pricing details locally.

Mitigation: Avoid including confidential details unless local retention is acceptable, and review or remove saved files as appropriate.

Risk: Public company research may be incomplete or lead to unsupported sales claims.

Mitigation: Check cited sources, label inferences, and surface missing information rather than inventing details.

Risk: Installing the PDF dependency on demand may conflict with locked-down environments.

Mitigation: Preinstall or explicitly approve reportlab instead of allowing ad hoc package installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ericgonzalez/skills/sales-call-prep)
- [Ten-stage prompt library](artifact/references/prompts.md)
- [Seller profile template](artifact/references/seller-profile.md)

## Skill Output:

**Output Type(s):** [Text, PDF, JSON]

**Output Format:** [PDF call-prep brief, local JSON payload, and short text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source references, labeled inferences and gaps, three key findings, and an unsent follow-up email draft.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
