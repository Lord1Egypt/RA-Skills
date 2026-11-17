## Description:

Helps agents retrieve and summarize public Vipshop product and promotion page information, including prices, reviews, specifications, and simple comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-research agents use this skill to summarize publicly available Vipshop product listings, promotion pages, item details, and comparable products. It is intended for lightweight analysis and reminders, not purchasing, account actions, reverse engineering, or bulk collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prices, promotions, and availability can change quickly.

Mitigation: Include the collection time with summaries and treat price or promotion details as time-sensitive.

Risk: Automating login-gated actions, purchases, or bulk collection could violate platform rules or trigger anti-abuse controls.

Mitigation: Keep use to explicitly requested public pages, avoid account actions and purchases, and use frequency limits.

## Reference(s):

- [Vipshop homepage](https://www.vip.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/vipshop)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with links, extracted fields, comparisons, and collection-time notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product titles, links, image URLs, prices, promotions, review counts, shop names, brands, specifications, and review-highlight keywords.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
