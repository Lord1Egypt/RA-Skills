## Description:

Classifies cybersecurity reports and builds attack paths using the TLCTC v2.7 threat taxonomy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barnes70](https://clawhub.ai/user/barnes70)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts use this skill to classify incidents, CVEs, threat intelligence, and vendor advisories under TLCTC v2.7. It helps explain causal threat steps, attack paths, and relevant control recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numbered references can trigger activation when a TLCTC analysis is not intended.

Mitigation: Use the skill only for explicit TLCTC requests or an established security-analysis context.

Risk: The optional Layer 3 authoring workflow depends on external repository instructions and content outside the supplied security verdict.

Mitigation: Review the linked repository instructions and assess external content before using that workflow.

## Reference(s):

- [TLCTC homepage](https://www.tlctc.net)
- [TLCTC canonical release](https://doi.org/10.5281/zenodo.20633176)
- [ClawHub skill release](https://clawhub.ai/barnes70/skills/tlctc-classify)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON]

**Output Format:** [Markdown analysis reports with optional JSON attack-path data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include classification rationale, attack-path notation, and control recommendations.]

## Skill Version(s):

2.7.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
