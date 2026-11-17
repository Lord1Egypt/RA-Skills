## Description:

Helps verify publisher identity integrity in AI agent ecosystems by detecting impersonation, key rotation anomalies, and identity gaps in the trust chain between skill publishers and their claimed identities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

External adopters, marketplace reviewers, and developers use this skill to investigate publisher IDs, skill identifiers, or marketplace search results for identity consistency, impersonation risk, key rotation anomalies, and cross-platform presence gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to propose live public-information lookups with curl or python3.

Mitigation: Review proposed commands before execution and confirm that they only query intended public sources.

Risk: Publisher identity reports can surface risk signals but cannot prove malicious intent or identity authenticity.

Mitigation: Use the report to prioritize deeper review and corroborate findings with platform-level identity checks where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/publisher-identity-verifier)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with scores, event timeline, risk assessment, presence map, trust rating, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested public-information lookups using curl or python3 when an agent applies the guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
