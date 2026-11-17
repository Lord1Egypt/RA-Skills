## Description:

Helps identify coordinated social trust manipulation in agent marketplaces by detecting reputation gaming through sockpuppet networks, coordinated upvoting, and manufactured community signals that can make unsafe skills appear trusted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, marketplace moderators, and security reviewers use this skill to assess whether a skill's trust reputation reflects independent community validation or coordinated manipulation. It supports reviews of skill identifiers, publisher accounts, or sets of skills for engagement velocity anomalies, cohort fingerprints, utility correlation, cross-publisher coordination, and review authenticity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Useful analysis may require marketplace engagement, review, account, or install metadata that is not always public.

Mitigation: Use only authorized data sources and treat lower-metadata assessments as lower confidence.

Risk: Future versions or workflows could request private platform credentials to obtain richer marketplace data.

Mitigation: Review credential requests before use and avoid sharing private platform access unless the workflow and data handling are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/social-trust-manipulation-detector)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown manipulation detection report with verdict and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may depend on access to marketplace engagement metadata, review text, account history, install counts, and cross-voting patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
