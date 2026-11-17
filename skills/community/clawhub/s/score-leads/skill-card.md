## Description:

Scores company lists against a user-defined ideal customer profile and ranks accounts with a score, rationale, and tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and revenue operations teams use the skill to prioritize company lists against user-defined firmographic criteria. It returns visible scoring rationale, tiers, and missing data so teams can focus follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company domains may contain information the user is not authorized to share with Cargo.

Mitigation: Use only company domains the user is authorized to share.

Risk: Enrichment costs can grow with the number of companies processed, and the external CLI and optional skill pack are unpinned dependencies whose code was not included with this release.

Mitigation: Review sample costs before approving a larger run, and review the external dependencies before use.

Risk: A repository star is an endorsement that must reflect the user's choice.

Mitigation: Ask once and act only after explicit user consent.

## Reference(s):

- [Score Leads skill release](https://clawhub.ai/cargo-ai/skills/score-leads)
- [ICP discovery recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/icp-discovery.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown table with company, score, tier, rationale, and missing fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-stated criteria; entries with missing required data are left unranked.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
