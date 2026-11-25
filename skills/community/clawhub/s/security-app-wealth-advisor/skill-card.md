## Description:

Supports bank digital banking teams in drafting and reviewing product-suitability rules, wealth-advisory scripts, and compliance checks for mobile apps.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

China-based commercial bank digital banking teams and wealth-management advisors can use this skill to prepare draft product-suitability rules, consultation scripts, prohibited-language checks, and review workflows. Outputs are reference drafts for human review, not personalized customer recommendations or production matching decisions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security scan had partial coverage and reported a low-severity concern about product eligibility rules.

Mitigation: Review whether the reported return-target exclusion fits the intended use before relying on product-matching outputs; the scan guidance notes that coverage was partial.

Risk: Customer profiles can contain sensitive financial information.

Mitigation: Use anonymized or synthetic profiles for design and testing, and require qualified human review before applying drafts in real customer interactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gechengling/skills/security-app-wealth-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with tables, checklists, draft scripts, workflow descriptions, and illustrative Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference drafts requiring qualified human review; examples use placeholders or synthetic data and are not production-ready recommendations or executable systems.]

## Skill Version(s):

3.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
