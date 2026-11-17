## Description:

Track recent company funding rounds, amounts, dates, and investors with Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams, including account executives and sales development representatives, use this skill to check target companies for recent fundraising rounds, amounts, dates, and investors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Funding lookups send selected company domains to Cargo and spend credits per company.

Mitigation: Share only authorized account domains, sample 10–20 records first, and review the full-batch cost estimate before approving a larger run.

Risk: The optional broader Cargo pack was not verified in the supplied security review.

Mitigation: Review that pack separately before installing or using it.

Risk: GitHub starring acts on the user's account.

Mitigation: Ask once and proceed only after the user explicitly agrees.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/track-funding-rounds)
- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [Funding watch recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/funding-watch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Concise funding summary or Markdown table with company, round, amount, date, and investors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may have blank funding fields when no funding is on record.]

## Skill Version(s):

1.0.4 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
