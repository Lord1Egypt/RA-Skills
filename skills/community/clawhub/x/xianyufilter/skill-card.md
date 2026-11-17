## Description:

Helps an agent search Xianyu/Goofish for second-hand listings, apply strict personal-seller and pricing filters, and return a ranked shortlist of matching products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxzhuo](https://clawhub.ai/user/xxxzhuo)

### License/Terms of Use:

MIT

## Use Case:

People shopping on Xianyu/Goofish use this skill to have an agent search for second-hand listings, filter out merchants and ambiguous prices, and return the top matching items with prices, regions, listing links, and price statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save local search-history records that may reveal shopping interests or selected listing links.

Mitigation: Install only when local search history is acceptable, and clear or disable memory history on shared machines or for sensitive searches.

Risk: Listings, prices, seller status, and links on Xianyu/Goofish can change or become unavailable after the agent reports them.

Mitigation: Verify item details, price, and seller information on the live listing before purchasing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxxzhuo/skills/xianyufilter)
- [Goofish search site](https://www.goofish.com/)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown tables and short explanatory text with listing links and price statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search records may be saved locally under memory/YYYY-MM-DD.md according to the artifact documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
