## Description:

什么值得买价格爬取Skill - 从smzdm.com爬取NAS、电脑、手机等商品价格

This skill is for research and development only.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to look up public price information from smzdm.com for NAS devices, computer hardware, phones, and other consumer electronics. It guides agents to extract page-structure data and return a concise lowest-price summary plus a sorted Markdown table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad NAS or brand-related price queries.

Mitigation: Use it only when the user explicitly wants public smzdm.com price lookup.

Risk: Frequent automated access could conflict with site expectations or terms.

Mitigation: Avoid excessive scraping and follow the site's usage terms.

Risk: Displayed prices may be delayed or differ from the final merchant price.

Mitigation: Verify prices on the actual merchant page before purchase decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/smzdm-price)
- [什么值得买](https://www.smzdm.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown price summary and table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tables include configuration, price, time, source, link, and notes, with prices sorted from low to high.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
