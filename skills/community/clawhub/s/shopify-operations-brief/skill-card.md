## Description:

Create a read-only Shopify store performance overview for a day, week, month, or valid custom period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify merchants, operators, and developers use this skill to create private store performance briefs from read-only Shopify Admin data. It helps review sales, orders, promotions, shipping speed, low stock on products sold, and near-term seasonal preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CLI execution can run a configured Shopify CLI path in the user's environment.

Mitigation: Review the skill before installing, use only a trusted Shopify CLI path, and avoid running it from shared or attacker-controlled workspaces.

Risk: HTML report output can write files in the current working directory and may replace files when force is approved.

Mitigation: Run reports from a merchant-owned private working directory and approve replacement only after reviewing the target path.

Risk: Generated reports and connection files can contain or expose private merchant operational data.

Mitigation: Keep skill-hub.env outside public repositories, use a merchant-owned read-only Shopify connection, and treat generated reports as private.

## Reference(s):

- [Shopify Operations Brief onboarding](references/onboarding-guide.md)
- [What each number means](references/metric-definitions.md)
- [Seasonal selling calendar](references/marketing-calendar.md)
- [Report layout and writing standard](references/design-tokens.md)
- [Skill homepage](https://github.com/lvsao/shopify-skill-hub)
- [ClawHub skill page](https://clawhub.ai/lvsao/skills/shopify-operations-brief)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files, JSON]

**Output Format:** [Markdown guidance with shell command examples; the skill can produce a self-contained HTML report or structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML reports are written inside the current working directory unless JSON-only output is requested.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
