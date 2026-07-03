## Description: <br>
帮助用户查询万豪集团旗下喜来登酒店的实时价格、详情和套餐优惠，并返回飞猪预订链接供用户完成预订。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search Sheraton hotels, compare prices and packages, inspect hotel details, and open Fliggy booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details may be sent through the publisher's cloud proxy to retrieve Fliggy results. <br>
Mitigation: Review the disclosed data flow before installing and avoid submitting travel details that should not be sent through the publisher proxy. <br>
Risk: Returned prices, availability, booking links, and terms may differ from final booking conditions. <br>
Mitigation: Use returned links as convenience links and verify final price, availability, cancellation policy, and terms on Fliggy before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/sheraton-hotel-booking) <br>
- [Publisher profile: travel-skills](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with hotel search results, hotel details, package offers, prices, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on destination, dates, filters, and current Fliggy availability.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence; artifact frontmatter and _meta.json report 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
