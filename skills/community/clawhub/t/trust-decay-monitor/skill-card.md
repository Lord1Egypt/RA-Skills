## Description:

Helps track how AI skill verification results decay over time as dependencies, attack vectors, and ecosystem context change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and marketplace operators use this skill to assess whether older verification results still justify trust and to prioritize re-verification across individual skills or portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future implementations that perform marketplace, CVE, dependency, or endpoint lookups could introduce network-call and private portfolio-data risks.

Mitigation: Review and scan any implementation before deployment, with particular attention to network destinations, data handling, and dependency or CVE lookup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/trust-decay-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown trust freshness report with scores, decay factors, urgency, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize individual skills or a portfolio-level batch.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
