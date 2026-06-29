## Description: <br>
搜索万豪集团旗下丽思卡尔顿酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistance agents use this skill to search Ritz-Carlton hotel options, inspect hotel details, compare package offers, and present booking links. It is intended for Ritz-Carlton hotel discovery, not direct booking completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details are sent to the configured proxy endpoint. <br>
Mitigation: Install only after confirming that the publisher and proxy endpoint are trusted, and prefer an approved HTTPS proxy host. <br>
Risk: The release evidence reports a Westin/Ritz metadata mismatch. <br>
Mitigation: Confirm the displayed skill identity and publisher before installation, and ask the publisher to correct the stale metadata. <br>
Risk: Hotel prices and availability can change after results are shown. <br>
Mitigation: Treat returned prices as current search results and verify final terms on the booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/ritz-carlton-hotel-booking) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style text containing hotel search results, prices, ratings, addresses, IDs, package details, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live travel-platform data returned through the configured proxy; prices can change and booking is completed outside the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
