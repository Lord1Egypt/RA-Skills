## Description:

Trading card analysis, grading guidance, market comps, and eBay listing optimization for sports cards, Pokemon, and other collectible cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmsneaks11-max](https://clawhub.ai/user/mmsneaks11-max)

### License/Terms of Use:

MIT-0

## Use Case:

Collectors, sellers, and listing operators use this skill to identify trading cards, estimate condition and value, decide whether grading is worthwhile, and draft factual eBay listing copy. Optional eBay and PSA enrichment can support market comps, active listing positioning, population context, and certification workflows when credentials and approved host integrations are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated eBay copy may include seller-status, feedback, shipping-speed, insurance, return-policy, or authenticity statements that are not verified for the seller account or item.

Mitigation: Review and customize all listing copy before publishing; remove any seller, shipping, return, insurance, or authenticity claim unless it is verified for the account and specific item.

Risk: Market, population, certification, or live comp claims may be misleading when optional eBay or PSA integrations are unavailable or were not queried.

Mitigation: Clearly label heuristic estimates, user-supplied comps, and live-data-backed findings; do not claim live marketplace, population, or certification verification unless an approved integration was actually used.

Risk: Optional eBay and PSA credentials could be mishandled if users store secrets in the skill package or local dotfiles.

Mitigation: Use runtime environment variables or host secret management, keep credentials out of the skill package, and request only credentials needed for the current task.

## Reference(s):

- [Skill Package](https://clawhub.ai/mmsneaks11-max/skills/trading-card-specialist)
- [Publisher Profile](https://clawhub.ai/user/mmsneaks11-max)
- [eBay Developer Program](https://developer.ebay.com/)
- [Listing Optimization Guide](references/LISTING-OPTIMIZATION.md)
- [Market Research Methodology](references/MARKET-RESEARCH.md)
- [Comprehensive Grading Strategy Guide](references/GRADING-STRATEGY.md)
- [Optional Integration Notes](references/INTEGRATIONS.md)
- [Security Notes](references/SECURITY.md)
- [eBay Listing Template Generator](assets/ebay-listing-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or concise plain text with optional shell environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include card summaries, condition estimates, value ranges, grading recommendations, eBay titles and descriptions, credential setup guidance, and notes on missing verification.]

## Skill Version(s):

2.0.5 (source: server release evidence, created 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
