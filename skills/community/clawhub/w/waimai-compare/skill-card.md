## Description:

外卖比价 helps agents compare takeout and food prices across Meituan, Ele.me, JD.com, Taobao, and related coupon sources, then generate an HTML comparison report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers and shopping assistants use this skill to collect recent price and coupon information for takeout or food products, compare platform totals, and produce a readable report for choosing an ordering option.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated HTML report can run browser code from report content and a remote chart library.

Mitigation: Open only reports generated from trusted search results, treat report contents as untrusted, and prefer a reviewed version that escapes all report data and pins or bundles the chart library.

Risk: Search-derived prices and coupons can be stale or location dependent.

Mitigation: Use the report as a planning aid and verify final prices, delivery fees, coupon terms, and availability inside each platform app before ordering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/waimai-compare)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with structured JSON data and a generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports should be treated as untrusted local HTML and checked against current platform prices before purchase decisions.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
