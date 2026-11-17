## Description:

AI rental advisor skill that helps users evaluate rental areas, search listings, estimate rent, and review contract risks based on budget, commute, unit type, and other conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanghou2025](https://clawhub.ai/user/fanghou2025)

### License/Terms of Use:

MIT-0

## Use Case:

External renters and housing-support agents use this skill to compare rental areas, find current listings, evaluate rent reasonableness, and identify contract risks before committing to a lease.

### Deployment Geography for Use:

China, focused on Beijing, Shanghai, Shenzhen, and Guangzhou

## Known Risks and Mitigations:

Risk: Broad live searches and shell-based scraping can retrieve unreliable, stale, or excessive listing data.

Mitigation: Restrict searches to user-requested rental queries, prefer bounded web/search tools over shell scraping, and report source dates and confidence.

Risk: Rental budgets, commute needs, rent records, and contract details may contain sensitive personal information.

Mitigation: Avoid storing or reusing rent and profile data unless the user explicitly agrees, and keep alerts or reminders opt-in.

Risk: Contract review output could be mistaken for legal advice.

Mitigation: Frame contract review as risk screening and direct users to a qualified professional for legal or high-value rental decisions.

## Reference(s):

- [Shanghai Area Reference](references/shanghai.md)
- [Beijing Area Reference](references/beijing.md)
- [Shenzhen Area Reference](references/shenzhen.md)
- [Guangzhou Area Reference](references/guangzhou.md)
- [Rent Estimation Reference Guide](references/pricing.md)
- [Rental Contract Review Detailed Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports and plain-language recommendations, with occasional inline shell commands for search workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's input language and uses live rental search results when available.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
