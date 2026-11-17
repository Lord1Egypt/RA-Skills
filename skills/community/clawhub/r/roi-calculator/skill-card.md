## Description:

Calculates influencer campaign ROI and ROAS, earned media value, attribution-modeled revenue, LTV-based ROI, and stakeholder-ready summaries from supplied campaign performance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Marketing teams, creators, and operators use this skill to calculate or project influencer campaign returns, compare ROI methods, evaluate individual creators or tiers, and prepare numbers for budget justification or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign, ecommerce, analytics, or CRM inputs may contain sensitive business performance information.

Mitigation: Review supplied data before use and authorize memory saves or connector-backed pulls only when those numbers may be reused for future campaign analysis.

Risk: ROI, attribution, or benchmark comparisons may overstate campaign performance when conversions, targets, or comparison baselines are unverified.

Mitigation: Use source-dated targets and attribution windows, label each figure as measured, user-provided, calculated, or estimated, and avoid attributable-return claims when conversions are unverified.

Risk: Earned media value is directional and can vary by methodology.

Mitigation: Present EMV as an estimate, disclose the CPM or engagement assumptions used, and avoid treating EMV as absolute revenue.

## Reference(s):

- [ROI templates and benchmark inputs](references/roi-templates.md)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/roi-calculator)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown calculation summaries and optional memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save ROI calculation files only after user authorization; can use connector-backed campaign data when available.]

## Skill Version(s):

19.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
