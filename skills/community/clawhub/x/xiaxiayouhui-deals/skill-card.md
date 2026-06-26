## Description: <br>
Helps an agent compare prices, find coupons, parse shopping links, surface daily deals, and show local-life discounts across supported e-commerce platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheese9102](https://clawhub.ai/user/cheese9102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare prices, find coupons, inspect pasted product links, browse daily deals, and locate city or category-specific local-life offers. The skill is intended for shopping research and deal discovery, not for completing purchases or making final buying decisions. <br>

### Deployment Geography for Use: <br>
Global, with practical coverage focused on Chinese e-commerce and local-life platforms. <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries, pasted product links or tokens, and optional city or category searches are sent to xiaxiayouhui.xyz. <br>
Mitigation: Share only the product or deal information needed for the task, and avoid pasting URLs that contain personal tracking, session, or account-linked parameters. <br>
Risk: Purchase buttons may route through third-party or affiliate-style redirects, and prices can change after the agent displays them. <br>
Mitigation: Review the final merchant page, price, coupon terms, seller identity, and checkout details before buying. <br>
Risk: The scan summary says the release under-discloses what is sent to the service and how purchase links are presented. <br>
Mitigation: Tell users when results come from xiaxiayouhui.xyz and treat purchase links as external redirects rather than neutral checkout links. <br>


## Reference(s): <br>
- [xiaxiayouhui.xyz homepage](https://xiaxiayouhui.xyz) <br>
- [ClawHub skill listing](https://clawhub.ai/cheese9102/xiaxiayouhui-deals) <br>
- [Publisher profile](https://clawhub.ai/user/cheese9102) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and short guidance, often derived from JSON API responses and illustrated with curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include prices, coupon amounts, freshness notes, affiliate-style purchase links, and caveats about availability or product-match confidence.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
